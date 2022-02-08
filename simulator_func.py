from os import listdir
from datetime import datetime
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import arrow_function
from geopandas import GeoDataFrame, read_file
from base64 import b64decode
from json import loads
import numpy as np
import csv
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import*


import re
import geopandas as gpd
import shapely
from shapely.geometry import LineString,MultiPoint,MultiPolygon,MultiLineString
from shapely.geometry import *
from shapely.ops import unary_union
from shapely.ops import cascaded_union
from shapely.ops import triangulate
from shapely.geometry import Point,Polygon
from shapely.ops import nearest_points
import math
from turfpy import measurement
from geojson import Feature
import pandas as pd
import scipy.signal as signal
from scipy.interpolate import interp1d
import quaternion


def default_layers(geojson_style) -> list:
    """
    return list of default layers (EG, 1OG, 4OG) with id to get hover info

    Parameters
    ----------
    geojson_style : geojson rendering logic in java script (assign)

    Returns
    -------
    layers : list of default layers
    """
    # initializing list to fill it with default layers
    layers = []
    # list of all default floorplan names
    floorplans = ["EG", "1OG", "4OG"]
    for fp in floorplans:
        geojson = dl.GeoJSON(
            url=f"assets/floorplans/{fp}.geojson",  # url to geojson file
            options=dict(style=geojson_style),  # style each polygon
            hoverStyle=arrow_function(dict(weight=1, color="orange")),  # style applied on hover
            hideout=dict(style={"weight": 0.2, "color": "blue"}, classes=[], colorscale=[], colorProp=""),
            id=fp)
        layers.append(dl.Overlay(geojson, name=fp, checked=False))
    return layers


def uploaded_layers(geojson_style):
    """
    - adds all converted layers to map
    - returns list of all overlays

    Parameters
    ----------
    geojson_style : geojson rendering logic in java script (assign)

    Returns
    -------
    html.Div : list of default layers + new uploaded layers
    """
    # getting list of layers (already filled with default layers)
    layers = default_layers(geojson_style)
    # parsing through all converted layers and adding them to <<layers>>
    for geojson_file in listdir("assets/floorplans"):
        name = geojson_file.split(".")[0]  # getting name of geojson file
        if name not in ["EG", "1OG", "4OG"]:
            geojson = dl.GeoJSON(
                url=f"assets/floorplans/{geojson_file}",  # url to geojson file
                options=dict(style=geojson_style),  # style each polygon
                hoverStyle=arrow_function(dict(weight=1, color='orange')),  # style applied on hover
                hideout=dict(style={"weight": 0.2, "color": "blue"}, classes=[], colorscale=[], colorProp=""))
            layers.append(dl.Overlay(geojson, name=name, checked=False))
    return html.Div(dl.LayersControl(layers))


def upload_decoder(content: str) -> str:
    """
    - decodes uploaded base64 file to originally uploaded file
    - returns decoded file
    """
    # decoding base64 to geojson
    encoded_content = content.split(",")[1]
    decoded_content = b64decode(encoded_content).decode("latin-1")  # should be a geojson like string
    return decoded_content


def crs32632_converter(filename: str, decoded_content: str) -> None:
    """
    - converts an EPSG: 32632 geojson file to WGS84
    - saves converted file
    """
    # converting crs (UTM -> EPSG: 32632) of given floorplan to WGS84 (EPSG: 4326)
    layer = GeoDataFrame(read_file(decoded_content), crs=32632).to_crs(4326)
    # saving converted layer
    layer.to_file(f"assets/floorplans/{filename}", driver="GeoJSON")


def export_data(data: dict) -> None:
    """
    - formats geojson like dict from layercontrol
    - saves formatted file as geojson file (>assets/export<)
    """
    # original export data must be formatted to proper geojson like string
    old = "'"
    new = """ " """
    # getting the current date and time for unique filename
    name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    # storing data as geojson file
    with open(f"assets/export/exportdata_{name}.geojson", "w") as file:
        # formatting data-string
        data_str = str(data).replace(old, new[1])
        # ...saving
        file.write(data_str)


def hover_info(feature=None):
    header = [html.H4("Space Information", style={"textAlign": "center"}), html.Hr(style={"width": "60%", "margin": "auto", "marginBottom": "10px"})]
    if not feature:
        return header + [html.P("Choose a layer. Hover over a segment.", style={"textAlign": "center"})]
    # creating table for properties
    table_header = [html.Thead(html.Tr([html.Th("Properties", style={"width": "80px", "color": "white"}), html.Th("Value", style={"color": "white"})]))]
    table_body_content = []
    # filling table_body with content
    for prop in feature["properties"]:
        table_body_content.append(html.Tr(
            [
                html.Td(
                    prop,
                    style={
                        "font-size": "15px",
                        "width": "80px",
                        "color": "white"
                    }
                ),
                html.Td(
                    feature["properties"][prop],
                    style={
                        "font-size": "15px",
                        "color": "white"
                    }
                )
            ]
        ))
    table_body = [html.Tbody(table_body_content[:-1])]
    # completing table
    table = dbc.Table(
        table_header + table_body,
        style={"marginBottom": "-3px"},
        size="sm",
        bordered=True,
        striped=True,
        dark=True
    )
    return html.Div([html.Div(header), table])


### Ground Truth class!!!
def init_parameters_filter(sample_freq, warmup_data, cut_off_freq=2):
    order = 4
    filter_b, filter_a = signal.butter(order, cut_off_freq / (sample_freq / 2), 'low', False) #filter parameters
    zf = signal.lfilter_zi(filter_b, filter_a)
    _, zf = signal.lfilter(filter_b, filter_a, warmup_data, zi=zf)
    _, filter_zf = signal.lfilter(filter_b, filter_a, warmup_data, zi=zf)

    return filter_b, filter_a, filter_zf

def compute_steps(acce_datas):
    step_timestamps = np.array([])
    step_indexs = np.array([], dtype=int)
    step_acce_max_mins = np.zeros((0, 4))
    sample_freq = 50 #50
    window_size = 22
    low_acce_mag = .6 #0.2 #0.6
    step_criterion = 1
    interval_threshold = 250 #460 #250

    acce_max = np.zeros((2,))
    acce_min = np.zeros((2,))
    acce_binarys = np.zeros((window_size,), dtype=int)
    acce_mag_pre = 0
    state_flag = 0

    warmup_data = np.ones((window_size,)) * 9.81
    filter_b, filter_a, filter_zf = init_parameters_filter(sample_freq, warmup_data)
    acce_mag_window = np.zeros((window_size, 1))

    # detect steps according to acceleration magnitudes
    for i in np.arange(0, np.size(acce_datas, 0)):
        acce_data = acce_datas[i, :]
        acce_mag = np.sqrt(np.sum(acce_data[1:] ** 2))

        acce_mag_filt, filter_zf = signal.lfilter(filter_b, filter_a, [acce_mag], zi=filter_zf)
        acce_mag_filt = acce_mag_filt[0]

        acce_mag_window = np.append(acce_mag_window, [acce_mag_filt])
        acce_mag_window = np.delete(acce_mag_window, 0)
        mean_gravity = np.mean(acce_mag_window)
        acce_std = np.std(acce_mag_window)
        mag_threshold = np.max([low_acce_mag, 0.4 * acce_std])

        # detect valid peak or valley of acceleration magnitudes
        acce_mag_filt_detrend = acce_mag_filt - mean_gravity
        if acce_mag_filt_detrend > np.max([acce_mag_pre, mag_threshold]):
            # peak
            acce_binarys = np.append(acce_binarys, [1])
            acce_binarys = np.delete(acce_binarys, 0)
        elif acce_mag_filt_detrend < np.min([acce_mag_pre, -mag_threshold]):
            # valley
            acce_binarys = np.append(acce_binarys, [-1])
            acce_binarys = np.delete(acce_binarys, 0)
        else:
            # between peak and valley
            acce_binarys = np.append(acce_binarys, [0])
            acce_binarys = np.delete(acce_binarys, 0)

        if (acce_binarys[-1] == 0) and (acce_binarys[-2] == 1):
            if state_flag == 0:
                acce_max[:] = acce_data[0], acce_mag_filt
                state_flag = 1
            elif (state_flag == 1) and ((acce_data[0] - acce_max[0]) <= interval_threshold) and (
                    acce_mag_filt > acce_max[1]):
                acce_max[:] = acce_data[0], acce_mag_filt
            elif (state_flag == 2) and ((acce_data[0] - acce_max[0]) > interval_threshold):
                acce_max[:] = acce_data[0], acce_mag_filt
                state_flag = 1

        # choose reasonable step criterion and check if there is a valid step
        # save step acceleration data: step_acce_max_mins = [timestamp, max, min, variance]
        step_flag = False
        if step_criterion == 2:
            if (acce_binarys[-1] == -1) and ((acce_binarys[-2] == 1) or (acce_binarys[-2] == 0)):
                step_flag = True
#         elif step_criterion == 3:
#             if (acce_binarys[-1] == -1) and (acce_binarys[-2] == 0) and (np.sum(acce_binarys[:-2]) > 1):
#                 step_flag = True
        else:
            if (acce_binarys[-1] == 0) and acce_binarys[-2] == -1:
                if (state_flag == 1) and ((acce_data[0] - acce_min[0]) > interval_threshold):
                    acce_min[:] = acce_data[0], acce_mag_filt
                    state_flag = 2
                    step_flag = True
                elif (state_flag == 2) and ((acce_data[0] - acce_min[0]) <= interval_threshold) and (
                        acce_mag_filt < acce_min[1]):
                    acce_min[:] = acce_data[0], acce_mag_filt
        if step_flag:
            step_timestamps = np.append(step_timestamps, acce_data[0])
            step_indexs = np.append(step_indexs, [i])
            step_acce_max_mins = np.append(step_acce_max_mins,
                                           [[acce_data[0], acce_max[1], acce_min[1], acce_std ** 2]], axis=0)
        acce_mag_pre = acce_mag_filt_detrend

    return step_timestamps, step_indexs, step_acce_max_mins

def step_counter():
    print('The number of stesps is:' ,  len(step_timestamps))


def compute_stride_length(step_acce_max_mins):
    K = 0.4
    K_max = 0.8
    K_min = 0.4
    para_a0 = 0.21468084
    para_a1 = 0.09154517
    para_a2 = 0.02301998

    stride_lengths = np.zeros((step_acce_max_mins.shape[0], 2))
    k_real = np.zeros((step_acce_max_mins.shape[0], 2))
    step_timeperiod = np.zeros((step_acce_max_mins.shape[0] - 1, ))
    stride_lengths[:, 0] = step_acce_max_mins[:, 0]
    window_size = 2
    step_timeperiod_temp = np.zeros((0, ))

    # calculate every step period - step_timeperiod unit: second
    for i in range(0, step_timeperiod.shape[0]):
        step_timeperiod_data = (step_acce_max_mins[i + 1, 0] - step_acce_max_mins[i, 0]) / 1000
        step_timeperiod_temp = np.append(step_timeperiod_temp, [step_timeperiod_data])
        if step_timeperiod_temp.shape[0] > window_size:
            step_timeperiod_temp = np.delete(step_timeperiod_temp, [0])
        step_timeperiod[i] = np.sum(step_timeperiod_temp) / step_timeperiod_temp.shape[0]

    # calculate parameters by step period and acceleration magnitude variance
    k_real[:, 0] = step_acce_max_mins[:, 0]
    k_real[0, 1] = K
    for i in range(0, step_timeperiod.shape[0]):
        k_real[i + 1, 1] = np.max([(para_a0 + para_a1 / step_timeperiod[i] + para_a2 * step_acce_max_mins[i, 3]), K_min])
        k_real[i + 1, 1] = np.min([k_real[i + 1, 1], K_max]) * (K / K_min)

    # calculate every stride length by parameters and max and min data of acceleration magnitude
    stride_lengths[:, 1] = np.max([(step_acce_max_mins[:, 1] - step_acce_max_mins[:, 2]),
                                   np.ones((step_acce_max_mins.shape[0], ))], axis=0)**(1 / 4) * k_real[:, 1]

    return stride_lengths

def get_rotation_matrix_from_vector(rotation_vector):
    q1 = rotation_vector[0]
    q2 = rotation_vector[1]
    q3 = rotation_vector[2] # rotation vector in 3, part of unit quaternion>>q1*q1 + q2*q2 + q3*q3 is less than 1

    if rotation_vector.size >= 4:
        q0 = rotation_vector[3]   #rotation vector input as unit quaternion should be like that(q1,q2,q3,q0)
    else:
        q0 = 1 - q1*q1 - q2*q2 - q3*q3
        if q0 > 0:
            q0 = np.sqrt(q0)
        else:
            q0 = 0

    sq_q1 = 2 * q1 * q1
    sq_q2 = 2 * q2 * q2
    sq_q3 = 2 * q3 * q3
    q1_q2 = 2 * q1 * q2
    q3_q0 = 2 * q3 * q0
    q1_q3 = 2 * q1 * q3
    q2_q0 = 2 * q2 * q0
    q2_q3 = 2 * q2 * q3
    q1_q0 = 2 * q1 * q0

    R = np.zeros((9,))
    if R.size == 9:
        R[0] = 1 - sq_q2 - sq_q3
        R[1] = q1_q2 - q3_q0
        R[2] = q1_q3 + q2_q0

        R[3] = q1_q2 + q3_q0
        R[4] = 1 - sq_q1 - sq_q3
        R[5] = q2_q3 - q1_q0

        R[6] = q1_q3 - q2_q0
        R[7] = q2_q3 + q1_q0
        R[8] = 1 - sq_q1 - sq_q2

        R = np.reshape(R, (3, 3))
    elif R.size == 16:
        R[0] = 1 - sq_q2 - sq_q3
        R[1] = q1_q2 - q3_q0
        R[2] = q1_q3 + q2_q0
        R[3] = 0.0

        R[4] = q1_q2 + q3_q0
        R[5] = 1 - sq_q1 - sq_q3
        R[6] = q2_q3 - q1_q0
        R[7] = 0.0

        R[8] = q1_q3 - q2_q0
        R[9] = q2_q3 + q1_q0
        R[10] = 1 - sq_q1 - sq_q2
        R[11] = 0.0

        R[12] = R[13] = R[14] = 0.0
        R[15] = 1.0

        R = np.reshape(R, (4, 4))

    return R


def get_orientation(R):
    if np.linalg.det(R) < 0:
        print(np.linalg.det(R))
    flat_R = R.flatten()
    values = np.zeros((3,))
    if np.size(flat_R) == 9:
        values[0] = np.arctan2(flat_R[1], flat_R[4])
#         if flat_R[1] < 0:
#             values[0] = -2*np.pi + np.arctan2(flat_R[1], flat_R[4])
#         else:
#             values[0] =  np.arctan2(flat_R[1], flat_R[4])
#         if flat_R[1]<0 and flat_R[4] < 0:
#             values[0] =  np.arctan2(flat_R[1], flat_R[4])
#         else:
#             values[0] =  np.arctan2(flat_R[1], flat_R[4])
        values[1] = np.arcsin(-flat_R[7])
        values[2] = np.arctan2(-flat_R[6], flat_R[8])
    else:
        values[0] = np.arctan2(flat_R[1], flat_R[5])
        values[1] = np.arcsin(-flat_R[9])
        values[2] = np.arctan2(-flat_R[8], flat_R[10])

    return values

def compute_headings(ahrs_datas):
    headings = np.zeros((np.size(ahrs_datas, 0), 2))
    for i in np.arange(0, np.size(ahrs_datas, 0)):
        ahrs_data = ahrs_datas[i, :]
        rot_mat = get_rotation_matrix_from_vector(ahrs_data[1:])
        azimuth, pitch, roll = get_orientation(rot_mat)
        around_z = (-azimuth) # % (2 * np.pi)
        headings[i, :] = ahrs_data[0], around_z
    return headings

def compute_step_heading(step_timestamps, headings):
    step_headings = np.zeros((len(step_timestamps), 2))
    step_timestamps_index = 0
    for i in range(0, len(headings)):
        if step_timestamps_index < len(step_timestamps):
            if headings[i, 0] == step_timestamps[step_timestamps_index]:
                step_headings[step_timestamps_index, :] = headings[i, :]
                step_timestamps_index += 1
        else:
            break
    assert step_timestamps_index == len(step_timestamps)

    return step_headings

def compute_rel_positions(stride_lengths, step_headings):
    rel_positions = np.zeros((stride_lengths.shape[0], 3))
    for i in range(0, stride_lengths.shape[0]):
        rel_positions[i, 0] = stride_lengths[i, 0]
        rel_positions[i, 1] = -stride_lengths[i, 1] * np.sin(step_headings[i, 1]) ########## Why - minus?!!!
        rel_positions[i, 2] = stride_lengths[i, 1] * np.cos(step_headings[i, 1])

    return rel_positions


def compute_step_positions(acce_datas, ahrs_datas, posi_datas):
    step_timestamps, step_indexs, step_acce_max_mins = compute_steps(acce_datas)
    headings = compute_headings(ahrs_datas)
    stride_lengths = compute_stride_length(step_acce_max_mins)
    step_headings = compute_step_heading(step_timestamps, headings)
    rel_positions = compute_rel_positions(stride_lengths, step_headings)
    step_positions = correct_positions(rel_positions, posi_datas)

    return step_positions

def correct_positions(rel_positions, reference_positions):
    """

    :param rel_positions:
    :param reference_positions:
    :return:
    """
    rel_positions_list = split_ts_seq(rel_positions, reference_positions[:, 0])
    if len(rel_positions_list) != reference_positions.shape[0] - 1:
        # print(f'Rel positions list size: {len(rel_positions_list)}, ref positions size: {reference_positions.shape[0]}')
        del rel_positions_list[-1]
    assert len(rel_positions_list) == reference_positions.shape[0] - 1

    corrected_positions = np.zeros((0, 3))
    for i, rel_ps in enumerate(rel_positions_list):
        start_position = reference_positions[i]
        end_position = reference_positions[i + 1]
        abs_ps = np.zeros(rel_ps.shape)
        abs_ps[:, 0] = rel_ps[:, 0]
#         abs_ps[:, 1:3] = rel_ps[:, 1:3] + start_position[1:3]
        abs_ps[0, 1:3] = rel_ps[0, 1:3] + start_position[1:3]
        for j in range(1, rel_ps.shape[0]):
            abs_ps[j, 1:3] = abs_ps[j-1, 1:3] + rel_ps[j, 1:3]
        abs_ps = np.insert(abs_ps, 0, start_position, axis=0)
        corrected_xys = correct_trajectory(abs_ps[:, 1:3], end_position[1:3])
        corrected_ps = np.column_stack((abs_ps[:, 0], corrected_xys))
        if i == 0:
            corrected_positions = np.append(corrected_positions, corrected_ps, axis=0)
        else:
            corrected_positions = np.append(corrected_positions, corrected_ps[1:], axis=0)

    corrected_positions = np.array(corrected_positions)

    return corrected_positions


def split_ts_seq(ts_seq, sep_ts):
    """

    :param ts_seq:
    :param sep_ts:
    :return:
    """
    tss = ts_seq[:, 0].astype(float)
    unique_sep_ts = np.unique(sep_ts)
    ts_seqs = []
    start_index = 0
    for i in range(0, unique_sep_ts.shape[0]):
        end_index = np.searchsorted(tss, unique_sep_ts[i], side='right')
        if start_index == end_index:
            continue
        ts_seqs.append(ts_seq[start_index:end_index, :].copy())
        start_index = end_index

    # tail data
    if start_index < ts_seq.shape[0]:
        ts_seqs.append(ts_seq[start_index:, :].copy())
    return ts_seqs

def correct_trajectory(original_xys, end_xy):
    """

    :param original_xys: numpy ndarray, shape(N, 2)
    :param end_xy: numpy ndarray, shape(1, 2)
    :return:
    """
    corrected_xys = np.zeros((0, 2))

    A = original_xys[0, :]
    B = end_xy
    Bp = original_xys[-1, :]

    angle_BAX = np.arctan2(B[1] - A[1], B[0] - A[0])
    angle_BpAX = np.arctan2(Bp[1] - A[1], Bp[0] - A[0])
    angle_BpAB = angle_BpAX - angle_BAX
    AB = np.sqrt(np.sum((B - A) ** 2))
    ABp = np.sqrt(np.sum((Bp - A) ** 2))

    corrected_xys = np.append(corrected_xys, [A], 0)
    for i in np.arange(1, np.size(original_xys, 0)):
        angle_CpAX = np.arctan2(original_xys[i, 1] - A[1], original_xys[i, 0] - A[0])

        angle_CAX = angle_CpAX - angle_BpAB

        ACp = np.sqrt(np.sum((original_xys[i, :] - A) ** 2))

        AC = ACp * AB / ABp

        delta_C = np.array([AC * np.cos(angle_CAX), AC * np.sin(angle_CAX)])

        C = delta_C + A

        corrected_xys = np.append(corrected_xys, [C], 0)

    return corrected_xys

def heading_thomas_without_zupt(acc,gyr,freq):
    
    A_geg = acc[:,1:]    
    W = 0
    W_save = []
    headings = np.zeros((np.size(gyr, 0), 2))
    for i in range(len(acc[:,0])):
        A_geg[1,:] = 0.05 * A_geg[1,:] + 0.95 * acc[i,1:]
        a = np.arctan(A_geg[0,1] /A_geg[0,2])  
        b = np.arctan(A_geg[0,0] /A_geg[0,2]) 
        Rx = np.array([[1, 0, 0],[0, np.cos(a), -np.sin(a)],[0, np.sin(a), np.cos(a)]])
        Ry = np.array([[np.cos(b), 0, -np.sin(b)],[0, 1, 0],[np.sin(b), 0, np.cos(b)]])
        Ryx = np.matmul(Rx,Ry)
        G_eben = np.matmul(Ryx,gyr[i,1:].transpose())
        W = W + G_eben[2]/freq
        #W = W +  G_eben.transpose()/freq
        #aroundz = W[i,2]
        #W_save.append(W)
        #A_eben = np.matmul(Ryx,A_geg.transpose())
        headings[i, :] = gyr[i,0], W
    return headings

def heading_thomas(acc, gyr, freq):
    #apply ZUPT0
    gyroofset = np.mean(gyr[0:200,1:4])
    gyrnew = np.zeros((np.size(gyr, 0), 4))
    gyrnew[:,1:4] = gyr[:,1:4] - gyroofset
    
    A_geg = acc[:,1:]    
    W = 0
    W_save = []
    headings = np.zeros((np.size(gyrnew, 0), 2))
    for i in range(len(acc[:,0])):
        A_geg[1,:] = .05 * A_geg[1,:] + 0.95 * acc[i,1:]
        a = np.arctan(A_geg[0,1] /A_geg[0,2])  
        b = np.arctan(A_geg[0,0] /A_geg[0,2]) 
        Rx = np.array([[1, 0, 0],[0, np.cos(a), -np.sin(a)],[0, np.sin(a), np.cos(a)]])
        Ry = np.array([[np.cos(b), 0, -np.sin(b)],[0, 1, 0],[np.sin(b), 0, np.cos(b)]])
        Ryx = np.matmul(Rx,Ry)
        G_eben = np.matmul(Ryx,gyrnew[i,1:].transpose())
        W = W + G_eben[2]/freq
        #W = W +  G_eben.transpose()/freq
        #aroundz = W[i,2]
        #W_save.append(W)
        #A_eben = np.matmul(Ryx,A_geg.transpose())
        headings[i, :] = gyr[i,0], W
        
        
    return headings



#### Coordinate Simulation class!!!

def closest_value(input_list, input_value):
    """
    return the closest value to a given input value from a list of given values

    Parameters
    ----------
    input_list : list of values - list of floats
    input_value : value for which the closest value is determined - float

    Returns
    -------
    arr[i] : closest value from the list to the given value - float
    """
    arr = np.asarray(input_list)

    i = (np.abs(arr - input_value)).argmin()

    return arr[i]


def semantic_error(number_range, error_range, intervall_range, time_stamps):
    """
        creating semantic error values. the number of occurences, the error values and the length of each intervall of
        semantic errors is randomly chosen from a given range

        Parameters
        ----------
        number_range : range of number of accurances of semantic errors - tuple of integers
        error_range : range of possible error values for the semantic error - tuple of floats
        intervall_range : range of possible lengths for the semantic errors - tuple of floats
        time_stamps : time stamps from the ground truth data - list of floats

        Returns
        -------
        intervall_lengths : length of all intervalls with semantic error - list of floats
        errors : standard deviations for each semantic error intervall - list of floats
        intervall_starts : start time of each semantic error intervall - list of floats
        """
    number_of_intervalls = np.random.randint(number_range[0], number_range[-1])
    intervall_lengths = []
    intervall_starts = []
    errors = []

    for i in range(number_of_intervalls):
        intervall_lengths.append(np.random.uniform(intervall_range[0], intervall_range[
            -1]))  # choose random intervalls (according to number of intervalls) from the timeline
        intervall_starts.append(np.random.choice(time_stamps[:-1]))
        errors.append(np.random.uniform(error_range[0], error_range[-1]))

    return intervall_lengths, errors, intervall_starts


def simulate_positions(filename, error, freq, number_range, error_range, intervall_range, semantic):
    """
        creating sample data points for 5G measurements with defined frequency and measurement error range. Semantic errors are
        generated in rondomly with chosen ranges for the duration, standard deviation and number of accurances

        Parameters
        ----------
        semantic : if True use semantic errors, if False don't use semantic errors - Boolean
        filename : name of csv file containing groundtrouth data points - string
        error : desired error for 5G positions  - float
        freq : frequency of 5G measurements in (number of measurements/second) - float
        number_range : range of number of accurances of semantic errors - tuple of integers
        error_range : range of possible error values for the semantic error - tuple of floats
        intervall_range : range of possible lengths for the semantic errors - tuple of floats

        Returns
        -------
        positions : simulated positions from 5G measurements - array of arrays (tuples) of floats
        time_stamps : timestamps of 5G measurements - array of floats
        error_list : list of the errors for each measurement - array of floats
        qualities_list : estimated qualities for each measurement (as closest value from an list of quality values to the real error) - array of floats
        """
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        rows = []
        positions = []
        time_stamps = []

        freq = freq / 1000

        error_list = []
        for row in reader:
            rows.append([float(row[0].split(' ')[0]), float(row[0].split(' ')[1]), float(row[0].split(' ')[2])])

        original_time_stamps = [r[0] for r in rows]
        intervall_lengths, semantic_errors, intervall_starts = semantic_error(number_range, error_range,
                                                                              intervall_range, original_time_stamps)
        count = 0
        semantic_active = False

        for r in range(len(rows)):

            time_stamps.append(rows[r][0])

            if semantic == True:
                if rows[r][0] >= intervall_starts[count] and rows[r][0] <= intervall_starts[count] + intervall_lengths[
                    count]:
                    current_error = semantic_errors[count]
                    semantic_active == True

                elif semantic_active == True:
                    current_error = semantic_errors[count]
                    count += 1
                elif semantic_active == False:
                    current_error = error
            else:
                current_error = error

            x_error = np.random.normal(0, current_error)
            y_error = np.random.normal(0, current_error)
            error_list.append(np.sqrt(x_error ** 2 + y_error ** 2))
            positions.append([rows[r][1] + x_error, rows[r][2] + y_error])

            dt = 1 / freq
            #t1 = rows[r][0]
            t2 = rows[r][0] + dt

            if r <= len(rows) - 2:
                dx = ((rows[r + 1][1] - rows[r][1]) / (rows[r + 1][0] - rows[r][0])) * dt
                dy = ((rows[r + 1][2] - rows[r][2]) / (rows[r + 1][0] - rows[r][0])) * dt
                # dz = ((rows[r-1][3] - rows[r][3])/(rows[r-1][0] - rows[r][0]))*dt

                x_temp = rows[r][1] + dx
                y_temp = rows[r][2] + dy
                # z_temp = rows[r][3] + dz

            while t2 < rows[-1][0] and t2 < rows[r + 1][0]:
                time_stamps.append(t2)
                x_error = np.random.normal(0, current_error)
                y_error = np.random.normal(0, current_error)
                error_list.append(np.sqrt(x_error ** 2 + y_error ** 2))
                positions.append([x_temp + dx + np.random.uniform(-current_error, current_error, 1)[0],
                                  y_temp + dy + np.random.uniform(-current_error, current_error, 1)[0]])
                t2 = t2 + dt
                x_temp = x_temp + dx
                y_temp = y_temp + dy

        qualities_list = []
        for e in error_list:
            quality = closest_value([error / 5, 2 * error / 5, 3 * error / 5, 4 * error / 5, 5 * error / 5], e)
            qualities_list.append(quality)

        return positions, time_stamps, error_list, qualities_list

    ##### Measurement Simulation Class!!!
    
    
    

if __name__ == "__main__":
    ###Ground Truth Generation
    #tips
    #step_timestamps, step_indexs, step_acce_max_mins = compute_steps(acc)
    #headings = heading_thomas(acc,gyr,100)
    #stride_lengths = compute_stride_length(step_acce_max_mins)
    #step_headings = compute_step_heading(step_timestamps, headings)
    #rel_positions = compute_rel_positions(stride_lengths, step_headings)
    #GroundTruth = correct_positions(rel_positions, ref[:,:3])
    
    ####Coordinate Simulation
    """
    check if the simulate_positions function is working
    """

    filename = 'assets/waypoints/GroundTruthZero2Four.csv'
    error = 2
    freq = 1
    number_range = [1, 10] # range of number of occurencies for segments with semantic error
    error_range = [1, 15] # range of possible values for the semantic errors
    intervall_range = [1 * 1000, 20 * 1000] # range of intervall lengths where semantic errors are generated
    semantic_is_used = False # set this to True if semantic errors are used
    positions,time_stamps, errors, qualities = simulate_positions(filename,2,1,number_range, error_range, intervall_range,semantic_is_used)
    print('qualities',qualities)
    print('errors', errors)

    points_positions = []
    for p in positions:
        points_positions.append(Point(p))

    print(points_positions)
    gpd.GeoSeries(points_positions).plot(figsize=(10, 10), color='red', markersize=100, label='5G positions')
    plt.pause(60)

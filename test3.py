##### Utils Simulator
###IMPORTS
# dash
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc
import dash_leaflet.express as dlx
import dash_leaflet as dl
from dash import html
# built in
from datetime import datetime
import numpy as np
import os
# installed
import shapely.geometry as sh
import geopandas as gp
# general utils
import utils as u


def gt2marker() -> list:
    """
    FUNCTION
    - converts lat and lon from crs32632 (groundtruth) to crs4326
    - makes leaflet markers out of coordinates
    -------
    RETURN
    markers : list of all created markers with converted lat and lon
    """
    # icon colors
    colors = ["red", "orange", "yellow", "purple", "green", "blue", "black", "brown"]
    # showing only last layer
    num_files = next(os.walk("assets/groundtruth"))[2]        # all existing ground truth files
    print(f"num_files: {num_files}")
    show = [False for _ in range(len(num_files)-1)] + [True]  # all False, but last True -> showing only last layer
    print(f"show: {show}")
    # making layers out of all generated ground truth data
    i = 0
    layers = []
    for csv_file in os.listdir("assets/groundtruth"):
        # layer & data name
        name = csv_file.split(".")[:-1]
        # data
        gt = np.loadtxt(f"assets/groundtruth/{csv_file}", skiprows=1)[:, 1:3]
        # designing icon (from https://icons8.de/icons/set/marker)
        icon = {
            "iconUrl": f"https://img.icons8.com/emoji/344/{colors[i%len(colors)]}-circle-emoji.png",
            "iconSize": [5, 5],  # size of the icon
            "iconAnchor": [0, 0],  # point of the icon which will correspond to marker"s location
        }
        # making points out of ground truth data for converting it (crs:32632 to crs:4326)
        points = {"GroundTruth": [i for i in range(1, gt.shape[0]+1)], "geometry": [sh.Point(lat, lon) for lat, lon in gt]}
        converted_points = gp.GeoDataFrame(points, crs=32632).to_crs(4326)
        # making geojson format for creating markers
        geojson = dlx.dicts_to_geojson([dict(lat=row[1].y, lon=row[1].x) for _, row in converted_points.iterrows()])
        # making and designing markers (adding tooltip and popup)
        markers = []
        for nr, row in converted_points.iterrows():
            marker = dl.Marker(position=[row[1].y, row[1].x], icon=icon)
            markers.append(marker)
        # making layer out of markers
        layers.append(dl.Overlay(dl.LayerGroup(markers), name=name, checked=show[i]))
        i += 1
    return layers



layers = gt2marker()
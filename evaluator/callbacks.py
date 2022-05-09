##### Callbacks Evaluator
#### IMPORTS
# dash
from dash import html, Output, Input, State, no_update, callback_context, dcc
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import plotly.express as px
# installed
import geopandas as gp
# built in
from os import listdir
from datetime import datetime
import numpy as np
import shutil as st
# utils (general & evaluator)
import utils as u
import evaluator.utils as eu



def eval_calls(app, geojson_style):
    # upload rest =======================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("eval_ul_warn", "is_open"),  # rest upload warn
        Output("eval_ul_done", "is_open"),  # rest upload done
        # loading
        Output("eval_spin1", "children"),   # loading status
        ### Inputs ###
        # modals
        State("eval_ul_warn", "is_open"),
        State("eval_ul_done", "is_open"),
        # maps
        Input("eval_ul_map", "contents"),
        State("eval_ul_map", "filename"),
        # ground truth
        Input("ul_gt", "contents"),
        State("ul_gt", "filename"),
        # trajectories
        Input("ul_tra", "contents"),
        State("ul_tra", "filename"),
        # gyroscope
        Input("eval_ul_gyr", "contents"),
        State("eval_ul_gyr", "filename"),
        # acceleration
        Input("eval_ul_acc", "contents"),
        State("eval_ul_acc", "filename"),
        # barometer
        Input("eval_ul_bar", "contents"),
        State("eval_ul_bar", "filename"),
        # magnetometer
        Input("eval_ul_mag", "contents"),
        State("eval_ul_mag", "filename")
    )
    def upload(
        ## modals
        ul_warn,
        ul_done,
        ## upload
        map_contents,   # maps
        map_filenames,
        gt_contents,   # ground truth
        gt_filenames,
        tra_contents,  # trajectory
        tra_filenames,
        #--- sensors
        gyr_contents,  # gyroscope
        gyr_filenames,
        acc_contents,  # acceleration
        acc_filenames,
        bar_contents,  # barometer
        bar_filenames,
        mag_contents,  # magnetometer
        mag_filenames
        ): 
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        # UPLOAD
        # ========== MAPS ==================================================================================================================
        if "eval_ul_map" in button:
            for i in range(len(map_filenames)):
                if map_filenames[i].split(".")[-1] in ["geojson"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(map_contents[i]) # decoding uploaded base64 file
                    gp_file = gp.read_file(decoded_content)
                    converted = gp.GeoDataFrame(gp_file, crs=gp_file.crs).to_crs(4326) # converting crs from uploaded file to WGS84
                    converted.to_file(f"assets/maps/{map_filenames[i]}", driver="GeoJSON") # saving converted layer
                    return ul_warn, not ul_done, no_update # if everything went fine ...
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========== GROUND TRUTH ==================================================================================================================
        if "ul_gt" in button:
            for i in range(len(gt_filenames)):
                if gt_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    gt_decoded = u.upload_encoder(gt_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/groundtruth/{gt_filenames[i]}", "w") as file: file.write(gt_decoded) # saving file
                    return ul_warn, not ul_done, no_update # if everything went fine ...
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========== TRAJECTORIES =================================================================================================================
        elif "ul_tra" in button:
            for i in range(len(tra_filenames)):
                if tra_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(tra_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/trajectories/{tra_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========== GYROSCOPE =================================================================================================================
        elif "eval_ul_gyr" in button:
            for i in range(len(gyr_filenames)):
                if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(gyr_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/gyr/{gyr_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========= ACCELERATION  ==============================================================================================================
        elif "eval_ul_acc" in button:
            for i in range(len(acc_filenames)):
                if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(acc_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/acc/{acc_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========= BAROMETER  =================================================================================================================
        elif "eval_ul_bar" in button:
            for i in range(len(bar_filenames)):
                if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(bar_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/bar/{bar_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ======== MAGNETOMETER  ===============================================================================================================
        elif "eval_ul_mag" in button:
            for i in range(len(mag_filenames)):
                if mag_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(mag_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/mag/{mag_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update  
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> no warnings
        else: return ul_warn, ul_done, no_update

        # open simulate measurement =========================================================================================================
    
    # open cdf =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("cdf_modal", "is_open"),      # modal
        Output("eval_gt_select", "options"), # ground truth dropdown
        Output("traj_select", "options"),    # trajectory dropdown
        Output("map_select", "options"),    # map dropdown
        ### Inputs ###
        # modal
        State("cdf_modal", "is_open"),
        # button
        Input("open_cdf", "n_clicks")
    )
    def open_cdf(
        # modal status
        cdf_modal,
        # button
        open_cdf
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "open_cdf" in button:
            gt_options   = [{"label": name.split(".")[0], "value": name.split(".")[0]} for name in listdir("assets/groundtruth")]
            traj_options = [{"label": name.split(".")[0], "value": name.split(".")[0]} for name in listdir("assets/trajectories")]
            map_options = [{"label": name.split(".")[0], "value": name.split(".")[0]} for name in listdir("assets/maps")]
            return not cdf_modal, gt_options, traj_options, map_options
        else: return cdf_modal, [], [], []

    # cdf =======================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("cdf_warn", "is_open"),
        Output("cdf_done", "is_open"),
        # graph
        Output("graph", "figure"),
        # spinner
        Output("eval_spin2", "children"),
        ### Inputs ###
        # modals
        State("cdf_warn", "is_open"),
        State("cdf_done", "is_open"),
        # data
        Input("eval_gt_select", "value"),
        Input("traj_select", "value"),
        Input("map_select", "value"),
        # button
        Input("cdf_btn", "n_clicks")
    )
    def cdf(
        # modals
        cdf_warn,
        cdf_done,
        # data
        gt_select,
        traj_select,
        map_select,
        # button
        cdf_btn
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "cdf_btn" in button:
            if  gt_select and traj_select:
                # data
                gt  = np.loadtxt(f"assets/groundtruth/{gt_select}.csv", delimiter=";", skiprows=1)
                traj = np.loadtxt(f"assets/trajectories/{traj_select}.csv", delimiter=";")
                # interpolation
                gt_ip, traj_ip = eu.interpolation(gt, traj)
                # name
                name = str(traj_select)
                # percentage
                if map_select:
                    perc = eu.percentage(gp.read_file(f"assets/maps/{map_select}.geojson"), gt_ip, traj_ip)*100
                    name = f"{traj_select} | perc: {perc:.2f}%"
                # cdf
                cdf = eu.cdf(gt_ip, traj_ip)
                # graph
                df = eu.dataframe4graph(cdf, name)
                fig = px.line(data_frame=df, x='err', y='cdf', title="CDF", color="Trajectory")
                fig.update_traces(mode='lines')
                return cdf_warn, not cdf_done, fig, no_update     # cdf successful
            else: return not cdf_warn, cdf_done,  {}, no_update   # cdf unsuccessful
        else: return cdf_warn, cdf_done,  {}, no_update       # modals are closed

    # visual modal =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("visual_modal", "is_open"),  # modal
        ### Inputs ###
        State("visual_modal", "is_open"),   # visual modal
        Input("open_visual", "n_clicks")    # button
    )
    def open_visual(
        # modal
        visual_modal,
        # button
        open_visual
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "open_visual" in button: return not visual_modal # open modal
        else: return visual_modal # let modal closed

    # help canvas =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("eval_help_cv", "is_open"),    # canvas
        ### Inputs ###
        State("eval_help_cv", "is_open"),     # canvas status
        Input("eval_help_btn", "n_clicks")    # button
    )
    def help(
        # canvas status
        eval_help_cv,
        # button
        help_clicks
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "eval_help_btn" in button: return not eval_help_cv     # activate help offcanvas
        else: return eval_help_cv


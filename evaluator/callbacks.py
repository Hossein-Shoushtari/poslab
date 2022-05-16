##### Callbacks Evaluator
#### IMPORTS
# dash
from dash import html, Output, Input, State, no_update, callback_context, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_leaflet as dl
# installed
import geopandas as gp
# built in
from os import listdir
import shutil as st
import pandas as pd
import numpy as np
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

    # open cdf =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("cdf_cv", "is_open"),         # canvas
        Output("eval_gt_select", "options"), # ground truth dropdown
        Output("traj_select", "options"),    # trajectory dropdown
        Output("map_select", "options"),     # map dropdown
        ### Inputs ###
        # modal
        State("cdf_cv", "is_open"),
        # button
        Input("open_cdf", "n_clicks")
    )
    def open_cdf(
        # canvas status
        cdf_cv,
        # button
        open_cdf
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "open_cdf" in button:
            gt_options   = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/groundtruth")]
            traj_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/trajectories")]
            map_options = [{"label": name[:-8], "value": name[:-8]} for name in listdir("assets/maps")]
            return not cdf_cv, gt_options, traj_options, map_options
        else: return cdf_cv, [], [], []

    # cdf =======================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("cdf_warn", "is_open"),
        Output("cdf_show", "is_open"),
        # graph
        Output("graph", "figure"),
        # spinner
        Output("eval_spin2", "children"),
        ### Inputs ###
        # modals
        State("cdf_warn", "is_open"),
        State("cdf_show", "is_open"),
        # checkboxes
        Input("percent", "value"),
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
        cdf_show,
        # checkboxes
        percent,
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
                gt  = np.loadtxt(f"assets/groundtruth/{gt_select}.csv", skiprows=1)
                trajs = [np.loadtxt(f"assets/trajectories/{traj}.csv", skiprows=1) for traj in traj_select]
                df = []
                # interpolation
                interpolations = eu.interpolation(gt, trajs)
                # cdf
                for i in range(len(traj_select)):
                    # name
                    name = str(traj_select[i])
                    # percentage
                    if map_select and percent[-1]:
                        perc = eu.percentage(gp.read_file(f"assets/maps/{map_select}.geojson"), interpolations[i][0], interpolations[i][1])*100
                        name = f"{traj_select[i]} | pip: {perc:.2f}%"
                    # cdf
                    cdf = eu.cdf(interpolations[i][0], interpolations[i][1])
                    df.append(eu.dataframe4graph(cdf, name))
                # figure
                fig = px.line(data_frame=pd.concat(df), x='RMSE [m]', y='CDF', title="CDF", color="trajectory")
                fig.update_traces(mode='markers')
                return cdf_warn, not cdf_show, fig, no_update     # cdf successful
            else: return not cdf_warn, cdf_show, {}, no_update    # cdf unsuccessful
        else: return cdf_warn, cdf_show, {}, no_update            # modals are closed

        # export ============================================================================================================================
    
    # export ============================================================================================================================
    @app.callback(
        ### Outputs ###
        # modal
        Output("eval_exp_done", "is_open"),    # export done status
        Output("eval_exp_warn", "is_open"),    # export warn status
        # download
        Output("eval_export", "data"),         # export data
        # loading
        Output("eval_spin3", "children"),      # loading status
        ### Inputs ###
        # modal
        State("eval_exp_done", "is_open"),     # done
        State("eval_exp_warn", "is_open"),     # warn
        # button
        Input("eval_exp_btn", "n_clicks"),     # export button click status
    )
    def export(
        # modal
        exp_done,
        exp_warn,
        # button
        exp_clicks
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "eval_exp_btn" in button:
            return exp_done, not exp_warn, no_update, no_update # nothing to export yet
        else:
            return exp_done, exp_warn, no_update, no_update # no button clicked

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


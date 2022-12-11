##### Callbacks Evaluator
#### IMPORTS
# dash
from dash import html, Output, Input, State, no_update, callback_context, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import dash_leaflet as dl
# installed
import geopandas as gp
# built in
from os import listdir
import shutil as st
import pandas as pd
import numpy as np
import json
import time
# utils (general & evaluator)
import evaluator.utils as eu
import utils as u



def eval_calls(app, nc):
    # upload maps =====================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("eval_usr_warn1", "is_open"),  # user missing
        Output("eval_map_warn", "is_open"),   # map upload warn
        # layers
        Output("eval_map_layers", "data"),
        # loading
        Output("eval_spin1", "children"),     # loading status
        ### Inputs ###
        # modal
        State("eval_usr_warn1", "is_open"),
        State("eval_map_warn", "is_open"),
        # maps
        Input("eval_ul_map", "contents"),
        State("eval_ul_map", "filename"),
        # user
        Input("usr_data", "data")
    )
    def upload(
        ## modal
        usr_warn,
        map_warn,
        ## upload
        map_contents,
        map_filenames,
        # user
        user
        ):
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        # UPLOAD
        #============= MAP =====================================================================================================================
        if "eval_ul_map" in button:
            # checking if user is logged in
            if user["username"]:
                un = user["username"]
                pw = user["password"]
                # start upload
                file_check = [name.split(".")[-1] for name in map_filenames if name.split(".")[-1] not in ["geojson"]] # getting all wrong file formats
                if len(file_check) > 0: return usr_warn, not map_warn, no_update, no_update # activating modal -> warn
                for i in range(len(map_filenames)): # only right files were uploaded
                    decoded_content = u.upload_encoder(map_contents[i]) # decoding uploaded base64 file
                    gp_file = gp.read_file(decoded_content)
                    converted = gp.GeoDataFrame(gp_file, crs=gp_file.crs).to_crs(4326) # converting crs from uploaded file to WGS84
                    converted.to_file(f"assets/users/{un}_{pw}/maps/{map_filenames[i]}", driver="GeoJSON") # saving converted layer
                    u.update_user_data(nc, f"{un}_{pw}/maps/{map_filenames[i]}") # push to cloud
                lon, lat = u.extract_coordinates(gp_file)
                bounds = u.boundaries(lon, lat) # boundaries for latest uploaded map
                layers = {
                    "layers": True,
                    "quantity": i+1,
                    "bounds": bounds,
                    "date": time.time()
                }
                return usr_warn, map_warn, layers, no_update # returning uploaded layers
            else:
                return not usr_warn, map_warn, no_update, no_update # returning uploaded layers
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> no warnings
        else: return usr_warn, map_warn, no_update, no_update

    # upload rest =======================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("eval_usr_warn2", "is_open"),  # user missing
        Output("eval_ul_warn", "is_open"),    # rest upload warn
        Output("eval_ul_done", "is_open"),     # rest upload done
        # layers
        Output("eval_gt_layers", "data"),
        Output("eval_traj_layers", "data"),
        # loading
        Output("eval_spin2", "children"),     # loading status
        ### Inputs ###
        # modals
        State("eval_usr_warn2", "is_open"),
        State("eval_ul_warn", "is_open"),
        State("eval_ul_done", "is_open"),
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
        State("eval_ul_mag", "filename"),
        # user
        Input("usr_data", "data")
    )
    def upload(
        ## modals
        usr_warn,
        ul_warn,
        ul_done,
        ## upload
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
        mag_filenames,
        # user
        user
        ):
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        un = user["username"]
        pw = user["password"]
        # UPLOAD
        # ========== GROUND TRUTH ==================================================================================================================
        if "ul_gt" in button:
            if un:
                for i in range(len(gt_filenames)):
                    if gt_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        gt_decoded = u.upload_encoder(gt_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}s/groundtruth/{gt_filenames[i]}", "w") as file: file.write(gt_decoded) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/groundtruth/{gt_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update, no_update # activating modal -> warn
                # getting zoom lvl and center point
                lon, lat = u.from_32632_to_4326(np.loadtxt(f"assets/users/{un}_{pw}/groundtruth/{gt_filenames[i]}", skiprows=1)[:,1:3])
                bounds = u.boundaries(lon, lat) # boundaries for latest uploaded map
                layers = {
                    "layers": True,
                    "quantity": i+1,
                    "bounds": bounds,
                    "date": time.time()
                }
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, layers, no_update, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update, no_update
        # ========== TRAJECTORIES =================================================================================================================
        elif "ul_tra" in button:
            if un:
                for i in range(len(tra_filenames)):
                    if tra_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(tra_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/trajectories/{tra_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/trajectories/{tra_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update, no_update # activating modal -> warn
                # getting zoom lvl and center point
                lon, lat = u.from_32632_to_4326(np.loadtxt(f"assets/users/{un}_{pw}/trajectories/{tra_filenames[i]}", skiprows=1)[:,1:3])
                bounds = u.boundaries(lon, lat) # boundaries for latest uploaded map
                # getting number of points -> overflow True or False
                if len(lon) > 500: overflow = True
                else: overflow = False
                layers = {
                    "layers": True,
                    "quantity": i+1,
                    "bounds": bounds,
                    "overflow": overflow,
                    "date": time.time()
                }
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update, layers, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update, no_update
        # ========== GYROSCOPE =================================================================================================================
        elif "eval_ul_gyr" in button:
            if un:
                for i in range(len(gyr_filenames)):
                    if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(gyr_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/sensors/gyr/{gyr_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/sensors/gyr/{gyr_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update, no_update # activating modal -> warn
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update, no_update, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update, no_update
        # ========= ACCELERATION  ==============================================================================================================
        elif "eval_ul_acc" in button:
            if un:
                for i in range(len(acc_filenames)):
                    if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(acc_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/sensors/acc/{acc_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/sensors/acc/{acc_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update, no_update # activating modal -> warn
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update, no_update, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update, no_update
        # ========= BAROMETER  =================================================================================================================
        elif "eval_ul_bar" in button:
            if un:
                for i in range(len(bar_filenames)):
                    if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(bar_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/sensors/bar/{bar_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/sensors/bar/{bar_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update, no_update # activating modal -> warn
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update, no_update, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update, no_update
        # ======== MAGNETOMETER  ===============================================================================================================
        elif "eval_ul_mag" in button:
            if un:
                for i in range(len(mag_filenames)):
                    if mag_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(mag_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/sensors/mag/{mag_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/sensors/mag/{mag_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update, no_update # activating modal -> warn
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update , no_update, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update, no_update
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> no warnings
        else: return usr_warn, ul_warn, ul_done, no_update, no_update, no_update

    # open cdf =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("cdf_cv", "is_open"),         # canvas
        Output("eval_gt_select", "options"), # ground truth dropdown
        Output("traj_select", "options"),    # trajectory dropdown
        Output("map_select", "options"),     # map dropdown
        ### Inputs ###
        # canvas
        State("cdf_cv", "is_open"),
        # button
        Input("open_cdf", "n_clicks"),
        # researcher login
        Input("eval_unlocked1", "data"),
        Input("eval_unlocked2", "data"),
        # user
        Input("usr_data", "data")
    )
    def open_cdf(
        # canvas status
        cdf_cv,
        # button
        open_cdf,
        # unlocked
        unlocked1,
        unlocked2,
        # user
        user
        ):
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        un = user["username"]
        pw = user["password"]
        if "open_cdf" in button:
            if un: # user logged in
                gt_options   = [{"label": name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/groundtruth")]
                traj_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/trajectories")]
                map_options = [{"label": name[:-8], "value": f"assets/users/{un}_{pw}/maps/{name[:-8]}"} for name in listdir(f"assets/users/{un}_{pw}/maps")]
                if unlocked1 or unlocked2:
                    map_options += [{"label": name[:-8], "value": f"assets/floorplans/{name[:-8]}"} for name in listdir("assets/floorplans")]
                return not cdf_cv, gt_options, traj_options, map_options
            else:
                map_options = []
                if unlocked1 or unlocked2:
                    map_options = [{"label": name[:-8], "value": f"assets/floorplans/{name[:-8]}"} for name in listdir("assets/floorplans")]
                return not cdf_cv, [], [], map_options
        else: return cdf_cv, [], [], []

    # cdf =======================================================================================================================
    @app.callback(
        ### Outputs ###
        # checkboxes
        Output("norm_box", "value"),
        Output("histo_box", "value"),
        Output("norm_status", "data"),
        Output("histo_status", "data"),
        # modals
        Output("cdf_warn", "is_open"),
        Output("cdf_show", "is_open"),
        # graph
        Output("graph", "figure"),
        # spinner
        Output("eval_spin3", "children"),
        ### Inputs ###
        # modals
        State("cdf_warn", "is_open"),
        State("cdf_show", "is_open"),
        # checkboxes
        Input("norm_box", "value"),
        Input("histo_box", "value"),
        Input("norm_status", "data"),
        Input("histo_status", "data"),
        Input("percent", "value"),
        # data
        Input("eval_gt_select", "value"),
        Input("traj_select", "value"),
        Input("map_select", "value"),
        # button
        Input("cdf_btn", "n_clicks"),
        # user
        Input("usr_data", "data")
    )
    def cdf(
        # modals
        cdf_warn,
        cdf_show,
        # checkboxes
        norm_box,
        histo_box,
        norm_status,
        histo_status,
        percent,
        # data
        gt_select,
        traj_select,
        map_select,
        # button
        cdf_btn,
        # user
        user
        ):
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        un = user["username"]
        pw = user["password"]
        if "cdf_btn" in button:
            if  gt_select and traj_select:
                # data
                gt  = np.loadtxt(f"assets/users/{un}_{pw}/groundtruth/{gt_select}.csv", skiprows=1)
                trajs = [np.loadtxt(f"assets/users/{un}_{pw}/trajectories/{traj}.csv", skiprows=1) for traj in traj_select]
                cdf_list = []
                # interpolation
                interpolations = eu.interpolation(gt, trajs)
                # cdf
                for i in range(len(traj_select)):
                    # name
                    name = str(traj_select[i])
                    # percentage
                    if map_select and percent:
                        perc = eu.percentage(gp.read_file(f"{map_select}.geojson"), interpolations[i][0], interpolations[i][1])*100
                        name = f"{traj_select[i]} | pip: {perc:.2f}%"
                    # cdf
                    if norm_box:
                        cdf = eu.normCDF(interpolations[i][0], interpolations[i][1])    # normalized
                        cdf_list.append(eu.dataframe4graph(cdf, name))
                    if histo_box:
                        cdf = eu.histoCDF(interpolations[i][0], interpolations[i][1])   # histogram
                        cdf_list.append(eu.dataframe4graph(cdf, name))

                # figure
                if norm_box:
                    fig = px.line(data_frame=pd.concat(cdf_list), x="RMSE [m]", y="CDF", title="Normalized", color="trajectory")
                    fig.update_traces(mode='lines')
                elif histo_box:
                    fig = px.line(data_frame=pd.concat(cdf_list), x="RMSE [m]", y="CDF", title="Histogram", color="trajectory")
                    fig.update_traces(mode='lines')

                return no_update, no_update, no_update, no_update, cdf_warn, not cdf_show, fig, no_update     # cdf successful
            else: return no_update, no_update, no_update, no_update, not cdf_warn, cdf_show, {}, no_update    # cdf unsuccessful
        else:
            if norm_box == 1 and histo_box == 1:
                return [1], [], [1], [], cdf_warn, cdf_show, {}, no_update
            elif norm_box != norm_status:
                if norm_box:
                    return no_update, [], [1], [], cdf_warn, cdf_show, {}, no_update
                else:
                    return [], [1], [], [1], cdf_warn, cdf_show, {}, no_update
            elif histo_box != histo_status:
                if histo_box:
                    return [], no_update, [], [1], cdf_warn, cdf_show, {}, no_update
                else:
                    return [1], [], [1], [], cdf_warn, cdf_show, {}, no_update
            else:
                return no_update, no_update, no_update, no_update, cdf_warn, cdf_show, {}, no_update     # nothing happend

    # open visual =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("visual_show", "is_open"),
        Output("vis_map_select", "options"),
        Output("vis_ref_select", "options"),
        Output("vis_gt_select", "options"),
        Output("vis_traj_select", "options"),
        Output("vis_ant_select", "options"),
        ### Inputs ###
        # modal
        State("visual_show", "is_open"),
        # button
        Input("open_visual", "n_clicks"),
        # researcher login
        Input("eval_unlocked3", "data"),
        # user
        Input("usr_data", "data")
    )
    def open_visual(
        # modal
        visual_show,
        # button
        open_visual,
        # unlocked
        unlocked,
        # user
        user
        ):
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        un = user["username"]
        pw = user["password"]
        if "open_visual" in button:
            if un: # user logged in
                map_options  = [{"label": name[:-8], "value": f"users/{un}_{pw}maps/{name[:-8]}"} for name in listdir(f"assets/users/{un}_{pw}/maps")]
                ref_options  = [{"label": name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/waypoints")]
                gt_options   = [{"label": name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/groundtruth")]
                traj_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/trajectories")]
                ant_options  = [{"label": name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/antennas")]
                if unlocked:
                    map_options += [{"label": name[:-8], "value": f"floorplans/{name[:-8]}"} for name in listdir("assets/floorplans")]
                return not visual_show, map_options, ref_options, gt_options, traj_options, ant_options
            else:
                map_options = []
                if unlocked:
                    map_options = [{"label": name[:-8], "value": f"floorplans/{name[:-8]}"} for name in listdir("assets/floorplans")]
                return not visual_show, map_options, [], [], [], []
        else: return visual_show, [], [], [], [], []

    # visual map =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("vis_map", "figure"),
        Output("vis_map", "config"),
        Output("eval_spin6", "children"),    # loading status
        ### Inputs ###
        Input("vis_map_select", "value"),
        Input("vis_ref_select", "value"),
        Input("vis_gt_select", "value"),
        Input("vis_traj_select", "value"),
        Input("vis_ant_select", "value"),
        Input("vis_bg_select", "value"),
        Input("vis_format_select", "value"),
        Input("vis_map", "figure"),
        # user
        Input("usr_data", "data")
    )
    def update_fig(
        # files
        _map,
        refs,
        gts,
        trajs,
        ant,
        bg,
        _format,
        FIG,
        # user
        user):
        # refreshing configurations
        trigger = [p["prop_id"] for p in callback_context.triggered][0]
        un = user["username"]
        pw = user["password"]
        if "vis_format_select" in trigger:
            if not _format: _format = "png"
            config={
                "staticPlot": False,        # True, False
                "scrollZoom": True,         # True, False
                "showTips": True,           # True, False
                "displayModeBar": "hover",  # True, False, "hover"
                "watermark": True,
                "editable": True,
                "toImageButtonOptions": {
                    "format": _format,      # one of png, svg, jpeg, webp
                    "filename": "map_plot",
                    "height": 1000,
                    "width": 2000,
                    "scale": 1              # multiply title/legend/axis/canvas sizes by this factor
                },
                "modeBarButtonsToAdd": [
                    "drawline",
                    "drawopenpath",
                    "drawclosedpath",
                    "drawcircle",
                    "drawrect",
                    "eraseshape"
                ]
            }
            return FIG, config, no_update
        # building figures 
        fig = go.Figure(go.Scattermapbox())
        layers = []
        zoom = 1
        center = (0, 0)
        if not bg: bg = "white-bg"
        if _map:
            # creating one dummy line for legend
            fig.add_trace(go.Scattermapbox(
                mode="lines",
                lon=[0,0],
                lat=[0,0],
                line={"color": "blue"},
                legendgrouptitle={"text": "Maps"},
                legendgroup="Maps",
                name=_map.split("/")[1]))
            # creating plotly layers
            with open(f"assets/{_map}.geojson") as json_file:
                data = json.load(json_file)
            layer = {
                "sourcetype": "geojson",
                "source": data,
                "type": "line",
                "color": "blue"
            }
            layers.append(layer)
            # getting zoom and center
            with open(f"assets/{_map}.geojson", "r") as file:
                data = file.read()
            lon, lat = u.extract_coordinates(gp.read_file(data))
            zoom = u.zoom_lvl(lon, lat)
            center = u.centroid(lon, lat)
        if refs:
            # creating plotly layers
            for ref in refs:
                data = np.loadtxt(f"assets/users/{un}_{pw}/waypoints/{ref}.csv", skiprows=1)[:, 1:3]
                lon, lat = u.from_32632_to_4326(data)
                fig.add_trace(go.Scattermapbox(
                    mode="markers",
                    lon=lon,
                    lat=lat,
                    marker={"size": 12},
                    legendgrouptitle={"text": "Waypoints"},
                    legendgroup="Waypoints",
                    name=ref))
            # getting zoom and center
            zoom = u.zoom_lvl(lon, lat)
            center = u.centroid(lon, lat)
        if gts:
            # creating plotly layers
            for gt in gts:
                data = np.loadtxt(f"assets/users/{un}_{pw}/groundtruth/{gt}.csv", skiprows=1)[:, 1:3]
                lon, lat = u.from_32632_to_4326(data)
                fig.add_trace(go.Scattermapbox(
                    mode="markers",
                    lon=lon,
                    lat=lat,
                    marker={"size": 6},
                    legendgrouptitle={"text": "Ground Truth"},
                    legendgroup="Ground Truth",
                    name=gt))
            # getting zoom and center
            zoom = u.zoom_lvl(lon, lat)
            center = u.centroid(lon, lat)
        if trajs:
            # creating plotly layers
            for traj in trajs:
                data = np.loadtxt(f"assets/users/{un}_{pw}/trajectories/{traj}.csv", skiprows=1)[:, 1:3]
                lon, lat = u.from_32632_to_4326(data)
                fig.add_trace(go.Scattermapbox(
                    mode="markers",
                    lon=lon,
                    lat=lat,
                    marker={"size": 6},
                    legendgrouptitle={"text": "Trajectories"},
                    legendgroup="Trajectories",
                    name=traj))
            # getting zoom and center
            zoom = u.zoom_lvl(lon, lat)
            center = u.centroid(lon, lat)
        if ant:
            # creating plotly layers
            data = np.loadtxt(f"assets/users/{un}_{pw}/antennas/{ant}.csv", skiprows=1)
            lon, lat = u.from_32632_to_4326(data)
            fig.add_trace(go.Scattermapbox(
                mode="markers",
                lon=lon,
                lat=lat,
                marker={"size": 14},
                legendgrouptitle={"text": "Antennas"},
                legendgroup="Antennas",
                name=ant))
            # getting zoom and center
            zoom = u.zoom_lvl(lon, lat)
            center = u.centroid(lon, lat)
        # completing figure with a nice layout
        fig.update_layout(
            margin={"l":0,"t":0,"b":0,"r":0},
            mapbox={
                # token got from https://mapbox.com/
                # heroku token: pk.eyJ1Ijoibml2cm9rMjAwMSIsImEiOiJjbDV0a3Mwa2gwbXAzM2RteDk0dnoyNnlsIn0.MwHtkUS1sevt4F8PqhbGZQ
                "accesstoken": "pk.eyJ1Ijoibml2cm9rMjAwMSIsImEiOiJjbDV0a3A3eGIweWJvM2JuMHhtYXF5aWVlIn0._01sVxeqJ8EQvGq2PclBBw", # default public token
                "center": {"lon": center[1], "lat": center[0]},
                "style": bg,
                "layers": layers,
                "zoom": zoom
            },
            legend={
                "yanchor": "top",
                "y": 0.99,
                "xanchor": "left",
                "x": 0.01
            },
            showlegend=True
        )
        return fig, no_update, no_update

    # example data =====================================================================================================================
    @app.callback(
        ### Outputs ###
        # download
        Output("eval_exdata_dl", "data"), # download data
        ### Inputs ###
        # button
        Input("eval_exdata", "n_clicks"), # export button click status
    )
    def example_data(btn):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "eval_exdata" in button:
            download = dcc.send_file("assets/example_data.zip", filename="example_data.zip")
            return download  # download
        else:
            return no_update # no button clicked

    # export ============================================================================================================================
    @app.callback(
        ### Outputs ###
        # modal
        Output("eval_usr_warn3", "is_open"),   # user missing
        Output("eval_exp_done", "is_open"),    # export done status
        Output("eval_exp_warn", "is_open"),    # export warn status
        # download
        Output("eval_export", "data"),         # export data
        # loading
        Output("eval_spin4", "children"),      # loading status
        ### Inputs ###
        # modal
        State("eval_usr_warn3", "is_open"),    # user warn
        State("eval_exp_done", "is_open"),     # done
        State("eval_exp_warn", "is_open"),     # warn
        # button
        Input("eval_exp_btn", "n_clicks"),     # export button click status
        # user
        Input("usr_data", "data")
    )
    def export(
        # modal
        usr_warn,
        exp_done,
        exp_warn,
        # button
        exp_clicks,
        # user
        user
        ):
        un = user["username"]
        pw = user["password"]
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "eval_exp_btn" in button:
            if un: # user logged in
                if len(listdir(f"assets/exports/results_{un}_{pw}/gt")) or len(listdir(f"assets/exports/results_{un}_{pw}/sm")) or len(listdir(f"assets/exports/results_{un}_{pw}/draw")):
                    # zipping & downloading
                    name = u.time()
                    zip_folder = st.make_archive(f"assets/exports/results_{name}", 'zip', f"assets/exports/results_{un}_{pw}")
                    download = dcc.send_file(f"assets/exports/results_{name}.zip", filename=f"L5IN_export_{name}.zip")
                    return usr_warn, not exp_done, exp_warn, download, no_update # export successful
                else: # nothing to export
                    return usr_warn, exp_done, not exp_warn, no_update, no_update
            else: # user isn't logged in
                return not usr_warn, exp_done, exp_warn, no_update, no_update
        else: # no button clicked
            return usr_warn, exp_done, exp_warn, no_update, no_update

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

    # hovering tooltips in hcu floorplans ===============================================================================================
    @app.callback(
        ### Outputs ###
        Output("eval_hover_info", "children"),  # info panel
        ### Inputs ###
        Input("EG_eval", "hover_feature"),      # EG
        Input("1OG_eval", "hover_feature"),     # 1OG
        Input("4OG_eval", "hover_feature"),     # 4OG
    )
    def hovering(
        # geojson info of all three layers
        feature_eg, feature_1og, feature_4og
        ):
        if feature_eg: return u.hover_info(feature_eg)       # if EG is clicked
        elif feature_1og: return u.hover_info(feature_1og)   # if 1OG is clicked
        elif feature_4og: return u.hover_info(feature_4og)   # if 4OGG is clicked
        else: return u.hover_info()                          # if nothing is clicked
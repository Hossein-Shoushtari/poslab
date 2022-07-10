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
# utils (general & evaluator)
import utils as u
import evaluator.utils as eu



def eval_calls(app, geojson_style):
    # upload maps =====================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("eval_map_warn", "is_open"), # map upload warn
        Output("eval_map_done", "is_open"), # map upload done
        # layers
        Output("eval_map_layer", "data"),
        # storage
        Output("eval_z_c_map", "data"),
        # loading
        Output("eval_spin1", "children"),   # loading status
        ### Inputs ###
        # modal
        State("eval_map_warn", "is_open"),
        State("eval_map_done", "is_open"),
        # maps
        Input("eval_ul_map", "contents"),
        State("eval_ul_map", "filename"),
    )
    def upload(
        ## modal
        map_warn,
        map_done,
        ## upload
        map_contents,
        map_filenames,
        ): 
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        # UPLOAD
        #============= MAP =====================================================================================================================
        if "eval_ul_map" in button:
            file_check = [name.split(".")[-1] for name in map_filenames if name.split(".")[-1] not in ["geojson"]] # getting all wrong file formats
            if len(file_check) > 0: return not map_warn, map_done, no_update, no_update, no_update # activating modal -> warn
            for i in range(len(map_filenames)): # only right files were uploaded
                decoded_content = u.upload_encoder(map_contents[i]) # decoding uploaded base64 file
                gp_file = gp.read_file(decoded_content)
                converted = gp.GeoDataFrame(gp_file, crs=gp_file.crs).to_crs(4326) # converting crs from uploaded file to WGS84
                converted.to_file(f"assets/maps/{map_filenames[i]}", driver="GeoJSON") # saving converted layer
            lon, lat = u.extract_coordinates(gp_file)
            zoom = u.zoom_lvl(lon, lat)               # zoom for latest uploaded map
            center = u.centroid(lon, lat)             # center of latest uploaded map
            # uploaded maps as converted layers
            layers = u.map2layer(geojson_style)
            return map_warn, not map_done, layers, [zoom, center], no_update # returning uploaded layers
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> no warnings
        else: return map_warn, map_done, [], [], no_update

    # upload rest =======================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("eval_ul_warn", "is_open"),  # rest upload warn
        Output("eval_ul_done", "is_open"),  # rest upload done
        # layers
        Output("eval_gt_layer", "data"),
        Output("traj_layer", "data"),
        # zoom & center
        Output("z_c_gt", "data"),
        Output("z_c_tr", "data"),
        # loading
        Output("eval_spin2", "children"),   # loading status
        ### Inputs ###
        # modals
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
        State("eval_ul_mag", "filename")
    )
    def upload(
        ## modals
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
        mag_filenames
        ): 
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        # UPLOAD
        # ========== GROUND TRUTH ==================================================================================================================
        if "ul_gt" in button:
            for i in range(len(gt_filenames)):
                if gt_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    gt_decoded = u.upload_encoder(gt_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/groundtruth/{gt_filenames[i]}", "w") as file: file.write(gt_decoded) # saving file
                else: return not ul_warn, ul_done, no_update, no_update, no_update, no_update, no_update # activating modal -> warn
            # getting zoom lvl and center point
            lon, lat = u.from_32632_to_4326(np.loadtxt(f"assets/groundtruth/{gt_filenames[i]}", skiprows=1)[:,1:3])
            zoom = u.zoom_lvl(lon, lat)     # zoom lvl
            center = u.centroid(lon, lat)   # center
            # making ground truth layers
            layers = u.gt2marker()
            # if everything went fine ...
            return ul_warn, not ul_done, layers, no_update, [zoom, center], no_update, no_update
        # ========== TRAJECTORIES =================================================================================================================
        elif "ul_tra" in button:
            for i in range(len(tra_filenames)):
                if tra_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(tra_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/trajectories/{tra_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update, no_update, no_update, no_update, no_update # activating modal -> warn
            # getting zoom lvl and center point
            lon, lat = u.from_32632_to_4326(np.loadtxt(f"assets/trajectories/{tra_filenames[i]}", skiprows=1)[:,1:3])
            zoom = u.zoom_lvl(lon, lat)     # zoom lvl
            center = u.centroid(lon, lat)   # center
            # making ground truth layers
            layers = u.traj2marker()
            # if everything went fine ...
            return ul_warn, not ul_done, no_update, layers, no_update, [zoom, center], no_update
        # ========== GYROSCOPE =================================================================================================================
        elif "eval_ul_gyr" in button:
            for i in range(len(gyr_filenames)):
                if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(gyr_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/gyr/{gyr_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update, no_update, no_update, no_update, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update, no_update, no_update, no_update, no_update
        # ========= ACCELERATION  ==============================================================================================================
        elif "eval_ul_acc" in button:
            for i in range(len(acc_filenames)):
                if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(acc_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/acc/{acc_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update, no_update, no_update, no_update, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update, no_update, no_update, no_update, no_update, no_update
        # ========= BAROMETER  =================================================================================================================
        elif "eval_ul_bar" in button:
            for i in range(len(bar_filenames)):
                if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(bar_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/bar/{bar_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update, no_update, no_update, no_update, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update, no_update, no_update, no_update, no_update
        # ======== MAGNETOMETER  ===============================================================================================================
        elif "eval_ul_mag" in button:
            for i in range(len(mag_filenames)):
                if mag_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(mag_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/mag/{mag_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update, no_update, no_update, no_update, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update , no_update, no_update, no_update, no_update
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> no warnings
        else: return ul_warn, ul_done, no_update, no_update, no_update, no_update, no_update

    # map display =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("eval_div_lc", "style"),     # div layer control
        Output("eval_lc", "children"),      # layer control        
        Output("eval_map", "center"),       # map center
        Output("eval_map", "zoom"),         # map zoom level
        Output("eval_hcu_panel", "style"),  # hcu info panel
        ### Inputs ###
        Input("eval_map_layer", "data"),    # maps
        Input("eval_z_c_map", "data"),      # zoom and center for latest map
        Input("traj_layer", "data"),        # trajectory
        Input("z_c_tr", "data"),            # zoom and center for traj
        Input("eval_gt_layer", "data"),     # ground truth
        Input("z_c_gt", "data"),            # zoom and center for rp and gt
        Input("eval_unlocked1", "data")     # unlocked status hcu maps
    )
    def display(
        #lays,
        map_layer,
        z_c_map,
        traj_layer,
        z_c_traj,
        gt_layer,
        z_c_gt,
        unlocked
        ):
        hcu_style = {"display": "None"}
        ly_style = {"display": "None"}
        # presetting map zoom level and center
        zoom = 4
        center = (49.845359730413186, 9.90578149727622) # center of Europe
        # getting all different layers
        layers = []
        if map_layer:
            zoom = z_c_map[0]               # zoom for latest uploaded map layer
            center = z_c_map[1]             # center of latest uploaded map layer
            layers += map_layer             # adding map (all previous + latest) layers to map
            ly_style = {"display": "block"}
        if traj_layer:
            zoom = z_c_traj[0]              # zoom
            center = z_c_traj[1]            # center
            layers += traj_layer            # adding trajectory layer to map
            ly_style = {"display": "block"}
        if gt_layer:
            zoom = z_c_gt[0]                # zoom
            center = z_c_gt[1]              # center
            layers += gt_layer              # adding gt points (all previous + latest) layers to map
            ly_style = {"display": "block"}
        if unlocked:
            zoom = 19
            center = (53.540239664876104, 10.004663417352164) # HCU coordinates
            layers += eu.floorplan2layer(geojson_style)       # adding hcu floorplans to map
            hcu_style = {"display": "block"}                  # displaying info panel
            ly_style = {"display": "block"}
        if layers: return ly_style, layers, center, zoom, hcu_style
        else: return ly_style, [], center, zoom, hcu_style
    
    # hcu canvas ========================================================================================================================
    @app.callback(
        Output("eval_research", "is_open"),
        Input("eval_hcu_maps", "n_clicks"),
        State("eval_research", "is_open")
    )
    def sim_hcu(hcu_maps, is_open):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "eval_hcu_maps" in button:
            return not is_open
        return is_open
        
    # unlock hcu maps ===================================================================================================================
    @app.callback(
        ### Outputs ###
        # return messages
        Output("eval_password", "valid"),
        Output("eval_password", "invalid"),
        # unlock status
        Output("eval_unlocked1", "data"),
        Output("eval_unlocked2", "data"),
        Output("eval_unlocked3", "data"),
        ### Inputs ###
        Input("eval_unlock", "n_clicks"),
        Input("eval_password", "value")
    )
    def unlock(unlock, password):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "eval_unlock" in button:
            if str(password) == "cpsimulation2022":
                return True, False, True, True, True
            return False, True, None, None, None
        return no_update, no_update, no_update, no_update, no_update

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
        Input("eval_unlocked2", "data")
    )
    def open_cdf(
        # canvas status
        cdf_cv,
        # button
        open_cdf,
        # unlocked
        unlocked
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "open_cdf" in button:
            gt_options   = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/groundtruth")]
            traj_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/trajectories")]
            map_options = [{"label": name[:-8], "value": f"assets/maps/{name[:-8]}"} for name in listdir("assets/maps")]
            if unlocked:
                map_options += [{"label": name[:-8], "value": f"assets/floorplans/{name[:-8]}"} for name in listdir("assets/floorplans")]
            return not cdf_cv, gt_options, traj_options, map_options
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
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "cdf_btn" in button:
            if  gt_select and traj_select:
                # data
                gt  = np.loadtxt(f"assets/groundtruth/{gt_select}.csv", skiprows=1)
                trajs = [np.loadtxt(f"assets/trajectories/{traj}.csv", skiprows=1) for traj in traj_select]
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
                        cdf_list.append(cdf + [name])

                # figure
                if norm_box:
                    fig = px.line(data_frame=pd.concat(cdf_list), x="RMSE [m]", y="CDF", title="Normalized", color="trajectory")
                    fig.update_traces(mode='markers')
                elif histo_box:
                    fig = go.Figure(data=[go.Histogram(x=err, y=cdf, name=name, showlegend=True, cumulative_enabled=True) for err, cdf, name in cdf_list],
                    layout={"title": "Histogram", "legend": {"title": "Trajectories"}, "xaxis": {"title": "RMSE [m]"}, "yaxis": {"title": "Counts"}})

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
        Output("vis_gt_select", "options"),
        Output("vis_traj_select", "options"),
        ### Inputs ###
        # modal
        State("visual_show", "is_open"),
        # button
        Input("open_visual", "n_clicks"),
        # researcher login
        Input("eval_unlocked3", "data")
        )
    def open_visual(
        # modal
        visual_show,
        # button
        open_visual,
        # unlocked
        unlocked
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        
        if "open_visual" in button:
            gt_options   = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/groundtruth")]
            traj_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/trajectories")]
            map_options = [{"label": name[:-8], "value": f"assets/maps/{name[:-8]}"} for name in listdir("assets/maps")]
            if unlocked:
                map_options += [{"label": name[:-8], "value": f"assets/floorplans/{name[:-8]}"} for name in listdir("assets/floorplans")]
            return not visual_show, map_options, gt_options, traj_options
        else: return visual_show, [], [], []

    # visual map =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("vis_map", "figure"),
        ### Inputs ###
        Input("vis_map_select", "value"),
        Input("vis_gt_select", "value"),
        Input("vis_traj_select", "value")
    )
    def update_fig(_maps, gts, trajs):
        layers = []
        if _maps:
            # creating plotly layers
            for _map in _maps:
                with open(f"{_map}.geojson") as json_file:
                    data = json.load(json_file)
                layer = {
                    "sourcetype": "geojson",
                    "source": data,
                    "type": "line",
                    "color": "blue"
                }
                layers.append(layer)
            # getting zoom and center
            with open(f"{_map}.geojson", "r") as file:
                data = file.read()
            lon, lat = u.extract_coordinates(gp.read_file(data))
            zoom = u.zoom_lvl(lon, lat)
            center = u.centroid(lon, lat)
        if gts:
            # creating plotly layers
            for gt in gts:
                data = np.loadtxt(f"assets/groundtruth/{gt}.csv", skiprows=1)[:, 1:3]
                geojson = eu.csv2geojson(data)
                layer = {
                    "sourcetype": "geojson",
                    "source": geojson,
                    "circle": {"radius": 2},
                    "color": "red"
                }
                layers.append(layer)
            # getting zoom and center
            lon, lat = u.from_32632_to_4326(data)
            zoom = u.zoom_lvl(lon, lat)
            center = u.centroid(lon, lat)
        if trajs:
            # creating plotly layers
            for traj in trajs:
                data = np.loadtxt(f"assets/trajectories/{traj}.csv", skiprows=1)[:, 1:3]
                geojson = eu.csv2geojson(data)
                layer = {
                    "sourcetype": "geojson",
                    "source": geojson,
                    "circle": {"radius": 2},
                    "color": "green"
                }
                layers.append(layer)
            # getting zoom and center
            lon, lat = u.from_32632_to_4326(data)
            zoom = u.zoom_lvl(lon, lat)
            center = u.centroid(lon, lat)
        if layers:
            fig = go.Figure(data=[go.Scattermapbox()])
            fig.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                mapbox=go.layout.Mapbox(
                    style="white-bg", 
                    zoom=zoom, 
                    center_lat = center[0],
                    center_lon = center[1],
                    layers=layers
                )
            )
            return fig
        else:
            return go.Figure(data=[go.Scattermapbox()]).update_layout(margin={"r":0,"t":0,"l":0,"b":0},mapbox=go.layout.Mapbox(style="white-bg"))

    # export ============================================================================================================================
    @app.callback(
        ### Outputs ###
        # modal
        Output("eval_exp_done", "is_open"),    # export done status
        Output("eval_exp_warn", "is_open"),    # export warn status
        # download
        Output("eval_export", "data"),         # export data
        # loading
        Output("eval_spin4", "children"),      # loading status
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
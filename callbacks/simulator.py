#### IMPORTS
# dash
from dash import html, Output, Input, State, no_update, callback_context, dcc
import dash_leaflet as dl
import dash_bootstrap_components as dbc
# installed
import geopandas as gp
# built in
from os import listdir
from datetime import datetime
import numpy as np
import shutil as st
from zipfile import ZipFile
# utils
import util as u
# generators/simulators/calculators
from ground_truth_generator import generate_gt, export_gt
from coordinate_simulation import simulate_positions, export_sim



def sim_calls(app, geojson_style):
    # upload maps =======================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("map_warn", "is_open"),   # map upload warn
        Output("map_done", "is_open"),   # map upload done
        # layers
        Output("new_layers", "data"),
        # storage
        Output("z_c_ly", "data"),
        # loading
        Output("spin1", "children"),     # loading status
        ### Inputs ###
        # modal
        State("map_warn", "is_open"),
        State("map_done", "is_open"),
        # maps
        Input("ul_map", "contents"),
        State("ul_map", "filename"),
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
        if "ul_map" in button:
            file_check = [name.split(".")[-1] for name in map_filenames if name.split(".")[-1] not in ["geojson"]] # getting all wrong file formats
            if len(file_check) > 0: return not map_warn, map_done, no_update, no_update, no_update # activating modal -> warn
            for i in range(len(map_filenames)): # only right files were uploaded
                decoded_content = u.upload_encoder(map_contents[i]) # decoding uploaded base64 file
                gp_file = gp.read_file(decoded_content)
                converted = gp.GeoDataFrame(gp_file, crs=gp_file.crs).to_crs(4326) # converting crs from uploaded file to WGS84
                converted.to_file(f"assets/maps/{map_filenames[i]}", driver="GeoJSON") # saving converted layer
            lon, lat = u.exctract_coordinates(gp_file)
            zoom = u.zoom_lvl(lon, lat)               # zoom for latest uploaded map
            center = u.centroid(lon, lat)             # center of latest uploaded map
            # uploaded maps as converted layers
            layers = u.upload2layer(geojson_style)
            return map_warn, not map_done, layers, [zoom, center], no_update # returning uploaded layers
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> no warnings
        else: return map_warn, map_done, no_update, no_update, no_update

    # upload rest =======================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("ul_warn", "is_open"),    # rest upload warn
        Output("ul_done", "is_open"),    # rest upload done
        # loading
        Output("spin2", "children"),     # loading status
        ### Inputs ###
        # modals
        State("ul_warn", "is_open"),
        State("ul_done", "is_open"),
        # waypoints
        Input("ul_way", "contents"),
        State("ul_way", "filename"),
        # antennas
        Input("ul_ant", "contents"),
        State("ul_ant", "filename"),
        # gyroscope
        Input("ul_gyr", "contents"),
        State("ul_gyr", "filename"),
        # acceleration
        Input("ul_acc", "contents"),
        State("ul_acc", "filename"),
        # barometer
        Input("ul_bar", "contents"),
        State("ul_bar", "filename"),
        # magnetometer
        Input("ul_mag", "contents"),
        State("ul_mag", "filename")
    )
    def upload(
        ## modals
        ul_warn,
        ul_done,
        ## upload
        way_contents,  # waypoints
        way_filenames,
        ant_contents,  # antennas
        ant_filenames,
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
        # ========== WAYPOINTS =================================================================================================================
        if "ul_way" in button:
            for i in range(len(way_filenames)):
                if way_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(way_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/waypoints/{way_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========== ANTENNAS ==================================================================================================================
        elif "ul_ant" in button:
            for i in range(len(ant_filenames)):
                if ant_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(ant_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/antennas/{ant_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========== GYROSCOPE =================================================================================================================
        elif "ul_gyr" in button:
            for i in range(len(gyr_filenames)):
                if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(gyr_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/gyr/{gyr_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========= ACCELERATION  ==============================================================================================================
        elif "ul_acc" in button:
            for i in range(len(acc_filenames)):
                if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(acc_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/acc/{acc_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========= BAROMETER  =================================================================================================================
        elif "ul_bar" in button:
            for i in range(len(bar_filenames)):
                if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = u.upload_encoder(bar_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/bar/{bar_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ======== MAGNETOMETER  ===============================================================================================================
        elif "ul_mag" in button:
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

    # hcu canvas ========================================================================================================================
    @app.callback(
        Output("research", "is_open"),
        Input("hcu_maps", "n_clicks"),
        State("research", "is_open")
    )
    def hcu(hcu_maps, is_open):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "hcu_maps" in button:
            return not is_open
        return is_open

    # unlock hcu maps ===================================================================================================================
    @app.callback(
        ### Outputs ###
        # return messages
        Output("password", "valid"),
        Output("password", "invalid"),
        # unlock status
        Output("unlocked", "data"),
        ### Inputs ###
        Input("unlock", "n_clicks"),
        Input("password", "value")
    )
    def unlock(unlock, password):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "unlock" in button:
            if str(password) == "cpsimulation2022":
                return True, False, True
            return False, True, None
        return no_update, no_update, no_update

    # map display =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("layers", "children"),    # layers
        Output("MAP", "center"),         # map center
        Output("MAP", "zoom"),           # map zoom level
        Output("hcu_panel", "style"),    # hcu info panel
        ### Inputs ###
        Input("new_layers", "data"),     # maps
        Input("z_c_ly", "data"),         # zoom and center for latest layer
        Input("z_c_rp_gt", "data"),      # zoom and center for rp and gt
        Input("rp_layer", "data"),       # reference points
        Input("gt_layer", "data"),       # ground truth
        Input("unlocked", "data")        # unlocked status hcu maps
    )
    def display(
        new_layers,
        zoom_center_ly,
        zoom_center_rp_gt,
        rp_layer,
        gt_layer,
        unlocked
        ):
        style = {"display": "None"}
        # presetting map zoom level and center
        zoom = 4
        center = (49.845359730413186, 9.90578149727622) # center of Europe
        # getting all different layers
        layers = []
        if new_layers:
            zoom = zoom_center_ly[0]      # zoom for latest uploaded map
            center = zoom_center_ly[1]    # center of latest uploaded map
            layers += new_layers          # adding newly uploaded layers to map
        if rp_layer:
            zoom = zoom_center_rp_gt[0]   # zoom
            center = zoom_center_rp_gt[1] # center
            layers += rp_layer            # adding ref points layer to map
        if gt_layer:
            zoom = zoom_center_rp_gt[0]   # zoom
            center = zoom_center_rp_gt[1] # center
            layers += gt_layer            # adding gt points layer to map
        if unlocked:
            zoom = 19
            center = (53.540239664876104, 10.004663417352164) # HCU coordinates
            layers += u.floorplan2layer(geojson_style)          # adding hcu floorplans to map
            style = {"display": "block"}                      # displaying info panel
        if layers: return html.Div(dl.LayersControl(layers)), center, zoom, style
        else: return html.Div(style={"display": "None"}), center, zoom, style

    # ground truth canvas ===============================================================================================================
    @app.callback(
        ### Outputs ###
        Output("gt_cv", "is_open"),       # canvas
        Output("ref_select", "options"),  # ref points dropdown
        Output("acc_select", "options"),  # acc data dropdown
        Output("gyr_select", "options"),  # gyr data dropdown
        ### Inputs ###
        State("gt_cv", "is_open"),        # canvas status
        Input("gt_btn", "n_clicks")       # button
    )
    def gt_canvas(
        # canvas status
        gt_cv,
        # button
        gt_clicks
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "gt_btn" in button:
            ref_options = [{"label": name.split(".")[0], "value": name.split(".")[0]} for name in listdir("assets/waypoints")]
            acc_options = [{"label": name.split(".")[0], "value": name.split(".")[0]} for name in listdir("assets/sensors/acc")]
            gyr_options = [{"label": name.split(".")[0], "value": name.split(".")[0]} for name in listdir("assets/sensors/gyr")]
            return not gt_cv, ref_options, acc_options, gyr_options     # activate gt offcanvas and filling dropdowns with data
        else: return gt_cv, [], [], []                                  # offcanvas is closed

    # reference points table ============================================================================================================
    @app.callback(
        ### Outputs ###
        Output("ref_tab", "children"),    # table
        Output("invisible", "children"),  # 100 invisible checkboxes
        Output("ref_data", "data"),       # filename from dropdown
        ### Inputs ###
        Input("ref_select", "value")      # dropdown
    )
    def ref_table(name):
        if name: # file is selected
            # list of rows filled with selecet coordinates
            tr_list = u.ref_tab(name)
            # filling table with rows
            table = dbc.Table(
                html.Tbody(tr_list),
                style={"marginTop": "-7px"},
                size="sm",
                bordered=True,
                color="primary"
            )
            # refreshing the invisible checklist
            checklist = [dbc.Checklist(options=[{"value": 1}], value=[1], id=f"check{i}") for i in range(len(tr_list), 100)]
            return table, checklist, name
        # no file selected
        else:
            table = dbc.Table(
                html.Tbody(),
                style={"marginTop": "-7px"},
                size="sm",
                bordered=True,
                color="primary"
            )
            return table, no_update, name

    # checkboxes ========================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("checked_boxes", "data"),  # filename from dropdown
        ### Inputs ###
        [Input(f"check{i}", "value") for i in range(100)]
    )
    def checkboxes(*check):
        return check

    # ref points and gt generating ======================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("gen_warn", "is_open"),    # gt generator warn
        Output("gen_done", "is_open"),    # gt generator done
        Output("sel_warn", "is_open"),    # show ref points warn
        # store ref points (layer)
        Output("rp_layer", "data"),
        # store layer of generated gt
        Output("gt_layer", "data"),
        # store zoom lvl and center point
        Output("z_c_rp_gt", "data"),
        # loading
        Output("spin3", "children"),      # loading status
        ### Inputs ###
        # modals
        State("gen_warn", "is_open"),
        State("gen_done", "is_open"),
        State("sel_warn", "is_open"),
        # buttons
        Input("gen_btn", "n_clicks"),
        Input("show_btn", "n_clicks"),
        # data from dropdowns
        Input("ref_data", "data"),
        Input("acc_select", "value"),
        Input("gyr_select", "value"),
        # checked waypoints
        Input("checked_boxes", "data")
    )
    def ref_gt_gen(
        ## modals
        gen_warn,
        gen_done,
        sel_warn,
        # gt generator
        gen_btn,
        # ref points
        show_btn,
        ref_data,
        acc_data,
        gyr_data,
        check
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        # ========= GROUND TRUTH =================================================================================================================
        if "gen_btn" in button:
            if ref_data and acc_data and gyr_data:
                # Loading Data
                ref = u.ref_checked(ref_data, check)
                acc = np.loadtxt(f"assets/sensors/acc/{acc_data}.csv")
                gyr = np.loadtxt(f"assets/sensors/gyr/{gyr_data}.csv")
                # generating ground truth data
                gt = generate_gt(ref, acc, gyr)
                if gt is not None: # gt generation went well
                    # formatting and saving groundtruth
                    export_gt(gt)
                    # converting crs and making markers
                    markers = u.gt2marker(gt[:, 1:3])
                    # getting zoom lvl and center point
                    lon, lat = u.from_32632_to_4326(gt[:,1:3])
                    zoom = u.zoom_lvl(lon, lat)     # zoom lvl
                    center = u.centroid(lon, lat)   # center
                    # making ground truth layer
                    layer = [dl.Overlay(dl.LayerGroup(markers), name="GroundTruth", checked=True)]
                    return gen_warn, not gen_done, sel_warn, no_update, layer, [zoom, center], no_update # successful generator
                else: return not gen_warn, gen_done, sel_warn, no_update, [], no_update, no_update      # gt generation went wrong
            else: return gen_warn, gen_done, not sel_warn, no_update, [], no_update, no_update          # no data selected
        # ========= REF POINTS  =================================================================================================================
        elif "show_btn" in button:
            if ref_data:
                # loading data
                data = np.loadtxt(f"assets/waypoints/{ref_data}.csv")[:, 1:3]
                # converting crs and making markers
                markers = u.ref2marker(data, check)
                # getting zoom lvl and center point
                lon, lat = u.from_32632_to_4326(data)
                zoom = u.zoom_lvl(lon, lat)     # zoom lvl
                center = u.centroid(lon, lat)   # center
                # turning ref points into markers
                layer = [dl.Overlay(dl.LayerGroup(markers), name="Waypoints", checked=True)]
                return gen_warn, gen_done, sel_warn, layer, no_update, [zoom, center], no_update    # successful
            else: return gen_warn, gen_done, not sel_warn, [], no_update, no_update, no_update # no data selected
        else: return gen_warn, gen_done, sel_warn, [], [], no_update, no_update                       # offcanvas is closed

    # simulation settings canvas ========================================================================================================
    @app.callback(
        ### Outputs ###
        Output("sim_set_cv", "is_open"),  # canvas
        ### Inputs ###
        State("sim_set_cv", "is_open"),   # canvas status
        Input("sim_set", "n_clicks")      # button
    )
    def sim_set_canvas(
        # canvas status
        sim_set_cv,
        # button
        sim_set_clicks
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "sim_set" in button: return not sim_set_cv     # activate sim_set offcanvas
        else: return sim_set_cv                      # offcanvas is closed
    
    # simulation settings range values ==================================================================================================
    @app.callback(
        ### Outputs ###
        Output("int_rang_min", "children"),     # intervall range
        Output("int_rang_max", "children"),
        Output("sem_err_rang_min", "children"), # semantic error range
        Output("sem_err_rang_max", "children"),
        ### Inputs ###
        Input("int_rang", "value"),
        Input("sem_err_rang", "value")
    )
    def sim_set_sliders(int_rang, sem_err_rang):
        return int_rang[0], int_rang[1], sem_err_rang[0], sem_err_rang[1]
    
    # set and restore simulation settings ===============================================================================================
    @app.callback(
        ### Outputs ###
        Output("int_rang", "value"),
        Output("sem_err_rang", "value"),
        Output("num_int", "value"),
        Output("net_cap", "value"),
        ### Inputs ###
        Input("ss_reset", "n_clicks")
    )
    def restore_sim_set_sliders(ss_reset_clicks):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "ss_reset" in button: return [4000, 6000], [1, 6], 2, 500   # restore default values
        else: return [4000, 6000], [1, 6], 2, 500   # set default values
    
        # ground truth canvas ===============================================================================================================
    
    # open simulate measurement =========================================================================================================
    @app.callback(
        ### Outputs ###
        Output("sim_modal", "is_open"),    # modal
        Output("gt_select", "options"),    # gt data dropdown
        ### Inputs ###
        # modal
        State("sim_modal", "is_open"),
        # button
        Input("open_sim", "n_clicks")
    )
    def gt_canvas(
        # modal status
        sim_modal,
        # button
        open_sim
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "open_sim" in button:
            options = [{"label": name.split(".")[0], "value": name.split(".")[0]} for name in listdir("assets/exports/gt")]
            return not sim_modal, options     # activate gt offcanvas and filling dropdown with data
        else: return sim_modal, []            # offcanvas is closed
    
    # simulate measurement ==============================================================================================================
    @app.callback(
        ### Outputs ###
        Output("sim_warn", "is_open"),   # freq and or err is missing
        Output("sim_done", "is_open"),   # simulation successful
        Output("sim_data", "data"),      # sim measurements data
        # loading (invisible div)
        Output("spin4", "children"),     # loading status
        ### Inputs ###
        # modal
        State("sim_warn", "is_open"),
        State("sim_done", "is_open"),
        # button
        Input("sim_btn", "n_clicks"),
        # data
        Input("gt_select", "value"),      # ground truth data from dropdown
        Input("err", "value"),            # error
        Input("ms_freq", "value"),        # measurement frequency
        Input("net_cap", "value"),        # query frequency
        Input("num_user", "value"),       # number of users
        Input("num_int", "value"),        # number of intervals
        Input("sem_err_rang", "value"),   # error range
        Input("int_rang", "value"),       # intervall range
        Input("sem_err", "value")         # semantic error
    )
    def simulation(
        # canvas status
        sim_warn,
        sim_done,
        # button
        sim_btn,
        # data
        gt_select,
        err,
        ms_freq,
        net_cap,
        num_user,
        num_int,
        sem_err_rang,
        int_rang,
        sem_err
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "sim_btn" in button:
            if gt_select and err and ms_freq and net_cap and num_user and num_int:
                try: # simulate measurement
                    simulation = simulate_positions(gt_select, float(err), float(ms_freq), float(net_cap), int(num_user), int(num_int), sem_err_rang, int_rang, sem_err)
                    # formatting and saving simulation data
                    export_sim(*simulation)
                    return sim_warn, not sim_done, True, no_update
                except: # simulation failed
                    return not sim_warn, sim_done, None, no_update
            else: return not sim_warn, sim_done, None, no_update
        else: return sim_warn, sim_done, None, no_update

    # export ============================================================================================================================
    @app.callback(
        ### Outputs ###
        # modal
        Output("exp_done", "is_open"),    # export done status
        Output("exp_warn", "is_open"),    # export warn status
        # download
        Output("export", "data"),         # export data
        # loading (invisible div)
        Output("spin5", "children"),      # loading status
        ### Inputs ###
        # modal
        State("exp_done", "is_open"),     # done
        State("exp_warn", "is_open"),     # warn
        # leaflet drawings
        Input("edit_control", "geojson"),
        # button
        Input("exp_btn", "n_clicks"),     # export button click status
    )
    def export(
        # modal
        exp_done,
        exp_warn,
        # drawings
        drawings,
        # button
        exp_clicks
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "exp_btn" in button:
            if drawings["features"]: # save drawn data if so
                u.export_drawings(drawings)
            if len(listdir("assets/exports/gt")) or len(listdir("assets/exports/draw")):
                # zipping
                zip_folder = st.make_archive(f"assets/zip/L5IN_export_{datetime.now().strftime('%H_%M_%S')}", 'zip', "assets/exports")
                # sending email with all data added
                u.sending_email()
                # downloading
                download = dcc.send_file(f"assets/zip/{zip_folder[-24:]}", filename=f"L5IN_export_{datetime.now().strftime('%H_%M_%S')}.zip")
                return not exp_done, exp_warn, download, no_update # export successful
            return exp_done, not exp_warn, no_update, no_update # export failed
        else:
            return exp_done, exp_warn, no_update, no_update # no button clicked
    # help canvas =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("help_cv", "is_open"),    # canvas
        ### Inputs ###
        Input("edit_control", "geojson"), # drawn data in geojson format
        State("help_cv", "is_open"),     # canvas status
        Input("help_btn", "n_clicks")    # button
    )
    def help(
        drawn_data,
        # canvas status
        help_cv,
        # button
        help_clicks
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "help_btn" in button:
            if drawn_data["features"]: # drawn data
                u.export_drawn_data(drawn_data)
            return not help_cv     # activate help offcanvas
        else:
            u.deleter() # when page refreshes, emptying all directories
            return help_cv

    # hovering tooltips in hcu floorplans ===============================================================================================
    @app.callback(
        ### Outputs ###
        Output("hover_info", "children"),  # info panel
        ### Inputs ###
        Input("EG", "hover_feature"),      # EG
        Input("1OG", "hover_feature"),     # 1OG
        Input("4OG", "hover_feature"),     # 4OG
    )
    def hovering(
        # geojson info of all three layers
        feature_eg, feature_1og, feature_4og
        ):
        if feature_eg: return u.hover_info(feature_eg)       # if EG is clicked
        elif feature_1og: return u.hover_info(feature_1og)   # if 1OG is clicked
        elif feature_4og: return u.hover_info(feature_4og)   # if 4OGG is clicked
        else: return u.hover_info()                          # if nothing is clicked


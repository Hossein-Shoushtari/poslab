##### Callbacks Simulator
#### IMPORTS
# dash
from dash import html, Output, Input, State, no_update, callback_context, dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
# installed
import geopandas as gp
# built in
from os import listdir
import shutil as st
import numpy as np
import time
# utils (general & simulator)
import simulator.utils as su
import utils as u
# ground truth & simulation
from simulator.simulation import simulate_positions, export_sim
from simulator.ground_truth import generate_gt, export_gt



def sim_calls(app, nc):
    # upload maps =====================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("sim_usr_warn1", "is_open"),  # user missing
        Output("sim_map_warn", "is_open"),   # map upload warn
        # layers
        Output("sim_map_layers", "data"),
        # loading
        Output("sim_spin1", "children"),     # loading status
        ### Inputs ###
        # modal
        State("sim_usr_warn1", "is_open"),
        State("sim_map_warn", "is_open"),
        # maps
        Input("sim_ul_map", "contents"),
        State("sim_ul_map", "filename"),
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
        if "sim_ul_map" in button:
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
        Output("sim_usr_warn2", "is_open"),  # user missing
        Output("sim_ul_warn", "is_open"),    # rest upload warn
        Output("sim_ul_done", "is_open"),    # rest upload done
        # antenna layer
        Output("sim_ant_layers", "data"),
        # loading
        Output("sim_spin2", "children"),     # loading status
        ### Inputs ###
        # modals
        State("sim_usr_warn2", "is_open"),
        State("sim_ul_warn", "is_open"),
        State("sim_ul_done", "is_open"),
        # waypoints
        Input("ul_way", "contents"),
        State("ul_way", "filename"),
        # antennas
        Input("ul_ant", "contents"),
        State("ul_ant", "filename"),
        # gyroscope
        Input("sim_ul_gyr", "contents"),
        State("sim_ul_gyr", "filename"),
        # acceleration
        Input("sim_ul_acc", "contents"),
        State("sim_ul_acc", "filename"),
        # barometer
        Input("sim_ul_bar", "contents"),
        State("sim_ul_bar", "filename"),
        # magnetometer
        Input("sim_ul_mag", "contents"),
        State("sim_ul_mag", "filename"),
        # user
        Input("usr_data", "data")
    )
    def upload(
        ## modals
        usr_warn,
        ul_warn,
        ul_done,
        ## upload
        way_contents,  # waypoints
        way_filenames,
        ant_content,  # antennas
        ant_filename,
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
        # ========== WAYPOINTS =================================================================================================================
        if "ul_way" in button:
            if un:
                for i in range(len(way_filenames)):
                    if way_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(way_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/waypoints/{way_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/waypoints/{way_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update # activating modal -> warn
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update
        # ========== ANTENNAS ==================================================================================================================
        elif "ul_ant" in button:
            if un:
                if ant_filename.split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    ant_decoded = u.upload_encoder(ant_content) # decoding uploaded base64 file
                    with open(f"assets/users/{un}_{pw}/antennas/antennas.csv", "w") as file: file.write(ant_decoded) # saving file
                    u.update_user_data(nc, f"{un}_{pw}/antennas/antennas.csv") # push to cloud
                    # getting zoom lvl and center point
                    lon, lat = u.from_32632_to_4326(np.loadtxt(f"assets/users/{un}_{pw}/antennas/antennas.csv", skiprows=1))
                    bounds = u.boundaries(lon, lat) # boundaries for latest uploaded map
                    layers = {
                        "layers": True,
                        "quantity": 1,
                        "bounds": bounds,
                        "date": time.time()
                    }
                    return usr_warn, ul_warn, ul_done, layers, no_update # if everything went fine ...
                else: return usr_warn, not ul_warn, ul_done, no_update, no_update # activating modal -> warn
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update
        # ========== GYROSCOPE =================================================================================================================
        elif "sim_ul_gyr" in button:
            if un:
                for i in range(len(gyr_filenames)):
                    if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(gyr_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/sensors/gyr/{gyr_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/sensors/gyr/{gyr_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update # activating modal -> warn
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update
        # ========= ACCELERATION  ==============================================================================================================
        elif "sim_ul_acc" in button:
            if un:
                for i in range(len(acc_filenames)):
                    if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(acc_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/sensors/acc/{acc_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/sensors/acc/{acc_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update # activating modal -> warn
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update
        # ========= BAROMETER  =================================================================================================================
        elif "sim_ul_bar" in button:
            if un:
                for i in range(len(bar_filenames)):
                    if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(bar_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/sensors/bar/{bar_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/sensors/bar/{bar_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update # activating modal -> warn
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update, no_update
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update
        # ======== MAGNETOMETER  ===============================================================================================================
        elif "sim_ul_mag" in button:
            if un:
                for i in range(len(mag_filenames)):
                    if mag_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                        decoded_content = u.upload_encoder(mag_contents[i]) # decoding uploaded base64 file
                        with open(f"assets/users/{un}_{pw}/sensors/mag/{mag_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                        u.update_user_data(nc, f"{un}_{pw}/sensors/mag/{mag_filenames[i]}") # push to cloud
                    else: return usr_warn, not ul_warn, ul_done, no_update, no_update # activating modal -> warn
                # if everything went fine ...
                return usr_warn, ul_warn, not ul_done, no_update, no_update  
            else: return not usr_warn, ul_warn, ul_done, no_update, no_update
        # ====== no button clicked =============================================================================================================
        else: return usr_warn, ul_warn, ul_done, no_update, no_update


    # ground truth canvas ===============================================================================================================
    @app.callback(
        ### Outputs ###
        Output("gt_cv", "is_open"),       # canvas
        Output("ref_select", "options"),  # ref points dropdown
        Output("acc_select", "options"),  # acc data dropdown
        Output("gyr_select", "options"),  # gyr data dropdown
        ### Inputs ###
        State("gt_cv", "is_open"),        # canvas status
        Input("gt_btn", "n_clicks"),      # button
        # user
        Input("usr_data", "data")
    )
    def gt_canvas(
        # canvas status
        gt_cv,
        # button
        gt_clicks,
        # user
        user
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        un = user["username"]
        pw = user["password"]
        if "gt_btn" in button:
            if un: # user logged in, activate gt canvas and filling dropdowns with data
                ref_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/waypoints")]
                acc_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/sensors/acc")]
                gyr_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/sensors/gyr")]
                return not gt_cv, ref_options, acc_options, gyr_options
            else: # user isn't logged in
                return not gt_cv, [], [], []
        # canvas is closed
        else: return gt_cv, [], [], []

    # reference points table ============================================================================================================
    @app.callback(
        ### Outputs ###
        Output("ref_tab", "children"),    # table
        Output("invisible", "children"),  # 100 invisible checkboxes
        Output("ref_data", "data"),       # filename from dropdown
        ### Inputs ###
        Input("ref_select", "value"),     # dropdown
        Input("usr_data", "data")
    )
    def ref_table(name, user):
        if name: # file is selected
            # list of rows filled with selecet coordinates
            tr_list = su.ref_tab(user, name)
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
        Output("sel_warn", "is_open"),    # show ref points warn
        # store ref points (layer)
        Output("sim_ref_layers", "data"),
        # store layer of generated gt
        Output("sim_gt_layers", "data"),
        # loading
        Output("sim_spin3", "children"),  # loading status
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
        Input("checked_boxes", "data"),
        # user
        Input("usr_data", "data")
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
        check,
        # user
        user
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        un = user["username"]
        pw = user["password"]
        # ========= GROUND TRUTH =================================================================================================================
        if "gen_btn" in button:
            if ref_data and acc_data and gyr_data:
                # Loading Data
                ref = su.ref_checked(user, ref_data, check)
                acc = np.loadtxt(f"assets/users/{un}_{pw}/sensors/acc/{acc_data}.csv", skiprows=1)
                gyr = np.loadtxt(f"assets/users/{un}_{pw}/sensors/gyr/{gyr_data}.csv", skiprows=1)
                # generating ground truth data
                gt = generate_gt(ref, acc, gyr)
                if gt is not None: # gt generation went well
                    # formatting and saving groundtruth
                    export_gt(nc, user, gt)
                    # getting zoom lvl and center point
                    lon, lat = u.from_32632_to_4326(gt[:,1:3])
                    bounds = u.boundaries(lon, lat) # boundaries for latest uploaded map
                    layers = {
                        "layers": True,
                        "quantity": 1,
                        "bounds": bounds,
                        "date": time.time()
                    }
                    return gen_warn, sel_warn, no_update, layers, no_update           # successful generator
                else: return not gen_warn, sel_warn, no_update, no_update, no_update  # gt generation went wrong
            else: return gen_warn, not sel_warn, no_update, no_update, no_update      # no data selected
        # ========= REF POINTS  =================================================================================================================
        elif "show_btn" in button:
            if ref_data:
                # loading data
                data = np.loadtxt(f"assets/users/{un}_{pw}/waypoints/{ref_data}.csv", skiprows=1)[:, 1:3]
                # getting zoom lvl and center point
                lon, lat = u.from_32632_to_4326(data)
                bounds = u.boundaries(lon, lat) # boundaries for latest uploaded map
                # turning ref points into layer of markers
                layer = {
                    "layers": su.ref2marker(data, check),
                    "quantity": None,
                    "bounds": bounds,
                    "date": time.time()
                }
                return gen_warn, sel_warn, layer, no_update, no_update             # successful
            else: return gen_warn, not sel_warn, no_update, no_update, no_update   # no data selected
        else: return gen_warn, sel_warn, no_update, no_update, no_update           # canvas is closed

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
        if "sim_set" in button: return not sim_set_cv     # activate sim_set canvas
        else: return sim_set_cv                      # canvas is closed
    
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
        if "ss_reset" in button: return [4, 6], [1, 6], 2, 500   # restore default values
        else: return [4, 6], [1, 6], 2, 500   # set default values
    
        # ground truth canvas ===============================================================================================================
    
    # open simulate measurement =========================================================================================================
    @app.callback(
        ### Outputs ###
        Output("sim_modal", "is_open"),     # modal
        Output("sim_gt_select", "options"), # gt data dropdown
        ### Inputs ###
        # modal
        State("sim_modal", "is_open"),
        # button
        Input("open_sim", "n_clicks"),      # button
        # user
        Input("usr_data", "data")
    )
    def open_sim(
        # modal status
        sim_modal,
        # button
        open_sim,
        # user
        user
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        un = user["username"]
        pw = user["password"]
        if "open_sim" in button:
            if un: # user logged in, activate gt canvas and filling dropdown with data
                options = [{"label":name[:-4], "value": name[:-4]} for name in listdir(f"assets/users/{un}_{pw}/groundtruth")]
                return not sim_modal, options
            else: # user isn't logged in, just open canvas
                return not sim_modal, []
        # canvas is closed
        else: return sim_modal, []
    
    # simulate measurement ==============================================================================================================
    @app.callback(
        ### Outputs ###
        Output("sim_warn", "is_open"),     # inputs are missing
        Output("sim_traj_layers", "data"),
        Output("sim_spin4", "children"),   # loading status
        ### Inputs ###
        # modal
        State("sim_warn", "is_open"),
        # button
        Input("sim_btn", "n_clicks"),
        # data
        Input("sim_gt_select", "value"),  # ground truth data from dropdown
        Input("err", "value"),            # error
        Input("ms_freq", "value"),        # measurement frequency
        Input("net_cap", "value"),        # query frequency
        Input("num_user", "value"),       # number of users
        Input("num_int", "value"),        # number of intervals
        Input("sem_err_rang", "value"),   # error range
        Input("int_rang", "value"),       # intervall range
        Input("sem_err", "value"),        # semantic error
        # user
        Input("usr_data", "data")         
    )
    def simulation(
        # canvas status
        sim_warn,
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
        sem_err,
        # user
        user
        ):
        un = user["username"]
        pw = user["password"]
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "sim_btn" in button:
            try:
                simulation = simulate_positions(user, gt_select, float(err), float(ms_freq), float(net_cap), int(num_user), int(num_int), sem_err_rang, int_rang, sem_err)
                # formatting and saving simulation data
                export_sim(user, *simulation, (ms_freq, err, num_user))
                # getting zoom lvl and center point
                lon, lat = u.from_32632_to_4326(np.loadtxt(f"assets/users/{un}_{pw}/trajectories/sim__freq{ms_freq}_err{err}_user{num_user}.csv", skiprows=1)[:,1:3])
                bounds = u.boundaries(lon, lat) # boundaries for latest uploaded map
                # getting number of points -> overflow True or False
                if len(simulation[0]) > 500: overflow = True
                else: overflow = False
                layers = {
                    "layers": True,
                    "quantity": 1,
                    "bounds": bounds,
                    "overflow": overflow,
                    "date": time.time()
                }
                return sim_warn, layers, no_update
            except:
                return not sim_warn, no_update, no_update
        else: return sim_warn, no_update, no_update

    # save drawings =====================================================================================================================
    @app.callback(
        ### Outputs ###
        # modal
        Output("sim_usr_warn3", "is_open"),  # user missing
        Output("sim_save_done", "is_open"),  # save done status
        ### Inputs ###
        # modal
        State("sim_usr_warn3", "is_open"),   # user warn
        State("sim_save_done", "is_open"),   # done
        # leaflet drawings
        Input("edit_control", "geojson"),
        # button
        Input("sim_save", "n_clicks"),       # save button click status
        # user
        Input("usr_data", "data")   
    )
    def save(
        # modal
        usr_warn,
        save_done,
        # drawings
        drawings,
        # button
        save_btn,
        # user
        user
        ):
        un = user["username"]
        pw = user["password"]
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "sim_save" in button:
            if drawings["features"]: # drawn data is there
                if un: # user logged in
                    su.save_drawings(user, drawings)
                    return usr_warn, not save_done # saving successful
                else: # user isn't logged in
                    return not usr_warn, save_done
            else: # nothing to save
                return usr_warn, save_done
        else:
            return usr_warn, save_done # no button clicked

    # example data =====================================================================================================================
    @app.callback(
        ### Outputs ###
        # download
        Output("sim_exdata_dl", "data"), # download data
        ### Inputs ###
        # button
        Input("sim_exdata", "n_clicks"), # export button click status
    )
    def example_data(btn):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "sim_exdata" in button:
            download = dcc.send_file("assets/example_data.zip", filename="example_data.zip")
            return download  # download
        else:
            return no_update # no button clicked

    # export ============================================================================================================================
    @app.callback(
        ### Outputs ###
        # modal
        Output("sim_usr_warn4", "is_open"),   # user missing
        Output("sim_exp_done", "is_open"),    # export done status
        Output("sim_exp_warn", "is_open"),    # export warn status
        # download
        Output("sim_export", "data"),         # export data
        # loading
        Output("sim_spin5", "children"),      # loading status
        ### Inputs ###
        # modal
        State("sim_usr_warn4", "is_open"),    # user warn
        State("sim_exp_done", "is_open"),     # export done
        State("sim_exp_warn", "is_open"),     # export warn
        # button
        Input("sim_exp_btn", "n_clicks"),     # export button click status
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
        if "sim_exp_btn" in button:
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
        Output("sim_help_cv", "is_open"),    # canvas
        ### Inputs ###
        State("sim_help_cv", "is_open"),     # canvas status
        Input("sim_help_btn", "n_clicks")    # button
    )
    def help(
        # canvas status
        sim_help_cv,
        # button
        help_clicks
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "sim_help_btn" in button: return not sim_help_cv     # activate help canvas
        else: return sim_help_cv

    # hovering tooltips in hcu floorplans ===============================================================================================
    @app.callback(
        ### Outputs ###
        Output("sim_hover_info", "children"),  # info panel
        ### Inputs ###
        Input("EG_sim", "hover_feature"),      # EG
        Input("1OG_sim", "hover_feature"),     # 1OG
        Input("4OG_sim", "hover_feature"),     # 4OG
    )
    def hovering(
        # geojson info of all three layers
        feature_eg, feature_1og, feature_4og
        ):
        if feature_eg: return u.hover_info(feature_eg)       # if EG is clicked
        elif feature_1og: return u.hover_info(feature_1og)   # if 1OG is clicked
        elif feature_4og: return u.hover_info(feature_4og)   # if 4OGG is clicked
        else: return u.hover_info()                          # if nothing is clicked

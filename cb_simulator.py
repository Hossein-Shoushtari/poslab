#### IMPORTS
# dash
from dash import html, Output, Input, State, no_update, callback_context
import dash_leaflet as dl
import dash_bootstrap_components as dbc
# installed
from geopandas import GeoDataFrame, read_file
# built in
from os import listdir
from datetime import datetime
# utils
from util import upload_encoder, floorplan2layer
from util import export_drawn_data, hover_info
from util import upload2layer, gt2marker, sending_email
from util import ref_tab, ref_checked, ref2marker
# generators/simulators/calculators
from ground_truth_generator import generate_gt, export_gt
from coordinate_simulation import simulate_positions, export_sim



def simulator_callbacks(app, geojson_style):
    # upload maps =======================================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("map_warn", "is_open"),   # map upload warn
        Output("map_done", "is_open"),   # map upload done
        # layers
        Output("new_layers", "data"),
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
            if len(file_check) > 0: return not map_warn, map_done, [], no_update # activating modal -> warn
            for i in range(len(map_filenames)): # only right files were uploaded
                decoded_content = upload_encoder(map_contents[i]) # decoding uploaded base64 file
                gp_file = read_file(decoded_content)
                converted = GeoDataFrame(gp_file, crs=gp_file.crs).to_crs(4326) # converting crs from uploaded file to WGS84
                converted.to_file(f"assets/maps/{map_filenames[i]}", driver="GeoJSON") # saving converted layer
            # uploaded maps as converted layers
            layers = upload2layer(geojson_style)
            return map_warn, not map_done, layers, no_update # returning uploaded layers
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> no warnings
        else: return map_warn, map_done, [], no_update

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
        gyr_content,  # gyroscope
        gyr_filename,
        acc_content,  # acceleration
        acc_filename,
        bar_content,  # barometer
        bar_filename,
        mag_content,  # magnetometer
        mag_filename
        ): 
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        # UPLOAD
        # ========== WAYPOINTS =================================================================================================================
        if "ul_way" in button:
            for i in range(len(way_filenames)):
                if way_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = upload_encoder(way_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/waypoints/{way_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========== ANTENNAS ==================================================================================================================
        elif "ul_ant" in button:
            for i in range(len(ant_filenames)):
                if ant_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                    decoded_content = upload_encoder(ant_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/antennas/{ant_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========== GYROSCOPE =================================================================================================================
        elif "ul_gyr" in button:
            if gyr_filename.split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(gyr_content) # decoding uploaded base64 file
                with open(f"assets/sensors/gyr.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========= ACCELERATION  ==============================================================================================================
        elif "ul_acc" in button:
            if acc_filename.split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(acc_content) # decoding uploaded base64 file
                with open(f"assets/sensors/acc.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========= BAROMETER  =================================================================================================================
        elif "ul_bar" in button:
            if bar_filename.split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(bar_content) # decoding uploaded base64 file
                with open(f"assets/sensors/bar.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ======== MAGNETOMETER  ===============================================================================================================
        elif "ul_mag" in button:
            if mag_filename.split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(mag_content) # decoding uploaded base64 file
                with open(f"assets/sensors/mag.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update  
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> no warnings
        else: return ul_warn, ul_done, no_update

    # hcu canvas ========================================================================================================================
    @app.callback(
        Output("modal", "is_open"),
        Input("hcu_maps", "n_clicks"),
        State("modal", "is_open")
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
        return False, False, None

    # map display =======================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("layers", "children"),    # layers
        Output("hcu_panel", "style"), # hcu info panel
        ### Inputs ###
        Input("new_layers", "data"),     # maps
        Input("rp_layer", "data"),       # reference points
        Input("gt_layer", "data"),       # ground truth
        Input("unlocked", "data")        # unlocked status hcu maps
    )
    def display(
        new_layers,
        rp_layer,
        gt_layer,
        unlocked
        ):
        layers = []
        style = {"display": "None"}
        if unlocked:
            layers = floorplan2layer(geojson_style)   # adding hcu floorplans to map
            style = {"display": "block"}              # displaying info panel
        if new_layers: layers += new_layers           # adding newly uploaded layers to map
        if rp_layer: layers += rp_layer               # adding ref points layer to map
        if gt_layer: layers += gt_layer               # adding ground truth layer to map

        if layers: return html.Div(dl.LayersControl(layers)), style
        else: return html.Div(style={"display": "None"}), style

    # ground truth canvas ===============================================================================================================
    @app.callback(
        ### Outputs ###
        Output("gt_cv", "is_open"),       # canvas
        Output("ref_select", "options"),  # ref points dropdown
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
            options = [{"label": name.split(".")[0], "value": name.split(".")[0]} for name in listdir("assets/waypoints")]
            return not gt_cv, options     # activate gt offcanvas and filling dropdown with data
        else: return gt_cv, []            # offcanvas is closed

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
            tr_list = ref_tab(name)
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
        else: return no_update, no_update, name

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
        # store generated gt (layer & data)
        Output("gt_layer", "data"),
        Output("gt_data", "data"),
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
        # reference points
        Input("ref_data", "data"),
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
        name,
        check
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        # ========= GROUND TRUTH =================================================================================================================
        if "gen_btn" in button:
            if name:
                ref = ref_checked(name, check)
                gt = generate_gt(ref) # generating ground truth data
                if gt is not None: # gt generation went well
                    # formatting and saving groundtruth
                    export_gt(gt)
                    markers = gt2marker(gt[:, 1:3]) # converting crs and making markers
                    # ground truth layer
                    layer = [dl.Overlay(dl.LayerGroup(markers), name="GroundTruth", checked=True)]
                    return gen_warn, not gen_done, sel_warn, no_update, layer, gt, no_update # successful generator
                else: return not gen_warn, gen_done, sel_warn, no_update, [], [], no_update  # gt generation went wrong
            else: return gen_warn, gen_done, not sel_warn, no_update, [], [], no_update      # no data selected
        # ========= REF POINTS  =================================================================================================================
        elif "show_btn" in button:
            if name:
                markers = ref2marker(name, check) # converting crs and making markers
                # ref points as markers
                layer = [dl.Overlay(dl.LayerGroup(markers), name="Waypoints", checked=True)]
                return gen_warn, gen_done, sel_warn, layer, no_update, no_update, no_update    # successful
            else: return gen_warn, gen_done, not sel_warn, [], no_update, no_update, no_update # no data selected
        else: return gen_warn, gen_done, sel_warn, [], [], [], no_update                       # offcanvas is closed

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
    
    # simulate measuremant ==============================================================================================================
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
        Input("gt_data", "data"),         # gorund truth data
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
        gt,
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
            if gt and err and ms_freq and net_cap and num_user and num_int:
                try: # simulate measurement
                    simulation = simulate_positions(gt, float(err), float(ms_freq), float(net_cap), int(num_user), int(num_int), sem_err_rang, int_rang, sem_err)
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
        # storage
        Output("export_gt", "data"),      # export gt data
        Output("export_sim", "data"),     # export sim data
        # badge
        Output("exp_badge", "children"),  # export sim data
        # loading (invisible div)
        Output("spin5", "children"),      # loading status
        ### Inputs ###
        # modal
        State("exp_done", "is_open"),     # done
        State("exp_warn", "is_open"),     # warn
        # button
        Input("exp_btn", "n_clicks"),     # export button click status
        # data
        Input("gt_data", "data"),         # gorund truth data
        Input("sim_data", "data"),        # sim measurements data
    )
    def export(
        ## modal
        exp_done,
        exp_warn,
        # button
        exp_clicks,
        # data
        gt_data,
        sim_data
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if sim_data and gt_data:
            badge = dbc.Badge(
                "✔️",
                color="success",
                pill=True,
                text_color="white",
                className="position-absolute top-0 start-100 translate-middle"
            )
            if "exp_btn" in button:
                # if data["features"]: # drawn data
                #     export_drawn_data(data)
                # sending email with all data added
                sending_email()
                # downloading it
                with open("assets/exports/ground_truth_trajectory.csv", "r") as f:
                    gt_format = f.read()
                with open("assets/exports/simulated_measurements.csv", "r") as f:
                    sim_format = f.read()
                gt_dl = dict(content = gt_format,  filename=f"ground_truth_trajectory-{datetime.now().strftime('%H:%M:%S')}.csv")
                sim_dl = dict(content = sim_format,  filename=f"simulated_measurements-{datetime.now().strftime('%H:%M:%S')}.csv")
                return not exp_done, exp_warn, gt_dl, sim_dl, badge, no_update # export successful
            return exp_done, exp_warn, no_update, no_update, badge, no_update # export doable
        else:
            if "exp_btn" in button:
                return exp_done, not exp_warn, no_update, no_update, no_update, no_update # export failed
            else:
                badge = dbc.Badge(
                    "🚫",
                    color="danger",
                    pill=True,
                    text_color="white",
                    className="position-absolute top-0 start-100 translate-middle"
                )
                return exp_done, exp_warn, no_update, no_update, badge, no_update # nothing is clicked. nothing happens

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
                export_drawn_data(drawn_data)
            return not help_cv     # activate help offcanvas
        else: help_cv

    # hovering tooltips in layers =======================================================================================================
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
        if feature_eg: return hover_info(feature_eg)       # if EG is clicked
        elif feature_1og: return hover_info(feature_1og)   # if 1OG is clicked
        elif feature_4og: return hover_info(feature_4og)   # if 4OGG is clicked
        else: return hover_info()                          # if nothing is clicked


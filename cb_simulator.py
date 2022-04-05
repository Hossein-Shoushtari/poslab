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
from time import sleep
# utils
from util import upload_encoder, floorplan2layer
from util import export_drawn_data, hover_info
from util import upload2layer, gt2marker
from util import ref_tab, ref_checked, ref2marker
# generators/simulators/calculators
from ground_truth_generator import generate_gt, export_gt
from coordinate_simulation import simulate_positions, export_sim



def simulator_callbacks(app, geojson_style):
    # ============== upload ============================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("ul_warn", "is_open"),    # upload warn
        Output("ul_done", "is_open"),    # upload done
        # loading (invisible div)
        Output("spin1", "children"),     # loading status
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
            for i in range(len(gyr_filenames)):
                if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = upload_encoder(gyr_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/gyr.csv", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========= ACCELERATION  ==============================================================================================================
        elif "ul_acc" in button:
            for i in range(len(acc_filenames)):
                if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = upload_encoder(acc_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/acc.csv", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ========= BAROMETER  =================================================================================================================
        elif "ul_bar" in button:
            for i in range(len(bar_filenames)):
                if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = upload_encoder(bar_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/bar.csv", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update
        # ======== MAGNETOMETER  ===============================================================================================================
        elif "ul_mag" in button:
            for i in range(len(mag_filenames)):
                if mag_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                    decoded_content = upload_encoder(mag_contents[i]) # decoding uploaded base64 file
                    with open(f"assets/sensors/mag.csv", "w") as file: file.write(decoded_content) # saving file
                else: return not ul_warn, ul_done, no_update # activating modal -> warn    
            # if everything went fine ...
            return ul_warn, not ul_done, no_update  
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> no warnings
        else: return ul_warn, ul_done, no_update


    # ============ map display =========================================================================================================
    @app.callback(
        ### Outputs ###
        # modals
        Output("map_warn", "is_open"),    # upload/display warn
        Output("map_done", "is_open"),    # upload/display done
        Output("gen_warn", "is_open"),    # gt generator warn
        Output("gen_done", "is_open"),    # gt generator done
        Output("show_warn", "is_open"),   # show ref points warn
        # layers
        Output("layers", "children"),    # layers
        # loading (invisible div)
        Output("spin2", "children"),     # loading status
        # store generated ground truth
        Output("gt_data", "data"),
        ### Inputs ###
        # modals
        State("map_warn", "is_open"),
        State("map_done", "is_open"),
        State("gen_warn", "is_open"),
        State("gen_done", "is_open"),
        State("show_warn", "is_open"),
        # maps
        Input("ul_map", "contents"),
        State("ul_map", "filename"),
        # ground truth generator
        Input("gen_btn", "n_clicks"),
        # reference points
        Input("show_btn", "n_clicks"),
        Input("ref_data", "data"),
        Input("checked_boxes", "data")
    )
    def display(
        ## modals
        map_warn,
        map_done,
        gen_warn,
        gen_done,
        show_warn,
        ## upload
        map_contents,  # maps
        map_filenames,
        # gt generator
        gen_btn,
        # ref points
        show_btn,
        name,
        check
        ):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        #============= MAP =====================================================================================================================
        if "ul_map" in button:
            file_check = [name.split(".")[-1] for name in map_filenames if name.split(".")[-1] not in ["geojson"]] # getting all wrong file formats
            if len(file_check) > 0: return not map_warn, map_done, gen_warn, gen_done, show_warn, no_update, no_update, no_update # activating modal -> warn
            for i in range(len(map_filenames)): # only right files were uploaded
                decoded_content = upload_encoder(map_contents[i]) # decoding uploaded base64 file
                converted = GeoDataFrame(read_file(decoded_content), crs=32632).to_crs(4326) # converting EPSG:32632 to WGS84 and saving it in floorplans_converted
                converted.to_file(f"assets/maps/{map_filenames[i]}", driver="GeoJSON") # saving converted layer
            # floorplans + uploaded maps
            layers = floorplan2layer(geojson_style) + upload2layer(geojson_style)
            return map_warn, not map_done, gen_warn, gen_done, show_warn, html.Div(dl.LayersControl(layers)), no_update, no_update # returning uploaded layers
        # ========= GT GENERATOR  =================================================================================================================
        elif "gen_btn" in button:
            if name:
                ref = ref_checked(name, check)
                gt = generate_gt(ref) # generating ground truth data
                markers = gt2marker(gt[:, 1:3]) # converting crs and making markers
                # floorplans + uploaded maps + markers
                layers = floorplan2layer(geojson_style) + upload2layer(geojson_style) + [dl.Overlay(dl.LayerGroup(markers), name="GroundTruth", checked=True)]
                return map_warn, map_done, gen_warn, not gen_done, show_warn, html.Div(dl.LayersControl(layers)), no_update, gt # successful generator
            else: return map_warn, map_done, not gen_warn, gen_done, show_warn, no_update, no_update, None # no data selected
        # ========= REF POINTS  =================================================================================================================
        elif "show_btn" in button:
            if name:
                markers = ref2marker(name, check) # converting crs and making markers
                # floorplans + uploaded maps + markers
                layers = floorplan2layer(geojson_style) + upload2layer(geojson_style) + [dl.Overlay(dl.LayerGroup(markers), name="Waypoints", checked=True)]
                return map_warn, map_done, gen_warn, gen_done, show_warn, html.Div(dl.LayersControl(layers)), no_update, no_update # successful
            else: return map_warn, map_done, gen_warn, gen_done, not show_warn, no_update, no_update, no_update # no data selected
        # ====== no button clicked =============================================================================================================
        # this else-section is always activated, when the page refreshes -> load layers
        else:
            layers = floorplan2layer(geojson_style) + upload2layer(geojson_style)
            return map_warn, map_done, gen_warn, gen_done, show_warn, html.Div(dl.LayersControl(layers)), no_update, None


    # ========== ground truth canvas ===================================================================================================
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


    # ======== reference points table ==================================================================================================
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


    # ============== checkboxes ========================================================================================================
    @app.callback(
        ### Outputs ###
        Output("checked_boxes", "data"),  # filename from dropdown
        ### Inputs ###
        [Input(f"check{i}", "value") for i in range(100)]
    )
    def checkboxes(*check):
        return check


    # ========== simulation settings canvas ============================================================================================
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
    
    
    # ========== simulation settings range values =======================================================================================
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
    
    
    # ========== set and restore simulation settings ===================================================================================
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
    
    # ========= simulate measuremant ===================================================================================================
    @app.callback(
        ### Outputs ###
        Output("sim_warn", "is_open"),   # freq and or err is missing
        Output("sim_done", "is_open"),   # simulation successful
        Output("sim_data", "data"),      # sim measurements data
        # loading (invisible div)
        Output("spin3", "children"),     # loading status
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
                    return sim_warn, not sim_done, simulation, no_update
                except: # simulation failed
                    return not sim_warn, sim_done, None, no_update
            else: return not sim_warn, sim_done, None, no_update
        else: return sim_warn, sim_done, None, no_update


    # =============== export ===========================================================================================================
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
        Output("spin4", "children"),      # loading status
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
                # formatting groundtruth
                gt_format = export_gt(gt_data)
                # formatting simulation
                sim_format = export_sim(*sim_data)
                # downloading it
                gt_dl = dict(content = gt_format,  filename=f"ground_truth_trajectory{datetime.now()}.csv")
                sim_dl = dict(content = sim_format,  filename=f"simulated_measurements{datetime.now()}.csv")
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


    # ============= help canvas ========================================================================================================
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


    # ====== hovering tooltips in layers ===============================================================================================
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


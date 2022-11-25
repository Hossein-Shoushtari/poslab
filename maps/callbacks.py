##### Callbacks Map display
#### IMPORTS
# dash
from dash import Output, Input, State, no_update, callback_context
# installed
import geopandas as gp
# built in
import time
# utils (general & simulator)
import simulator.utils as su
import utils as u


def maps_calls(app, geojson_style):
    # open researcher login ==============================================================================================================
    @app.callback(
        Output("research", "is_open"),
        Input("sim_hcu_maps", "n_clicks"),
        Input("eval_hcu_maps", "n_clicks"),
        State("research", "is_open")
    )
    def sim_hcu(sim, eval, is_open):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "sim_hcu_maps" in button or "eval_hcu_maps" in button:
            return not is_open
        return is_open

    # unlock hcu maps ===================================================================================================================
    @app.callback(
        ### Outputs ###
        # return messages
        Output("hcu_pw", "valid"),
        Output("hcu_pw", "invalid"),
        # unlock status
        Output("unlocked", "data"),
        Output("eval_unlocked1", "data"),
        Output("eval_unlocked2", "data"),
        Output("eval_unlocked3", "data"),
        ### Inputs ###
        Input("unlock", "n_clicks"),
        Input("hcu_pw", "value")
    )
    def unlock(unlock, password):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "unlock" in button:
            if str(password) == "cpsimulation2022":
                unlocked = {
                    "unlocked": True,
                    "date": time.time()
                }
                return True, False, unlocked, True, True, True
            else:
                unlocked = {
                    "unlocked": False,
                    "date": 0
                }
                return False, True, unlocked, False, False, False
        return no_update, no_update, no_update, no_update, no_update, no_update

    # map display =======================================================================================================================
    @app.callback(
        ### OUTPUTS ###
        # modal #
        Output("display_done", "is_open"),
        Output("overflow", "is_open"),
        # loading status #
        Output("map_spin", "children"),
        # layers #
        Output("layers", "data"),
        ## simulator ##
        Output("sim_div_lc", "style"),      # div layer control
        Output("sim_lc", "children"),       # layer control        
        Output("sim_map", "bounds"),        # map bounds
        Output("sim_hcu_panel", "style"),   # hcu info panel
        ## evaluator ##
        Output("eval_div_lc", "style"),     # div layer control
        Output("eval_lc", "children"),      # layer control        
        Output("eval_map", "bounds"),       # map bounds
        Output("eval_hcu_panel", "style"),  # hcu info panel
        ### INPUTS ###
        State("display_done", "is_open"),   # modal
        State("overflow", "is_open"),       # modal
        Input("unlocked", "data"),          # unlocked status hcu maps
        Input("layers", "data"),
        ## simulator ##
        Input("sim_map_layers", "data"),    # maps
        Input("sim_ant_layers", "data"),    # antennas
        Input("sim_ref_layers", "data"),    # reference points
        Input("sim_gt_layers", "data"),     # ground truth
        Input("sim_traj_layers", "data"),   # trajectories
        ## evaluator ##
        Input("eval_map_layers", "data"),   # maps
        Input("eval_gt_layers", "data"),    # ground truth
        Input("eval_traj_layers", "data"),  # trajectories
        ## buttons ##
        Input("sim_zoom", "n_clicks"),
        Input("eval_zoom", "n_clicks"),
        ## user ##
        Input("usr_data", "data")
    )
    def display(
        ## modal
        display_done,
        overflow,
        ## HCU
        unlocked,
        ## layers
        layers,
        # simulator
        sim_map_layers,
        sim_ant_layers,
        sim_ref_layers,
        sim_gt_layers,
        sim_traj_layers,
        # evaluator
        eval_map_layers,
        eval_gt_layers,
        eval_traj_layers,
        ## buttons
        sim_zoom_btn,
        eval_zoom_btn,
        user
        ):
        # getting triggered element
        trigger = [p["prop_id"] for p in callback_context.triggered][0]
        if "usr_data" in trigger:
            return no_update
        # ============================================================================================================================================================== #
        ly_style = {"display": "None"}
        bounds=[[35.81781315869664, -47.90039062500001], [60.71619779357716, 67.67578125000001]] # center of Europe as centroid
        # getting bounds from latest change
        dates = [
            sim_map_layers["date"],
            sim_ant_layers["date"],
            sim_ref_layers["date"],
            sim_gt_layers["date"],
            sim_traj_layers["date"],
            eval_map_layers["date"],
            eval_gt_layers["date"],
            eval_traj_layers["date"],
            unlocked["date"]
        ]
        date = dates.index(max(dates))
        if sum(dates):
            if   date == 0: bounds = sim_map_layers["bounds"]
            elif date == 1: bounds = sim_ant_layers["bounds"]
            elif date == 2: bounds = sim_ref_layers["bounds"]
            elif date == 3: bounds = sim_gt_layers["bounds"]
            elif date == 4: bounds = sim_traj_layers["bounds"]
            elif date == 5: bounds = eval_map_layers["bounds"]
            elif date == 6: bounds = eval_gt_layers["bounds"]
            elif date == 7: bounds = eval_traj_layers["bounds"]
            elif date == 8: bounds = [[53.53985942305863, 10.003506584890614], [53.54054129105324, 10.005749166803048]] # HCU boundaries
        # ============================================================================================================================================================== #
        ## regain focus ##
        # focus
        if "sim_zoom" in trigger or "eval_zoom" in trigger:
            return display_done, overflow, no_update, no_update, no_update, no_update, bounds, no_update, no_update, no_update, bounds, no_update
        # ============================================================================================================================================================== #
        # getting all different layers
        sim_layers = []
        eval_layers = []
        sim_layers += (layers)
        eval_layers += (layers)
        # hcu floorplans --------------------------------------------------------------------
        if unlocked["unlocked"] == True: # adding floorplans to map
            hcu_style = {"display": "block"}
            # adding floorplans
            sim_layers += u.floorplan2layer(geojson_style, "sim")
            eval_layers += u.floorplan2layer(geojson_style, "eval")
            ly_style = {"display": "block"}
        if unlocked["unlocked"] == False: # removing floorplans from map
            hcu_style = {"display": "None"}
            ly_style = {"display": "None"}
        # maps ------------------------------------------------------------------------------
        if "sim_map_layers" in trigger:
            maps = u.map2layer(user, sim_map_layers["quantity"], geojson_style)
            layers += maps
            sim_layers += maps
            eval_layers += maps
            ly_style = {"display": "block"}
            return not display_done, overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        elif "eval_map_layers" in trigger:
            maps = u.map2layer(user, eval_map_layers["quantity"], geojson_style)
            layers += maps
            sim_layers += maps
            eval_layers += maps
            ly_style = {"display": "block"}
            return not display_done, overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        # antennas --------------------------------------------------------------------------
        elif "sim_ant_layers" in trigger:
            ants = su.ant2marker(user)
            layers.append(ants)
            sim_layers.append(ants)
            eval_layers.append(ants)
            ly_style = {"display": "block"}
            return not display_done, overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        # waypoints -------------------------------------------------------------------------
        elif "sim_ref_layers" in trigger :
            to_remove = {"status": False, "index": None}
            for i in range(len(layers)):
                if layers[i]["props"]["name"] == "Waypoints":
                    to_remove = {"status": True, "index": i}
            if to_remove["status"] == True:
                layers.pop(to_remove["index"])
                sim_layers.pop(to_remove["index"])
                eval_layers.pop(to_remove["index"])
            refs = sim_ref_layers["layers"]
            layers.append(refs)
            sim_layers.append(refs)
            eval_layers.append(refs)
            ly_style = {"display": "block"}
            return display_done, overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        # ground truth ----------------------------------------------------------------------
        elif "sim_gt_layers" in trigger:
            gts = u.gt2marker(user, sim_gt_layers["quantity"])
            layers += gts
            sim_layers += gts
            eval_layers += gts
            ly_style = {"display": "block"}
            return not display_done, overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        elif "eval_gt_layers" in trigger:
            gts = u.gt2marker(user, eval_gt_layers["quantity"])
            layers += gts
            sim_layers += gts
            eval_layers += gts
            ly_style = {"display": "block"}
            return not display_done, overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        # trajectories ----------------------------------------------------------------------
        elif "sim_traj_layers" in trigger:
            trajs = u.traj2marker(user, sim_traj_layers["quantity"])
            layers += trajs
            sim_layers += trajs
            eval_layers += trajs
            ly_style = {"display": "block"}
            if sim_traj_layers["overflow"] == True: # more than 500 points
                return display_done, not overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
            if sim_traj_layers["overflow"] == False: # less than 500 points
                return not display_done, overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        elif "eval_traj_layers" in trigger:
            trajs = u.traj2marker(user, eval_traj_layers["quantity"])
            layers += trajs
            sim_layers += trajs
            eval_layers += trajs
            ly_style = {"display": "block"}
            if eval_traj_layers["overflow"] == True: # more than 500 points
                return display_done, not overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
            if eval_traj_layers["overflow"] == False: # less than 500 points
                return not display_done, overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        else: return display_done, overflow, no_update, layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
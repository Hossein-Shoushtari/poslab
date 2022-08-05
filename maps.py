##### Callbacks Map display
#### IMPORTS
# dash
from dash import Output, Input, State, no_update, callback_context
# installed
import geopandas as gp
# built in
import time
# utils
import simulator.utils as su
import evaluator.utils as eu
import utils as u


def map_display(app, geojson_style):
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
        Output("password", "valid"),
        Output("password", "invalid"),
        # unlock status
        Output("unlocked", "data"),
        Output("eval_unlocked1", "data"),
        Output("eval_unlocked2", "data"),
        Output("eval_unlocked3", "data"),
        ### Inputs ###
        Input("unlock", "n_clicks"),
        Input("password", "value")
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
        # loading status #
        Output("map_spin", "children"),
        # layers #
        Output("sim_layers", "data"),
        Output("eval_layers", "data"),
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
        Input("unlocked", "data"),          # unlocked status hcu maps
        Input("sim_layers", "data"),
        Input("eval_layers", "data"),
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
        # tab change
        Input("tabs", "value")
    )
    def display(
        ## modal
        display_done,
        ## HCU
        unlocked,
        ## layers
        sim_layers,
        eval_layers,
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
        ## tab change
        tabs
        ):
        # getting triggered element
        trigger = [p["prop_id"] for p in callback_context.triggered][0]
        # ============================================================================================================================================================== #
        ## just a tab change ##
        if "tabs" in trigger:
            return display_done, no_update, no_update, no_update, no_update, sim_layers, no_update, no_update, no_update, eval_layers, no_update, no_update
        # ============================================================================================================================================================== #
        if unlocked["unlocked"]: hcu_style = {"display": "block"}
        else: hcu_style = {"display": "None"}
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
            return display_done, no_update, no_update, no_update, no_update, no_update, bounds, no_update, no_update, no_update, bounds, no_update
        # ============================================================================================================================================================== #
        # getting all different layers
        # maps ------------------------------------------------------------------------------
        if "sim_map_layers" in trigger:
            maps = u.map2layer(sim_map_layers["quantity"], geojson_style)
            sim_layers += maps
            eval_layers += maps
            ly_style = {"display": "block"}
            return not display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        elif "eval_map_layers" in trigger:
            maps = u.map2layer(eval_map_layers["quantity"], geojson_style)
            sim_layers += maps
            eval_layers += maps
            ly_style = {"display": "block"}
            return not display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        # antennas --------------------------------------------------------------------------
        elif "sim_ant_layers" in trigger:
            ants = su.ant2marker()
            sim_layers.append(ants)
            eval_layers.append(ants)
            ly_style = {"display": "block"}
            return not display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        # waypoints -------------------------------------------------------------------------
        elif "sim_ref_layers" in trigger :
            to_remove = {"status": False, "index": None}
            for i in range(len(sim_layers)): # counts for both - sim & eval layers
                if sim_layers[i]["props"]["name"] == "Waypoints":
                    to_remove = {"status": True, "index": i}
            if to_remove["status"] == True:
                sim_layers.pop(to_remove["index"])
                eval_layers.pop(to_remove["index"])
            refs = sim_ref_layers["layers"]
            sim_layers.append(refs)
            eval_layers.append(refs)
            ly_style = {"display": "block"}
            return not display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        # ground truth ----------------------------------------------------------------------
        elif "sim_gt_layers" in trigger:
            gts = u.gt2marker(sim_gt_layers["quantity"])
            sim_layers += gts
            eval_layers += gts
            ly_style = {"display": "block"}
            return not display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        elif "eval_gt_layers" in trigger:
            gts = u.gt2marker(eval_gt_layers["quantity"])
            sim_layers += gts
            eval_layers += gts
            ly_style = {"display": "block"}
            return not display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        # trajectories ----------------------------------------------------------------------
        elif "sim_traj_layers" in trigger:
            trajs = u.traj2marker(sim_traj_layers["quantity"])
            sim_layers += trajs
            eval_layers += trajs
            ly_style = {"display": "block"}
            return not display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        elif "eval_traj_layers" in trigger:
            trajs = u.traj2marker(eval_traj_layers["quantity"])
            sim_layers += trajs
            eval_layers += trajs
            ly_style = {"display": "block"}
            return not display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        # hcu floorplans --------------------------------------------------------------------
        elif "unlocked" in trigger:
            if unlocked["unlocked"] == True: # adding floorplans to map
                # first check whether floor plans already exist
                exist = False
                for i in range(len(sim_layers)): # counts for both - sim & eval layers
                    try:
                        if "assets/floorplans/" in sim_layers[i]["props"]["children"]["props"]["url"]:
                            exist = True
                    except: pass
                if exist == True: # no update
                    return display_done, no_update, no_update, no_update, no_update, no_update, bounds, no_update, no_update, no_update, bounds, no_update
                else: # now, adding floorplans
                    sim_layers += su.floorplan2layer(geojson_style)
                    eval_layers += eu.floorplan2layer(geojson_style)
                    ly_style = {"display": "block"}
                    return display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
            if unlocked["unlocked"] == False: # removing floorplans from map
                to_remove = {"status": False, "indices": []}
                for i in range(len(sim_layers)): # counts for both - sim & eval layers
                    try:
                        if "assets/floorplans/" in sim_layers[i]["props"]["children"]["props"]["url"]:
                            to_remove["status"] = True
                            to_remove["indices"].append(i)
                    except: pass
                if to_remove["status"] == True:
                    sim_layers = eval_layers = [layer for i, layer in enumerate(sim_layers) if i not in to_remove["indices"]]
                return display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        else: return display_done, no_update, sim_layers, eval_layers, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
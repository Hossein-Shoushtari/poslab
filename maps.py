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
        Output("sim_unlocked", "data"),
        Output("eval_unlocked1", "data"),
        Output("eval_unlocked2", "data"),
        Output("eval_unlocked3", "data"),
        Output("eval_unlocked4", "data"),
        Output("eval_unlocked5", "data"),
        ### Inputs ###
        Input("unlock", "n_clicks"),
        Input("password", "value")
    )
    def unlock(unlock, password):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        if "unlock" in button:
            if str(password) == "cpsimulation2022":
                return True, False, True, True, True, True, time.time(), True
            return False, True, None, None, None, None, no_update, None
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    # map display =======================================================================================================================
    @app.callback(
        ### OUTPUTS ###
        # modal #
        Output("display_done", "is_open"),
        # loading status #
        Output("map_spin", "children"),
        # tab change #
        Output("tabs_status", "data"),
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
        State("display_done", "is_open"),
        ## simulator ##
        Input("sim_map_layers", "data"),    # maps
        Input("sim_ant_layers", "data"),    # antennas
        Input("sim_ref_layers", "data"),    # reference points
        Input("sim_gt_layers", "data"),     # ground truth
        Input("sim_traj_layers", "data"),   # trajectories
        Input("sim_unlocked", "data"),      # unlocked status hcu maps
        ## evaluator ##
        Input("eval_map_layers", "data"),   # maps
        Input("eval_gt_layers", "data"),    # ground truth
        Input("eval_traj_layers", "data"),  # trajectories
        Input("eval_unlocked5", "data"),    # unlocked status hcu maps
        ## buttons ##
        Input("sim_zoom", "n_clicks"),
        Input("eval_zoom", "n_clicks"),
        # only unlock hcu
        Input("eval_unlocked4", "data"),
        # tab change
        Input("tabs", "value"),
        Input("tabs_status", "data")

    )
    def display(
        ## modal
        display_done,
        ## layers
        # simulator
        sim_map_layers,
        sim_ant_layers,
        sim_ref_layers,
        sim_gt_layers,
        sim_traj_layers,
        sim_unlocked,
        # evaluator
        eval_map_layers,
        eval_gt_layers,
        eval_traj_layers,
        eval_unlocked,
        ## buttons
        sim_zoom_btn,
        eval_zoom_btn,
        # unlock
        unlocked,
        ## tab change
        tab_now,
        tab_before
        ):
        # ============================================================================================================================================================== #
        ## just a tab change ##
        if tab_now != tab_before:
            return display_done, no_update, tab_now, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        # ============================================================================================================================================================== #
        hcu_style = {"display": "None"}
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
            eval_traj_layers["date"]
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
        # ============================================================================================================================================================== #
        ## regain focus ##
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        # focus
        if "sim_zoom" in button or "eval_zoom" in button:
            if sim_unlocked or eval_unlocked: # if hcu floorplans are unlocked
                bounds = [[53.53985942305863, 10.003506584890614], [53.54054129105324, 10.005749166803048]] # HCU boundaries
            return display_done, no_update, no_update, no_update, no_update, bounds, no_update, no_update, no_update, bounds, no_update
        # ============================================================================================================================================================== #
        if time.time() - unlocked > 5: onlyHCU = False
        else: onlyHCU = True
        # getting all different layers
        sim_layers = []
        eval_layers = []
                        # maps
        if sim_map_layers["layers"] or eval_map_layers["layers"]:
            maps = u.map2layer(geojson_style)
            sim_layers += maps
            eval_layers += maps
            ly_style = {"display": "block"}
                      # antennas
        if sim_ant_layers["layers"]:
            ants = su.ant2marker()
            sim_layers.append(ants)
            eval_layers.append(ants)
            ly_style = {"display": "block"}
                    # ground truth
        if sim_gt_layers["layers"] or eval_gt_layers["layers"]:
            gts = u.gt2marker()
            sim_layers += gts
            eval_layers += gts
            ly_style = {"display": "block"}
                    # trajectories
        if sim_traj_layers["layers"] or eval_traj_layers["layers"]:
            trajs = u.traj2marker()
            sim_layers += trajs
            eval_layers += trajs
            ly_style = {"display": "block"}
                      # waypoints
        if sim_ref_layers["layers"]:
            refs = sim_ref_layers["layers"]
            sim_layers.append(refs)
            eval_layers.append(refs)
            ly_style = {"display": "block"}
                   # hcu floorplans
        if sim_unlocked or eval_unlocked:
            bounds = [[53.53985942305863, 10.003506584890614], [53.54054129105324, 10.005749166803048]] # HCU boundaries
            sim_layers += su.floorplan2layer(geojson_style)
            eval_layers += eu.floorplan2layer(geojson_style)
            hcu_style = {"display": "block"}
            ly_style = {"display": "block"}

        if onlyHCU: return display_done, no_update, no_update, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        elif sim_layers: return not display_done, no_update, no_update, ly_style, sim_layers, bounds, hcu_style, ly_style, eval_layers, bounds, hcu_style
        else: return display_done, no_update, no_update, ly_style, [], bounds, hcu_style, ly_style, [], bounds, hcu_style
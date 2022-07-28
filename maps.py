##### Callbacks Map display
#### IMPORTS
# dash
from dash import Output, Input, State, no_update, callback_context
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
        # modal #
        Output("display_done", "is_open"),
        # loading status #
        Output("map_spin", "children"),
        ### OUTPUTS ###
        ## simulator ##
        Output("sim_div_lc", "style"),      # div layer control
        Output("sim_lc", "children"),       # layer control        
        Output("sim_map", "center"),        # map center
        Output("sim_map", "zoom"),          # map zoom level
        Output("sim_hcu_panel", "style"),   # hcu info panel
        ## evaluator ##
        Output("eval_div_lc", "style"),     # div layer control
        Output("eval_lc", "children"),      # layer control        
        Output("eval_map", "center"),       # map center
        Output("eval_map", "zoom"),         # map zoom level
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
        # only unlock hcu,
        Input("eval_unlocked4", "data")
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
        sim_zoom,
        eval_zoom,
        # unlock
        unlocked
        ):
        # presetting styles / zoom / center
        hcu_style = {"display": "None"}
        ly_style = {"display": "None"}
        zoom = 4
        center = (49.845359730413186, 9.90578149727622) # center of Europe
        # getting zoom and center from latest change
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
            if date == 0: zoom, center = sim_map_layers["zoom"], sim_map_layers["center"]
            elif date == 1: zoom, center = sim_ant_layers["zoom"], sim_ant_layers["center"]
            elif date == 2: zoom, center = sim_ref_layers["zoom"], sim_ref_layers["center"]
            elif date == 3: zoom, center = sim_gt_layers["zoom"], sim_gt_layers["center"]
            elif date == 4: zoom, center = sim_traj_layers["zoom"], sim_traj_layers["center"]
            elif date == 5: zoom, center = eval_map_layers["zoom"], eval_map_layers["center"]
            elif date == 6: zoom, center = eval_gt_layers["zoom"], eval_gt_layers["center"]
            elif date == 7: zoom, center = eval_traj_layers["zoom"], eval_traj_layers["center"]
        # ============================================================================================================================================================== #
        ## regain focus ##
        # getting clicked button
        button = [p["prop_id"] for p in callback_context.triggered][0]
        # focus
        if "sim_zoom" in button or "eval_zoom" in button:
            if sim_unlocked or eval_unlocked: # if hcu floorplans are unlocked
                zoom = 19
                center = (53.540239664876104, 10.004663417352164)
            return display_done, no_update, no_update, no_update, center, zoom, no_update, no_update, no_update, center, zoom, no_update
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
            zoom = 19
            center = (53.540239664876104, 10.004663417352164) # HCU coordinates
            sim_layers += su.floorplan2layer(geojson_style)
            eval_layers += eu.floorplan2layer(geojson_style)
            hcu_style = {"display": "block"}
            ly_style = {"display": "block"}
        if onlyHCU: return display_done, no_update, ly_style, sim_layers, center, zoom, hcu_style, ly_style, eval_layers, center, zoom, hcu_style
        elif sim_layers: return not display_done, no_update, ly_style, sim_layers, center, zoom, hcu_style, ly_style, eval_layers, center, zoom, hcu_style
        else: return display_done, no_update, ly_style, [], center, zoom, hcu_style, ly_style, [], center, zoom, hcu_style
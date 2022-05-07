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
# utils (general & simulator)
import utils as u
import simulator.utils as su
# simulation & ground truth
from simulator.ground_truth import generate_gt, export_gt
from simulator.simulation import simulate_positions, export_sim



def eval_calls(app, geojson_style):
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
        else:
            u.deleter() # when page refreshes, emptying all directories
            return eval_help_cv


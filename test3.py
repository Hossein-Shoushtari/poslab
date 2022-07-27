#### IMPORTS
# dash
from dash_extensions.javascript import assign
from dash import Dash, dcc, html, Output, Input, State, no_update, callback_context
from dash_extensions.javascript import assign
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gp
import pandas as pd
import numpy as np
import json
import shapely.geometry as sh
import json
from os import listdir
import utils as u
import random
##### Evaluator Tab -- Layout
###IMPORTS
# dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import html, dcc
import dash_leaflet as dl
# utils (general & evaluator)
import evaluator.utils as eu
import utils as u

# Geojson rendering logic, must be JavaScript and only initialized once!
geojson_style = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    return style;}"""
)

# ---------------- HTML ---------------- #
# designing the webpage using dash
ex_ss = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=ex_ss)
server = app.server
# title
app.title = "Test"
_map = html.Div(dbc.Button(html.Img(src="assets/images/settings_sign1.svg"), id="sim_set", color="light", outline=True, style={"border": "0px"}))

# putting all together
app.layout = html.Div(
    [  
        _map
    ]
)

# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)
#### IMPORTS
# dash
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

def csv2geojson(coordinates: list) -> str:
    # making points out of ground truth data for converting it (crs:32632 to crs:4326)
    points = {"GroundTruth": [i for i in range(1, coordinates.shape[0]+1)], "geometry": [sh.Point(lat, lon) for lat, lon in coordinates]}
    converted_points = gp.GeoDataFrame(points, crs=32632).to_crs(4326)
    # adding all coordinates to geojson
    features = []
    for nr, row in converted_points.iterrows():
        f = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row[1].x, row[1].y]
            }
        }
        features.append(f)
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson

# ---------------- HTML ---------------- #
# designing the webpage using dash
ex_ss = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=ex_ss)
server = app.server
# title
app.title = "Test" 
map_bgs = ["basic", "carto-darkmatter", "carto-positron", "dark", "light", "outdoors", "satellite", "satellite-streets", "stamen-terrain", "stamen-toner", "stamen-watercolor", "streets", "white-bg"]
div = html.Div([
    html.Button("VISUAL", id="open_visual"),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("VISUAL")),
            dbc.ModalBody([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Maps", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_map_select",
                                options=[],
                                placeholder="Select Data",
                                clearable=True,
                                optionHeight=35,
                                multi=True,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Ground Truth", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_gt_select",
                                options=[],
                                placeholder="Select Data",
                                clearable=True,
                                optionHeight=35,
                                multi=True,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Trajectories", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_traj_select",
                                options=[],
                                placeholder="Select Data",
                                clearable=True,
                                optionHeight=35,
                                multi=True,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Background", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_bg_select",
                                options=[{"label": bg, "value": bg} for bg in map_bgs],
                                value="carto-darkmatter",
                                placeholder="Select Background",
                                clearable=True,
                                optionHeight=35,
                                multi=False,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ])
                    ])],
                    style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}
                ),
                dcc.Graph(
                    figure=go.Figure(data=[go.Scattermapbox()]).update_layout(margin={"r":0,"t":0,"l":0,"b":0},mapbox=go.layout.Mapbox(style="white-bg")),
                    config={
                        "staticPlot": False,        # True, False
                        "scrollZoom": True,         # True, False
                        "showTips": True,           # True, False
                        "displayModeBar": "hover",  # True, False, "hover"
                        "watermark": True,
                        "editable": True,
                        "toImageButtonOptions": {
                            "format": "png",        # one of png, svg, jpeg, webp
                            "filename": "my_plot",
                            "height": 700,
                            "width": 1200,
                            "scale": 1              # multiply title/legend/axis/canvas sizes by this factor
                        },
                        "modeBarButtonsToAdd": [
                            "drawline",
                            "drawopenpath",
                            "drawclosedpath",
                            "drawcircle",
                            "drawrect",
                            "eraseshape"
                        ]
                    },
                    id="vis_map",
                    className="six columns",
                    style={"height": "600px"})
            ])
        ],
        id="visual_show",
        size="xl",
        backdrop="static",
        is_open=False
    )
])

# putting all together
app.layout = html.Div(
    [  
        div
    ]
)

@app.callback(
    ### Outputs ###
    Output("visual_show", "is_open"),
    Output("vis_map_select", "options"),
    Output("vis_gt_select", "options"),
    Output("vis_traj_select", "options"),
    ### Inputs ###
    # modal
    State("visual_show", "is_open"),
    # button
    Input("open_visual", "n_clicks"),
    )
def open_cdf(
    # modal
    visual_show,
    # button
    open_visual
    ):
    button = [p["prop_id"] for p in callback_context.triggered][0]
    if "open_visual" in button:
        map_options = [{"label": name[:-8], "value": name[:-8]} for name in listdir("assets/maps")]
        gt_options   = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/groundtruth")]
        traj_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/trajectories")]
        return not visual_show, map_options, gt_options, traj_options
    else: return visual_show, [], [], []


@app.callback(
    ### Outputs ###
    Output("vis_map", "figure"),
    ### Inputs ###
    Input("vis_map_select", "value"),
    Input("vis_gt_select", "value"),
    Input("vis_traj_select", "value"),
    Input("vis_bg_select", "value")
)
def update_fig(_maps, gts, trajs, bg):
    fig = go.Figure(go.Scattermapbox())
    layers = []
    zoom = 1
    center = (0, 0)
    if not bg: bg = "white-bg"
    if _maps:
        # creating plotly layers
        for _map in _maps:
            r, g, b = random.randint(0,255), random.randint(0,255), random.randint(0,255)
            with open(f"assets/maps/{_map}.geojson") as json_file:
                data = json.load(json_file)
            layer = {
                "sourcetype": "geojson",
                "source": data,
                "type": "line",
                "color": f"rgb({r}, {g}, {b})"
            }
            layers.append(layer)
        # getting zoom and center
        with open(f"assets/maps/{_map}.geojson", "r") as file:
            data = file.read()
        lon, lat = u.extract_coordinates(gp.read_file(data))
        zoom = u.zoom_lvl(lon, lat)
        center = u.centroid(lon, lat)
    if gts:
        # creating plotly layers
        for gt in gts:
            data = np.loadtxt(f"assets/groundtruth/{gt}.csv", skiprows=1)[:, 1:3]
            lon, lat = u.from_32632_to_4326(data)
            fig.add_trace(go.Scattermapbox(
                mode="markers",
                lon=lon,
                lat=lat,
                marker={"size": 4},
                name=gt))
        # getting zoom and center
        zoom = u.zoom_lvl(lon, lat)
        center = u.centroid(lon, lat)
    if trajs:
        # creating plotly layers
        for traj in trajs:
            data = np.loadtxt(f"assets/trajectories/{traj}.csv", skiprows=1)[:, 1:3]
            lon, lat = u.from_32632_to_4326(data)
            fig.add_trace(go.Scattermapbox(
                mode="markers",
                lon=lon,
                lat=lat,
                marker={"size": 4},
                name=traj))
        # getting zoom and center
        zoom = u.zoom_lvl(lon, lat)
        center = u.centroid(lon, lat)
    # completing figure with a nice layout
    fig.update_layout(
        margin={"l":0,"t":0,"b":0,"r":0},
        mapbox={
            # token got from https://mapbox.com/
            # default public token: pk.eyJ1Ijoibml2cm9rMjAwMSIsImEiOiJjbDV0a3A3eGIweWJvM2JuMHhtYXF5aWVlIn0._01sVxeqJ8EQvGq2PclBBw
            "accesstoken": "pk.eyJ1Ijoibml2cm9rMjAwMSIsImEiOiJjbDV0a3Mwa2gwbXAzM2RteDk0dnoyNnlsIn0.MwHtkUS1sevt4F8PqhbGZQ", # heroku token
            "center": {"lon": center[1], "lat": center[0]},
            "style": bg,
            "zoom": zoom,
            "layers": layers
        },
        legend={
            "yanchor": "top",
            "y": 0.99,
            "xanchor": "left",
            "x": 0.01
        },
        showlegend=True
    )
    return fig

# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)
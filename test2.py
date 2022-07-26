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
                        ]),
                        dbc.Col([
                            dbc.Label("Plot Format [800x2000]", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_format_select",
                                options=[{"label": f, "value": f} for f in ["png", "svg", "jpeg", "webp"]],
                                value="png",
                                placeholder="Select Format",
                                clearable=True,
                                optionHeight=35,
                                multi=False,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Waypoints", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_ref_select",
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
                            dbc.Label("Antennas", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_ant_select",
                                options=[],
                                placeholder="Select Data",
                                clearable=True,
                                optionHeight=35,
                                multi=False,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
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
                        ])
                    ])],
                    style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}
                ),
                dcc.Graph(
                    id="vis_map",
                    className="six columns",
                    style={"height": "80vh"})
            ])
        ],
        id="visual_show",
        fullscreen=True,
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
    Output("vis_ref_select", "options"),
    Output("vis_gt_select", "options"),
    Output("vis_traj_select", "options"),
    Output("vis_ant_select", "options"),
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
        map_options  = [{"label": name[:-8], "value": name[:-8]} for name in listdir("assets/maps")]
        ref_options  = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/waypoints")]
        gt_options   = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/groundtruth")]
        traj_options = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/trajectories")]
        ant_options  = [{"label": name[:-4], "value": name[:-4]} for name in listdir("assets/antennas")]
        return not visual_show, map_options, ref_options, gt_options, traj_options, ant_options
    else: return visual_show, [], [], [], [], []


@app.callback(
    ### Outputs ###
    Output("vis_map", "figure"),
    Output("vis_map", "config"),
    ### Inputs ###
    Input("vis_map_select", "value"),
    Input("vis_ref_select", "value"),
    Input("vis_gt_select", "value"),
    Input("vis_traj_select", "value"),
    Input("vis_ant_select", "value"),
    Input("vis_bg_select", "value"),
    Input("vis_format_select", "value"),
)
def update_fig(_maps, refs, gts, trajs, ant, bg, _format):
    fig = go.Figure(go.Scattermapbox())
    layers = []
    zoom = 1
    center = (0, 0)
    if not bg: bg = "white-bg"
    if not _format: _format = "png"
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
                "color": "blue"
            }
            layers.append(layer)
        # getting zoom and center
        with open(f"assets/maps/{_map}.geojson", "r") as file:
            data = file.read()
        lon, lat = u.extract_coordinates(gp.read_file(data))
        zoom = u.zoom_lvl(lon, lat)
        center = u.centroid(lon, lat)
    if refs:
        # creating plotly layers
        for ref in refs:
            data = np.loadtxt(f"assets/waypoints/{ref}.csv", skiprows=1)[:, 1:3]
            lon, lat = u.from_32632_to_4326(data)
            fig.add_trace(go.Scattermapbox(
                mode="markers",
                lon=lon,
                lat=lat,
                marker={"size": 12},
                legendgrouptitle={"text": "Waypoints"},
                legendgroup="Waypoints",
                name=ref))
        # getting zoom and center
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
                marker={"size": 6},
                legendgrouptitle={"text": "Ground Truth"},
                legendgroup="Ground Truth",
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
                marker={"size": 6},
                legendgrouptitle={"text": "Trajectories"},
                legendgroup="Trajectories",
                name=traj))
        # getting zoom and center
        zoom = u.zoom_lvl(lon, lat)
        center = u.centroid(lon, lat)
    if ant:
        # creating plotly layers
        data = np.loadtxt(f"assets/antennas/{ant}.csv", skiprows=1)
        lon, lat = u.from_32632_to_4326(data)
        fig.add_trace(go.Scattermapbox(
            mode="markers",
            lon=lon,
            lat=lat,
            marker={"size": 14},
            legendgrouptitle={"text": "Antennas"},
            legendgroup="Antennas",
            name=ant))
        # getting zoom and center
        zoom = u.zoom_lvl(lon, lat)
        center = u.centroid(lon, lat)
    # completing figure with a nice layout
    fig.update_layout(
        margin={"l":0,"t":0,"b":0,"r":0},
        mapbox={
            # token got from https://mapbox.com/
            # default public token: pk.eyJ1Ijoibml2cm9rMjAwMSIsImEiOiJjbDV0a3Mwa2gwbXAzM2RteDk0dnoyNnlsIn0.MwHtkUS1sevt4F8PqhbGZQ
            "accesstoken": "pk.eyJ1Ijoibml2cm9rMjAwMSIsImEiOiJjbDV0a3A3eGIweWJvM2JuMHhtYXF5aWVlIn0._01sVxeqJ8EQvGq2PclBBw", # heroku token
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
    # refreshing configurations
    config={
        "staticPlot": False,        # True, False
        "scrollZoom": True,         # True, False
        "showTips": True,           # True, False
        "displayModeBar": "hover",  # True, False, "hover"
        "watermark": True,
        "editable": True,
        "toImageButtonOptions": {
            "format": _format,      # one of png, svg, jpeg, webp
            "filename": "my_plot",
            "height": 800,
            "width": 2000,
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
    }
    return fig, config

# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)
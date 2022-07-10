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
                        ])
                    ])],
                    style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}
                ),
                dcc.Graph(
                    figure=go.Figure(data=[go.Scattermapbox()]).update_layout(margin={"r":0,"t":0,"l":0,"b":0},mapbox=go.layout.Mapbox(style="white-bg")),
                    config={
                        "staticPlot": False,     # True, False
                        "scrollZoom": True,      # True, False
                        "doubleClick": "reset",  # "reset", "autosize" or "reset+autosize", False
                        "showTips": True,        # True, False
                        "displayModeBar": True,  # True, False, "hover"
                        "watermark": True
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
    Input("vis_traj_select", "value")
)
def update_fig(_maps, gts, trajs):
    layers = []
    if _maps:
        # creating plotly layers
        for _map in _maps:
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
    if gts:
        # creating plotly layers
        for gt in gts:
            data = np.loadtxt(f"assets/groundtruth/{gt}.csv", skiprows=1)[:, 1:3]
            geojson = csv2geojson(data)
            layer = {
                "sourcetype": "geojson",
                "source": geojson,
                "circle": {"radius": 2},
                "color": "red"
            }
            layers.append(layer)
        # getting zoom and center
        lon, lat = u.from_32632_to_4326(data)
        zoom = u.zoom_lvl(lon, lat)
        center = u.centroid(lon, lat)
    if trajs:
        # creating plotly layers
        for traj in trajs:
            data = np.loadtxt(f"assets/trajectories/{traj}.csv", skiprows=1)[:, 1:3]
            geojson = csv2geojson(data)
            layer = {
                "sourcetype": "geojson",
                "source": geojson,
                "circle": {"radius": 2},
                "color": "green"
            }
            layers.append(layer)
        # getting zoom and center
        lon, lat = u.from_32632_to_4326(data)
        zoom = u.zoom_lvl(lon, lat)
        center = u.centroid(lon, lat)
    if layers:
        fig = go.Figure(data=[go.Scattermapbox()])
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            mapbox=go.layout.Mapbox(
                style="white-bg", 
                zoom=zoom, 
                center_lat = center[0],
                center_lon = center[1],
                layers=layers
            )
        )
        return fig
    else:
        return no_update

# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)
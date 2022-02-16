##### Utils
###IMPORTS
# dash
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function
# built in
from datetime import datetime
from base64 import b64decode
from os import listdir
# installed
from geopandas import GeoDataFrame, read_file
from shapely.geometry import Point

def geojson_converter(filename: str, decoded_content: str) -> None:
    """
    FUNCTION
    - converts geojson from crs:32632 to crs:4326
    - saves converted file
    -------
    PARAMETERS
    filename : filename of file
    decoded_content : decoded content of file
    -------
    RETURN
    None
    """
    # converting crs (UTM -> EPSG: 32632) of given floorplan to WGS84 (EPSG: 4326)
    layer = GeoDataFrame(read_file(decoded_content), crs=32632).to_crs(4326)
    # saving converted layer
    layer.to_file(f"assets/floorplans/{filename}", driver="GeoJSON")

def upload_encoder(content: str) -> str:
    """
    FUNCTION
    - encodes uploaded base64 file to originally uploaded file
    -------
    PARAMETER
    content : decoded content
    -------
    RETURN
    encoded content
    """
    # decoding base64 to geojson
    encoded_content = content.split(",")[1]
    decoded_content = b64decode(encoded_content).decode("latin-1")  # should be a geojson like string

    return decoded_content

def export_data(data: dict) -> None:
    """
    FUNCTION
    - formats received dictionary (replaces ' with ")
    - saves formatted file as geojson file (>assets/export<)
    -------
    PARAMETER
    data : data to export/save
    -------
    RETURN
    None
    """
    # original export data must be formatted to proper geojson like string
    old = "'"
    new = """ " """
    # getting the current date and time for unique filename
    name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    # storing data as geojson file
    with open(f"assets/export/exportdata_{name}.geojson", "w") as file:
        # formatting data-string
        data_str = str(data).replace(old, new[1])
        # ...saving
        file.write(data_str)

def hover_info(feature=None) -> 'html.Div':
    """
    FUNCTION
    - builds info panel (right corner on map)
    - fills table with geojson properties when hovering
    -------
    PARAMETER
    feature : default None (no hover)
              MultiPolygon (while hover)
    -------
    RETURN
    info panel : html.Div
    """
    # creating header (always on)
    header = [html.H4("Space Information", style={"textAlign": "center"}), html.Hr(style={"width": "60%", "margin": "auto", "marginBottom": "10px"})]
    # while no hover...
    if not feature:
        return header + [html.P("Choose a layer. Hover over a segment.", style={"textAlign": "center"})]
    # when hover...
    # creating table for properties
    table_header = [html.Thead(html.Tr([html.Th("Properties", style={"width": "80px", "color": "white"}), html.Th("Value", style={"color": "white"})]))]
    table_body_content = []
    # filling table_body with content
    for prop in feature["properties"]:
        table_body_content.append(html.Tr(
            [
                html.Td(
                    prop,
                    style={
                        "font-size": "15px",
                        "width": "80px",
                        "color": "white"
                    }
                ),
                html.Td(
                    feature["properties"][prop],
                    style={
                        "font-size": "15px",
                        "color": "white"
                    }
                )
            ]
        ))
    table_body = [html.Tbody(table_body_content[:-1])]
    # completing table
    table = dbc.Table(
        table_header + table_body,
        style={"marginBottom": "-3px"},
        size="sm",
        bordered=True,
        striped=True,
        dark=True
    )

    return html.Div([html.Div(header), table])

def floorplan2layer(geojson_style) -> list:
    """
    FUNCTION
    - makes layers out of flooplans (gejson)
    -------
    PARAMETER
    geojson_style : geojson rendering logic in java script (assign)
    -------
    RETURN
    layers : list of layered floorplans
    """
    # initializing list to fill it with default layers
    layers = []
    # list of all default floorplan names
    floorplans = ["EG", "1OG", "4OG"]
    for fp in floorplans:
        geojson = dl.GeoJSON(
            url=f"assets/floorplans/{fp}.geojson",  # url to geojson file
            options=dict(style=geojson_style),  # style each polygon
            hoverStyle=arrow_function(dict(weight=1, color="orange")),  # style applied on hover
            hideout=dict(style={"weight": 0.2, "color": "blue"}, classes=[], colorscale=[], colorProp=""),
            id=fp)
        layers.append(dl.Overlay(geojson, name=fp, checked=False))

    return layers

def upload2layer(geojson_style) -> list:
    """
    FUNCTION
    - makes layers out of newly uploaded geojson files
    -------
    PARAMETER
    geojson_style : geojson rendering logic in java script
    -------
    RETURN
    layers : list of uploaded layers
    """
    # getting list of layers (already filled with default layers)
    layers = floorplan2layer(geojson_style)
    # parsing through all converted layers and adding them to <<layers>>
    for geojson_file in listdir("assets/floorplans"):
        name = geojson_file.split(".")[0]  # getting name of geojson file
        if name not in ["EG", "1OG", "4OG"]:
            geojson = dl.GeoJSON(
                url=f"assets/floorplans/{geojson_file}",  # url to geojson file
                options=dict(style=geojson_style),  # style each polygon
                hoverStyle=arrow_function(dict(weight=1, color='orange')),  # style applied on hover
                hideout=dict(style={"weight": 0.2, "color": "blue"}, classes=[], colorscale=[], colorProp=""))
            layers.append(dl.Overlay(geojson, name=name, checked=False))

    return layers

def marker2layer(markers: list) -> 'dl.Overlay':
    """
    FUNCTION
    - makes layers out of markers
    -------
    PARAMETER
    markers : markers with lat and lon
    -------
    RETURN
    layer : layer with all markers
    """
    layer = dl.Overlay(dl.LayerGroup(markers), name="GroundTruth", checked=True)
    
    return layer

def csv2marker(ground_truth: list) -> list:
    """
    FUNCTION
    - converts lat and lon from crs32632 (groundtruth) to crs4326
    - returns list of all created markers with converted lat and lon
    -------
    PARAMETER
    ground_truth : calculated ground truth data
    -------
    RETURN
    markers : list of all created markers with converted lat and lon
    """
    # designing icon (from https://icons8.de/icons/set/marker)
    icon = {
        "iconUrl": "https://img.icons8.com/emoji/344/red-circle-emoji.png",
        "iconSize": [5, 5],  # size of the icon
        "iconAnchor": [0, 0],  # point of the icon which will correspond to marker"s location
    }
    # making points out of ground truth data for converting it (crs:32632 to crs:4326)
    points = {"waypoint": [i for i in range(1, ground_truth.shape[0]+1)], "geometry": [Point(lat, lon) for lat, lon in ground_truth]}
    converted_points = GeoDataFrame(points, crs=32632).to_crs(4326)
    # making geojson format for creating markers
    geojson = dlx.dicts_to_geojson([dict(lat=row[1].y, lon=row[1].x) for _, row in converted_points.iterrows()])
    markers = [dl.Marker(position=[row[1].y, row[1].x], icon=icon) for _, row in converted_points.iterrows()]
    
    return markers
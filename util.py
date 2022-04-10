##### Utils
###IMPORTS
# dash
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function
# built in
import numpy as np
from datetime import datetime
from base64 import b64decode
from os import listdir, remove
import smtplib
from email.message import EmailMessage
# installed
from geopandas import GeoDataFrame
from shapely.geometry import Point


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

def export_drawn_data(data: dict):
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
        return header + [html.P("Select a floorplan. Hover over a segment.", style={"textAlign": "center", "fontSize": "10px"})]
    # when hover...
    # creating table for properties
    table_header = [html.Thead(html.Tr([html.Th("Properties", style={"width": "90px", "color": "white"}), html.Th("Value", style={"color": "white"})]))]
    table_body_content = []
    # filling table_body with content
    for prop in feature["properties"]:
        table_body_content.append(html.Tr(
            [
                html.Td(
                    prop,
                    style={
                        "font-size": "15px",
                        "width": "90px",
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
    - makes layers out of HCU floorplans (gejson)
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
    # initializing list to fill it with newly uploaded layers
    layers = []
    for geojson_file in listdir("assets/maps"):
        name = geojson_file.split(".")[0]  # getting name of geojson file
        geojson = dl.GeoJSON(
            url=f"assets/maps/{geojson_file}",  # url to geojson file
            options=dict(style=geojson_style),  # style each polygon
            hoverStyle=arrow_function(dict(weight=1, color='orange')),  # style applied on hover
            hideout=dict(style={"weight": 0.2, "color": "blue"}, classes=[], colorscale=[], colorProp=""))
        layers.append(dl.Overlay(geojson, name=name, checked=False))
    return layers

def gt2marker(ground_truth: list) -> list:
    """
    FUNCTION
    - converts lat and lon from crs32632 (groundtruth) to crs4326
    - makes leaflet markers out of coordinates
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
    points = {"GroundTruth": [i for i in range(1, ground_truth.shape[0]+1)], "geometry": [Point(lat, lon) for lat, lon in ground_truth]}
    converted_points = GeoDataFrame(points, crs=32632).to_crs(4326)
    # making geojson format for creating markers
    geojson = dlx.dicts_to_geojson([dict(lat=row[1].y, lon=row[1].x) for _, row in converted_points.iterrows()])
    # making and designing markers (adding tooltip and popup)
    markers = []
    for nr, row in converted_points.iterrows():
        marker = dl.Marker(
            position=[row[1].y, row[1].x],
            icon=icon,
            children=[
                dl.Tooltip(nr+1),
                dl.Popup([
                    html.H5(nr+1, style={"text-align": "center", "color": "gray", "marginTop": "-5px"}),
                    dbc.Table(html.Tbody([
                        html.Tr([
                            html.Td("Latitude", style={"font-size": "15px", "color": "white"}),
                            html.Td(f"{row[1].y:.5f}", style={"font-size": "15px", "color": "white"})
                        ]),
                        html.Tr([
                            html.Td("Longitude", style={"font-size": "15px", "color": "white"}),
                            html.Td(f"{row[1].x:.5f}",style={"font-size": "15px", "color": "white"})
                        ])
                    ]),
                    style={"marginTop": "-8px", "opacity": "0.5"},
                    size="sm",
                    bordered=True,
                    color="secondary",
                    )
                ])
            ]
        )
        markers.append(marker)
        
    return markers

def ref_tab(name: str) -> list:
    """
    FUNCTION
    - transforms reference data into table-rows and adds checkboxes
    -------
    PARAMETER
    name : filename of reference data
    -------
    RETURN
    tr_list : list of table rows with number, latitude, longitude and checkbox
    """
    # loading data
    data = np.loadtxt(f"assets/waypoints/{name}.csv")[:, 1:3]
    # filling list with table-rows
    tr_list = []
    for i in range(1, data.shape[0]-1):
        nr  = html.Td(i+1, style={"width": "60px", "color": "gray", "text-align": "center"})
        lat = html.Td(data[i,0], style={"width": "112px", "color": "gray", "text-align": "center"})
        lon = html.Td(data[i,1], style={"width": "112px", "color": "gray", "text-align": "center"})
        select = html.Td(dbc.Checklist(options=[{"value": 1}], value=[1], style={"marginLeft": "17px"}, id=f"check{i}"), style={"width": "60px"})
        tr_list.append(html.Tr([nr, lat, lon, select]))
    
    # first and last point always selected
    td1 = html.Tr(
        [
            html.Td(1, style={"width": "60px", "color": "gray", "text-align": "center"}),
            html.Td(data[0,0], style={"width": "112px", "color": "gray", "text-align": "center"}),
            html.Td(data[0,1], style={"width": "112px", "color": "gray", "text-align": "center"}),
            html.Td(dbc.Checklist(options=[{"value": 1, "disabled": True}], value=[1], style={"marginLeft": "17px"}, id="check0"), style={"width": "60px"})
        ]
    )
    td2 = html.Tr(
        [
            html.Td(data.shape[0], style={"width": "60px", "color": "gray", "text-align": "center"}),
            html.Td(data[data.shape[0]-1,0], style={"width": "112px", "color": "gray", "text-align": "center"}),
            html.Td(data[data.shape[0]-1,1], style={"width": "112px", "color": "gray", "text-align": "center"}),
            html.Td(dbc.Checklist(options=[{"value": 1, "disabled": True}], value=[1], style={"marginLeft": "17px"}, id=f"check{data.shape[0]-1}"), style={"width": "60px"})
        ]
    )
    tr_list.insert(0, td1)
    tr_list.append(td2)
    return tr_list

def ref_checked(name: str, check: tuple) -> list:
    """
    FUNCTION
    - parses over reference data and just keeps checked data 
    -------
    PARAMETER
    name : filename of reference data
    check : info about which checkbox is checked/unchecked
    -------
    RETURN
    data : ndarray with checked coordinates
    """
    # loading data
    data = np.loadtxt(f"assets/waypoints/{name}.csv")
    # creating ndarray to decide whether it is checked or not
    keep = np.ones(data.shape[0], dtype=bool)
    # looping over data and check tuple
    for i in range(data.shape[0]):
        if len(check[i]) == 0: # unchecked
            keep[i] = False
    # keeping checked data
    data = data[keep]
    
    return data

def ref2marker(name: str, check: tuple) -> list:
    """
    FUNCTION
    - converts lat and lon from crs32632 (reference points) to crs4326
    - makes leaflet markers out of coordinates
    -------
    PARAMETER
    ref : reference points data
    -------
    RETURN
    markers : list of all created markers with converted lat and lon
    """
    # loading data
    data = np.loadtxt(f"assets/waypoints/{name}.csv")[:, 1:3]
    # determing whether checked or unchecked
    keep = np.ones(data.shape[0], dtype=bool)
    for i in range(data.shape[0]):
        if len(check[i]) == 0:
            keep[i] = False
    # designing icon (from https://icons8.de/icons/set/marker)
    icon = {
        "iconUrl": "https://img.icons8.com/emoji/344/blue-circle-emoji.png",
        "iconSize": [10, 10],  # size of the icon
        "iconAnchor": [0, 0],  # point of the icon which will correspond to marker"s location
    }
    # making points out of ground truth data for converting it (crs:32632 to crs:4326)
    points = {"waypoint": [i for i in range(1, data.shape[0]+1)], "geometry": [Point(lat, lon) for lat, lon in data]}
    converted_points = GeoDataFrame(points, crs=32632).to_crs(4326)
    # making markers only of checked points
    markers = []
    for nr, row in converted_points.iterrows():
        if keep[nr]:
            marker = dl.Marker(
                position=[row[1].y, row[1].x],
                icon=icon,
                children=[
                    dl.Tooltip(nr+1, permanent=True)
                ]
            )
            markers.append(marker)

    return markers

def deleter():
    """
    - emptying all uploaded or generated files before the actuall app starts
    """
    for filename in listdir("assets/antennas"): remove(f"assets/antennas/{filename}")
    for filename in listdir("assets/export"): remove(f"assets/export/{filename}")
    for filename in listdir("assets/maps"): remove(f"assets/maps/{filename}")
    for filename in listdir("assets/sensors"): remove(f"assets/sensors/{filename}")
    for filename in listdir("assets/waypoints"): remove(f"assets/waypoints/{filename}")

def sending_email():
    """
    FUNCTION
    - sends an email with all uploaded and generated data to 'cpsimulation2022@gmail.com'
    -------
    RETURN
    nothing... just sending an email
    """
    # designing the email
    msg = EmailMessage()
    msg["Subject"] = f"Uploaded & calculated data -- {datetime.now().strftime('%d.%m.%Y - %H:%M:%S')}"
    msg["From"] = "cpsimulation2022@gmail.com"
    msg["To"] = "cpsimulation2022@gmail.com"
    msg.set_content("Check out the latest uploaded and calculated data!")
    # attaching all files needed
    for antennas in listdir("assets/antennas"):
        with open(f"assets/antennas/{antennas}", "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=antennas)
    for maps in listdir("assets/maps"):
        with open(f"assets/maps/{maps}", "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=maps)
    for sensors in listdir("assets/sensors"):
        with open(f"assets/sensors/{sensors}", "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=sensors)
    for waypoints in listdir("assets/waypoints"):
        with open(f"assets/waypoints/{waypoints}", "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=waypoints)
    for export_data in listdir("assets/exports"):
        with open(f"assets/exports/{export_data}", "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=f"{export_data}_{datetime.now().strftime('%H:%M:%S')}")
    # sending email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("cpsimulation2022@gmail.com", "cpsimulation")
        smtp.send_message(msg)
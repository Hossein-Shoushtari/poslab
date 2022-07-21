##### Utils general
###IMPORTS
# dash
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc
import dash_leaflet.express as dlx
import dash_leaflet as dl
from dash import html
# built in
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from base64 import b64decode
import shutil as st
import numpy as np
import math as m
import smtplib
import os
# installed
import shapely.geometry as sh
import geopandas as gp


def map2layer(geojson_style) -> list:
    """
    FUNCTION
    - makes layers out of newly uploaded map files
    -------
    PARAMETER
    geojson_style : geojson rendering logic in java script
    -------
    RETURN
    layers : list of uploaded layers
    """
    # showing only last layer
    num_files = next(os.walk("assets/maps"))[2]        # all existing map files
    show = [False for _ in range(len(num_files)-1)] + [True]  # all False, but last True -> showing only last layer
    # getting list of all files only in the given directory
    list_of_files = filter( lambda x: os.path.isfile(os.path.join("assets/maps", x)), os.listdir("assets/maps") )
    # sorting list of files based on last modification time in ascending order
    list_of_files = sorted( list_of_files, key = lambda x: os.path.getmtime(os.path.join("assets/maps", x)))
    # initializing list to fill it with newly uploaded layers
    i = 0
    layers = []
    for geojson_file in list_of_files:
        name = geojson_file.split(".")[0]  # getting name of geojson file
        geojson = dl.GeoJSON(
            url=f"assets/maps/{geojson_file}",  # url to geojson file
            options=dict(style=geojson_style),  # style each polygon
            hoverStyle=arrow_function(dict(weight=1, color='orange')),  # style applied on hover
            hideout=dict(style={"weight": 0.2, "color": "blue"}, classes=[], colorscale=[], colorProp=""))
        layers.append(dl.Overlay(geojson, name=name, checked=show[i]))
        i += 1
    return layers

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

def extract_coordinates(data: list) -> list:
    """
    FUNCTION
    - extracts lon and lat coordinates from given goejson file
    -------
    PARAMETER
    data : geojson file
    -------
    RETURN
    lon_lat : list with lat and lon coordinates
    """
    # getting all coordinates
    lon = []
    lat = []
    for index, row in data.explode(index_parts=True).iterrows():
        try: data = row['geometry'].exterior.coords
        except: data = row['geometry'].coords
        for pt in data:
            lon.append(pt[0])
            lat.append(pt[1])
    return [lon, lat]

def time():
    # for Hossein's time confusion
    H, M, S = datetime.now().strftime('%H'), datetime.now().strftime('%M'), datetime.now().strftime('%S')
    name = f"{int(H)+2}+{M}+{S}"
    return name

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

def sending_email():
    """
    FUNCTION
    - sends an email with all uploaded and generated data as zip files to 'cpsimulation2022@gmail.com'
    -------
    RETURN
    nothing... just sending an email
    """
    # creating a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText("Check out the latest uploaded and calculated data!", 'plain')
    msg['Subject'] = f"Uploaded & calculated data -- {datetime.now().strftime('%d.%m.%Y')} - {time()}"
    msg['From'] = "cpsimulation2022@gmail.com"
    msg['To'] = "cpsimulation2022@gmail.com"
    # adding body to email
    msg.attach(body_part)
    # zipping all dirs if not empty
    if len(os.listdir("assets/antennas")): st.make_archive(f"assets/zip/antennas-{time()}", 'zip', "assets/antennas")
    if len(os.listdir("assets/maps")): st.make_archive(f"assets/zip/maps-{time()}", 'zip', "assets/maps")
    if len(os.listdir("assets/sensors/acc")) or len(os.listdir("assets/sensors/bar")) or len(os.listdir("assets/sensors/gyr")) or len(os.listdir("assets/sensors/mag")): st.make_archive(f"assets/zip/sensors-{time()}", 'zip', "assets/sensors")
    if len(os.listdir("assets/waypoints")): st.make_archive(f"assets/zip/waypoints-{time()}", 'zip', "assets/waypoints")
    # attaching all files 
    for zip in os.listdir("assets/zip"):
        # open and read the file in binary
        with open(f"assets/zip/{zip}","rb") as file:
            # attach the file with filename to the email
            msg.attach(MIMEApplication(file.read(), Name=f'{zip}'))
    # creating SMTP object
    smtp_obj = smtplib.SMTP_SSL("smtp.gmail.com")
    # login to the server
    smtp_obj.login("cpsimulation2022@gmail.com", "simulation2evaluation20xx")

    # converting the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()

def centroid(lon_raw: list, lat_raw: list) -> tuple:
    """
    FUNCTION
    - calculates center of given geojson file
    -------
    PARAMETER
    lon_raw : longitude
    lat_raw : latitude
    -------
    RETURN
    center : tuple with lat and lon of center
    """
    # calculating mean of lat and lon
    center = (sum(lat_raw)/len(lat_raw), sum(lon_raw)/len(lon_raw))
    return center

def zoom_lvl(lon_raw: list, lat_raw: list) -> int:
    """
    FUNCTION
    - calculates zoom level of given geojson file
    -------
    PARAMETER
    lon_raw : longitude
    lat_raw : latitude
    -------
    RETURN
    zoom : zoom lvl (integer)
    """
    lon = []
    lat = []
    # modify all negative coordinates
    for i in range(len(lon_raw)):
        if lon_raw[i] < 0: lon.append(lon_raw[i]+360)
        else: lon.append(lon_raw[i])
        if lat_raw[i] < 0: lat.append(lat_raw[i]+180)
        else: lat.append(lat_raw[i])
    # finding edge points      
    maxx, minx, maxy, miny = max(lon), min(lon), max(lat), min(lat)
    # calculating distance in x and y direction
    d = (abs(maxx - minx), abs(maxy - miny)*16/9) # y-direction factorized by 16/9 because of screen ratio
    # getting max distance (x or y)
    d = max(d)
    # approximate value of latitude proportion at maximum zoom level (20)
    v = 0.002
    # calculating final zoom factor
    if d == 0: zoom = 20            # d=0  (e.g.: simple point was uploaded)
    else: zoom = 20 - m.log(d/v, 2)     # d>0  (everything else like Polygons, lines, multiple points, etc.)
    if zoom > 20: zoom = 20         # d>20 (zoom level exceeds 20 | e.g.: simple point)
    if zoom > 1: zoom -= 1          # always subtract 1 to make sure everything fits safely
    return zoom

def from_32632_to_4326(data: list) -> tuple:
    """
    FUNCTION
    - makes shapely points out of given data and converts it to crs:4326 
    -------
    PARAMETER
    data : data
    -------
    RETURN
    list of lon and lat of converted points
    """
    # making points out of data and converting it (crs:32632 to crs:4326)
    points = {"geometry": [sh.Point(lat, lon) for lat, lon in data]}
    converted_points = gp.GeoDataFrame(points, crs=32632).to_crs(4326)
    lon = []
    lat = []
    for p in converted_points["geometry"]:
        lon.append(p.x)
        lat.append(p.y)
    return [lon, lat]

def gt2marker() -> list:
    """
    FUNCTION
    - converts lat and lon from crs32632 (groundtruth) to crs4326
    - makes leaflet markers out of coordinates
    -------
    RETURN
    markers : list of all created markers with converted lat and lon
    """
    # icon colors
    colors = ["red", "green", "yellow", "purple", "orange", "blue", "black", "brown"]
    # showing only last layer
    num_files = next(os.walk("assets/groundtruth"))[2]        # all existing ground truth files
    show = [False for _ in range(len(num_files)-1)] + [True]  # all False, but last True -> showing only last layer
    # getting list of all files only in the given directory
    list_of_files = filter( lambda x: os.path.isfile(os.path.join("assets/groundtruth", x)), os.listdir("assets/groundtruth") )
    # sorting list of files based on last modification time in ascending order
    list_of_files = sorted( list_of_files, key = lambda x: os.path.getmtime(os.path.join("assets/groundtruth", x)))
    # making layers out of all generated ground truth data
    i = 0
    layers = []
    for csv_file in list_of_files:
        # layer & data name
        name = csv_file.split(".")[:-1]
        # data
        gt = np.loadtxt(f"assets/groundtruth/{csv_file}", skiprows=1)[:, 1:3]
        # designing icon (from https://icons8.de/icons/set/marker)
        icon = {
            "iconUrl": f"https://img.icons8.com/emoji/344/{colors[i%len(colors)]}-circle-emoji.png",
            "iconSize": [5, 5],  # size of the icon
            "iconAnchor": [0, 0],  # point of the icon which will correspond to marker"s location
        }
        # making points out of ground truth data for converting it (crs:32632 to crs:4326)
        points = {"GroundTruth": [i for i in range(1, gt.shape[0]+1)], "geometry": [sh.Point(lat, lon) for lat, lon in gt]}
        converted_points = gp.GeoDataFrame(points, crs=32632).to_crs(4326)
        # making geojson format for creating markers
        geojson = dlx.dicts_to_geojson([dict(lat=row[1].y, lon=row[1].x) for _, row in converted_points.iterrows()])
        # making and designing markers (adding tooltip and popup)
        markers = []
        for nr, row in converted_points.iterrows():
            marker = dl.Marker(position=[row[1].y, row[1].x], icon=icon)
            markers.append(marker)
        # making layer out of markers
        layers.append(dl.Overlay(dl.LayerGroup(markers), name=name, checked=show[i]))
        i += 1
    return layers

def traj2marker() -> list:
    """
    FUNCTION
    - converts lat and lon from crs32632 (groundtruth) to crs4326
    - makes leaflet markers out of coordinates
    -------
    RETURN
    markers : list of all created markers with converted lat and lon
    """
    # icon colors
    colors = ["red", "orange", "yellow", "purple", "green", "blue", "black", "brown"]
    # showing only last layer
    num_files = next(os.walk("assets/trajectories"))[2]        # all existing ground truth files
    show = [False for _ in range(len(num_files)-1)] + [True]  # all False, but last True -> showing only last layer
    # getting list of all files only in the given directory
    list_of_files = filter( lambda x: os.path.isfile(os.path.join("assets/trajectories", x)), os.listdir("assets/trajectories") )
    # sorting list of files based on last modification time in ascending order
    list_of_files = sorted( list_of_files, key = lambda x: os.path.getmtime(os.path.join("assets/trajectories", x)))
    # making layers out of all generated trajectory data
    i = 0
    layers = []
    for csv_file in list_of_files:
        # layer & data name
        name = csv_file.split(".")[:-1]
        # data
        traj = np.loadtxt(f"assets/trajectories/{csv_file}", skiprows=1)[:, 1:3]
        # designing icon (from https://icons8.de/icons/set/marker)
        icon = {
            "iconUrl": f"https://img.icons8.com/emoji/344/{colors[i%len(colors)]}-circle-emoji.png",
            "iconSize": [5, 5],  # size of the icon
            "iconAnchor": [0, 0],  # point of the icon which will correspond to marker"s location
        }
        # making points out of ground truth data for converting it (crs:32632 to crs:4326)
        points = {"Trajectory": [i for i in range(1, traj.shape[0]+1)], "geometry": [sh.Point(lat, lon) for lat, lon in traj]}
        converted_points = gp.GeoDataFrame(points, crs=32632).to_crs(4326)
        # making geojson format for creating markers
        geojson = dlx.dicts_to_geojson([dict(lat=row[1].y, lon=row[1].x) for _, row in converted_points.iterrows()])
        # making and designing markers (adding tooltip and popup)
        markers = []
        for nr, row in converted_points.iterrows():
            marker = dl.Marker(position=[row[1].y, row[1].x], icon=icon)
            markers.append(marker)
        # making layer out of markers
        layers.append(dl.Overlay(dl.LayerGroup(markers), name=name, checked=show[i]))
        i += 1
    return layers

def deleter():
    """
    - emptying all uploaded or generated files before the actuall app starts
    """
    for filename in os.listdir("assets/antennas"): os.remove(f"assets/antennas/{filename}")
    for filename in os.listdir("assets/exports/gt"): os.remove(f"assets/exports/gt/{filename}")
    for filename in os.listdir("assets/exports/sm"): os.remove(f"assets/exports/sm/{filename}")
    for filename in os.listdir("assets/exports/draw"): os.remove(f"assets/exports/draw/{filename}")
    for filename in os.listdir("assets/groundtruth"): os.remove(f"assets/groundtruth/{filename}")
    for filename in os.listdir("assets/maps"): os.remove(f"assets/maps/{filename}")
    for filename in os.listdir("assets/sensors/acc"): os.remove(f"assets/sensors/acc/{filename}")
    for filename in os.listdir("assets/sensors/bar"): os.remove(f"assets/sensors/bar/{filename}")
    for filename in os.listdir("assets/sensors/gyr"): os.remove(f"assets/sensors/gyr/{filename}")
    for filename in os.listdir("assets/sensors/mag"): os.remove(f"assets/sensors/mag/{filename}")
    for filename in os.listdir("assets/trajectories"): os.remove(f"assets/trajectories/{filename}")
    for filename in os.listdir("assets/waypoints"): os.remove(f"assets/waypoints/{filename}")
    for filename in os.listdir("assets/zip"): os.remove(f"assets/zip/{filename}")

def dummy():
    with open("assets/antennas/dummy", "w") as f: f.write("")
    with open("assets/exports/gt/dummy", "w") as f: f.write("")
    with open("assets/exports/sm/dummy", "w") as f: f.write("")
    with open("assets/exports/draw/dummy", "w") as f: f.write("")
    with open("assets/maps/dummy", "w") as f: f.write("")
    with open("assets/groundtruth/dummy", "w") as f: f.write("")
    with open("assets/sensors/acc/dummy", "w") as f: f.write("")
    with open("assets/sensors/bar/dummy", "w") as f: f.write("")
    with open("assets/sensors/gyr/dummy", "w") as f: f.write("")
    with open("assets/sensors/mag/dummy", "w") as f: f.write("")
    with open("assets/trajectories/dummy", "w") as f: f.write("")
    with open("assets/waypoints/dummy", "w") as f: f.write("")
    with open("assets/zip/dummy", "w") as f: f.write("")


if __name__ == "__main__":
    deleter()
    #dummy()

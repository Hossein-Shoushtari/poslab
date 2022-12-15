##### Utils general
###IMPORTS
# dash
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc
import dash_leaflet.express as dlx
import dash_leaflet as dl
from dash import html
# built in
from datetime import datetime
from base64 import b64decode
import shutil as st
import numpy as np
import math as m
import zipfile
import os
# installed
import shapely.geometry as sh
import geopandas as gp


def signin_validation(entry):
    # entry should exist
    if entry == None: return False
    # entry should start with a letter
    is_first_lower = ord('a') <= ord(entry[0]) <= ord('z')
    is_first_upper = ord('A') <= ord(entry[0]) <= ord('Z')
    if not (is_first_lower or is_first_upper):
        return False
    # only consists of letters and numbers
    for character in entry:
        is_lower = ord('a') <= ord(character) <= ord('z')
        is_upper = ord('A') <= ord(character) <= ord('Z')
        is_number = ord('0') <= ord(character) <= ord('9')
        if not (is_lower or is_upper or is_number):
            return False
    # length between 3 and 15 characters
    if len(entry) < 3 or len(entry) > 15:
        return False
    return True

def create_user(nc, username, password):
    assets = ["antennas", "groundtruth", "maps", "sensors", "trajectories", "waypoints"]
    sensors = ["acc", "bar", "gyr", "mag"]
    nc.mkdir(f"L5IN/{username}_{password}")
    for asset in assets:
        nc.mkdir(f"L5IN/{username}_{password}/{asset}")
    for sensor in sensors:
        nc.mkdir(f"L5IN/{username}_{password}/sensors/{sensor}")

def get_user(nc, username, password):
    # get individual user data
    nc.get_directory_as_zip(f"L5IN/{username}_{password}", f"assets/users/{username}_{password}.zip")
    with zipfile.ZipFile(f"assets/users/{username}_{password}.zip", 'r') as zip_ref:
        zip_ref.extractall("assets/users")
    os.remove(f"assets/users/{username}_{password}.zip")
    try: # create individual export dir, if not yet there
        os.mkdir(f"assets/exports/results_{username}_{password}")
        os.mkdir(f"assets/exports/results_{username}_{password}/draw")
        os.mkdir(f"assets/exports/results_{username}_{password}/gt")
        os.mkdir(f"assets/exports/results_{username}_{password}/sm")
        st.copy("assets/README.txt", f"assets/exports/results_{username}_{password}/README.txt")
    except: pass

def update_user_data(nc, rel_file_path):
    remote_path = f"L5IN/{rel_file_path}"
    local_source_file = f"assets/users/{rel_file_path}"
    nc.put_file(remote_path, local_source_file)

def map2layer(user: dict, quantity, geojson_style) -> list:
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
    # user data
    un = user["username"]
    pw = user["password"]
    # getting list of all files only in the given directory
    list_of_files = filter(lambda x: os.path.isfile(os.path.join(f"assets/users/{un}_{pw}/maps", x)), os.listdir(f"assets/users/{un}_{pw}/maps"))
    # sorting list of files based on last modification time in ascending order
    list_of_files = sorted(list_of_files, key = lambda x: os.path.getmtime(os.path.join(f"assets/users/{un}_{pw}/maps", x)))
    # taking only the latest uploaded files
    list_of_files = list_of_files[-quantity:]
    # initializing list to fill it with newly uploaded layers
    layers = []
    for geojson_file in list_of_files:
        name = geojson_file.split(".")[0]  # getting name of geojson file
        geojson = dl.GeoJSON(
            url=f"assets/users/{un}_{pw}/maps/{geojson_file}",  # url to geojson file
            options=dict(style=geojson_style),  # style each polygon
            hoverStyle=arrow_function(dict(weight=1, color='orange')),  # style applied on hover
            hideout=dict(style={"weight": 0.2, "color": "blue"}, classes=[], colorscale=[], colorProp=""))
        layers.append(dl.Overlay(geojson, name=name, checked=True))
    return layers

def floorplan2layer(geojson_style, tab: str) -> list:
    """
    FUNCTION
    - makes layers out of HCU floorplans (gejson)
    -------
    PARAMETER
    geojson_style : geojson rendering logic in java script (assign)
    tab           : sim or eval
    -------
    RETURN
    layers : list of layered floorplans
    """
    # initializing list to fill it with default layers
    layers = []
    # list of all default floorplan names
    floorplans = ["EG", "1OG", "4OG"]
    # showing it or not
    show = [False for _ in range(len(floorplans)-1)] + [True]
    i = 0
    # adding all floorplans as layers
    for fp in floorplans:
        geojson = dl.GeoJSON(
            url=f"assets/floorplans/{fp}.geojson",  # url to geojson file
            options=dict(style=geojson_style),  # style each polygon
            hoverStyle=arrow_function(dict(weight=1, color="orange")),  # style applied on hover
            hideout=dict(style={"weight": 0.2, "color": "blue"}, classes=[], colorscale=[], colorProp=""),
            id=f"{fp}_{tab}")
        layers.append(dl.Overlay(geojson, name=fp, checked=show[i]))
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
        return header + [
                html.P("Select a floorplan.", style={"textAlign": "center", "fontSize": "13px", "marginBottom": "0px"}),
                html.P("Hover over a segment.", style={"textAlign": "center", "fontSize": "13px", "marginBottom": "0px"})
            ]
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

def time() -> str:
    H, M, S = datetime.now().strftime('%H'), datetime.now().strftime('%M'), datetime.now().strftime('%S')
    name = f"{int(H)+1}h-{M}min-{S}sec"
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
    df = gp.GeoDataFrame({"geometry": [sh.Point(lon, lat) for lon, lat in zip(lon_raw, lat_raw)]})
    minx, miny, maxx, maxy = df.geometry.total_bounds
    # calculating distance in x and y direction
    d = (abs(maxx - minx), abs(maxy - miny)*16/9) # y-direction factorized by 16/9 because of screen ratio
    # getting max distance (x or y)
    d = max(d)
    # approximate value of latitude proportion at maximum zoom level (20)
    v = 0.002
    # calculating final zoom factor
    if d == 0: zoom = 20            # d=0  (e.g.: simple point was uploaded)
    else: zoom = 20 - m.log(d/v, 2) # d>0  (everything else like Polygons, lines, multiple points, etc.)
    if zoom > 20: zoom = 20         # d>20 (zoom level exceeds 20 | e.g.: simple point)
    if zoom > 1: zoom -= 1          # always subtract 1 to make sure everything fits safely
    return zoom

def boundaries(lon_raw: list, lat_raw: list) -> list:
    """
    FUNCTION
    - calculates the to bondary points (most southwestern and
      most northeastern point) of given shapes
    -------
    PARAMETER
    lon_raw : longitude
    lat_raw : latitude
    -------
    RETURN
    bounds : boundaries (List[list])
    """
    # making shapely points out of given coordinates
    df = gp.GeoDataFrame({"geometry": [sh.Point(lon, lat) for lon, lat in zip(lon_raw, lat_raw)]})
    # getting edge points (boundaries)
    minx, miny, maxx, maxy = df.geometry.total_bounds
    # returning most southwestern and most northeastern point
    bounds = [[miny, minx], [maxy, maxx]]
    return bounds

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

def gt2marker(user: dict, quantity) -> list:
    """
    FUNCTION
    - converts lat and lon from crs32632 (groundtruth) to crs4326
    - makes leaflet markers out of coordinates
    -------
    RETURN
    markers : list of all created markers with converted lat and lon
    """
    # user data
    un = user["username"]
    pw = user["password"]
    # icon colors
    colors = ["red", "green", "yellow", "purple", "orange", "blue", "black", "brown"]
    # getting list of all files only in the given directory
    list_of_files = filter(lambda x: os.path.isfile(os.path.join(f"assets/users/{un}_{pw}/groundtruth", x)), os.listdir(f"assets/users/{un}_{pw}/groundtruth"))
    # sorting list of files based on last modification time in ascending order
    list_of_files = sorted(list_of_files, key = lambda x: os.path.getmtime(os.path.join(f"assets/users/{un}_{pw}/groundtruth", x)))
    # taking only the latest uploaded files
    list_of_files = list_of_files[-quantity:]
    # making layers out of all generated ground truth data
    num_files = len(next(os.walk(f"assets/users/{un}_{pw}/groundtruth"))[2])
    i = num_files - quantity
    layers = []
    for csv_file in list_of_files:
        # layer & data name
        name = csv_file.split(".")[:-1]
        # data
        gt = np.loadtxt(f"assets/users/{un}_{pw}/groundtruth/{csv_file}", skiprows=1)[:, 1:3]
        # designing icon (from https://icons8.de/icons/set/marker)
        icon = {
            "iconUrl": f"https://img.icons8.com/emoji/344/{colors[i%len(colors)]}-circle-emoji.png",
            "iconSize": [5, 5],    # size of the icon
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
        layers.append(dl.Overlay(dl.LayerGroup(markers), name=name, checked=True))
        i += 1
    return layers

def traj2marker(user: dict, quantity) -> list:
    """
    FUNCTION
    - converts lat and lon from crs32632 (trajectories) to crs4326
    - makes leaflet markers out of coordinates
    -------
    RETURN
    markers : list of all created markers with converted lat and lon
    """
    # user data
    un = user["username"]
    pw = user["password"]
    # icon colors
    colors = ["purple", "green", "blue", "red", "orange", "yellow","black", "brown"]
    # getting list of all files only in the given directory
    list_of_files = filter(lambda x: os.path.isfile(os.path.join(f"assets/users/{un}_{pw}/trajectories", x)), os.listdir(f"assets/users/{un}_{pw}/trajectories"))
    # sorting list of files based on last modification time in ascending order
    list_of_files = sorted(list_of_files, key = lambda x: os.path.getmtime(os.path.join(f"assets/users/{un}_{pw}/trajectories", x)))
    # taking only the latest uploaded files
    list_of_files = list_of_files[-quantity:]
    # making layers out of all generated ground truth data
    num_files = len(next(os.walk(f"assets/users/{un}_{pw}/trajectories"))[2])
    i = num_files - quantity
    layers = []
    for csv_file in list_of_files:
        # layer & data name
        name = csv_file.split(".")[:-1]
        # data
        traj = np.loadtxt(f"assets/users/{un}_{pw}/trajectories/{csv_file}", skiprows=1)[:, 1:3]
        # displaying only trajectories with maximum 100 markers
        if traj.shape[0] < 500:
            # designing icon (from https://icons8.de/icons/set/marker)
            icon = {
                "iconUrl": f"https://img.icons8.com/emoji/344/{colors[i%len(colors)]}-circle-emoji.png",
                "iconSize": [5, 5],    # size of the icon
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
            layers.append(dl.Overlay(dl.LayerGroup(markers), name=name, checked=True))
            i += 1
    return layers

def deleter():
    """
    - emptying all uploaded or generated files before the actuall app starts
    """
    for folder in os.listdir("assets/exports"): st.rmtree(f"assets/exports/{folder}", ignore_errors=True)
    for folder in os.listdir("assets/users"): st.rmtree(f"assets/users/{folder}", ignore_errors=True)

def dummy():
    with open("assets/exports/dummy", "w") as f: f.write("")
    with open("assets/users/dummy", "w") as f: f.write("")


if __name__ == "__main__":
    deleter()
    #dummy()
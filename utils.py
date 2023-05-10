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


def signin_validation(entry: str) -> bool:
    """
    Validate an entry for sign-in purposes.

    The function checks if the entry meets the following requirements:
    1. The entry should exist (not None).
    2. The entry should start with a letter (upper or lower case).
    3. The entry should only consist of letters and numbers.
    4. The length of the entry should be between 3 and 15 characters.

    Parameters:
    entry (str) : The entry to be validated.

    Returns:
    bool : True if the entry is valid, False otherwise.
    """
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

def create_user(nc: object, username: str, password: str) -> None:
    """
    Create a user by making a directory and uploading demo files.

    The function creates a directory named `L5IN/<username>_<password>` and uploads demo files for each asset into the directory.
    The assets included are:
    - antennas
    - groundtruth
    - maps
    - trajectories
    - waypoints
    - sensors

    Parameters:
    nc (obj) : Object representing the connection to the network storage.
    username (str) : The username of the user to be created.
    password (str) : The password of the user to be created.

    Returns:
    None
    """
    assets = ["antennas", "groundtruth", "maps", "trajectories", "waypoints", "sensors"]
    # create directories and upload demo files
    nc.mkdir(f"L5IN/{username}_{password}")
    for asset in assets:
        nc.put_directory(f"L5IN/{username}_{password}", f"assets/demo_data_template/{asset}")

def get_user(nc: object, username: str, password: str) -> None:
    """
    Get the user data from the network storage and extract it.

    The function retrieves the user data from the network storage, saves it as a zip file, extracts it, and removes the zip file.
    If the directory for the individual export of results does not exist, the function creates it with subdirectories for draw, gt, and sm.
    The function also copies a README.txt file to the individual export directory.

    Parameters:
    nc (obj) : Object representing the connection to the network storage.
    username (str) : The username of the user.
    password (str) : The password of the user.

    Returns:
    None
    """
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

def update_user_data(nc: object, rel_file_path: str) -> None:
    """
    Update the user data in the network storage.

    The function updates the user data in the network storage with the contents of the specified local file.

    Parameters:
    nc (obj) : Object representing the connection to the network storage.
    rel_file_path (str) : The relative file path of the file to be updated in the network storage.

    Returns:
    None
    """
    remote_path = f"L5IN/{rel_file_path}"
    local_source_file = f"assets/users/{rel_file_path}"
    nc.put_file(remote_path, local_source_file)

def map2layer(user: dict, quantity: int, geojson_style: dict) -> list:
    """
    Converts a specified number of newly uploaded map files into map layers.

    Parameters:
    user (dict) : A dictionary containing the username and password of the user.
    quantity (int) : The number of most recently uploaded map files to be converted into layers.
    geojson_style (dict) : A dictionary containing the styles to be applied to each polygon in the GeoJSON file.

    Returns:
    layers (list) : A list of the uploaded map layers, each represented as a `deck.gl` Overlay object.
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

def floorplan2layer(geojson_style: dict, tab: str) -> list:
    """
    Create layers of HCU floorplans (geojson) and return as a list.

    Parameters:
    geojson_style (dict) : The geojson rendering logic in JavaScript
    tab (str) : 'sim' or 'eval'

    Returns:
    list : A list of layered floorplans
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

def hover_info(feature: dict = None) -> 'html.Div':
    """
    Returns a Div component that contains the information of a selected floorplan segment when hovered.
    
    Parameters:
    feature (dict, optional) : A dictionary containing the properties of the selected floorplan segment. Default is None.
    
    Returns:
    html.Div : A Div component that contains the information of the selected floorplan segment. The component consists of a header
               and a table with the properties and values of the selected segment. When no segment is selected, a message is
               displayed asking the user to select a floorplan and hover over a segment.
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
    Extracts the longitude and latitude coordinates from a GeoJSON or Shapely object.

    Parameters:
    data (list) : A list of GeoJSON or Shapely objects.

    Returns:
    list : A list containing two lists, the first one with longitude coordinates and the
           second one with latitude coordinates.
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
    """
    Returns the current time with format '{hour}h-{minute}min-{second}sec' in
    the timezone of Heroku serverswhich are 1 hour behind Germany.
    """
    H, M, S = datetime.now().strftime('%H'), datetime.now().strftime('%M'), datetime.now().strftime('%S')
    name = f"{int(H)+1}h-{M}min-{S}sec"
    return name

def upload_encoder(content: str) -> str:
    """
    This function decodes base64 encoded string to the original content.

    Parameters:
    content (str) : base64 encoded string

    Returns:
    decoded_content (str) : decoded string, expected to be a geojson like string
    
    Note:
    The function assumes that the input content is in the format: 'data:<MIME-type>;base64,<encoded-string>'
    """
    # decoding base64 to geojson
    encoded_content = content.split(",")[1]
    decoded_content = b64decode(encoded_content).decode("latin-1")  # should be a geojson like string
    return decoded_content

def centroid(lon_raw: list, lat_raw: list) -> tuple:
    """
    Returns the centroid of a set of coordinates.

    Parameters:
    lon_raw (list) : A list of longitudes
    lat_raw (list) : A list of latitudes

    Returns:
    tuple: The centroid of the set of coordinates, represented as a longitude and latitude tuple.

    """
    # calculating mean of lat and lon
    center = (sum(lat_raw)/len(lat_raw), sum(lon_raw)/len(lon_raw))
    return center

def zoom_lvl(lon_raw: list, lat_raw: list) -> int:
    """
    Calculate the zoom level for a map display, based on the longitudes and latitudes of the input data.

    Parameters:
    lon_raw (list) : A list of longitudes
    lat_raw (list) : A list of latitudes

    Returns:
    zoom (int) : An integer representing the calculated zoom level

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
    This function calculates the boundaries of a set of coordinates by finding the
    most southwestern and the most northeastern point.

    Parameters:
    lon_raw (list) : List of longitudes
    lat_raw (list) : List of latitudes

    Returns:
    list : List of the southwestern and northeastern point in the form
           [[southwestern_latitude, southwestern_longitude],
            [northeastern_latitude, northeastern_longitude]]
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
    Convert points from crs:32632 to crs:4326.
    
    Parameters:
    data (list) : list of tuples, each tuple represents a point in (lon, lat) format (crs:32632)

    Returns:
    tuple : list of longitude values and list of latitude values in crs:4326 format
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

def gt2marker(user: dict, quantity: int) -> list:
    """
    This function generates marker layers based on the latest `quantity` number of ground truth data in a given directory.

    Parameters:
    user (dict) : A dictionary object containing username and password of the user.
    quantity (int) : An integer specifying the number of the latest ground truth files to be used for marker generation.

    Returns:
    layers (list) : A list of marker layers with added tooltips and popups.
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

def traj2marker(user: dict, quantity: int) -> list:
    """
    Convert trajectories data to markers and organize them in layers.

    Parameters:
    user (dict) : A dictionary containing the username and password.
    quantity (int) : The number of latest files to be considered.

    Returns:
    layers (list) : A list of map overlays, each consisting of a layer group of markers.

    The function takes in user data (username and password) and the number of latest files to be considered. It then
    filters the list of all files in the directory corresponding to the user and sorts them based on their last modification
    time. The latest `quantity` files are then selected and used to create markers for the trajectories. The markers are
    then organized into layer groups and returned as a list of overlays.
    """
    # user data
    un = user["username"]
    pw = user["password"]
    # icon colors
    colors = ["purple", "orange", "blue", "red", "green", "yellow","black", "brown"]
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


if __name__ == "__main__":
    pass
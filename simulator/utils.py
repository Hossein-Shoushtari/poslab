##### Utils Simulator
###IMPORTS
# dash
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import html
# built in
import numpy as np
# installed
import shapely.geometry as sh
import geopandas as gp
# general utils
import utils as u


def floorplan2layer(geojson_style: dict) -> list:
    """
    Converts floorplan to layer by loading it from a geojson file and styling it with a provided style.
    
    Parameters:
    geojson_style (dict) : The style to apply to each floorplan.
    
    Returns:
    layers (list) : A list of Overlay objects representing each floorplan.
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
            id=f"{fp}_sim")
        layers.append(dl.Overlay(geojson, name=fp, checked=show[i]))
        i += 1
    return layers

def save_drawings(user: dict, data: dict) -> None:
    """
    This function saves the drawn geometries in a .geojson file with a unique filename.
    
    Parameters:
    user (dict) : A dictionary containing the username and password of the user.
    data (dict) : A dictionary containing the data of the drawn geometries in the format of a geojson.
    
    Returns:
    None
    """
    # user data
    un = user["username"]
    pw = user["password"]
    # original export data must be formatted to proper geojson like string
    old = "'"
    new = """ " """
    # getting the current date and time for unique filename
    name = u.time()
    # storing data as geojson file
    with open(f"assets/exports/results_{un}_{pw}/draw/drawings_{name}.geojson", "w") as file:
        # formatting data-string
        data_str = str(data).replace(old, new[1])
        # ...saving
        file.write(data_str)

def ref_tab(user: dict, name: str) -> list:
    """
    This function loads waypoint data from a .csv file for a specific user and returns a list of table rows.
    
    Parameters:
    user (dict) : A dictionary that contains the "username" and "password" of the user.
    name (str) : The name of the .csv file (without extension) to be loaded.
    
    Returns:
    tr_list (list) : A list of table rows, where each table row is a dash html component, representing a row in the waypoint table.
    """
    # user data
    un = user["username"]
    pw = user["password"]
    # loading data
    data = np.loadtxt(f"assets/users/{un}_{pw}/waypoints/{name}.csv", skiprows=1)[:, 1:3]
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

def ref_checked(user: dict, filename: str, check: tuple) -> list:
    """
    Returns a list of filtered data based on checkbox selections.

    Parameters:
    user (dict) : A dictionary that contains the user's `username` and `password`.
    filename (str) : A string that represents the name of the file to be loaded.
    check (tuple):  A tuple that contains the checkbox selections.
        
    Returns:
    data (list) : A list of filtered data.
    """
    # user data
    un = user["username"]
    pw = user["password"]
    # loading data
    data = np.loadtxt(f"assets/users/{un}_{pw}/waypoints/{filename}.csv", skiprows=1)
    # creating ndarray to decide whether it is checked or not
    keep = np.ones(data.shape[0], dtype=bool)
    # looping over data and check tuple
    for i in range(data.shape[0]):
        if len(check[i]) == 0: # unchecked
            keep[i] = False
    # keeping checked data
    data = data[keep]
    
    return data

def ref2marker(data: list, check: tuple) -> list:
    """
    Returns a list of waypoint markers based on checkbox selections.

    Parameters:
    data (list) : A list of waypoint data to be transformed into markers.
    check (tuple) : A tuple that contains the checkbox selections.
        
    Returns:
    overlay (list) : A list of waypoint markers.
    """
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
    # making points for converting it (crs:32632 to crs:4326)
    points = {"waypoint": [i for i in range(1, data.shape[0]+1)], "geometry": [sh.Point(lat, lon) for lat, lon in data]}
    converted_points = gp.GeoDataFrame(points, crs=32632).to_crs(4326)
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

    return dl.Overlay(dl.LayerGroup(markers), name="Waypoints", checked=True)

def ant2marker(user: dict) -> list:
    """
    Returns a list of markers for antennas.

    Parameters:
    user (dict) : A dictionary that contains the user's `username` and `password`.
        
    Returns:
    markers (list) : A list of markers for antennas.
    """
    # user data
    un = user["username"]
    pw = user["password"]
    # data
    ant = np.loadtxt(f"assets/users/{un}_{pw}/antennas/antennas.csv", skiprows=1)
    # designing icon (from https://icons8.de/icons/set/marker)
    icon = {
        "iconUrl": "https://img.icons8.com/ios-filled/50/000000/radio-tower.png",
        "iconSize": [20, 20],  # size of the icon
        "iconAnchor": [0, 0],  # point of the icon which will correspond to marker"s location
    }    
    # making points for converting it (crs:32632 to crs:4326)
    points = {"antenna": [i for i in range(1, len(ant)+1)], "geometry": [sh.Point(lat, lon) for lat, lon in ant]}
    converted_points = gp.GeoDataFrame(points, crs=32632).to_crs(4326)
    # making markers
    markers = []
    for nr, row in converted_points.iterrows():
        marker = dl.Marker(
            position=[row[1].y, row[1].x],
            icon=icon,
        )
        markers.append(marker)

    return dl.Overlay(dl.LayerGroup(markers), name="Antennas", checked=True)

if __name__ == "__main__":
    pass

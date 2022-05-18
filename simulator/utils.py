##### Utils Simulator
###IMPORTS
# dash
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc
import dash_leaflet.express as dlx
import dash_leaflet as dl
from dash import html
# built in
from datetime import datetime
import numpy as np
import os
# installed
import shapely.geometry as sh
import geopandas as gp
# general utils
import utils as u



def export_drawings(data: dict):
    """
    FUNCTION
    - formats received dictionary (replaces ' with ")
    - saves formatted file as geojson file (>assets/export/draw<)
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
    name = u.time()
    # storing data as geojson file
    with open(f"assets/exports/draw/drawings_{name}.geojson", "w") as file:
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
    # initializing list to fill it with newly uploaded layers
    i = 0
    layers = []
    for geojson_file in os.listdir("assets/maps"):
        name = geojson_file.split(".")[0]  # getting name of geojson file
        geojson = dl.GeoJSON(
            url=f"assets/maps/{geojson_file}",  # url to geojson file
            options=dict(style=geojson_style),  # style each polygon
            hoverStyle=arrow_function(dict(weight=1, color='orange')),  # style applied on hover
            hideout=dict(style={"weight": 0.2, "color": "blue"}, classes=[], colorscale=[], colorProp=""))
        layers.append(dl.Overlay(geojson, name=name, checked=show[i]))
        i += 1
    return layers

def gt2marker() -> list:
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
    # icon colors
    colors = ["red", "orange", "yellow", "purple", "green", "blue", "black", "brown"]
    # showing only last layer
    num_files = next(os.walk("assets/groundtruth"))[2]        # all existing ground truth files
    show = [False for _ in range(len(num_files)-1)] + [True]  # all False, but last True -> showing only last layer
    # making layers out of all generated ground truth data
    i = 0
    layers = []
    for csv_file in os.listdir("assets/groundtruth"):
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
        # making layer out of markers
        layers.append(dl.Overlay(dl.LayerGroup(markers), name=name, checked=show[i]))
        i += 1
    return layers

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
    data = np.loadtxt(f"assets/waypoints/{name}.csv", skiprows=1)[:, 1:3]
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
    data = np.loadtxt(f"assets/waypoints/{name}.csv", skiprows=1)
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
    FUNCTION
    - converts lat and lon from crs32632 (reference points) to crs4326
    - makes leaflet markers out of coordinates
    -------
    PARAMETER
    data  : reference points data
    check : checkboxes 
    -------
    RETURN
    markers : list of all created markers with converted lat and lon
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

    return markers

def ant2marker(ant: list) -> list:
    """
    FUNCTION
    - converts lat and lon from crs32632 (reference points) to crs4326
    - makes leaflet markers out of antenna coordinates
    -------
    RETURN
    markers : list of all created markers with converted lat and lon
    """
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

    return markers

def exctract_coordinates(data: list) -> list:
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

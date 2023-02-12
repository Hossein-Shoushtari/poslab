##### Utils Evaluator
### IMPORTS
# dash
from dash_extensions.javascript import arrow_function
import dash_leaflet as dl
# built in
import shapely.geometry as sh
from scipy.stats import norm
import geopandas as gp
import pandas as pd
import numpy as np
import math as m
import json

def plotly_map_traces(filename: str) -> list:
    """
    This function reads a geojson file and returns a list of polygon and marker coordinates.

    Parameters:
    filename (str) : The name of the geojson file (without '.geojson' extension).
    
    Returns:
    list : A list of polygon and marker coordinates.
    """
    # data
    polygons = []
    markers = []
    with open(f"assets/{filename}.geojson", "r") as data:
        data = json.loads(data.read())
        features = data["features"]
    # getting polygon and marker coordinates
    for feature in features:
        _type = feature["geometry"]["type"]
        if "Point" in _type:
            coordinates = feature["geometry"]["coordinates"]
            markers.append([coordinates[0], coordinates[1]])

        if "Polygon" in _type:
            coordinates_list = feature["geometry"]["coordinates"]
            for coordinates in coordinates_list:
                try:
                    lat = [coors[0] for coors in coordinates[0]]
                    lon = [coors[1] for coors in coordinates[0]]
                except:
                    lat = [coors[0] for coors in coordinates]
                    lon = [coors[1] for coors in coordinates]
                polygons.append([lat, lon])
    return [polygons, markers]

def floorplan2layer(geojson_style) -> list:
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
            id=f"{fp}_eval")
        layers.append(dl.Overlay(geojson, name=fp, checked=show[i]))
        i += 1

    return layers

def interpolation(gt: list, trajectories: list) -> list:
    """
    Interpolates the ground truth and trajectories to match the same time stamps and store the result as 2D arrays.

    Parameters:
    gt (ndarray) : 2D array containing ground truth data with timestamps as the first column, x-coordinate as the second
                   column, and y-coordinate as the third column.
    trajectories (list) : List of 2D arrays containing trajectory data with timestamps as the first column, x-coordinate as
                          the second column, and y-coordinate as the third column.

    Returns:
    list : List of 2D arrays containing the interpolated ground truth and trajectory data. Each sublist contains two arrays
           with first array being the interpolated ground truth and second array being the interpolated trajectory.
    """
    # data
    data = []
    t_gt  = gt[:,0]
    x_gt  = gt[:,1]
    y_gt  = gt[:,2]
    # interpolation for each trajectory
    for traj in trajectories:
        t_traj = traj[:,0]
        x_traj = traj[:,1]
        y_traj = traj[:,2]
        # finding limits for new time stamps T*
        minimum = min(gt[0][0], traj[0][0])
        maximum = max(gt[-1][0], traj[-1][0])
        # creating new time stamps T*
        T_new = np.arange(minimum, maximum, 500)
        # interpolation
        ip_x_gt  = np.interp(T_new, t_gt, x_gt)
        ip_y_gt  = np.interp(T_new, t_gt, y_gt)
        ip_x_traj = np.interp(T_new, t_traj, x_traj)
        ip_y_traj = np.interp(T_new, t_traj, y_traj)
        # storing
        data.append([np.column_stack((ip_x_gt, ip_y_gt)), np.column_stack((ip_x_traj, ip_y_traj))])
    return data

def normCDF(gt: list, traj: list) -> list:
    """
    This function calculates the normal cumulative distribution function (CDF)
    of the errors between ground truth (gt) and trajectory (traj).
    
    Parameters:
    gt (list) : Ground truth data with x and y coordinates.
    traj (list) : Trajectory data with x and y coordinates.
    
    Returns:
    xy (list) : A 2D array with columns for error and cdf values, sorted by error values.
    
    """
    # data
    gt_x = gt[:,0]
    gt_y = gt[:,1]
    traj_x = traj[:,0]
    traj_y =traj[:,1]
    # calculating errors (= distances)
    err = [np.sqrt((traj_x[i]-gt_x[i])**2 + (traj_y[i]-gt_y[i])**2) for i in range(gt_x.shape[0])]
    # getting cdf
    E = sum(err)/len(err)
    s = np.sqrt(sum([(erri-E)**2 for erri in err])/(len(err)-1))
    cdf = norm.cdf(err, E, s)
    # stack x and y
    xy = np.column_stack((err, cdf))
    # sort it
    xy = xy[xy[:, 0].argsort()]
    return xy

def histoCDF(gt: "ndarray", traj: "ndarray") -> "ndarray":
    """
    This function calculates the histogram cumulative distribution function (CDF)
    of the error between the ground truth and a given trajectory.
    
    Parameters:
    gt (ndarray) : A list containing the ground truth values, where each value is represented as a tuple of x and y coordinates.
    traj (ndarray) : A list containing the values of the trajectory, where each value is represented as a tuple of x and y coordinates.
    
    Returns:
    ndarray : A list containing the CDF of the error between the ground truth and the given trajectory, represented as tuples of bin edges and cumulative probability.
    
    """
    # # data
    gt_x = gt[:,0]
    gt_y = gt[:,1]
    traj_x = traj[:,0]
    traj_y =traj[:,1]
    # calculating errors (= distances)
    err = [np.sqrt((traj_x[i]-gt_x[i])**2 + (traj_y[i]-gt_y[i])**2) for i in range(gt_x.shape[0])]
    # getting cdf
    dens_y, dens_bins = np.histogram(err, density=True, bins = 100)
    bin_width = dens_bins[1] - dens_bins[0]
    cdf = np.cumsum(dens_y * bin_width)
    return np.column_stack((dens_bins[1:], cdf))

def dataframe4graph(data: "ndarray", name: str) -> "DataFrame":
    """
    Transform input data into a pandas DataFrame format for plotting.

    Parameters:
    data (ndarray) : The input data, a two-dimensional array where each row represents
                     the error and cumulative density function values.
    name (str) : The name of the input data.

    Returns:
    data_fram (DataFrame) : The transformed data in pandas DataFrame format. The data contains three columns: "trajectory", 
                            "RMSE [m]", and "CDF". The "trajectory" column is the name of the input data, "RMSE [m]" is the error 
                            values, and "CDF" is the cumulative density function values.
    """
    err = data[:,0]
    cdf = data[:,1]
    n = int(m.log(cdf.shape[0]/15000, 2))
    for i in range(n):
        err = np.delete(err, np.arange(1, err.shape[0], 2))
        cdf = np.delete(cdf, np.arange(1, cdf.shape[0], 2))
    name = [name for _ in range(err.shape[0])]
    data_frame = pd.DataFrame(np.column_stack((name, np.column_stack((err, cdf)))), columns=["trajectory", "RMSE [m]", "CDF"])
    data_frame["RMSE [m]"] = data_frame["RMSE [m]"].astype(float, errors = "raise")
    data_frame["CDF"] = data_frame["CDF"].astype(float, errors = "raise")
    return data_frame

def percentage(plan: "GeoDataFrame", gt: "GeoDataFrame", traj: "GeoDataFrame") -> float:
    """
    Calculates the percentage of trajectory points that are in the same polygon
    as their corresponding ground truth points.
    
    Parameters:
    plan (GeoDataFrame) : The map to compare the points against.
    gt (GeoDataFrame) : The ground truth data, represented as a GeoDataFrame with 'latitude' and 'longitude' columns.
    traj (GeoDataFrame) : The trajectory data, represented as a GeoDataFrame with 'latitude' and 'longitude' columns.
    
    Returns:
    perc (float): The percentage of similarity between the ground truth and trajectory points in relation to the map.
    """
    # getting polygons out of map
    polygons = plan["geometry"]
    # ground truth points (converted)
    gt = {"geometry": [sh.Point(lat, lon) for lat, lon in gt]}
    gt = gp.GeoDataFrame(gt, crs=32632).to_crs(4326)
    # trajectory points (converted)
    traj = {"geometry": [sh.Point(lat, lon) for lat, lon in traj]}
    traj = gp.GeoDataFrame(traj, crs=32632).to_crs(4326)
    # True/False of each point in each polygon
    gt_within = gt.assign(**{str(key): gt.within(geom) for key, geom in polygons.items()})
    traj_within = traj.assign(**{str(key): traj.within(geom) for key, geom in polygons.items()})
    # amount of points in each polygon
    gt_amount = np.array([list(gt_within[str(i)]).count(True) for i in range(len(polygons))])
    traj_amount = np.array([list(traj_within[str(i)]).count(True) for i in range(len(polygons))])
    # percentage
    perc = 1 - sum(abs(gt_amount - traj_amount))/traj_amount.shape[0]
    return perc

def csv2geojson(coordinates: list) -> dict:
    """
    This function takes in a list of coordinates in the form of [(lat1, lon1), (lat2, lon2), ..., (latn, lonn)].
    The function converts the coordinates to a GeoJSON representation, which is a geographic data format
    commonly used for encoding a variety of geographic data structures, including points, lines, and polygons.
    
    Parameters:
    coordinates (list): A list of coordinates in the form of [(lat1, lon1), (lat2, lon2), ..., (latn, lonn)].

    Returns:
    geojson (dict): A GeoJSON representation of the input coordinates in the form of a dictionary.
    """
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
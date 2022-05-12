##### Utils Evaluator
###IMPORTS
# built in
import shapely.geometry as sh
from scipy.stats import norm
import geopandas as gp
import pandas as pd
import numpy as np
import math as m

def interpolation(gt: "ndarray", trajectories: list) -> list:
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

def cdf(gt: "ndarray", traj: "ndarray") -> "ndarray":
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
    return np.column_stack((err, cdf))

def dataframe4graph(data: "ndarray", name: str) -> "DataFrame":
    err = data[:,0]
    cdf = data[:,1]
    n = int(m.log(cdf.shape[0]/15000, 2))
    for i in range(n):
        err = np.delete(err, np.arange(1, err.shape[0], 2))
        cdf = np.delete(cdf, np.arange(1, cdf.shape[0], 2))
    name = [name for _ in range(err.shape[0])]
    data_frame = pd.DataFrame(np.column_stack((name, np.column_stack((err, cdf)))), columns=["trajectory", "err", "cdf"])
    data_frame["err"] = data_frame["err"].astype(float, errors = "raise")
    data_frame["cdf"] = data_frame["cdf"].astype(float, errors = "raise")
    return data_frame

def percentage(plan: "GeoDataFrame", gt: "GeoDataFrame", traj: "GeoDataFrame") -> float:
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


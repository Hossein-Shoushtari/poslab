import geopandas as gp
import numpy as np
from shapely.geometry import Point
import test as t
import shapely.geometry as sh

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
    perc = sum(abs(gt_amount - traj_amount))/gt.shape[0]
    return perc


# data
floorplan = gp.read_file("assets/floorplans/4OG.geojson")
gt = np.loadtxt("gt.csv", delimiter=";", skiprows=1)
traj = np.loadtxt("PDR.csv", delimiter=";")
# interpolation
gt_ip, traj_ip = t.interpolation(gt, traj)
# percentage
perc = percentage(floorplan, gt_ip, traj_ip)

print(perc)

import utils as u
import geopandas as gp
import shapely.geometry as sh

def boundaries(lon_raw: list, lat_raw: list) -> list:
    # making shapely points out of given coordinates
    df = gp.GeoDataFrame({"geometry": [sh.Point(lon, lat) for lon, lat in zip(lon_raw, lat_raw)]})
    # getting edge points (boundaries)
    minx, miny, maxx, maxy = df.geometry.total_bounds
    # returning most southwestern and most northeastern point
    bounds = [[miny, minx], [maxy, maxx]]
    return bounds



with open(f"assets/floorplans/4OG.geojson", "r") as file:
    data = file.read()
lon, lat = u.extract_coordinates(gp.read_file(data))
bounds = boundaries(lon, lat)
print(bounds)


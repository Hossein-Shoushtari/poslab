import json
import numpy as np

with open("assets/maps/4OG.geojson") as json_file:
    data = json.load(json_file)

# array = [np.array(data["features"][i]["geometry"]["coordinates"])[0][:, 0] for i in range(len(data["features"]))]
# print(array)
# np.array(data["features"][0]["geometry"]["coordinates"])[0][:, 0]
lons = []
lats = []
for i in range(len(data["features"])):
    lon = np.array(data["features"][i]["geometry"]["coordinates"][0])[:, 0]
    lat = np.array(data["features"][i]["geometry"]["coordinates"][0])[:, 1]
    lons += list(lon)
    lats += list(lat)

# print(lats)

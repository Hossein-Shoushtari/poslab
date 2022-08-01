import json

def plotly_map_traces(filename: str) -> list:
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


result = plotly_map_traces("maps/test")

print(result)
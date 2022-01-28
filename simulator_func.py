from os import listdir
from dash import html
import dash_leaflet as dl
from dash_extensions.javascript import arrow_function
from geopandas import GeoDataFrame, read_file
from base64 import b64decode
from json import loads
import numpy as np
import csv
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import*

def _map():
    """
    - adds all converted layers to map
    - returns list of all overlays
    """
    # Tile Layer
    url = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
    # Map info
    attribution = "&copy; <a href='https://stadiamaps.com/'>Stadia Maps</a> "
    # HCU coordinates
    hcu = (53.540252, 10.004814073621176)
    # initializing list of all layers. first item is BaseLayer
    layers = [dl.BaseLayer(dl.TileLayer(url=url, attribution=attribution), name="base", checked=True)]
    # parsing through all converted layers and adding them to <<layers>>
    for geojson_file in listdir("assets/floorplans"):
        name = geojson_file.split(".")[0]  # getting name of geojson file
        geojson = dl.GeoJSON(
            url=f"assets/floorplans/{geojson_file}",  # url to geojson file
            #options=dict(style=geojson_style),  # style each polygon
            hoverStyle=arrow_function(dict(weight=1, color='orange')),  # style applied on hover
            hideout=dict(style={"weight": 0.2, "color": "#DAF7A6"}, classes=[], colorscale=[], colorProp=""))
        layers.append(dl.Overlay(geojson, name=name, checked=False))
    return html.Div([dl.Map(
            [
                dl.LayersControl(layers)
            ],
            zoom=18,
            center=hcu,
            style={'width': '100%', 'height': '70vh', 'margin': "auto", "display": "block"})
        ])

def upload_decoder(content: str) -> str:
    """
    - decodes uploaded base64 file to originally uploaded file
    - returns decoded file
    """
    # decoding base64 to geojson
    encoded_content = content.split(",")[1]
    decoded_content = b64decode(encoded_content).decode("latin-1")  # should be a geojson like string
    return decoded_content

def crs32632_converter(filename: str, decoded_content: str) -> None:
    """
    - converts an EPSG: 32632 geojson file to WGS84
    - saves converted file
    """
    # converting crs (UTM -> EPSG: 32632) of given floorplan to WGS84 (EPSG: 4326)
    layer = GeoDataFrame(read_file(decoded_content), crs=32632).to_crs(4326)
    # saving converted layer
    layer.to_file(f"assets/floorplans/{filename}", driver="GeoJSON")



def closest_value(input_list, input_value):
    """
        return the closest value to a given input value from a list of given values

        Parameters
        ----------
        input_list : list of values - list of floats
        input_value : value for which the closest value is determined - float

        Returns
        -------
        arr[i] : closest value from the list to the given value - float
        """
    arr = np.asarray(input_list)

    i = (np.abs(arr - input_value)).argmin()

    return arr[i]


def simulate_positions(filename, error, freq):
    """
        creating sample data points for 5G measurements with chosen frequency and position error

        Parameters
        ----------
        filename : name of csv file containing groundtrouth data points - string
        error : desired error for 5G positions (as std) - float
        freq : frequency of 5G measurements in (number of measurements/second)  - float

        Returns
        -------
        positions : simulated positions from 5G measurements - array of arrays (tuples) of floats
        time_stamps : timestamps of 5G measurements - array of floats
        error_list : list of the error for each measurement - list of floats
        qualities_list : list of the quality value for each measurement - list of floats
        """
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        rows = []
        positions = []
        time_stamps = []
        freq = freq / 1000
        error_list = []
        for row in reader:
            rows.append([float(row[0].split(' ')[0]), float(row[0].split(' ')[1]), float(row[0].split(' ')[2])])

        for r in range(len(rows)):
            time_stamps.append(rows[r][0])
            x_error = np.random.normal(0, error)
            y_error = np.random.normal(0, error)
            error_list.append(np.sqrt(x_error ** 2 + y_error ** 2))
            positions.append([rows[r][1] + x_error, rows[r][2] + y_error])

            dt = 1 / freq
            t1 = rows[r][0]
            t2 = rows[r][0] + dt

            if r <= len(rows) - 2:
                dx = ((rows[r + 1][1] - rows[r][1]) / (rows[r + 1][0] - rows[r][0])) * dt
                dy = ((rows[r + 1][2] - rows[r][2]) / (rows[r + 1][0] - rows[r][0])) * dt
                # dz = ((rows[r-1][3] - rows[r][3])/(rows[r-1][0] - rows[r][0]))*dt

                x_temp = rows[r][1] + dx
                y_temp = rows[r][2] + dy
                # z_temp = rows[r][3] + dz

            while t2 < rows[-1][0] and t2 < rows[r + 1][0]:
                time_stamps.append(t2)
                x_error = np.random.normal(0, error)
                y_error = np.random.normal(0, error)
                error_list.append(np.sqrt(x_error ** 2 + y_error ** 2))
                positions.append([x_temp + dx + x_error,
                                  y_temp + dy + y_error])

                t2 = t2 + dt
                x_temp = x_temp + dx
                y_temp = y_temp + dy
        qualities_list = []
        # assigning the real error to the closest quality value (defined error/5). Might be more useful to
        # assign the error to the intervall between two qualities or the next hiegher quality value
        for e in error_list:
            intervalls = [error / 5, 2 * error / 5, 3 * error / 5, 4 * error / 5, 5 * error / 5]
            quality = closest_value(intervalls, e)
            qualities_list.append(quality)

        return positions, time_stamps, error_list, qualities_list

if __name__ == "__main__":
    """
            check if the simulate_positions function is working
            """

    filename = 'assets/waypoints/GroundTruthZero2Four.csv'
    error = 2
    freq = 1
    positions, time_stamps, errors, qualities = simulate_positions(filename, error, freq)
    print('qualities',qualities)
    print('errors', errors)

    points_positions = []
    for p in positions:
        points_positions.append(Point(p))

    print(points_positions)
    gpd.GeoSeries(points_positions).plot(figsize=(10, 10), color='red', markersize=100, label='5G positions')
    plt.pause(60)
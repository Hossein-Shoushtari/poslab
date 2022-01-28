from os import listdir
from dash import html
from geopandas import GeoDataFrame, read_file
from folium import GeoJson, LayerControl, GeoJsonTooltip
from base64 import b64decode
from maps import _map
from math import atan2, pi, sqrt
from json import loads
import numpy as np
import csv
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import*

def get_map() -> 'html.Iframe':
    '''
    - adds all converted layers to map
        -> first initializing map | no layers on map
        -> then parsing through all geojson files
        -> simultaneously adding layers to map
    - adds LayerControl
    - saves base_map as 'map.html'
    - returns map as html.Iframe 
    '''
    base_map = _map() # (re)creating blank base_map
    # adding all converted layers to map
    for geojson_file in listdir('assets/floorplans'):
        # tooltips only where further information is available
        props_dict: dict = loads(open(f'assets/floorplans/{geojson_file}').read())['features'][0]['properties']
        properties: list = [key for key in props_dict.keys()]
        if properties == []: tooltips = 'no info'
        else: tooltips = GeoJsonTooltip(fields=properties)
        # adding everything to base map
        name = geojson_file.split('.')[0]
        GeoJson(
            f'assets/floorplans/{geojson_file}',
            name=name,
            tooltip=tooltips,
            style_function=lambda x: {'weight': 0.5,'color': 'blue'},
            highlight_function=lambda x: {'weight': 1,'color': 'orange'},
            show=False
        ).add_to(base_map)
        
    # saving map as an html file with LayerControl
    LayerControl().add_to(base_map)
    base_map.save('map.html')
    return html.Iframe(
            srcDoc=open('map.html').read(),
            style=
            {
                'width': '100%',
                'height': '60vh'
            }
    )

def upload_decoder(content: str) -> str:
    '''
    - decodes uploaded base64 file to originally uploaded file
    - returns decoded file
    '''
    # decoding base64 to geojson
    encoded_content = content.split(',')[1]
    decoded_content = b64decode(encoded_content).decode('latin-1')  # should be a geojson like string
    return decoded_content

def crs32632_converter(filename: str, decoded_content: str) -> None:
    '''
    - converts an EPSG: 32632 geojson file to WGS84
    - saves converted file
    '''
    # converting crs (UTM -> EPSG: 32632) of given floorplan to WGS84 (EPSG: 4326)
    layer = GeoDataFrame(read_file(decoded_content), crs=32632).to_crs(4326)
    # saving converted layer
    layer.to_file(f'assets/floorplans/{filename}', driver='GeoJSON')


def distance(ax: float, ay: float, bx: float, by: float) -> float:
    '''
    - calculates Distance between two points
    '''
    return sqrt((bx-ax)**2 + (by-ay)**2)

def azimuth(ax: float, ay: float, bx: float, by: float) -> float:
    '''
    - calculates Azimuth between two points
    - exception : two points are identical -> False
    '''
    delta_x = bx-ax
    delta_y = by-ay
    if delta_x == 0 and delta_y == 0:
        return False
    elif delta_x < 0 and delta_y < 0 or delta_x == 0 and delta_y < 0 or delta_x > 0 and delta_y < 0:
        return atan2((delta_y), (delta_x)) + 2*pi
    else:
        return atan2((delta_y), (delta_x))

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
        """
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        rows = []
        positions = []
        time_stamps = []
        freq = freq / 1000
        for row in reader:
            rows.append([float(row[0].split(' ')[0]), float(row[0].split(' ')[1]), float(row[0].split(' ')[2])])

        for r in range(len(rows)):
            time_stamps.append(rows[r][0])
            x_error = np.random.normal(0, error)
            y_error = np.random.normal(0, error)
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
                positions.append([x_temp + dx + np.random.uniform(-error, error, 1)[0],
                                  y_temp + dy + np.random.uniform(-error, error, 1)[0]])

                t2 = t2 + dt
                x_temp = x_temp + dx
                y_temp = y_temp + dy

        return positions, time_stamps

if __name__ == "__main__":
    """
            check if the simulate_positions function is working
            """

    filename = 'assets/waypoints/GroundTruthZero2Four.csv'
    error = 2
    freq = 1
    positions, time_stamps = simulate_positions(filename, error, freq)

    points_positions = []
    for p in positions:
        points_positions.append(Point(p))

    print(points_positions)
    gpd.GeoSeries(points_positions).plot(figsize=(10, 10), color='red', markersize=100, label='5G positions')
    plt.pause(60)
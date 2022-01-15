from os import listdir
from dash import html
from geopandas import GeoDataFrame, read_file
from folium import GeoJson, LayerControl, GeoJsonTooltip
from base64 import b64decode
from maps import _map
from math import atan2, pi, sqrt
from json import loads

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
        if loads(open(f'assets/floorplans/{geojson_file}').read())['features'][0]['properties'] == {}: tooltips = 'no info'
        else:  tooltips = GeoJsonTooltip(fields=['usage', 'spaceID'])
        # adding everything to base map
        name = geojson_file.split('.')[0]
        GeoJson(
            f'assets/floorplans/{geojson_file}',
            name=name,
            #tooltip=tooltips,
            #style_function=lambda x: {'weight': 0.5,'color': 'blue'},
            #highlight_function=lambda x: {'weight': 1,'color': 'orange'},
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
                'height': '80vh'
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

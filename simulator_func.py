from os import listdir
from dash import html
from geopandas import GeoDataFrame, read_file
from folium import GeoJson, LayerControl
from base64 import b64decode
from maps import _map

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
    for geojson_file in listdir('assets/floorplans_converted'):
        # adding it to base map
        name = geojson_file.split('.')[0]
        GeoJson(f'assets/floorplans_converted/{geojson_file}', name=name, show=False).add_to(base_map)
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

def geojson_decoder(content: str) -> str:
    '''
    - converts base64 file to geojson
    - returns decoded geojson file
    '''
    # decoding base64 to geojson
    encoded_content = content.split(',')[1]
    decoded_content = b64decode(encoded_content).decode('latin-1')  # should be a geojson like string
    return decoded_content

def crs32632_converter(filename: str, decoded_content: str) -> None:
    '''
    - converts decoded every geojson fileto WGS84
    - saves converted file
    '''
    # converting crs (UTM -> EPSG: 32632) of given floorplan to WGS84 (EPSG: 4326) ...y
    layer = GeoDataFrame(read_file(decoded_content), crs=32632).to_crs(4326)
    # saving converted layer
    layer.to_file(f'assets/floorplans_converted/{filename}', driver='GeoJSON')




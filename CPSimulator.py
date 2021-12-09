import os
from base64 import b64decode
from dash import html, dcc, Dash, Output, Input, State, no_update
from folium import Map, GeoJson, LayerControl, TileLayer
from folium.plugins import Fullscreen, MiniMap, MeasureControl, Draw
from geopandas import GeoDataFrame, read_file
from datetime import datetime

def map():
    # creating a base map and get an hcu-centered view using folium
    hcu_coordinates = (53.540355074570655, 10.004814073621176)
    base_map = Map(location=hcu_coordinates, tiles='OpenStreetMap', zoom_start=19, max_zoom=19, control_scale=True)

    # adding new TileLayers
    TileLayer('Stamen Toner').add_to(base_map)

    # plugin for mini map
    minimap = MiniMap(toggle_display=True)
    # add minimap to map
    base_map.add_child(minimap)

    # add full screen button to map
    Fullscreen(position='topleft').add_to(base_map)

    # measure control
    measure_control = MeasureControl(position='topleft',
                                     active_color='red',
                                     completed_color='red',
                                     primary_length_unit='meters')
    # add measure control to map
    base_map.add_child(measure_control)

    # draw tools
    # export=True exports the drawn shapes as a geojson file
    draw = Draw(export=True,
                filename=f'{datetime.now()}.geojson',
                position='topleft',
                draw_options={'polyline': {'allowIntersection': False}},
                edit_options={'poly': {'allowIntersection': False}})
    # add draw tools to map
    draw.add_to(base_map)
    return base_map

# LAYERS!
def converting(geojson_file: str) -> None:
    '''
    :param geojson_file: str
    :return: None
    file should be located in the floorplans_32632 directory
    '''
    # converting the crs (UTM -> EPSG: 32632) of the given floorplan to WGS84 (EPSG: 4326) ...
    layer = GeoDataFrame(read_file(f'floorplans_32632/{geojson_file}'), crs=32632).to_crs(4326)
    # saving converted layer
    layer.to_file(f'floorplans_4326/{geojson_file}', driver='GeoJSON')

def layer() -> None:
    # recreating the base_map
    base_map = map()
    # adding all converted layers to the map
    for geojson_file in os.listdir('floorplans_4326'):
        # adding it to the base map
        name = geojson_file.split('.')[0]
        GeoJson(f'floorplans_4326/{geojson_file}', name=name, show=False).add_to(base_map)
    # saving the map as an html file with LayerControl
    LayerControl().add_to(base_map)
    base_map.save('index.html')

# making layers out of existing data
for geojson_file in os.listdir('floorplans_32632'):
    if geojson_file not in os.listdir('floorplans_4326'): # assuming there is no converted version of this GeoJSON file
        converting(geojson_file) # making a layer
# adding all layers to the map incl. LayerControl panel
layer()

# in case of an empty floorplans_4326 directory, a layerless map should be created
if len(os.listdir('floorplans_4326')) == 0: map()


# ----------------------------------------------------------------------------------

# designing the webpage using dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'CP Simulator'

# pushing it to the web
app.layout = html.Div([
                dcc.ConfirmDialog(
                    id='data-warning',
                    message='Warning! Please only upload geojson files!',
                ),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select',
                               style={
                                   'color': 'red'
                               }),
                        ' a GeoJSON file.'
                    ]),
                    style={
                        'width': '100%',
                        'height': '100%',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'marginTop': '10px',
                        'marginBottom': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                # for the map
                html.Div(id='map')
            ])

# updating map with uploaded Layer
def update_layer(content, filename):
    # decoding binary file to a string
    content_type, content_string = content.split(',')
    decoded = b64decode(content_string).decode('latin-1')  # should be a geojson like string
    # saving it
    with open(f'floorplans_32632/{filename}', 'w') as geojson_file:
        geojson_file.write(decoded)
    # converting it
    converting(filename)
    # uploading the layers
    layer()
    # returning a the new map with the refreshed LayerControl
    return html.Iframe(srcDoc=open('index.html').read(),
                       style={
                           'width': '100%',
                           'height': '600px'
                       })

# handling upload
@app.callback(
    Output('data-warning', 'displayed'),
    Output('map', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def upload(list_of_contents, list_of_filenames):
    if list_of_filenames is not None:  # assuming something was uploaded
        for file in range(len(list_of_filenames)):
            filename = list_of_filenames[file]
            content = list_of_contents[file]
            if 'geojson' in filename:  # assuming user uploaded a GeoJSON file
                children = update_layer(content, filename)
                # returning the new Iframe
                return no_update, children
            else:
                # returning True for warning reasons
                return True, no_update
    else:
        # this else-section is always activated, when the page refreshes
        # returning the current Iframe
        return no_update, html.Iframe(srcDoc=open('index.html').read(),
                                      style={
                                          'width': '100%',
                                          'height': '600px'
                                      })



# pushing the map to the web
if __name__ == '__main__':
    app.run_server(debug=True)

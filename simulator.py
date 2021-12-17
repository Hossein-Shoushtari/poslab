import os
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
from geopandas import GeoDataFrame, read_file
from folium import GeoJson, LayerControl
from base64 import b64decode
from maps import _map

def simulator_card():
    ### MAP
    # map is initialized in GeoJSON() below
    ### MODAL
    modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("WARNING")),
            dbc.ModalBody("Wrong file was uploaded!")
        ],
        id="sim_modal",
        is_open=False
    )
    ### BUTTONS
    button_style = {
        'marginTop': '10px',
        'marginBottom': '10px'
    }
    buttons = html.Div(
        [
            dcc.Upload(
                id='upload_geojson',
                children=html.Div(dbc.Button("GeoJSON", color="info", outline=True), className="d-grid gap-2 col-6 mx-auto"),
                style=button_style
            ),
            dcc.Upload(
                id='upload_txt',
                children=html.Div(dbc.Button("TXT", color="info", outline=True), className="d-grid gap-2 col-6 mx-auto" ),
                style=button_style
            ),
            dcc.Upload(
                id='upload_csv',
                children=html.Div(dbc.Button("CSV", color="info", outline=True), className="d-grid gap-2 col-6 mx-auto"),
                style=button_style
            )
        ]
    )
    # left column
    hr_style = {
        'width': '80%',
        'margin': 'auto',
        'marginBottom': '2.5vh'
    }
    div_style = {
        'border':'1px solid',
        'border-radius': 10,
        'color': 'silver'
    }
    left_column = html.Div(
        [
            html.Div(
                [
                    html.H5('Uploads', style={'textAlign': 'center', 'color': 'grey', 'paddingTop': '3vh'}),
                    html.Hr(style=hr_style),
                    buttons
                ],
                style=div_style
            ),
            html.Br(),
            html.Div(
                [
                    html.H5('Simulation', style={'textAlign': 'center', 'color': 'grey', 'paddingTop': '3vh'}),
                    html.Hr(style=hr_style),
                    html.Div(
                        dbc.Button("Simulate", color="success", outline=True),
                        className="d-grid gap-2 col-6 mx-auto",
                        style=button_style
                    )
                ],
                style=div_style
            )
        ]
    )
    ### returning filled Card
    return dbc.Card(
        dbc.CardBody(
            [
                # simulator modal
                modal,
                # card content
                html.P("SIMULATOR", className="card-text"),
                dbc.Row(
                    [
                        dbc.Col(left_column, width=2),
                        dbc.Col(html.Div(id='map'))
                    ]
                )
            ]
        ),
        className='mt-3'
    )

class GeoJSON:
    def __init__(self, content = None, filename = None):
        self.__content = content
        self.__filename = filename

    def convert_to_crs32632(self, filename: str) -> None:
        '''
        - converts decoded geojson file (EPSG:32632) to WGS84
        - saves converted file
        '''
        # converting the crs (UTM -> EPSG: 32632) of the given floorplan to WGS84 (EPSG: 4326) ...
        layer = GeoDataFrame(read_file(f'assets/floorplans_raw/{filename}'), crs=32632).to_crs(4326)
        # saving converted layer
        layer.to_file(f'assets/floorplans_converted/{filename}', driver='GeoJSON')

    def add_layer(self) -> None:
        '''
        - adds new created layer to map
           -> first initializing map again | no layers on map
           -> then parsing through all geojson files in the converted directory
           -> simultaneously adding layers to map incl. new one
        - adds LayerControl
        - saves the base_map as 'index.html'
        '''
        base_map = _map() # recreating the base_map
        # adding all converted layers to the map
        for geojson_file in os.listdir('assets/floorplans_converted'):
            # adding it to the base map
            name = geojson_file.split('.')[0]
            GeoJson(f'assets/floorplans_converted/{geojson_file}', name=name, show=False).add_to(base_map)
        # saving the map as an html file with LayerControl
        LayerControl().add_to(base_map)
        base_map.save('index.html')

    def upload(self):
        '''
        - GeoJSON() needs to be initilized with both parameters:
                content  &  filename !!
        - displays an uploaded file on the map
        - returns either a refreshed map with uploaded file
          as an html.Iframe or 'None' because of a wrong file
          format of uploaded file
        '''
        if 'geojson' in self.__filename:  # assuming user uploaded a GeoJSON file
            # decoding uploaded base64 file and saving it in floorplans_raw
            self.__convert_to_geojson(self.__content, self.__filename)
            # converting EPSG:32632 to WGS84 and saving it in floorplans_converted
            self.convert_to_crs32632(self.__filename)
            # adding new layer to the layer control
            self.add_layer()
            # returning an html.Iframe with the refreshed map
            return self.__map_Iframe()
        else:
            return None  # wrong file format was uploaded

    def __convert_to_geojson(self, uploaded_content: str, uploaded_filename: str) -> None:
        '''
        - converts uploaded base64 file to geojson
        - saves decoded geojson file (EPSG:32632)
        '''
        # decoding base64 to geojson
        content_type, content_string = uploaded_content.split(',')
        decoded = b64decode(content_string).decode('latin-1')  # should be a geojson like string
        # saving it
        with open(f'assets/floorplans_raw/{uploaded_filename}', 'w') as geojson_file:
            geojson_file.write(decoded)

    def __map_Iframe(self) -> str:
        '''
        returns created/updated map as an html.Iframe
        '''
        return html.Iframe(
            srcDoc=open('index.html').read(),
            style=
            {
                'width': '100%',
                'height': '80vh'
            }
        )


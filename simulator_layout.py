import os
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
from geopandas import GeoDataFrame, read_file
from folium import GeoJson, LayerControl
from base64 import b64decode
from maps import _map

def simulator_card():
    ### MAP
    # map is initialized in main.py
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
    # tooltips for more information
    tooltips = html.Div([
        dbc.Tooltip(
            "maps --- geoJSON | displayed as layer on map",
            target="ul_map",
            placement='top'),
        dbc.Tooltip(
            "waypoints --- txt or csv",
            target="ul_way",
            placement='bottom'),
        dbc.Tooltip(
            "gyroscope",
            target="ul_gyr",
            placement='top'),
        dbc.Tooltip(
            "acceleration",
            target="ul_acc",
            placement='bottom'),
        dbc.Tooltip(
            "barometer",
            target="ul_bar",
            placement='top'),
        dbc.Tooltip(
            "magnetometer",
            target="ul_mag",
            placement='bottom')
    ])
    # maps and waypoints
    buttons1 = html.Div([
        dcc.Upload(
            id='ul_map',
            children=html.Div(dbc.Button("Maps", color="info", outline=True), className="d-grid gap-2 col-8 mx-auto"),
            style={'marginTop': '1vh', 'marginBottom': '1vh'},
            multiple=True),
        dcc.Upload(
            id='ul_way',
            children=html.Div(dbc.Button("Waypoints", color="info", outline=True), className="d-grid gap-2 col-8 mx-auto" ),
            style={'marginBottom': '1.5vh'},
            multiple=True)
    ])
    # gyroscope, acceleration, barometer and magnetometer
    buttons2 = html.Div(dbc.Row([
        dbc.Col(html.Div([
            dcc.Upload(
                id='ul_gyr',
                children=html.Div(dbc.Button("G", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginLeft': 'auto'}),
                multiple=True,
                style={'marginBottom': '0.7vh'}),
            dcc.Upload(
                id='ul_acc',
                children=html.Div(dbc.Button("A", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginLeft': 'auto'}),
                multiple=True)
        ])),
        dbc.Col(html.Div([
            dcc.Upload(
                id='ul_bar',
                children=html.Div(dbc.Button("B", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginRight': 'auto'}),
                multiple=True,
                style={'marginBottom': '0.7vh'}),
            dcc.Upload(
                id='ul_mag',
                children=html.Div(dbc.Button("M", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginRight': 'auto'}),
                multiple=True)
        ]))],
        className="row g-0"
        ),
        style={'marginBottom': '1vh'}
    )

    # simulation
    buttons3 = html.Div([
        html.Div(
            dbc.Button("Calculate ground truth", id='calc', color="success", outline=True),
            className="d-grid gap-2 col-8 mx-auto",
            style={'marginTop': '1vh', 'marginBottom': '1vh'}),
        html.Div(
            dbc.Button("Simulate measurement", id='sim', color="success", outline=True),
            className="d-grid gap-2 col-8 mx-auto",
            style={'marginTop': '1vh', 'marginBottom': '1vh'})            
    ])

    ## putting all together | left column
    hr_style = {
        'width': '80%',
        'margin': 'auto',
        'marginBottom': '1.5vh'}
    div_style = {
        'border':'1px solid',
        'border-radius': 10,
        'color': 'silver'}
    H5_style = {
        'textAlign': 'center',
        'color': 'grey',
        'paddingTop': '1vh' }
    left_column = html.Div(
        [
            # TOOLTIPS
            tooltips,
            # UPLOAD
            html.Div(
                [
                    html.H5('Upload', style=H5_style),
                    html.Hr(style=hr_style),
                    buttons1,
                    html.Hr(style={'width': '30%', 'margin': 'auto', 'marginBottom': '1.5vh'}),
                    buttons2
                ],
                style=div_style
            ),
            html.Br(),
            # SIMULATION
            html.Div(
                [
                    html.H5('Simulation', style=H5_style),
                    html.Hr(style=hr_style),
                    buttons3
                ],
                style=div_style
            ),
            html.Br(),
            # EXPORT
            html.Div(
                [
                    html.H5('Export', style=H5_style),
                    html.Hr(style=hr_style),
                    html.Div(
                        dbc.Button("Get results", id='exp', color="warning", outline=True),
                        className="d-grid gap-2 col-8 mx-auto",
                        style={'marginTop': '1vh', 'marginBottom': '1vh'})
                ],
                style=div_style
            )
        ]
    )
    ### returning filled Card
    return dbc.Card(
        dbc.CardBody(
            [
                # simulator modal giving alert
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



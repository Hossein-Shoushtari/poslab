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

    ### UPLOAD
    # tooltips for more information
    ul_tt = html.Div([
        dbc.Tooltip(
            "geojson",
            target="ul_map",
            placement='right'),
        dbc.Tooltip(
            "txt, csv or geojson",
            target="ul_way",
            placement='right'),
        dbc.Tooltip(
            "txt, csv or geojson",
            target="ul_ant",
            placement='right'),
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
    ## Buttons
    # maps and waypoints
    buttons1 = html.Div([
        dcc.Upload(
            id='ul_map',
            children=html.Div(dbc.Button("Maps", color="info", outline=True), className="d-grid gap-2 col-8 mx-auto"),
            style={'marginTop': '1vh', 'marginBottom': '0.5vh'},
            multiple=True),
        dcc.Upload(
            id='ul_way',
            children=html.Div(dbc.Button("Waypoints", color="info", outline=True), className="d-grid gap-2 col-8 mx-auto" ),
            style={'marginTop': '0.5vh', 'marginBottom': '0.5vh'},
            multiple=True),
        dcc.Upload(
            id='ul_ant',
            children=html.Div(dbc.Button("Antennas", color="info", outline=True), className="d-grid gap-2 col-8 mx-auto" ),
            style={'marginBottom': '1.5vh'},
            multiple=True)
    ])
    # gyroscope, acceleration, barometer and magnetometer
    buttons2 = html.Div(dbc.Row([
        dbc.Col(html.Div([  # left column
            dcc.Upload(
                id='ul_gyr',
                children=html.Div(dbc.Button("G", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginLeft': 'auto'}),
                multiple=True,
                style={'marginBottom': '4px'}),
            dcc.Upload(
                id='ul_acc',
                children=html.Div(dbc.Button("A", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginLeft': 'auto'}),
                multiple=True)
        ])),
        dbc.Col(html.Div([  # right column
            dcc.Upload(
                id='ul_bar',
                children=html.Div(dbc.Button("B", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginRight': 'auto'}),
                multiple=True,
                style={'marginBottom': '4px'}),
            dcc.Upload(
                id='ul_mag',
                children=html.Div(dbc.Button("M", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginRight': 'auto'}),
                multiple=True)
        ]))],
        className="row g-0"
        ),
        style={'marginBottom': '1vh'}
    )

    ### SIMULATION
    # tooltips
    se_tt = html.Div([
        dbc.Tooltip(
            "quality",
            target="ti_coo",
            placement='top'),
        dbc.Tooltip(
            "quality",
            target="ti_dis",
            placement='bottom'),
        dbc.Tooltip(
            "quality",
            target="ti_ang",
            placement='top'),
        dbc.Tooltip(
            "error",
            target="ti_sym",
            placement='bottom')
    ])
    # styles
    input_style1 = {
        'color': 'silver',
        'backgroundColor': '222222',
        'border': '1px solid #917033'
    }
    input_style2 = {
        'color': 'silver',
        'backgroundColor': '222222',
        'border': '1px solid #966200'
    }
    label_style = {
        'color': 'silver',
        'font-size': '12px',
    }
    ## Entries
    text_input = html.Div([
        html.Div(dbc.Row([
            dbc.Col(html.Div([  # left column
                dbc.FormFloating([
                    dbc.Input(id='ti_coo', type='text', placeholder=0, style=input_style1),
                    dbc.Label('Coordinate', style=label_style)
                    ],
                    style={'width': '83px', 'marginBottom': '0.5vh', 'marginLeft': '9px'}),
                dbc.FormFloating([
                    dbc.Input(id='ti_dis', type='text', placeholder=0, style=input_style1),
                    dbc.Label('Distance', style=label_style)
                    ],
                    style={'width': '83px', 'marginBottom': '0.5vh', 'marginLeft': '9px', 'textAlign': 'center'})
            ])),
            dbc.Col(html.Div([  # right column
                dbc.FormFloating([
                    dbc.Input(id='ti_ang', type='text', placeholder=0, style=input_style1),
                    dbc.Label('Angle', style=label_style)
                    ],
                    style={'width': '83px', 'marginBottom': '0.5vh', 'marginLeft': '3px', 'textAlign': 'center'}),
                dbc.FormFloating([
                    dbc.Input(id='ti_sym', type='text', placeholder=0, style=input_style2),
                    dbc.Label('Symantic', style=label_style)
                    ],
                    style={'width': '83px', 'marginBottom': '0.5vh', 'marginLeft': '3px', 'textAlign': 'center'})
            ]))],
            className="row g-0"
        ))])
    ## Buttons
    buttons3 = html.Div([
        html.Div(
            dbc.Button("Calculate ground truth", id='calc', color="warning", outline=True),
            className="d-grid gap-2 col-8 mx-auto",
            style={'marginTop': '1vh', 'marginBottom': '0.5vh'}),
        html.Div(
            dbc.Button("Simulate measurement", id='sim', color="warning", outline=True),
            className="d-grid gap-2 col-8 mx-auto",
            style={'marginTop': '0.5vh', 'marginBottom': '1vh'})            
    ])

    ## putting all together | left column
    #styles
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
            ul_tt,  # Upload section
            se_tt,  # Simulator section
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
                    text_input,
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
                        dbc.Button("Get results", id='exp', color="success", outline=True),
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
                        dbc.Col(left_column, width='auto'),
                        dbc.Col(html.Div(id='map'))
                    ]
                )
            ]
        ),
        className='mt-3'
    )



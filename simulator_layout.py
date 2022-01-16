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
    modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("WARNING")),
        dbc.ModalBody("Wrong file was uploaded!")],
        id="sim_modal",
        is_open=False
    )

    ### UPLOAD
    # tooltips for more information
    ul_tt = html.Div([
        dbc.Tooltip("geojson",             target="maps_upload",      placement='right'),
        dbc.Tooltip("txt, csv or geojson", target="waypoints_upload", placement='right'),
        dbc.Tooltip("txt, csv or geojson", target="antennas_upload",  placement='right'),
        dbc.Tooltip("gyroscope",           target="ul_gyr",           placement='top'),
        dbc.Tooltip("acceleration",        target="ul_acc",           placement='bottom'),
        dbc.Tooltip("barometer",           target="ul_bar",           placement='top'),
        dbc.Tooltip("magnetometer",        target="ul_mag",           placement='bottom')
    ])
    ## Buttons
    # maps and waypoints
    ul_buttons1 = html.Div([
        dcc.Upload(
            id='ul_map',
            children=html.Div(dbc.Button("Maps", id='maps_upload', color="info", outline=True), className="d-grid gap-2 col-8 mx-auto"),
            style={'marginTop': '10px', 'marginBottom': '5px'},
            multiple=True),
        dcc.Upload(
            id='ul_way',
            children=html.Div(dbc.Button("Waypoints", id='waypoints_upload', color="info", outline=True), className="d-grid gap-2 col-8 mx-auto" ),
            style={'marginTop': '5px', 'marginBottom': '5px'},
            multiple=True),
        dcc.Upload(
            id='ul_ant',
            children=html.Div(dbc.Button("Antennas", id='antennas_upload', color="info", outline=True), className="d-grid gap-2 col-8 mx-auto" ),
            style={'marginTop': '5px', 'marginBottom': '15px'},
            multiple=True)
    ])
    # gyroscope, acceleration, barometer and magnetometer
    ul_buttons2 = html.Div(dbc.Row([
        dbc.Col(html.Div([  # left column
            dcc.Upload(
                id='ul_gyr',
                children=html.Div(dbc.Button("G", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginLeft': 'auto'}),
                multiple=True,
                style={'marginBottom': '4px'}),
            dcc.Upload(
                id='ul_acc',
                children=html.Div(dbc.Button("A", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginLeft': 'auto'}),
                multiple=True)])),
        dbc.Col(html.Div([  # right column
            dcc.Upload(
                id='ul_bar',
                children=html.Div(dbc.Button("B", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginRight': 'auto'}),
                multiple=True,
                style={'marginBottom': '4px'}),
            dcc.Upload(
                id='ul_mag',
                children=html.Div(dbc.Button("M", color="primary", size="lg", className="me-1", outline=True), className="d-grid gap-2 col-8", style={'marginRight': 'auto'}),
                multiple=True)]))],
        className="row g-0"),
        style={'marginBottom': '10px'}
    )

    ### SIMULATION
    # styles
    from_style = {
        'display': 'flex',
        'justify-content': 'center',
        'marginBottom': '5px'
    }
    input_style = {
        'color': 'gray',
        'width': '320px',
        'textAlign': 'center',
        'backgroundColor': 'silver',
        'border': '1px solid #917033'
    }
    label_style = {
        'marginLeft': '30px',
        'color': 'gray'
    }
    ## Entries
    text_input = html.Div([
        dbc.FormFloating([    # Distance Quality
            dbc.Input(id='ti_dis', type='text', placeholder=0, style=input_style),
            dbc.Label('Distance Quality', style=label_style)],
        style=from_style),
        dbc.FormFloating([    # Angle Quality
            dbc.Input(id='ti_ang', type='text', placeholder=0, style=input_style),
            dbc.Label('Angle Quality', style=label_style)],
        style=from_style),
        dbc.FormFloating([    # Coordinate Quality
            dbc.Input(id='ti_coo', type='text', placeholder=0, style=input_style),
            dbc.Label('Coordinate Quality', style=label_style)],
        style=from_style),
        dbc.FormFloating([    # Symantic Error
            dbc.Input(id='ti_sym', type='text', placeholder=0, style=input_style),
            dbc.Label('Symantic Error', style=label_style)],
        style={'display': 'flex', 'justify-content': 'center','marginBottom': '15px'})
    ])
    ## Buttons
    sim_buttons = html.Div([
        html.Div(
            dbc.Button("Calculate ground truth", id='calc', color="warning", outline=True),
            className="d-grid gap-2 col-8 mx-auto",
            style={'marginTop': '10px', 'marginBottom': '5px'}),
        html.Div(
            dbc.Button("Simulate measurement", id='sim', color="warning", outline=True),
            className="d-grid gap-2 col-8 mx-auto",
            style={'marginTop': '5px', 'marginBottom': '10px'})            
    ])

    ## OFFCANVAS
    ## putting everything it its appropriate offcanvas
    #styles
    hr_style1 = {
        'width': '80%',
        'margin': 'auto',
        'marginBottom': '15px'
    }
    hr_style2 = {
        'width': '30%',
        'margin': 'auto',
        'marginBottom': '15px'
    }
    div_style1 = {
        'border':'1px solid orange',
        'border-radius': 10,
        'padding': '10px'
    }
    div_style2 = {
        'border':'1px solid',
        'border-radius': 10,
        'color': 'silver'
    }
    H5_style = {
        'textAlign': 'center',
        'marginLeft': '40px',
        'marginRight': '40px',
        'color': 'grey',
        'paddingTop': '10px'
    }
    btn_style = {
        'marginTop': '10px',
        'marginBottom': '10px'
    }
    # UPLOAD
    # offcanvas
    ul_canvas = html.Div([
        dbc.Offcanvas(
            html.Div([
                html.Div([
                    # info text
                    html.P('⚠  Please note:'),
                    html.P('As Maps only GeoJSON files of type crs:32632 or directly crs:4326 are excepted. Waypoints and Antennas both except either TXT, CSV or GeoJSON.', style={'textAlign': 'left'})],
                style=div_style1),
                html.Br(),
                html.Div([
                    ul_tt,  # tooltips
                    html.H5('Upload', style=H5_style), # title
                    html.Hr(style=hr_style1),           # horizontal line
                    ul_buttons1,                       # buttons
                    html.Hr(style=hr_style2),
                    ul_buttons2],                      # buttons
                style=div_style2)
            ]),
            id="ul_cv",
            scrollable=True,
            title="Upload",
            is_open=False)
    ])
    # button
    ul_cv_btn = html.Div(
        dbc.Button("Data", id='ul_btn', color="info", outline=True),
        className="d-grid gap-2 col-10 mx-auto",
        style=btn_style)
    # SIMULATION
    # offcanvas
    sim_canvas = html.Div([
        dbc.Offcanvas(
            html.Div([
                html.H5('Simulation', style=H5_style),
                html.Hr(style=hr_style1),
                text_input,
                html.Hr(style=hr_style2),
                sim_buttons],
            style=div_style2
            ),
            id="sim_cv",
            scrollable=True,
            title="Simulation",
            is_open=False)
    ])
    # button
    sim_cv_btn = html.Div(
        dbc.Button("Simulate", id='sim_btn', color="warning", outline=True),
        className="d-grid gap-2 col-10 mx-auto",
        style=btn_style)

    ## putting all together | left column
    left_column = html.Div([
        # UPLOAD
        ul_canvas,  # offcanvas
        html.Div([   # button
            html.H5('Upload', style=H5_style),
            html.Hr(style=hr_style1),
            ul_cv_btn],
            style=div_style2),
        html.Br(),
        # SIMULATION
        sim_canvas,  # offcanvas
        html.Div([   # button
            html.H5('Simulation', style=H5_style),
            html.Hr(style=hr_style1),
            sim_cv_btn],
            style=div_style2),
        html.Br(),
        # EXPORT
        html.Div([
            html.H5('Export', style=H5_style),
            html.Hr(style=hr_style1),
            html.Div(
                dbc.Button("Get results", id='exp', color="success", outline=True),
                className="d-grid gap-2 col-10 mx-auto",
                style=btn_style)],
            style=div_style2)
    ])
    ### returning filled Card
    return dbc.Card(dbc.CardBody([
        # modal, giving alert
        modal,
        # card content
        html.P("SIMULATOR", className="card-text"),
        dbc.Row([
            dbc.Col(left_column, width='auto'),
            dbc.Col(html.Div(id='map'))
        ])
    ]),
    className='mt-3')



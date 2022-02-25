##### Simulator Tab -- Layout
###IMPORTS
# dash
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import arrow_function
# built in
from base64 import b64decode
# utils
from util import floorplan2layer, hover_info

def simulator_card(geojson_style):
    ### SPINNERs
    spin1 = dbc.Spinner(
        children=[html.Div(id="spin1", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "black"},
        spinnerClassName="spinner"
    )
    spin2 = dbc.Spinner(
        children=[html.Div(id="spin2", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "black"},
        spinnerClassName="spinner"
    )
    spin3 = dbc.Spinner(
        children=[html.Div(id="spin3", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "black"},
        spinnerClassName="spinner"
    )

    ### STORAGE
    # dcc.Store to store and share data between callbacks
    storage = html.Div([
        # filename from dropdown
        dcc.Store(id='ref_data', data=[], storage_type='memory'),
        # checked boxes
        dcc.Store(id='checked_boxes', data=[], storage_type='memory'),
        # generated ground truth
        dcc.Store(id='gt_data', data=[], storage_type='memory'),
        # simulated measurements
        dcc.Store(id='sim_data', data=[], storage_type='memory')
    ])

    ### DOWNLOAD
    export_gt = dcc.Download(id="export_gt")
    export_sim = dcc.Download(id="export_sim")

    ### MODALs
    # upload warning
    ul_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("WARNING")),
        dbc.ModalBody("At least one wrong file was uploaded!")],
        id="ul_warn",
        is_open=False
    )
    # upload done
    ul_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("File(s) uploaded successfully!")],
        id="ul_done",
        is_open=False
    )
    # map warning
    map_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("WARNING")),
        dbc.ModalBody("At least one wrong file was uploaded!")],
        id="map_warn",
        is_open=False
    )
    # map done
    map_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("File(s) uploaded and layered successfully!")],
        id="map_done",
        is_open=False
    )
    # calculation warning
    gen_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Please select data first!")],
        id="gen_warn",
        is_open=False
    )
    # calculation done
    gen_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("Generation successful!")],
        id="gen_done",
        is_open=False
    )
    # export warning
    exp_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Please generate ground truth and simulate measurement first!")],
        id="exp_warn",
        is_open=False
    )
    # export done
    exp_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("Export successful!")],
        id="exp_done",
        is_open=False
    )
    # ref show warning
    show_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Please select data first!")],
        id="show_warn",
        is_open=False
    )
    # simulation warning
    sim_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Please generate GroundTruth first, as well as enter integer values for frequency and error!")],
        id="sim_warn",
        is_open=False
    )
    # simulation done
    sim_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("Simulation successful!")],
        id="sim_done",
        is_open=False
    )


    ### MAP
    # info panel for geojson layer segments (tooltips while hovering)
    info = html.Div(
        children=hover_info(),
        id="hover_info",
        style={
            "position": "absolute",
            "top": "10px",
            "right": "120px",
            "z-index": "500",
            "color": "black",
            "backgroundColor": "white",
            "opacity": "0.6",
            "border": "2px solid #B2AFAC",
            "border-radius": 5,
            "padding": "10px",
            "width": "240px"
        }
    )
    # HCU coordinates
    hcu = (53.5403169239316, 10.004875659942629)
    # Tile Layer
    url = "https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png"
    # Map info
    attribution = "&copy; <a href='https://stadiamaps.com/'>Stadia Maps</a>, &copy; <a href='https://openmaptiles.org/'>OpenMapTiles</a> &copy; <a href='http://openstreetmap.org'>OpenStreetMap</a> contributors"
    # putting all together to map
    _map = html.Div(
        dl.Map(
            [   
                info,
                dl.TileLayer(url=url, maxZoom=20, attribution=attribution), # Base layer (OpenStreetMap)
                html.Div(id="layers", children=dl.LayersControl(floorplan2layer(geojson_style))), # is previously filled with floorplans
                dl.FullscreenControl(), # possibility to get map fullscreen
                dl.FeatureGroup(dl.EditControl(
                                    id="edit_control",
                                    draw=dict(rectangle=False, circle=False), # possibility to draw/edit data
                                    position="topleft")),
            ],
            zoom=19,
            center=hcu,
            style={'width': '100%', 'height': '70vh', 'margin': "auto", "display": "block"}
        )
    )
    
    ### UPLOAD
    # tooltips for more information
    ul_tt = html.Div([
        dbc.Tooltip("geojson",              target="maps_upload",      placement="right"),
        dbc.Tooltip("csv",  target="waypoints_upload", placement="right"),
        dbc.Tooltip("txt, csv or geojson",  target="antennas_upload",  placement="right"),
        dbc.Tooltip("gyroscope, CSV",       target="ul_gyr",           placement="top"),
        dbc.Tooltip("acceleration, CSV",    target="ul_acc",           placement="bottom"),
        dbc.Tooltip("barometer, CSV",       target="ul_bar",           placement="top"),
        dbc.Tooltip("magnetometer, CSV",    target="ul_mag",           placement="bottom")
    ])
    ## Buttons
    # maps and waypoints
    ul_buttons1 = html.Div([
        dcc.Upload(
            id="ul_map",
            children=html.Div(dbc.Button("Maps", id="maps_upload", color="info", outline=True, style={"width": "148px"})),
            style={"marginTop": "8px", "marginBottom": "5px"},
            multiple=True),
        dcc.Upload(
            id="ul_way",
            children=html.Div(dbc.Button("Waypoints", id="waypoints_upload", color="info", outline=True, style={"width": "148px"})),
            style={"marginTop": "5px", "marginBottom": "5px"},
            multiple=True),
        dcc.Upload(
            id="ul_ant",
            children=html.Div(dbc.Button("Antennas", id="antennas_upload", color="info", outline=True, style={"width": "148px"})),
            style={"marginTop": "5px", "marginBottom": "8px"},
            multiple=True)],
        style={"width": "150px"}
    )
    # gyroscope, acceleration, barometer and magnetometer
    ul_buttons2 = html.Div(dbc.Row([
        dbc.Col(html.Div([  # left column
            dcc.Upload(
                id="ul_gyr",
                children=html.Div(dbc.Button("G", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True,
                style={"marginBottom": "6px"}),
            dcc.Upload(
                id="ul_acc",
                children=html.Div(dbc.Button("A", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True)],
            style={"textAlign": "left", "marginTop": "18px", "marginBottom": "18px"})),
        dbc.Col(html.Div([  # right column
            dcc.Upload(
                id="ul_bar",
                children=html.Div(dbc.Button("B", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True,
                style={"marginBottom": "6px"}),
            dcc.Upload(
                id="ul_mag",
                children=html.Div(dbc.Button("M", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True)],
            style={"textAlign": "right", "marginTop": "18px", "marginBottom": "18px"}))],
        className="g-0"),
        style={"width": "180px"}
    )

    ### SIMULATION
    # styles
    from_style = {
        "display": "flex",
        "justify-content": "left",
        "marginLeft": "12px",
        "marginBottom": "5px"
    }
    input_style = {
        "color": "gray",
        "width": "200px",
        "textAlign": "center",
        "backgroundColor": "silver",
        "border": "1px solid gray"
    }
    label_style = {
        "marginLeft": "5px",
        "color": "gray"
    }
    ## Entries
    text_input = html.Div([
        dbc.FormFloating([    # Distance Quality
            dbc.Input(id="fr_dis", type="text", placeholder=0, style=input_style),
            dbc.Label("Frequency", style=label_style)],
        style=from_style),
        dbc.FormFloating([    # Coordinate Quality
            dbc.Input(id="ti_coo", type="text", placeholder=0, style=input_style),
            dbc.Label("Coordinate Quality", style=label_style)],
        style=from_style),
        # dbc.FormFloating([    # Distance Quality
        #     dbc.Input(id="ti_dis", type="text", placeholder=0, style=input_style),
        #     dbc.Label("Distance Quality", style=label_style)],
        # style=from_style),
        # dbc.FormFloating([    # Angle Quality
        #     dbc.Input(id="ti_ang", type="text", placeholder=0, style=input_style),
        #     dbc.Label("Angle Quality", style=label_style)],
        # style=from_style),
        # dbc.FormFloating([    # Symantic Error
        #     dbc.Input(id="ti_sym", type="text", placeholder=0, style=input_style),
        #     dbc.Label("Symantic Error", style=label_style)],
        # style={"display": "flex", "justify-content": "center","marginBottom": "15px"})
    ])
    ## Buttons
    sim_buttons = html.Div([
        html.Div(
            dbc.Button("Ground Truth", id="gt_btn", color="light", outline=True, style={"width": "200px"}),
            style={"marginBottom": "5px"}),
        html.Div(
            dbc.Button("Simulate Measurement", id="sim_btn", color="light", outline=True, style={"width": "200px"}),
            style={"marginTop": "5px"})            
    ])

    ## OFFCANVAS
    #styles
    hr_style = {
        "width": "60%",
        "margin": "auto"
    }
    H5_style = {
        "textAlign": "center",
        "color": "grey",
        "marginTop": "5px"
    }
    # HELP
    help_canvas = html.Div([
        dbc.Offcanvas(
            [   
                html.Div([
                    # info upload
                    html.H5("UPLOAD", style={"text-align": "center", "color": "#3B5A7F"}),
                    html.Hr(style={"margin": "auto", "width": "80%", "color": "#3B5A7F"}),
                    html.P("All 7 buttons are for uploading the data required for the simulation.", style={"color": "gray"}),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Maps:", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("Only GeoJSON files of type crs:32632 are accepted.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Waypoints:", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("Only CSV files are accepted.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Antennas:", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("Only TXT, CSV or GeoJSON files are accepted.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Sensors:", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("Only CSV files are accepted.", style={"color": "gray"}))
                    ], className="g-0")],
                style={"border":"1px solid #3B5A7F", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}),
                html.Br(),
                html.Div([
                    # info simulation
                    html.H5("SIMULATION", style={"text-align": "center", "color": "silver"}),
                    html.Hr(style={"margin": "auto", "width": "80%", "color": "silver"}),
                    html.P("Guide for simulating measurements:", style={"color": "gray"}),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Frequency:", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Accepts float values.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Coord. Qual.:", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Accepts float values.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Ground Truth:", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Choose data and generate ground truth trajectory.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Sim. Measm.:", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Simulate the measurement to finish the calculation.", style={"color": "gray"}))
                    ], className="g-0"),
                    html.Div(html.P("The ground truth trajectory and the simulated measurement can now be downloaded as two seperate CSV files!", style={"color": "gray"}),
                    style={"borderLeft": "2px solid #36BD8E", "paddingLeft": "5px"})],
                style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}),
            ],
        id="help_cv",
        scrollable=True,
        title="Help",
        is_open=False)
    ])
    # GROUND TRUTH
    gt_canvas = html.Div([
        dbc.Offcanvas([
            # steps
            html.Div([
                html.H5("Procedure", style={"color": "silver", "text-indent": "15px"}),
                html.P("🢖 Select the data", style={"color": "gray", "marginBottom": "-5px", "text-indent": "10px"}),
                html.P("🢖 Show Waypoints on the map", style={"color": "gray", "marginBottom": "-5px", "text-indent": "10px"}),
                html.P("🢖 Select Waypoints you want", style={"color": "gray", "marginBottom": "-5px", "text-indent": "10px"}),
                html.P("🢖 Generate Ground Truth Trajectory", style={"color": "gray", "marginBottom": "3px", "text-indent": "10px"}),
                html.P("⚠️ Please note:", style={"color": "gray", "marginBottom": "-7px"}),
                html.P(" The first and last point is always selected.", style={"color": "gray", "text-indent": "26px"}),
            ],
            style={"border": "1px solid #E45E07", "border-radius": 10, "padding": "10px", "marginBottom": "15px", "height": "180px"}),

            html.Div([
                # buttons
                html.Div(dbc.Row([
                    dbc.Col(dbc.Button("Show", id="show_btn", color="light", outline=True, style={"width": "160px"})),
                    dbc.Col(dbc.Button("Generate", id="gen_btn", color="light", outline=True, style={"width": "160px"}))
                ], className="g-0"),
                style={"text-align": "center", "marginBottom": "15px"}),
                # dropdown
                dcc.Dropdown(
                    id="ref_select",
                    options=[],
                    placeholder="Select Data",
                    clearable=True,
                    optionHeight=35,
                    multi=False,
                    searchable=True,
                    style={"marginBottom": "15px", "color": "black"},
                ),
                # headline
                html.Div(html.H5("Waypoints", style={"color": "#ADB5BD", "text-align": "center"}),
                    style={"background": "#375A7F", "border": "1px solid #4B6B8C", "borderBottom": "0px", "paddingBottom": "4px"}),
                # table header
                dbc.Table(html.Thead(
                    html.Tr(
                        [
                            html.Th("№", style={"width": "60px", "color": "gray", "text-align": "center"}),
                            html.Th("Latitude", style={"width": "112px", "color": "gray", "text-align": "center"}),
                            html.Th("Longitude", style={"width": "112px", "color": "gray", "text-align": "center"}),
                            html.Th("Select", style={"width": "60px", "color": "gray", "text-align": "center"})
                        ])),
                    style={"marginTop": "-7px", "marginBottom": "7px"},
                    size="sm",
                    bordered=True,
                    color="primary"),
                # table body -> reference points
                html.Div(id="ref_tab"),

                # creating an invisible div with enough checkboxes (100) for later ref points displayment
                html.Div(id="invisible",
                    children=[dbc.Checklist(options=[{"value": 1}], value=[1], id=f"check{i}") for i in range(100)],
                    style={"display": "none"})
            ],
            style={"border":"1px solid silver", "border-radius": 10, "padding": "10px"})],
        id="gt_cv",
        scrollable=True,
        title="Ground Truth Generation",
        is_open=False)
    ])
    # card content
    first_row = html.Div([dbc.Row(
        [
            dbc.Col(html.Div([
                    html.H5("Upload", style=H5_style),
                    html.Hr(style=hr_style),
                    dbc.Row([
                        dbc.Col(html.Div(html.Div(ul_buttons1), style={"marginLeft": "40px"})),
                        dbc.Col(html.Div(html.Div(ul_buttons2)))],
                    className="g-0")],
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "180px", "width": "435px", "marginBottom": "4px"})),

            dbc.Col(html.Div([
                    html.H5("Simulation", style=H5_style),
                    html.Hr(style=hr_style),
                    dbc.Row([
                        dbc.Col(html.Div(text_input, style= {"marginTop": "10px"})),
                        dbc.Col(html.Div(sim_buttons, style= {"marginTop": "30px"}))],
                    className="g-0")],
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "180px", "width": "435px", "marginBottom": "4px"})),

            dbc.Col(html.Div([
                html.Div(
                    [
                        html.H5("Export", style={"textAlign": "center", "color": "grey", "marginTop": "5px"}),
                        html.Hr(style={"width": "60%", "margin": "auto"}),
                        html.Div(
                            [
                                dbc.Button(
                                    [
                                        "Get results",
                                        html.Div(id="exp_badge")
                                    ],
                                    color="success",
                                    className="position-relative",
                                    outline=True,
                                    style={"width": "150px"},
                                    id="exp_btn",
                                )
                            ],
                            style={"textAlign": "center", "marginTop": "10px"}
                        )
                    ],            
                    style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "100px", "width": "435px"}
                ),
                html.Div([
                    html.Div(dbc.Button("Help", id="help_btn", color="warning", outline=False, style={"width": "150px"}), style={"textAlign": "center", "marginTop": "19px"})],
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "76px", "width": "435px", "marginTop": "4px", "marginBottom": "4px"})]))
        ],
        className="g-0")
    ])

    ### returning filled Card
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    # storage
                    storage,
                    # download
                    export_sim,
                    export_gt,
                    # modals
                    ul_warn,
                    ul_done,
                    map_warn,
                    map_done,
                    gen_warn,
                    gen_done,
                    exp_warn,
                    exp_done,
                    show_warn,
                    sim_done,
                    sim_warn,
                    # tooltips
                    ul_tt,
                    # canvas
                    help_canvas,
                    gt_canvas,
                    # spinners
                    spin1,
                    spin2,
                    spin3,
                    # card content
                    html.Div(
                        [
                            first_row,
                            html.Br(),
                            dbc.Row(_map)
                        ]
                    ),
                ]
            ),
            dbc.CardFooter("Copyright © 2022 Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
        ]
    )



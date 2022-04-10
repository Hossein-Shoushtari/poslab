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


def storage():
    ### STORAGE
    # dcc.Store to store and share data between callbacks
    storage = html.Div([
        # new layers
        dcc.Store(id="new_layers", data=[], storage_type="memory"),
        # password status
        dcc.Store(id="unlocked", data=[], storage_type="memory"),
        # filename from dropdown
        dcc.Store(id="ref_data", data=[], storage_type="memory"),
        # checked boxes
        dcc.Store(id="checked_boxes", data=[], storage_type="memory"),
        # reference points layer
        dcc.Store(id="rp_layer", data=[], storage_type="memory"),
        # ground truth
        dcc.Store(id="gt_data", data=[], storage_type="memory"),
        dcc.Store(id="gt_layer", data=[], storage_type="memory"),
        # simulated measurements
        dcc.Store(id="sim_data", data=[], storage_type="memory")
    ])
    return storage

def tooltips():
    # tooltips for more information
    tooltips = html.Div([
        dbc.Tooltip("geojson",              target="maps_upload",      placement="right"),
        dbc.Tooltip("csv",                  target="waypoints_upload", placement="right"),
        dbc.Tooltip("txt, csv or geojson",  target="antennas_upload",  placement="right"),
        dbc.Tooltip("gyroscope, csv",       target="ul_gyr",           placement="top"),
        dbc.Tooltip("acceleration, csv",    target="ul_acc",           placement="bottom"),
        dbc.Tooltip("barometer, csv",       target="ul_bar",           placement="top"),
        dbc.Tooltip("magnetometer, csv",    target="ul_mag",           placement="bottom"),
        dbc.Tooltip("reset",                target="ss_reset",         placement="right"),
        dbc.Tooltip("settings",             target="sim_set",          placement="right")
    ])
    return tooltips

def spinners():
    ### SPINNERs
    spin1 = dbc.Spinner(
        children=[html.Div(id="spin1", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin2 = dbc.Spinner(
        children=[html.Div(id="spin2", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin3 = dbc.Spinner(
        children=[html.Div(id="spin3", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin4 = dbc.Spinner(
        children=[html.Div(id="spin4", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin5 = dbc.Spinner(
        children=[html.Div(id="spin5", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    return html.Div([spin1, spin2, spin3, spin4, spin5])

def modals():
    ### MODALs
    # upload warning
    ul_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("WARNING")),
        dbc.ModalBody("At least one wrong file was meant to be uploaded! Upload denied.")],
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
        dbc.ModalBody("At least one wrong file was meant to be uploaded! Upload denied.")],
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
    # data selection warning
    sel_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Please select data first!")],
        id="sel_warn",
        is_open=False
    )
    # gt calculation warning
    gen_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Apparently acc and gyr are missing. Please upload them first!")],
        id="gen_warn",
        is_open=False
    )
    # gt calculation done
    gen_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("Generation successful!")],
        id="gen_done",
        is_open=False
    )
    # simulation warning
    sim_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Please generate GroundTruth first, as well as enter values for all required inputs!")],
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
    # export warning
    exp_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Please simulate measurements first!")],
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
    # unlock hcu maps
    hcu_modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Researcher Login")),
            dbc.ModalBody(
                html.Div(
                    [
                        dbc.Label("Password"),
                        dbc.Input(id="password", type="password", placeholder="Enter password", style={"color": "white"}),
                        dbc.FormFeedback("Access granted", type="valid"),
                        dbc.FormFeedback("Access denied", type="invalid")
                    ]
                )
            ),
            dbc.ModalFooter(
                dbc.Button("Unlock", color="primary", id="unlock")
            ),
        ],
    id="modal",
    backdrop="static",
    is_open=False,
    )
    return html.Div([ul_warn, ul_done, map_warn, map_done, gen_warn, gen_done, sel_warn, exp_warn, exp_done, sim_done, sim_warn, hcu_modal])

def sim_map(geojson_style):
    ### MAP
    # info panel for hcu maps
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
    # unlock hcu maps button
    btn_style = {
        "position": "absolute",
        "top": "325px",
        "left": "10px",
        "z-index": "500",
        "backgroundColor": "white",
        "border": "2px solid #B2AFAC",
        "border-radius": 4,
        "width": "34px",
        "height": "34px"
    }
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
                html.Div(id="hcu_panel", children=info, style={"display": "None"}),
                html.Button("🎓", id="hcu_maps", style=btn_style),
                dl.TileLayer(url=url, maxZoom=20, attribution=attribution), # Base layer (OpenStreetMap)
                html.Div(id="layers", children=html.Div(dl.LayersControl(floorplan2layer(geojson_style)), style={"display": "None"})), # is previously filled with invisible floorplans for initialization
                dl.FullscreenControl(), # possibility to get map fullscreen
                dl.FeatureGroup(dl.EditControl(
                                    id="edit_control",
                                    draw=dict(rectangle=False, circle=False), # possibility to draw/edit data
                                    position="topleft")),
            ],
            zoom=19,
            center=hcu,
            style={"width": "100%", "height": "70vh", "margin": "auto", "display": "block"}
        )
    )
    return _map

def help_canvas():
    ## OFFCANVAS
    # HELP
    help_canvas = html.Div([
        dbc.Offcanvas(
            [   
                html.Div([
                    # info upload
                    html.H5("UPLOAD", style={"text-align": "center", "color": "#3B5A7F"}),
                    html.Hr(style={"margin": "auto", "width": "80%", "color": "silver", "marginBottom": "3px"}),
                    html.P("All 7 buttons are for uploading the data required for the simulation.", style={"color": "gray"}),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Maps:", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("Only GeoJSON files of any type are accepted.", style={"color": "gray"}))
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
                    html.Hr(style={"margin": "auto", "width": "80%", "color": "silver", "marginBottom": "3px"}),
                    html.P("Instructions for simulating measurements:", style={"color": "gray"}),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Ground Truth:", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Select data and generate a ground truth trajectory. Note: acc and gyr data is needed!", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("⚙", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Change presets to customize the simulation.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Frequency:", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Accepts float values.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Error:", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Accepts float values.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Semantic Error:", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Check or uncheck.", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Sim. Measm.:", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("Simulate the measurements to complete the calculation.", style={"color": "gray"}))
                    ], className="g-0"),
                    html.Div(html.P("The ground truth trajectory and the simulated measurements can now be downloaded as two separate CSV files!", style={"color": "gray"}),
                    style={"borderLeft": "2px solid #36BD8E", "paddingLeft": "5px"})],
                style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}),
                html.Br(),
                html.Div([
                    # bug info upload
                    html.H5("🐞", style={"text-align": "center"}),
                    html.Hr(style={"margin": "auto", "width": "80%", "color": "silver", "marginBottom": "3px"}),
                    html.P("After uploading new layers sometimes the layer names in the layer control as well as some tooltips are messed up.", style={"color": "gray"}),
                    html.P("Changing tabs will automatically update the names.", style={"color": "gray", "marginTop": "-10px"})],
                style={"border":"1px solid red", "border-radius": 10, "padding": "10px", "marginBottom": "0px"})
            ],
        id="help_cv",
        scrollable=True,
        title="Help",
        is_open=False)
    ])
    return help_canvas

def gt_canvas():
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
    return gt_canvas

def sim_set_canvas():
    ## OFFCANVAS
    # SIM SETTINGS
    sim_set_canvas = html.Div([
        dbc.Offcanvas(
            [   
                html.Div(
                    [
                    # Semantic Errors
                    html.H5("Semantic Errors", style={"text-align": "left", "color": "silver"}),
                    html.Div(dbc.Button("↺", id="ss_reset", color="light", outline=True, style={"border": "0px"}),
                        style={"text-align": "right","marginTop": "-39px", "marginRight": "-5px"}),
                    html.Hr(style={"margin": "auto", "width": "100%", "color": "silver", "height": "3px", "marginBottom": "-10px"}),
                    html.Br(),

                    html.P("Number of intervals", style={"text-align": "center", "color": "silver", "marginBottom": "2px"}),
                    html.Div(dbc.Input(id="num_int", placeholder="Type a number...", type="text", style={"color": "silver", "textAlign": "center"})),

                    html.P("Interval range [sec]", style={"text-align": "center", "color": "silver", "marginBottom": "0px", "marginTop": "10px"}),
                    dcc.RangeSlider(id="int_rang", min=0, max=7000),
                    html.Div(dbc.Row([dbc.Col(html.P(id="int_rang_min")), dbc.Col(html.P(id="int_rang_max", style={"text-align": "right"}))]), style={"margin": "auto", "marginTop": "-25px", "width": "280px"}),
                    
                    html.P("Semantic error", style={"text-align": "center", "color": "silver", "marginBottom": "0px", "marginTop": "-20px"}),
                    dcc.RangeSlider(id="sem_err_rang", min=0, max=20),
                    html.Div(dbc.Row([dbc.Col(html.P(id="sem_err_rang_min")), dbc.Col(html.P(id="sem_err_rang_max", style={"text-align": "right"}))]), style={"margin": "auto", "marginTop": "-25px", "width": "280px"}),
                    ],
                style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}),
                html.Br(),
                html.Div(
                    [
                    # Multiple Users
                    html.H5("Multiple Users", style={"text-align": "left", "color": "silver"}),
                    html.Hr(style={"margin": "auto", "width": "100%", "color": "silver", "height": "3px", "marginBottom": "-10px"}),
                    html.Br(),

                    html.P("Network Capacity [req/sec]", style={"text-align": "center", "color": "silver", "marginBottom": "2px"}),
                    html.Div(dbc.Input(id="net_cap", placeholder="Type a number...", type="text", style={"color": "silver", "textAlign": "center"})),
                    ],
                style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}),
            ],
        id="sim_set_cv",
        scrollable=True,
        title="Simulation Settings",
        is_open=False)
    ])

    return sim_set_canvas


def simulator_card(geojson_style):

    ### DOWNLOAD
    export_gt = dcc.Download(id="export_gt")
    export_sim = dcc.Download(id="export_sim")

    ### UPLOAD
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
                multiple=False,
                style={"marginBottom": "6px"}),
            dcc.Upload(
                id="ul_acc",
                children=html.Div(dbc.Button("A", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=False)],
            style={"textAlign": "left", "marginTop": "18px", "marginBottom": "18px"})),
        dbc.Col(html.Div([  # right column
            dcc.Upload(
                id="ul_bar",
                children=html.Div(dbc.Button("B", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=False,
                style={"marginBottom": "6px"}),
            dcc.Upload(
                id="ul_mag",
                children=html.Div(dbc.Button("M", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=False)],
            style={"textAlign": "right", "marginTop": "18px", "marginBottom": "18px"}))],
        className="g-0"),
        style={"width": "180px"}
    )

    ### SIMULATION
    # styles
    input_style = {
        "color": "gray",
        "width": "120px",
        "height": "60px",
        "textAlign": "center",
        "backgroundColor": "silver",
        "border": "1px solid gray"
    }
    
    # card content
    # styles
    hr_style = {
    "width": "80%",
    "margin": "auto"
    }
    H5_style = {
        "textAlign": "center",
        "color": "grey",
        "marginTop": "5px"
    }
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
                html.Div(
                    [
                        html.H5("Simulation", style=H5_style),
                        html.Div(dbc.Button("⚙", id="sim_set", color="light", outline=True, style={"border": "0px"}),
                            style={"text-align": "right","marginTop": "-35px", "marginRight": "3px"})
                    ]
                ),
                html.Hr(style=hr_style),
                dbc.Row(
                    [
                        dbc.Col(html.Div(dbc.Button(
                                "Ground Truth",
                                id="gt_btn",
                                color="light",
                                outline=False,
                                style={"line-height": "1.5", "height": "70px", "width": "70px", "padding": "0px"}),
                                style={"marginTop": "15px", "marginBottom": "15px"}),
                            style={"text-align": "center", "width": "90px", "margin": "auto", "borderRight": "1px solid #494949"},
                            width=2
                        ),

                        dbc.Col(html.Div(
                            [
                                dbc.FormFloating(
                                    [    # Frequency
                                        dbc.Input(id="ms_freq", type="text", placeholder=0, style=input_style),
                                        dbc.Label("Frequency", style={"color": "gray"})
                                    ],
                                    style={"marginBottom": "4px"}
                                ),
                                dbc.FormFloating(
                                    [    # User
                                        dbc.Input(id="num_user", type="text", placeholder=0, style=input_style),
                                        dbc.Label("User", style={"color": "gray"})
                                    ]
                                )
                            ],
                            style={"width": "120px", "margin": "auto", "marginTop": "8px", "marginLeft": "10px", "height": "126px"})
                        ),

                        dbc.Col(html.Div(
                            [
                                dbc.FormFloating([    # Error
                                    dbc.Input(id="err", type="text", placeholder=0, style=input_style),
                                    dbc.Label("Error", style={"color": "gray"})]),
                                html.Div(
                                    [
                                        html.Div(html.P("Semantic Error:"),
                                            style={"width": "118px", "height": "29px", "text-align": "center"}),
                                        html.Div(dbc.Checklist(options=[{"value": 1}], value=[1], id="sem_err", style={"marginLeft": "50px"}),
                                            style={"width": "118px", "height": "29px" }
                                        )
                                    ],
                                    style={"marginTop": "4px", "border": "1px solid #808080", "border-radius": "5px", "height": "60px",  "text-align": "center"}
                                )
                            ],
                            style={"width": "120px", "margin": "auto", "marginTop": "8px", "marginLeft": "0px", "height": "126px"})
                        ),

                        dbc.Col(html.Div(dbc.Button(
                                html.P("Simulate", style={"marginTop": "12px"}),
                                id="sim_btn",
                                color="light",
                                outline=False,
                                style={"line-height": "1.5", "height": "124px", "width": "70px", "padding": "0px"}),
                                style={"marginTop": "6px", "marginLeft": "-17px"}),
                            style={"text-align": "center", "margin": "auto"},
                        width=2
                        )
                    ],
                className="g-0")],
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "180px", "width": "435px", "marginBottom": "4px"}
            )),

            dbc.Col(html.Div([
                html.Div(
                    [
                        html.H5("Export", style={"textAlign": "center", "color": "grey", "marginTop": "5px"}),
                        html.Hr(style=hr_style),
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
                    storage(),
                    # download
                    export_sim,
                    export_gt,
                    # modals
                    modals(),
                    # canvas
                    help_canvas(),
                    gt_canvas(),
                    sim_set_canvas(),
                    # card content
                    html.Div(
                        [
                            first_row,
                            html.Br(),
                            dbc.Row(sim_map(geojson_style))
                        ]
                    ),
                    # spinners
                    spinners(),
                    # tooltips
                    tooltips()
                ]
            ),
            dbc.CardFooter("Copyright © 2022 Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
        ]
    )



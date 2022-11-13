##### Simulator Tab -- Layout
###IMPORTS
# dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_leaflet as dl
# utils (general & simulator)
import simulator.utils as su
import utils as u
# built in
import datetime


def storage():
    ### STORAGE
    # dcc.Store to store and share data between callbacks
    storage = html.Div([
        # layers
        dcc.Store(id="sim_map_layers", data={"layers": None, "zoom": 0, "center": 0, "date": 0}, storage_type="memory"),
        dcc.Store(id="sim_ref_layers", data={"layers": None, "zoom": 0, "center": 0, "date": 0}, storage_type="memory"),
        dcc.Store(id="sim_ant_layers", data={"layers": None, "zoom": 0, "center": 0, "date": 0}, storage_type="memory"),
        dcc.Store(id="sim_gt_layers", data={"layers": None, "zoom": 0, "center": 0, "date": 0}, storage_type="memory"),
        dcc.Store(id="sim_traj_layers", data={"layers": None, "zoom": 0, "center": 0, "date": 0}, storage_type="memory"),
        # filename from ref dropdown
        dcc.Store(id="ref_data", data=[], storage_type="memory"),
        # checked boxes
        dcc.Store(id="checked_boxes", data=[], storage_type="memory")
    ])
    return storage

def tooltips():
    # tooltips for more information
    tooltips = html.Div([
        dbc.Tooltip("geojson",              target="sim_maps_upload",  placement="right"),
        dbc.Tooltip("csv",                  target="waypoints_upload", placement="right"),
        dbc.Tooltip("csv",                  target="antennas_upload",  placement="right"),
        dbc.Tooltip("gyroscope | csv",      target="sim_ul_gyr",       placement="top"),
        dbc.Tooltip("accelerator | csv",    target="sim_ul_acc",       placement="bottom"),
        dbc.Tooltip("barometer | csv",      target="sim_ul_bar",       placement="top"),
        dbc.Tooltip("magnetometer | csv",   target="sim_ul_mag",       placement="bottom"),
        dbc.Tooltip("settings",             target="sim_set_img",      placement="right"),
        dbc.Tooltip("save",                 target="sim_save_img",     placement="right"),
        dbc.Tooltip("focus",                target="sim_zoom_img",     placement="right")
    ])
    return tooltips

def spinners():
    ### SPINNERs
    spin1 = dbc.Spinner(
        children=[html.Div(id="sim_spin1", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin2 = dbc.Spinner(
        children=[html.Div(id="sim_spin2", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin3 = dbc.Spinner(
        children=[html.Div(id="sim_spin3", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin4 = dbc.Spinner(
        children=[html.Div(id="sim_spin4", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin5 = dbc.Spinner(
        children=[html.Div(id="sim_spin5", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    return html.Div([spin1, spin2, spin3, spin4, spin5])

def modals():
    ### MODALs
    modals = html.Div(
        [
            # upload warning
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/error_sign.svg"))),
                dbc.ModalBody("Wrong file format! Upload denied.")],
                id="sim_ul_warn",
                size="sm",
                is_open=False
            ),
            # upload done
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/done_sign.svg"))),
                dbc.ModalBody("Upload successful!")],
                id="sim_ul_done",
                size="sm",
                is_open=False
            ),
            # map warning
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/error_sign.svg"))),
                dbc.ModalBody("Wrong file format! Upload denied.")],
                id="sim_map_warn",
                size="sm",
                is_open=False
            ),
            # map display done
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/done_sign.svg"))),
                dbc.ModalBody("Successful!")],
                id="sim_display",
                size="sm",
                is_open=False
            ),
            # data selection warning
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/caution_sign.svg"))),
                dbc.ModalBody("Please select data first!")],
                id="sel_warn",
                size="sm",
                is_open=False
            ),
            # gt calculation warning
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/error_sign.svg"))),
                dbc.ModalBody("Something went wrong. Please check the formats.")],
                id="gen_warn",
                size="sm",
                is_open=False
            ),
            # gt calculation done
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/done_sign.svg"))),
                dbc.ModalBody("Generation successful!")],
                id="gen_done",
                size="sm",
                is_open=False
            ),
            # simulation warning
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/caution_sign.svg"))),
                dbc.ModalBody("Please select and enter the right data first!")],
                id="sim_warn",
                size="sm",
                is_open=False
            ),
            # save drawings done
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/done_sign.svg"))),
                dbc.ModalBody("Saved!")],
                id="sim_save_done",
                size="sm",
                is_open=False
            ),
            # export warning
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/caution_sign.svg"))),
                dbc.ModalBody("Nothing to export!")],
                id="sim_exp_warn",
                size="sm",
                is_open=False
            ),
            # export done
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/done_sign.svg"))),
                dbc.ModalBody("Export successful!")],
                id="sim_exp_done",
                size="sm",
                is_open=False
            ),
            # simulate measurements - select ground truth
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Simulate Measurements")),
                    dbc.ModalBody(
                        html.Div(
                            [
                                dbc.Label("Ground Truth"),
                                dcc.Dropdown(
                                    id="sim_gt_select",
                                    options=[],
                                    placeholder="Select Data",
                                    clearable=True,
                                    optionHeight=35,
                                    multi=False,
                                    searchable=True,
                                    style={"marginBottom": "15px", "color": "black"},
                                )
                            ]
                        )
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Simulate", color="primary", id="sim_btn")
                    )
                ],
                id="sim_modal",
                backdrop="static",
                is_open=False,
            )
        ]
    )
    return modals
    
def sim_map(geojson_style):
    ### MAP
    # info panel for hcu maps
    info = html.Div(
        children=u.hover_info(),
        id="sim_hover_info",
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
    # save botton
    save_style = {
        "position": "absolute",
        "top": "310px",
        "left": "10px",
        "z-index": "1000",
        "backgroundColor": "white",
        "border": "2px solid #CCCCCC",
        "border-top": "1px solid #CCCCCC",
        "border-bottom-left-radius": 4,
        "border-bottom-right-radius": 4,
        "width": "34px",
        "height": "34px"
    }
    # zoom botton
    focus_style = {
        "position": "absolute",
        "top": "355px",
        "left": "10px",
        "z-index": "500",
        "backgroundColor": "white",
        "border": "2px solid #CCCCCC",
        "border-radius": 4,
        "width": "34px",
        "height": "34px"
    }
    # unlock hcu maps button
    research_style = {
        "position": "absolute",
        "top": "400px",
        "left": "10px",
        "z-index": "500",
        "backgroundColor": "white",
        "border": "2px solid #CCCCCC",
        "border-radius": 4,
        "width": "34px",
        "height": "34px"
    }
    # Tile Layer
    url = "https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png"
    # Map info
    attribution = "&copy; <a href='https://stadiamaps.com/'>Stadia Maps</a>, &copy; <a href='https://openmaptiles.org/'>OpenMapTiles</a> &copy; <a href='http://openstreetmap.org'>OpenStreetMap</a> contributors"
    # putting all together to map
    _map = html.Div(
        dl.Map(
            [   
                html.Div(id="sim_hcu_panel", children=info, style={"display": "None"}),
                html.Button(html.Img(src="assets/images/signs/save_sign.svg", id="sim_save_img"), id="sim_save", style=save_style),
                html.Button(html.Img(src="assets/images/signs/focus_sign2.svg", id="sim_zoom_img"), id="sim_zoom", style=focus_style),
                html.Button(html.Img(src="assets/images/signs/research_sign.svg"), id="sim_hcu_maps", style=research_style),
                dl.TileLayer(url=url, maxZoom=20, attribution=attribution), # Base layer (OpenStreetMap)
                html.Div(id="sim_div_lc", children=dl.LayersControl(id="sim_lc", children=su.floorplan2layer(geojson_style))), # is previously filled with invisible floorplans for initialization
                dl.FullscreenControl(), # possibility to get map fullscreen
                dl.FeatureGroup(dl.EditControl(
                                    id="edit_control",
                                    draw=dict(rectangle=False, circle=False), # possibility to draw/edit data
                                    position="topleft")),
            ],
            style={"width": "100%", "height": "70vh", "margin": "auto", "display": "block", "border-radius": 10},
            id="sim_map",
            bounds=[[35.81781315869664, -47.90039062500001], [60.71619779357716, 67.67578125000001]] # center of Europe as centroid
        )
    )
    return _map

def help_canvas():
    ## OFFCANVAS
    # HELP
    help_canvas = html.Div([
        dbc.Offcanvas(
            [   
                dbc.Alert(
                    [
                        html.Div(html.Img(src="assets/images/signs/focus_sign1.svg"), style={"marginRight": "10px"}),
                        "Use the focus tool on the map to restore the last view!"
                    ],
                    className="d-flex align-items-center",
                    style={"height": "75px", "color": "silver", "background": "#4598DB", "border-radius": 10}
                ),
                dbc.Alert(
                    [
                        html.Button(html.Img(src="assets/images/signs/download_sign.svg", style={"marginLeft": "-8px"}), id="sim_exdata", style={"marginRight": "10px", "width": "48px", "background": "transparent", "border": "0px"}),
                        html.Div(
                            [
                                html.P("Not sure about the file formats?", style={"marginBottom": "0px"}),
                                html.P("Download example data here!", style={"marginBottom": "0px"}),
                            ]
                        ),
                    ],
                    className="d-flex align-items-center",
                    style={"height": "75px", "color": "silver", "background": "#008000", "border-radius": 10}
                ),
                dbc.Alert(
                    [
                        html.Div(html.Img(src="assets/images/signs/bug_sign.svg"), style={"marginRight": "10px"}),
                        html.Div(
                            [
                                html.P("Are the layer names mixed up?", style={"marginBottom": "0px"}),
                                html.P("Just switch tabs and come back!", style={"marginBottom": "0px"}),
                            ]
                        ),
                    ],
                    className="d-flex align-items-center",
                    style={"height": "75px", "color": "silver", "background": "#70251B", "border-radius": 10}
                ),
                html.Div([
                    # info upload
                    html.H5("UPLOAD", style={"text-align": "center", "color": "#3B5A7F"}),
                    html.Hr(style={"margin": "auto", "width": "80%", "color": "silver", "marginBottom": "3px"}),
                    html.P("All buttons are for uploading the data required for simulation. Each file needs the first line as a header. The delimiter is a single space.", style={"color": "gray"}),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Maps", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("optional; GeoJSON, any CRS", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Waypoints", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("used for ground truth; CSV, UTM", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Antennas", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("optional; CSV, UTM", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Sensors", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("acc&gyr used for ground truth, bar&mag optional; CSV", style={"color": "gray"}))
                    ], className="g-0")],
                style={"border":"1px solid #3B5A7F", "border-radius": 10, "padding": "10px", "marginBottom": "16px"}),
                html.Div([
                    # info simulation
                    html.H5("SIMULATION", style={"text-align": "center", "color": "silver"}),
                    html.Hr(style={"margin": "auto", "width": "80%", "color": "silver", "marginBottom": "15px"}),
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/signs/warning_sign.svg"), style={"marginRight": "10px"}),
                            "For performance reasons, only trajectories up to 500 points are displayed on the map.",
                        ],
                        className="d-flex align-items-center",
                        style={"height": "90px", "color": "gray", "background": "#774E06"}
                    ),
                    html.P("Instructions for simulating measurements:", style={"color": "gray"}),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Ground Truth", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("select data to generate ground truth trajectories", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Settings", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("change presets and customize the simulation", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Frequency", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("accepts float values", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Error", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("accepts float values", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("User", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("accepts int values", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Semantic Error", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("check or uncheck", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Simulate", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
                        dbc.Col(html.P("simulate measurements to complete the calculation", style={"color": "gray"}))
                    ], className="g-0"),
                    html.Div(html.P("Ground truth trajectories, simulated measurements and drawings can be downloaded in a ZIP file!", style={"color": "gray"}),
                    style={"borderLeft": "2px solid #36BD8E", "paddingLeft": "5px"})],
                style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"})
            ],
        id="sim_help_cv",
        scrollable=False,
        title="Help",
        is_open=False)
    ])
    return help_canvas

def gt_canvas():
    # GROUND TRUTH
    gt_canvas = html.Div([
        dbc.Offcanvas([
            # steps
            dbc.Alert(
                [
                    html.Div(html.Img(src="assets/images/signs/list_sign.svg"), style={"marginRight": "30px"}),
                    html.Div(
                        [
                            html.P("Select all data needed", style={"marginBottom": "0px"}),
                            html.P("Show waypoints on the map", style={"marginBottom": "0px"}),
                            html.P("Select required waypoints", style={"marginBottom": "0px"}),
                            html.P("Generate ground truth", style={"marginBottom": "0px"}),
                        ]
                    ),
                ],
                className="d-flex align-items-center",
                style={"height": "115px", "color": "silver", "background": "#3B5A7F", "border-radius": 10}
            ),
            dbc.Alert(
                [
                    html.Div(html.Img(src="assets/images/signs/warning_sign.svg"), style={"marginRight": "30px"}),
                    "The first and the last waypoint should always be selected.",
                ],
                className="d-flex align-items-center",
                style={"height": "75px", "color": "gray", "background": "#774E06", "border-radius": 10}
            ),
            html.Div([
                # buttons
                html.Div(dbc.Row([
                    dbc.Col(dbc.Button("Show", id="show_btn", color="light", outline=True, style={"width": "160px"})),
                    dbc.Col(dbc.Button("Generate", id="gen_btn", color="light", outline=True, style={"width": "160px"}))
                ], className="g-0"),
                style={"text-align": "center", "marginBottom": "15px"}),
                # dropdown
                html.Div(dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        id="acc_select",
                        options=[],
                        placeholder="Accelerator",
                        clearable=True,
                        optionHeight=35,
                        multi=False,
                        searchable=True,
                        style={"margin": "auto", "color": "black", "width": "160px"},
                    )),
                    dbc.Col(dcc.Dropdown(
                        id="gyr_select",
                        options=[],
                        placeholder="Gyroscope",
                        clearable=True,
                        optionHeight=35,
                        multi=False,
                        searchable=True,
                        style={"margin": "auto", "color": "black", "width": "160px"},
                    ))
                ], className="g-0"),
                style={"marginBottom": "8px"}),
                dcc.Dropdown(
                    id="ref_select",
                    options=[],
                    placeholder="Waypoints",
                    clearable=True,
                    optionHeight=35,
                    multi=False,
                    searchable=True,
                    style={"margin": "auto", "marginBottom": "15px", "color": "black", "width": "324px"},
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
        scrollable=False,
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
                    html.Div(dbc.Button(html.Img(src="assets/images/signs/reset_sign.svg", id="ss_reset_img"), id="ss_reset", style={"border": "0px", "background": "transparent"}),
                        style={"text-align": "right","marginTop": "-39px", "marginRight": "-5px"}),
                    html.Hr(style={"margin": "auto", "width": "100%", "color": "silver", "height": "3px", "marginBottom": "-10px"}),
                    html.Br(),

                    html.P("Number of Intervals", style={"text-align": "center", "color": "silver", "marginBottom": "2px"}),
                    html.Div(dbc.Input(id="num_int", placeholder="Type a number...", type="text", style={"color": "silver", "textAlign": "center"})),

                    html.P("Interval Range [sec]", style={"text-align": "center", "color": "silver", "marginBottom": "0px", "marginTop": "10px"}),
                    dcc.RangeSlider(id="int_rang", min=0, max=30),
                    html.Div(dbc.Row([dbc.Col(html.P(id="int_rang_min")), dbc.Col(html.P(id="int_rang_max", style={"text-align": "right"}))]), style={"margin": "auto", "marginTop": "-25px", "width": "280px"}),
                    
                    html.P("Semantic Error [m]", style={"text-align": "center", "color": "silver", "marginBottom": "0px", "marginTop": "-20px"}),
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
        scrollable=False,
        title="Simulation Settings",
        is_open=False)
    ])

    return sim_set_canvas


def sim_layout(geojson_style):

    ### DOWNLOAD
    export = dcc.Download(id="sim_export")
    example_data = dcc.Download(id="sim_exdata_dl")

    ### UPLOAD
    ## Buttons
    # maps and waypoints
    ul_buttons1 = html.Div([
        dcc.Upload(
            id="sim_ul_map",
            children=html.Div(dbc.Button("Maps", id="sim_maps_upload", color="info", outline=True, style={"width": "148px"})),
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
            multiple=False)],
        style={"width": "150px"}
    )
    # gyroscope, acceleration, barometer and magnetometer
    ul_buttons2 = html.Div(dbc.Row([
        dbc.Col(html.Div([  # left column
            dcc.Upload(
                id="sim_ul_gyr",
                children=html.Div(dbc.Button("G", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True,
                style={"marginBottom": "6px"}),
            dcc.Upload(
                id="sim_ul_acc",
                children=html.Div(dbc.Button("A", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True)],
            style={"textAlign": "left", "marginTop": "18px", "marginBottom": "18px"})),
        dbc.Col(html.Div([  # right column
            dcc.Upload(
                id="sim_ul_bar",
                children=html.Div(dbc.Button("B", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True,
                style={"marginBottom": "6px"}),
            dcc.Upload(
                id="sim_ul_mag",
                children=html.Div(dbc.Button("M", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True)],
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
        "color": "gray",
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
            style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "180px", "width": "435px", "marginBottom": "4px", "display": "inline-block"})),

            dbc.Col(html.Div([
                html.Div(
                    [
                        html.H5("Simulation", style=H5_style),
                        html.Div(dbc.Button(html.Img(src="assets/images/signs/settings_sign.svg", id="sim_set_img"), id="sim_set", style={"border": "0px", "background": "transparent"}),
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
                                        html.Div(html.P("Semantic Error"),
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
                                id="open_sim",
                                color="light",
                                outline=False,
                                style={"line-height": "1.5", "height": "124px", "width": "70px", "padding": "0px"}),
                                style={"marginTop": "6px", "marginLeft": "-17px"}),
                            style={"text-align": "center", "margin": "auto"},
                        width=2
                        )
                    ],
                className="g-0")],
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "180px", "width": "435px", "marginBottom": "4px", "display": "inline-block"}
            )),

            dbc.Col(html.Div([
                html.Div(
                    [
                        html.H5("Export", style={"textAlign": "center", "color": "gray", "marginTop": "5px"}),
                        html.Hr(style=hr_style),
                        html.Div(
                            [
                                dbc.Button("Get results",
                                    color="success",
                                    className="position-relative",
                                    outline=True,
                                    style={"width": "150px"},
                                    id="sim_exp_btn",
                                )
                            ],
                            style={"textAlign": "center", "marginTop": "10px"}
                        )
                    ],            
                    style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "100px", "width": "435px"}
                ),
                html.Div([
                    html.Div(dbc.Button("Help", id="sim_help_btn", color="warning", outline=False, style={"width": "150px"}), style={"textAlign": "center", "marginTop": "19px"})],
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "76px", "width": "435px", "marginTop": "4px", "marginBottom": "4px"})], style={"display": "inline-block"}))
        ],
        className="g-0")
    ], style={"text-align": "center"})

    ### returning filled Card
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    # storage
                    storage(),
                    # download
                    export,
                    example_data,
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
            dbc.CardFooter(f"Copyright © {datetime.date.today().strftime('%Y')} Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
        ]
    )


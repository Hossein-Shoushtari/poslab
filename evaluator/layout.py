##### Layout Evaluator
### IMPORTS
# dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import html, dcc
import dash_leaflet as dl
# utils (general & evaluator)
import evaluator.utils as eu
import utils as u
# built in
import datetime

def storage():
    ### STORAGE
    # dcc.Store to store and share data between callbacks
    storage = html.Div([
        # layers
        dcc.Store(id="eval_map_layers", data={"layers": None, "zoom": 0, "center": 0, "date": 0}, storage_type="memory"),
        dcc.Store(id="eval_gt_layers", data={"layers": None, "zoom": 0, "center": 0, "date": 0}, storage_type="memory"),
        dcc.Store(id="eval_traj_layers", data={"layers": None, "zoom": 0, "center": 0, "date": 0}, storage_type="memory"),
        # password status
        dcc.Store(id="eval_unlocked1", data=[], storage_type="memory"),
        dcc.Store(id="eval_unlocked2", data=[], storage_type="memory"),
        dcc.Store(id="eval_unlocked3", data=[], storage_type="memory"),
        # HistoNorm checkboxes
        dcc.Store(id="norm_status", data=[], storage_type="memory"),
        dcc.Store(id="histo_status", data=[], storage_type="memory")
    ])
    return storage

def tooltips():
    # tooltips for more information
    tooltips = html.Div([
        dbc.Tooltip("geojson",              target="eval_maps_upload",   placement="top"),
        dbc.Tooltip("geojson",              target="paths_upload",       placement="top"),
        dbc.Tooltip("csv",                  target="gt_upload",          placement="right"),
        dbc.Tooltip("csv",                  target="trajectory_upload",  placement="right"),
        dbc.Tooltip("gyroscope | csv",      target="eval_ul_gyr",        placement="top"),
        dbc.Tooltip("accelerator | csv",    target="eval_ul_acc",        placement="bottom"),
        dbc.Tooltip("barometer | csv",      target="eval_ul_bar",        placement="top"),
        dbc.Tooltip("magnetometer | csv",   target="eval_ul_mag",        placement="bottom"),
        dbc.Tooltip("focus",                target="eval_zoom_img",      placement="right")
    ])
    return tooltips

def spinners():
    ### SPINNERs
    spin1 = dbc.Spinner(
        children=[html.Div(id="eval_spin1", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin2 = dbc.Spinner(
        children=[html.Div(id="eval_spin2", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin3 = dbc.Spinner(
        children=[html.Div(id="eval_spin3", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin4 = dbc.Spinner(
        children=[html.Div(id="eval_spin4", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin5 = dbc.Spinner(
        children=[html.Div(id="map_spin", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    spin6 = dbc.Spinner(
        children=[html.Div(id="eval_spin6", style={"display": "none"})],
        type=None,
        fullscreen=True,
        fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
        spinnerClassName="spinner"
    )
    return html.Div([spin1, spin2, spin3, spin4, spin5, spin6])

def modals():
    ### MODALs
    modals = html.Div(
        [
            # login and registration
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/error_sign.svg"), style={"margin-right": "30px"}),
                            "Please login first!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(255, 0, 0, 0.3)", "border-radius": 5, "border": "1px solid #FF0000", "height": "70px"}
                ),
                id="eval_usr_warn1",
                is_open=False
            ),
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/error_sign.svg"), style={"margin-right": "30px"}),
                            "Please login first!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(255, 0, 0, 0.3)", "border-radius": 5, "border": "1px solid #FF0000", "height": "70px"}
                ),
                id="eval_usr_warn2",
                is_open=False
            ),
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/error_sign.svg"), style={"margin-right": "30px"}),
                            "Please login first!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(255, 0, 0, 0.3)", "border-radius": 5, "border": "1px solid #FF0000", "height": "70px"}
                ),
                id="eval_usr_warn3",
                is_open=False
            ),
            # upload warning
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/error_sign.svg"), style={"margin-right": "30px"}),
                            "Wrong file format!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(255, 0, 0, 0.3)", "border-radius": 5, "border": "1px solid #FF0000", "height": "70px"}
                ),
                id="eval_ul_warn",
                is_open=False
            ),
            # upload done
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/done_sign.svg"), style={"margin-right": "30px"}),
                            "Upload successful!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(0, 179, 0, 0.3)", "border-radius": 5, "border": "1px solid #00b300", "height": "70px"}
                ),
                id="eval_ul_done",
                is_open=False
            ),
            # map warning
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/error_sign.svg"), style={"margin-right": "30px"}),
                            "Wrong file format!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(255, 0, 0, 0.3)", "border-radius": 5, "border": "1px solid #FF0000", "height": "70px"}
                ),
                id="eval_map_warn",
                is_open=False
            ),
            # map display done
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/done_sign.svg"), style={"margin-right": "30px"}),
                            "Successful!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(0, 179, 0, 0.3)", "border-radius": 5, "border": "1px solid #00b300", "height": "70px"}
                ),
                id="eval_display",
                is_open=False
            ),
            # cdf warning
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/caution_sign.svg"), style={"margin-right": "30px"}),
                            "Please select data first!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(243, 156, 18, 0.3)", "border-radius": 5, "border": "1px solid #F39C12", "height": "70px"}
                ),
                id="cdf_warn",
                is_open=False
            ),
            # cdf graph
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("CDF Plot")),
                    dbc.ModalBody(
                        dcc.Graph(figure={}, config={
                            "staticPlot": False,     # True, False
                            "scrollZoom": True,      # True, False
                            "doubleClick": False,    # "reset", "autosize" or "reset+autosize", False
                            "showTips": True,        # True, False
                            "displayModeBar": True,  # True, False, "hover"
                            "watermark": True,
                            "toImageButtonOptions": {
                                "format": "png",      # one of png, svg, jpeg, webp
                                "filename": "cdf_plot",
                                "scale": 1              # multiply title/legend/axis/canvas sizes by this factor
                            }
                            },
                            id="graph",
                            className="six columns")
                        )
                ],
                id="cdf_show",
                size="xl",
                backdrop="static",
                is_open=False
            ),
            # visual
            visual_modal(),
            # export warning
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/caution_sign.svg"), style={"margin-right": "30px"}),
                            "Nothing to export!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(243, 156, 18, 0.3)", "border-radius": 5, "border": "1px solid #F39C12", "height": "70px"}
                ),
                id="eval_exp_warn",
                is_open=False
            ),
            # export done
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/svg/signs/done_sign.svg"), style={"margin-right": "30px"}),
                            "Export successful!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(0, 179, 0, 0.3)", "border-radius": 5, "border": "1px solid #00b300", "height": "70px"}
                ),
                id="eval_exp_done",
                is_open=False
            )
        ]
    )
    return modals

def eval_map(geojson_style):
    ### MAP
    # info panel for hcu maps
    info = html.Div(
        children=u.hover_info(),
        id="eval_hover_info",
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
    # zoom botton
    focus_style = {
        "position": "absolute",
        "top": "110px",
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
        "top": "150px",
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
                html.Div(id="eval_hcu_panel", children=info, style={"display": "None"}),
                html.Button(html.Img(src="assets/images/svg/signs/focus_sign2.svg", id="eval_zoom_img"), id="eval_zoom", style=focus_style),
                html.Button(html.Img(src="assets/images/svg/signs/research_sign.svg"), id="eval_hcu_maps", style=research_style),
                dl.TileLayer(url=url, maxZoom=20, attribution=attribution), # Base layer (OpenStreetMap)
                html.Div(id="eval_div_lc", children=dl.LayersControl(id="eval_lc", children=eu.floorplan2layer(geojson_style)), style={"display": "None"}), # is previously filled with invisible floorplans for initialization
                dl.FullscreenControl(), # possibility to get map fullscreen
            ],
            style={"width": "100%", "height": "70vh", "margin": "auto", "display": "block", "border-radius": 10},
            id="eval_map",
            bounds=[[35.81781315869664, -47.90039062500001], [60.71619779357716, 67.67578125000001]] # center of Europe as centroid
        )
    )
    return _map

def cdf_canvas():
    ## OFFCANVAS
    # CDF
    cdf_canvas = html.Div([
        dbc.Offcanvas(
            [
                html.Div([
                    html.Div([
                        dbc.Label("Ground Truth", style={"color": "silver"}),
                        dcc.Dropdown(
                            id="eval_gt_select",
                            options=[],
                            placeholder="Select Data",
                            clearable=True,
                            optionHeight=35,
                            multi=False,
                            searchable=True,
                            style={"marginBottom": "15px", "color": "black"}
                        ),
                        dbc.Label("Trajectory", style={"color": "silver"}),
                        dcc.Dropdown(
                            id="traj_select",
                            options=[],
                            placeholder="Select Data",
                            clearable=True,
                            optionHeight=35,
                            multi=True,
                            searchable=True,
                            style={"marginBottom": "15px", "color": "black"}
                        ),
                        html.Hr(style={"margin": "auto", "width": "80%", "color": "silver", "marginBottom": "3px"}),
                        dbc.Label("MAP (optional ➔ check 'Percentage')", style={"color": "silver"}),
                        dcc.Dropdown(
                            id="map_select",
                            options=[],
                            placeholder="Select Data",
                            clearable=True,
                            optionHeight=35,
                            multi=False,
                            searchable=True,
                            style={"marginBottom": "15px", "color": "black"}
                        )],
                        style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "paddingBottom": "5px", "marginBottom": "10px"}),
                    html.Div(dbc.Button("Show CDF", color="light", outline=True, id="cdf_btn"), style={"textAlign": "right"})])
            ],
        id="cdf_cv",
        scrollable=False,
        title="CDF",
        is_open=False)
    ])
    return cdf_canvas

def visual_modal():
    map_bgs = ["basic", "carto-darkmatter", "carto-positron", "dark", "light", "outdoors", "satellite", "satellite-streets", "stamen-terrain", "stamen-toner", "stamen-watercolor", "streets", "white-bg"]
    visual_modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("VISUAL")),
            dbc.ModalBody([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Background", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_bg_select",
                                options=[{"label": bg, "value": bg} for bg in map_bgs],
                                value="carto-darkmatter",
                                placeholder="Select Background",
                                clearable=True,
                                optionHeight=35,
                                multi=False,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Format [2kx1k]", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_format_select",
                                options=[{"label": f.upper(), "value": f} for f in ["png", "svg", "jpeg", "webp"]],
                                value="png",
                                placeholder="Select Format",
                                clearable=True,
                                optionHeight=35,
                                multi=False,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Waypoints", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_ref_select",
                                options=[],
                                placeholder="Select Data",
                                clearable=True,
                                optionHeight=35,
                                multi=True,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Ground Truth", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_gt_select",
                                options=[],
                                placeholder="Select Data",
                                clearable=True,
                                optionHeight=35,
                                multi=True,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Trajectories", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_traj_select",
                                options=[],
                                placeholder="Select Data",
                                clearable=True,
                                optionHeight=35,
                                multi=True,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Antennas", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_ant_select",
                                options=[],
                                placeholder="Select Data",
                                clearable=True,
                                optionHeight=35,
                                multi=False,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ]),
                        dbc.Col([
                            dbc.Label("Maps", style={"color": "silver"}),
                            dcc.Dropdown(
                                id="vis_map_select",
                                options=[],
                                placeholder="Select Data",
                                clearable=True,
                                optionHeight=35,
                                multi=False,
                                searchable=True,
                                style={"marginBottom": "7px", "color": "black"})
                        ])
                    ])],
                    style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}
                ),
                dcc.Graph(
                    id="vis_map",
                    config={
                        "staticPlot": False,        # True, False
                        "scrollZoom": True,         # True, False
                        "showTips": True,           # True, False
                        "displayModeBar": "hover",  # True, False, "hover"
                        "watermark": True,
                        "editable": True,
                        "toImageButtonOptions": {
                            "format": "png",      # one of png, svg, jpeg, webp
                            "filename": "map_plot",
                            "height": 1000,
                            "width": 2000,
                            "scale": 1              # multiply title/legend/axis/canvas sizes by this factor
                        },
                        "modeBarButtonsToAdd": [
                            "drawline",
                            "drawopenpath",
                            "drawclosedpath",
                            "drawcircle",
                            "drawrect",
                            "eraseshape"
                        ]
                    },
                    className="six columns",
                    style={"height": "660px"})
            ]),
            dbc.ModalFooter(html.Div(f"© {datetime.date.today().strftime('%Y')} Level 5 Indoor Navigation Plus. All Rights Reserved", style={"textAlign": "center", "width": "100%"}))
        ],
        id="visual_show",
        fullscreen=True,
        backdrop="static",
        scrollable=True,
        is_open=False
    )
    return visual_modal

def help_canvas():
    help_canvas = html.Div([
        dbc.Offcanvas(
            [
                dbc.Alert(
                    [
                        html.Div(html.Img(src="assets/images/svg/signs/focus_sign1.svg"), style={"margin-right": "10px"}),
                        "Use the focus tool on the map to restore the last view!"
                    ],
                    className="d-flex align-items-center",
                    style={"height": "75px", "color": "silver", "background": "rgba(81, 155, 214, 0.3)", "border-radius": 10, "border": "1px solid #519bd6", "color": "gray"}
                ),
                dbc.Alert(
                    [
                        html.Button(html.Img(src="assets/images/svg/signs/download_sign.svg", style={"margin-left": "-8px"}), id="eval_exdata", style={"margin-right": "10px", "width": "48px", "background": "transparent", "border": "0px"}),
                        html.Div(
                            [
                                html.P("Not sure about the file formats?", style={"margin-bottom": "0px"}),
                                html.P("Download example data here!", style={"margin-bottom": "0px"}),
                            ]
                        ),
                    ],
                    className="d-flex align-items-center",
                    style={"height": "75px", "color": "silver", "background": "rgba(0, 128, 0, 0.3)", "border-radius": 10, "border": "1px solid #008000", "color": "gray"}
                ),
                dbc.Alert(
                    [
                        html.Div(html.Img(src="assets/images/svg/signs/bug_sign.svg"), style={"margin-right": "10px"}),
                        html.Div(
                            [
                                html.P("Are the layer names mixed up?", style={"margin-bottom": "0px"}),
                                html.P("Just switch tabs and come back!", style={"margin-bottom": "0px"}),
                            ]
                        ),
                    ],
                    className="d-flex align-items-center",
                    style={"height": "75px", "color": "silver", "background": "rgba(255, 0, 0, 0.3)", "border-radius": 10, "border": "1px solid #FF0000", "color": "gray"}
                ),
                html.Div([
                    # info upload
                    html.H5("UPLOAD", style={"text-align": "center", "color": "#3B5A7F"}),
                    html.Hr(style={"margin": "auto", "width": "80%", "color": "silver", "marginBottom": "3px"}),
                    html.P("All buttons are for uploading the data required for evaluation. Each file needs the first line as a header. The delimiter is a single space.", style={"color": "gray"}),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Maps", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("optional; GeoJSON, any CRS", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Paths", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("temporarily unavailable", style={"color": "gray", "font-style": "italic"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Ground Truth", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("optional; CSV, UTM", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Trajectory", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("optional; CSV, UTM", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Sensors", style={"color": "gray"}), style={"borderLeft": "2px solid #7C9D9C", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("optional; CSV", style={"color": "gray"}))
                    ], className="g-0")],
                style={"border":"1px solid #3B5A7F", "border-radius": 10, "padding": "10px", "marginBottom": "16px"}),
                html.Div([
                    # info evaluation
                    html.H5("EVALUATION", style={"text-align": "center", "color": "silver"}),
                    html.Hr(style={"margin": "auto", "width": "80%", "color": "silver", "marginBottom": "3px"}),
                    html.P("Instructions for evaluating results:", style={"color": "gray"}),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("CDF", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("graph either normalized or histogrammed cumulative distribution function", style={"color": "gray"}))
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(html.P("Visual", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=4),
                        dbc.Col(html.P("view all layers on a selected map background and plot it as an image", style={"color": "gray"}))
                    ], className="g-0")],
                style={"border":"1px solid silver", "border-radius": 10, "padding": "10px", "marginBottom": "10px"})
            ],
        id="eval_help_cv",
        scrollable=False,
        title="Help",
        is_open=False)
    ])
    return help_canvas


def eval_layout(geojson_style):
    ### DOWNLOAD
    export = dcc.Download(id="eval_export")
    example_data = dcc.Download(id="eval_exdata_dl")

    ### UPLOAD
    ## Buttons
    # maps and waypoints
    ul_buttons1 = html.Div([
        dbc.Row(
            [
                dbc.Col(
                    dcc.Upload(
                        id="eval_ul_map",
                        children=html.Div(dbc.Button("Maps", id="eval_maps_upload", color="info", outline=True, style={"width": "72px"})),
                        style={"marginTop": "8px", "marginBottom": "0px", "width": 75},
                        multiple=True)),
                dbc.Col(
                    dcc.Upload(
                        id="ul_paths",
                        children=html.Div(dbc.Button("Paths", id="paths_upload", color="info", outline=True, style={"width": "73px"})),
                        style={"marginTop": "8px", "marginBottom": "0px", "width": 75},
                        multiple=True))
            ],
            className="g-0"
        ),
        dcc.Upload(
            id="ul_gt",
            children=html.Div(dbc.Button("Ground Truth", id="gt_upload", color="info", outline=True, style={"width": "148px"})),
            style={"marginTop": "5px", "marginBottom": "5px"},
            multiple=True),
        dcc.Upload(
            id="ul_tra",
            children=html.Div(dbc.Button("Trajectory", id="trajectory_upload", color="info", outline=True, style={"width": "148px"})),
            style={"marginTop": "5px", "marginBottom": "8px"},
            multiple=True)],
        style={"width": "150px"}
    )
    # gyroscope, acceleration, barometer and magnetometer
    ul_buttons2 = html.Div(dbc.Row([
        dbc.Col(html.Div([  # left column
            dcc.Upload(
                id="eval_ul_gyr",
                children=html.Div(dbc.Button("G", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True,
                style={"marginBottom": "6px"}),
            dcc.Upload(
                id="eval_ul_acc",
                children=html.Div(dbc.Button("A", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True)],
            style={"textAlign": "left", "marginTop": "18px", "marginBottom": "18px"})),
        dbc.Col(html.Div([  # right column
            dcc.Upload(
                id="eval_ul_bar",
                children=html.Div(dbc.Button("B", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True,
                style={"marginBottom": "6px"}),
            dcc.Upload(
                id="eval_ul_mag",
                children=html.Div(dbc.Button("M", color="primary", size="lg", outline=True, style={"width": "86px"})),
                multiple=True)],
            style={"textAlign": "right", "marginTop": "18px", "marginBottom": "18px"}))],
        className="g-0"),
        style={"width": "180px"}
    )

    ### EVALUATION
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
                html.H5("Evaluation", style=H5_style),
                html.Hr(style=hr_style),
                dbc.Row(
                    [
                        dbc.Col(html.Div(dbc.Button(
                                "CDF",
                                id="open_cdf",
                                color="light",
                                outline=False,
                                style={"line-height": "1.5", "height": "124px", "width": "70px", "padding": "0px"}),
                                style={"marginTop": "3px"}),
                            style={"text-align": "center", "width": "90px", "margin": "auto", "marginRight": "-2px", "marginBottom": "2px"},
                            width=2
                        ),

                        dbc.Col(html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(html.P("Normalized"),
                                            style={"width": "118px", "height": "29px", "text-align": "center"}),
                                        html.Div(dbc.Checklist(options=[{"value": 1}], value=[1], id="norm_box", style={"marginLeft": "50px"}),
                                            style={"width": "118px", "height": "29px" }
                                        )
                                    ],
                                    style={"marginTop": "4px", "border": "1px solid #808080", "border-radius": "5px", "height": "60px",  "text-align": "center"}
                                ),
                                html.Div(
                                    [
                                        html.Div(html.P("ATE Table"),
                                            style={"width": "118px", "height": "29px", "text-align": "center"}),
                                        html.Div(dbc.Checklist(options=[{"value": 0, "disabled": True}], value=[1], id="ate", style={"marginLeft": "50px"}),
                                            style={"width": "118px", "height": "29px" }
                                        )
                                    ],
                                    style={"marginTop": "4px", "border": "1px solid #808080", "border-radius": "5px", "height": "60px",  "text-align": "center"}
                                )
                            ],
                            style={"width": "120px", "margin": "auto", "marginTop": "8px", "marginLeft": "0px", "height": "126px"})
                        ),

                        dbc.Col(html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(html.P("Histogram"),
                                            style={"width": "118px", "height": "29px", "text-align": "center"}),
                                        html.Div(dbc.Checklist(options=[{"value": 1}], value=[1], id="histo_box", style={"marginLeft": "50px"}),
                                            style={"width": "118px", "height": "29px" }
                                        )
                                    ],
                                    style={"marginTop": "4px", "border": "1px solid #808080", "border-radius": "5px", "height": "60px",  "text-align": "center"}
                                ),
                                html.Div(
                                    [
                                        html.Div(html.P("Percentage"),
                                            style={"width": "118px", "height": "29px", "text-align": "center"}),
                                        html.Div(dbc.Checklist(options=[{"value": 1}], value=[1], id="percent", style={"marginLeft": "50px"}),
                                            style={"width": "118px", "height": "29px" }
                                        )
                                    ],
                                    style={"marginTop": "4px", "border": "1px solid #808080", "border-radius": "5px", "height": "60px",  "text-align": "center"}
                                )
                            ],
                            style={"width": "120px", "margin": "auto", "marginTop": "8px", "marginLeft": "-10px", "height": "126px"})
                        ),

                        dbc.Col(html.Div(dbc.Button(
                                "Visual",
                                id="open_visual",
                                color="light",
                                outline=False,
                                style={"line-height": "1.5", "height": "70px", "width": "70px", "padding": "0px"}),
                                style={"marginTop": "15px", "marginBottom": "15px"}),
                            style={"text-align": "center", "width": "90px", "margin": "auto", "marginLeft": "-11px", "borderLeft": "1px solid #494949"},
                        width=2
                        )
                    ],
                className="g-0")
                ],
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
                                    id="eval_exp_btn",
                                )
                            ],
                            style={"textAlign": "center", "marginTop": "10px"}
                        )
                    ],            
                    style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "100px", "width": "435px"}
                ),
                html.Div([
                    html.Div(dbc.Button("Help", id="eval_help_btn", color="warning", outline=False, style={"width": "150px"}), style={"textAlign": "center", "marginTop": "19px"})],
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
                    cdf_canvas(),
                    # card content
                    html.Div(
                        [
                            html.Br(),
                            html.Br(),
                            first_row,
                            html.Br(),
                            dbc.Row(eval_map(geojson_style))
                        ]
                    ),
                    # spinners
                    spinners(),
                    # tooltips
                    tooltips()
                ]
            ),
            dbc.CardFooter(
                f"© {datetime.date.today().strftime('%Y')} Level 5 Indoor Navigation Plus. All Rights Reserved",
                class_name="eval-footer"
            )
        ]
    )


##### Evaluator Tab -- Layout
###IMPORTS
# dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_leaflet as dl
# utils (simulator)
import simulator.utils as su


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
        dbc.Tooltip("magnetometer | csv",   target="eval_ul_mag",        placement="bottom")
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
        children=[html.Div(id="eval_spin5", style={"display": "none"})],
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
        id="eval_ul_warn",
        is_open=False
    )
    # upload done
    ul_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("File(s) uploaded successfully!")],
        id="eval_ul_done",
        is_open=False
    )
    # cdf warning
    cdf_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Select data first!")],
        id="cdf_warn",
        is_open=False
    )
    graph_modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("CDF Plot")),
            dbc.ModalBody(
                dcc.Graph(figure={}, config={
                    'staticPlot': False,     # True, False
                    'scrollZoom': True,      # True, False
                    'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                    'showTips': True,        # True, False
                    'displayModeBar': True,  # True, False, 'hover'
                    'watermark': True
                    },
                    id="graph",
                    className="six columns")
                )
        ],
        id="cdf_show",
        size="xl",
        backdrop="static",
        is_open=False
    )
    # export warning
    exp_warn = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Nothing to export!")],
        id="eval_exp_warn",
        is_open=False
    )
    # export done
    exp_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("Export successful!")],
        id="eval_exp_done",
        is_open=False
    )
    return html.Div([ul_warn, ul_done, cdf_warn, graph_modal, exp_warn, exp_done])

def eval_map(geojson_style):
    ### MAP
    # info panel for hcu maps
    info = html.Div(
        children=su.hover_info(),
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
    # unlock hcu maps button
    btn_style = {
        "position": "absolute",
        "top": "110px",
        "left": "10px",
        "z-index": "500",
        "backgroundColor": "white",
        "border": "2px solid #B2AFAC",
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
                html.Button("🎓", id="eval_hcu_maps", style=btn_style),
                dl.TileLayer(url=url, maxZoom=20, attribution=attribution), # Base layer (OpenStreetMap)
                #html.Div(id="eval_layers", children=html.Div(dl.LayersControl(), style={"display": "None"})), # is previously filled with invisible floorplans for initialization
                dl.FullscreenControl(), # possibility to get map fullscreen
            ],
            style={"width": "100%", "height": "70vh", "margin": "auto", "display": "block"},
            center=(49.845359730413186, 9.90578149727622),
            zoom=4,
            id="eval_map"
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

def help_canvas():
    ## OFFCANVAS
    # HELP
    help_canvas = html.Div([
        dbc.Offcanvas(
            [
                html.Div()
            ],
        id="eval_help_cv",
        scrollable=True,
        title="Help",
        is_open=False)
    ])
    return help_canvas


def eval_layout(geojson_style):
    ### DOWNLOAD
    export = dcc.Download(id="eval_export")

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
                        style={"marginTop": "8px", "marginBottom": "0px"},
                        multiple=True)),
                dbc.Col(
                    dcc.Upload(
                        id="ul_paths",
                        children=html.Div(dbc.Button("Paths", id="paths_upload", color="info", outline=True, style={"width": "73px"})),
                        style={"marginTop": "8px", "marginBottom": "0px"},
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
            style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "180px", "width": "435px", "marginBottom": "4px"})),

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
                                        html.Div(dbc.Checklist(options=[{"value": 1, "disabled": True}], value=[1], id="norm", style={"marginLeft": "50px"}),
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
                                        html.Div(dbc.Checklist(options=[{"value": 0, "disabled": True}], value=[1], id="histo", style={"marginLeft": "50px"}),
                                            style={"width": "118px", "height": "29px" }
                                        )
                                    ],
                                    style={"marginTop": "4px", "border": "1px solid #808080", "border-radius": "5px", "height": "60px",  "text-align": "center"}
                                ),
                                html.Div(
                                    [
                                        html.Div(html.P("Percentage"),
                                            style={"width": "118px", "height": "29px", "text-align": "center"}),
                                        html.Div(dbc.Checklist(options=[{"value": 1}], value=[0], id="percent", style={"marginLeft": "50px"}),
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
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "180px", "width": "435px", "marginBottom": "4px"}
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
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "76px", "width": "435px", "marginTop": "4px", "marginBottom": "4px"})]))
        ],
        className="g-0")
    ])

    ### returning filled Card
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    # download
                    export,
                    # modals
                    modals(),
                    # canvas
                    help_canvas(),
                    cdf_canvas(),
                    # card content
                    html.Div(
                        [
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
            dbc.CardFooter("Copyright © 2022 Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
        ]
    )



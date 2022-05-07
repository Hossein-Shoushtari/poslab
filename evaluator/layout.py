##### Simulator Tab -- Layout
###IMPORTS
# dash
from dash import html, dcc
import dash_bootstrap_components as dbc
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
            id="eval_map"
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
                        dbc.Col(html.Div(html.P("Semantic Error", style={"color": "gray"}), style={"borderLeft": "2px solid white", "paddingLeft": "5px"}), width=5),
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
            id="ul_traj",
            children=html.Div(dbc.Button("Trajectory", id="trajectory_upload", color="info", outline=True, style={"width": "148px"})),
            style={"marginTop": "5px", "marginBottom": "8px"},
            multiple=False)],
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
                html.H5("Evaluation", style=H5_style),
                html.Hr(style=hr_style),
                dbc.Row(
                    [
                        dbc.Col(html.Div(dbc.Button(
                                "CDF",
                                id="cdf_btn",
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
                                        html.Div(dbc.Checklist(options=[{"value": 1}], value=[0], id="norm", style={"marginLeft": "50px"}),
                                            style={"width": "118px", "height": "29px" }
                                        )
                                    ],
                                    style={"marginTop": "4px", "border": "1px solid #808080", "border-radius": "5px", "height": "60px",  "text-align": "center"}
                                ),
                                html.Div(
                                    [
                                        html.Div(html.P("ATE"),
                                            style={"width": "118px", "height": "29px", "text-align": "center"}),
                                        html.Div(dbc.Checklist(options=[{"value": 1}], value=[0], id="ate", style={"marginLeft": "50px"}),
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
                                        html.Div(dbc.Checklist(options=[{"value": 1}], value=[0], id="histo", style={"marginLeft": "50px"}),
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
                        html.H5("Export", style={"textAlign": "center", "color": "grey", "marginTop": "5px"}),
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
                    # canvas
                    help_canvas(),
                    # card content
                    html.Div(
                        [
                            first_row,
                            html.Br(),
                            dbc.Row(eval_map(geojson_style))
                        ]
                    ),
                    # tooltips
                    tooltips()
                ]
            ),
            dbc.CardFooter("Copyright © 2022 Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
        ]
    )



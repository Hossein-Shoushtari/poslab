import os
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from simulator_func import default_layers
from dash_extensions.javascript import arrow_function
from geopandas import GeoDataFrame, read_file
from base64 import b64decode
from simulator_func import hover_info

def simulator_card(geojson_style):
    ### MAP
    # info panel for geojson layer segments (tooltips while hovering)
    info = html.Div(children=hover_info(), id="hover_info",
                style={
                    "position": "absolute",
                    "top": "10px",
                    "right": "120px",
                    "z-index": "1000",
                    "color": "black",
                    "backgroundColor": "white",
                    "opacity": "0.6",
                    "border": "2px solid #B2AFAC",
                    "border-radius": 5,
                    "padding": "10px",
                    "width": "240px"})
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
                html.Div(id="layers", children=dl.LayersControl(default_layers(geojson_style))), # default layers + later all uploaded new layers
                dl.FullscreenControl(), # possibility to get map fullscreen
                dl.FeatureGroup(dl.EditControl(id="edit_control")), # possibility to draw/edit data
                
            ],
            zoom=19,
            center=hcu,
            style={'width': '100%', 'height': '70vh', 'margin': "auto", "display": "block"}
        )
    )
    
    ### MODALs
    # upload warning
    ul_warning = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("WARNING")),
        dbc.ModalBody("Wrong file was uploaded!")],
        id="ul_warn",
        is_open=False
    )
    # upload done
    ul_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("File uploaded successfully!")],
        id="ul_done",
        is_open=False
    )
    # export warning
    exp_warning = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CAUTION")),
        dbc.ModalBody("Nothing to export yet!")],
        id="exp_warn",
        is_open=False
    )
    # export done
    exp_done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("Drawn data successfully exported!")],
        id="exp_done",
        is_open=False
    )

    ### UPLOAD
    # tooltips for more information
    ul_tt = html.Div([
        dbc.Tooltip("geojson",              target="maps_upload",      placement="right"),
        dbc.Tooltip("txt, csv or geojson",  target="waypoints_upload", placement="right"),
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
            dbc.Button("Calculate ground truth", id="calc", color="light", outline=True, style={"width": "200px"}),
            style={"marginBottom": "5px"}),
        html.Div(
            dbc.Button("Simulate measurement", id="sim", color="light", outline=True, style={"width": "200px"}),
            style={"marginTop": "5px"})            
    ])

    ## OFFCANVAS
    ## putting everything it its appropriate offcanvas
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
    # offcanvas
    help_canvas = html.Div([
        dbc.Offcanvas(
            [   
                html.Div([
                    # info bug
                    html.P("🐞 Something's wrong with the map?"),
                    html.P("Just scale your browser window smaller and then back to normal or simply click the FullScreen Button right under the zoom section.", style={"color": "gray"})],
                style={"border":"1px solid red", "border-radius": 10, "padding": "10px", "marginBottom": "10px"}),
                html.Div([
                    # info upload
                    html.P("⚠  Please note:"),
                    html.P("Only GeoJSON files of type crs:32632 or directly crs:4326 are accepted as Maps.", style={"color": "gray"}),
                    html.P("Both Waypoints and Antennas accept TXT, CSV or GeoJSON.", style={"color": "gray", "marginTop": "-10px"})],
                style={"border":"1px solid orange", "border-radius": 10, "padding": "10px"})
            ],
        id="help_cv",
        scrollable=True,
        title="Help",
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
                html.Div([
                    html.H5("Export", style=H5_style),
                    html.Hr(style=hr_style),
                    html.Div(dbc.Button("Get results", id="exp_btn", color="success", outline=True, style={"width": "150px"}), style={"textAlign": "center", "marginTop": "10px"})],
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "100px", "width": "435px"}),
                html.Div([
                    html.Div(dbc.Button("Help", id="help_btn", color="warning", outline=False, style={"width": "150px"}), style={"textAlign": "center", "marginTop": "19px"})],
                style={"border":"1px solid", "border-radius": 10, "color": "orange", "height": "76px", "width": "435px", "marginTop": "4px", "marginBottom": "4px"})]))
        ],
        className="g-0")
    ])

    ### returning filled Card
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    # modals, giving alert
                    ul_warning,
                    ul_done,
                    exp_warning,
                    exp_done,
                    # tooltips
                    ul_tt,
                    # canvas
                    help_canvas,
                    # card content
                    html.Div(
                        [
                            first_row,
                            html.Br(),
                            dbc.Row(_map)
                        ]
                    )
                ]
            ),
            dbc.CardFooter("Copyright © 2022 Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
        ]
    )



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
    
    ### MODALs
    # warning
    warning = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("WARNING")),
        dbc.ModalBody("Wrong file was uploaded!")],
        id="sim_warning",
        is_open=False
    )
    # done
    done = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("DONE")),
        dbc.ModalBody("File uploaded successfully!")],
        id="sim_done",
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
        'width': '60%',
        'margin': 'auto'
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
            html.Div([
                # info text
                html.P("⚠  Please note:"),
                html.P("Only GeoJSON files of type crs:32632 or directly crs:4326 are accepted as Maps.", style={"textAlign": "left"}),
                html.P(" Both Waypoints and Antennas accept TXT, CSV or GeoJSON.", style={"textAlign": "left", "marginTop": "-10px"})],
            style={"border":"1px solid orange", "border-radius": 10, "padding": "10px"}),
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
                    html.Div(dbc.Button("Get results", id="exp", color="success", outline=True, style={"width": "150px"}), style={"textAlign": "center", "marginTop": "10px"})],
                style={"border":"1px solid", "border-radius": 10, "color": "silver", "height": "100px", "width": "435px"}),
                html.Div([
                    html.Div(dbc.Button("Help", id="help_btn", color="warning", outline=False, style={"width": "150px"}), style={"textAlign": "center", "marginTop": "19px"})],
                style={"border":"1px solid", "border-radius": 10, "color": "orange", "height": "78px", "width": "435px", "marginTop": "4px", "marginBottom": "4px"})]))
        ],
        className="g-0")
    ])

    ### returning filled Card
    return dbc.Card(dbc.CardBody([
        # modals, giving alert
        warning,
        done,
        # tooltips
        ul_tt,
        # canvas
        help_canvas,
        # card content
        html.Div([
            first_row,
            html.Br(),
            dbc.Row(html.Div(id="map"))
        ])
    ]),
    className="mt-3")



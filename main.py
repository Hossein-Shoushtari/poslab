from dash import html, Dash, Output, Input, State, no_update, callback_context
import dash_bootstrap_components as dbc
from simulator_layout import simulator_card
from simulator_func import _map, upload_decoder, crs32632_converter
from evaluator_layout import evaluator_card
from coming_soon_layout import coming_soon_card
from home_layout import home_card
from dash_extensions.javascript import assign

# ---------------- MAP ----------------- #
# Geojson rendering logic, must be JavaScript
geojson_style = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    return style;
}""")

# ---------------- HTML ---------------- #
# designing the webpage using dash
ex_ss = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=ex_ss)
server = app.server
# title
app.title = "L5IN"

### LAYOUT ###
## Home page ##
home_tab_content = home_card()  # getting the card content from home.py
## Simulator ##
sim_tab_content = simulator_card()  # from simulator.py
## Evaluator ##
ev_tab_content = evaluator_card()  # from evaluator.py
## Comming Soon ##
cs_tab_content = coming_soon_card()  # from comming_soon.py    

# putting all together
app.layout = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(home_tab_content, label="Home", active_label_style={"color": "#DC7633"}),
                dbc.Tab(sim_tab_content, label="Simulator", active_label_style={"color": "#DC7633"}),
                dbc.Tab(ev_tab_content, label="Evaluator", active_label_style={"color": "#DC7633"}),
                dbc.Tab(cs_tab_content, label="Coming Soon", disabled=True)
            ]
        )
    ]
)
# ==============================================================================
# handling upload
@app.callback(
    ### Outputs ###
    Output("sim_warning", "is_open"),   # warning
    Output("sim_done", "is_open"),      # done
    Output("map", "children"),          # map
    Output("help_cv", "is_open"),       # help - canvas
    ### Inputs ###
    # modals
    State("sim_warning", "is_open"),
    State("sim_done", "is_open"),
    # canvas
    Input("help_btn", "n_clicks"),   # help
    State("help_cv", "is_open"),     # help
    # maps
    Input("ul_map", "contents"),
    State("ul_map", "filename"),
    # waypoints
    Input("ul_way", "contents"),
    State("ul_way", "filename"),
    # antennas
    Input("ul_ant", "contents"),
    State("ul_ant", "filename"),
    # gyroscope
    Input("ul_gyr", "contents"),
    State("ul_gyr", "filename"),
    # acceleration
    Input("ul_acc", "contents"),
    State("ul_acc", "filename"),
    # barometer
    Input("ul_bar", "contents"),
    State("ul_bar", "filename"),
    # magnetometer
    Input("ul_mag", "contents"),
    State("ul_mag", "filename"),
)
def callback(
    ## modals
    warning_state,
    done_state,
    ## offcanvas
    help_clicks,  # help
    help_state,   # help
    ## upload
    map_contents,  # maps
    map_filenames,
    way_contents,  # waypoints
    way_filenames,
    ant_contents,  # antennas
    ant_filenames,
    #--- sensors
    gyr_contents,  # gyroscope
    gyr_filenames,
    acc_contents,  # acceleration
    acc_filenames,
    bar_contents,  # barometer
    bar_filenames,
    mag_contents,  # magnetometer
    mag_filenames
    ): 
    # getting clicked button
    button = [p["prop_id"] for p in callback_context.triggered][0]
    # =========== CANVAS ============
    # UPLOAD
    if "help_btn" in button: return warning_state, done_state, no_update, not help_state     # activate upload offcanvas
    #============= MAP =============
    elif "ul_map" in button:
        for i in range(len(map_filenames)):
            if map_filenames[i].split(".")[-1] in ["geojson"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(map_contents[i]) # decoding uploaded base64 file
                crs32632_converter(map_filenames[i], decoded_content) # converting EPSG:32632 to WGS84 and saving it in floorplans_converted
            else: return not warning_state, done_state, no_update, help_state # activating modal -> warning    
        # if everything went fine ...
        return warning_state, not done_state, _map(geojson_style), help_state # returning an html.Iframe with refreshed map
    # ========== WAYPOINTS ==========
    elif "ul_way" in button:
        for i in range(len(way_filenames)):
            if way_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(way_contents[i]) # decoding uploaded base64 file
                with open(f"assets/waypoints/{way_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not warning_state, done_state, no_update, help_state # activating modal -> warning    
        # if everything went fine ...
        return warning_state, not done_state, no_update, help_state
    # ========== ANTENNAS ===========
    elif "ul_ant" in button:
        for i in range(len(ant_filenames)):
            if ant_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(ant_contents[i]) # decoding uploaded base64 file
                with open(f"assets/antennas/{ant_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not warning_state, done_state, no_update, help_state # activating modal -> warning    
        # if everything went fine ...
        return warning_state, not done_state, no_update, help_state
    # ========== GYROSCOPE ==========
    elif "ul_gyr" in button:
        for i in range(len(gyr_filenames)):
            if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(gyr_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/{gyr_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not warning_state, done_state, no_update, help_state # activating modal -> warning    
        # if everything went fine ...
        return warning_state, not done_state, no_update, help_state
    # ========= ACCELERATION  =======
    elif "ul_acc" in button:
        for i in range(len(acc_filenames)):
            if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(acc_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/{acc_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not warning_state, done_state, no_update, help_state # activating modal -> warning    
        # if everything went fine ...
        return warning_state, not done_state, no_update, help_state
    # ========= BAROMETER  ==========
    elif "ul_bar" in button:
        for i in range(len(bar_filenames)):
            if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(bar_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/{bar_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not warning_state, done_state, no_update, help_state # activating modal -> warning    
        # if everything went fine ...
        return warning_state, not done_state, no_update, help_state
    # ======== MAGNETOMETER  ========
    elif "ul_mar" in button:
        for i in range(len(mar_filenames)):
            if mar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(mar_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/{mar_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not warning_state, done_state, no_update, help_state # activating modal -> warning    
        # if everything went fine ...
        return warning_state, not done_state, no_update, help_state
    # ====== no button clicked ======
    # this else-section is always activated, when the page refreshes
    else: return warning_state, done_state, _map(geojson_style), help_state # returning the current Iframe/map


# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)

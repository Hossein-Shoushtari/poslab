from dash import html, Dash, Output, Input, State, no_update, callback_context
import dash_bootstrap_components as dbc
from simulator_layout import simulator_card
from simulator_func import _layers, upload_decoder, crs32632_converter, export_data
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
    Output("ul_warn", "is_open"),    # warning
    Output("ul_done", "is_open"),    # done
    Output("layers", "children"),    # layers
    ### Inputs ###
    # modals
    State("ul_warn", "is_open"),
    State("ul_done", "is_open"),
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
def upload(
    ## modals
    ul_warning_state,
    ul_done_state,
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
    # UPLOAD
    #============= MAP =============
    if "ul_map" in button:
        for i in range(len(map_filenames)):
            if map_filenames[i].split(".")[-1] in ["geojson"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(map_contents[i]) # decoding uploaded base64 file
                crs32632_converter(map_filenames[i], decoded_content) # converting EPSG:32632 to WGS84 and saving it in floorplans_converted
            else: return not ul_warning_state, ul_done_state, no_update # activating modal -> warning    
        # if everything went fine ...
        return ul_warning_state, not ul_done_state, _layers(geojson_style) # returning an html.Iframe with refreshed map
    # ========== WAYPOINTS ==========
    elif "ul_way" in button:
        for i in range(len(way_filenames)):
            if way_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(way_contents[i]) # decoding uploaded base64 file
                with open(f"assets/waypoints/{way_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not ul_warning_state, ul_done_state, no_update # activating modal -> warning    
        # if everything went fine ...
        return ul_warning_state, not ul_done_state, no_update
    # ========== ANTENNAS ===========
    elif "ul_ant" in button:
        for i in range(len(ant_filenames)):
            if ant_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(ant_contents[i]) # decoding uploaded base64 file
                with open(f"assets/antennas/{ant_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not ul_warning_state, ul_done_state, no_update # activating modal -> warning    
        # if everything went fine ...
        return ul_warning_state, not ul_done_state, no_update
    # ========== GYROSCOPE ==========
    elif "ul_gyr" in button:
        for i in range(len(gyr_filenames)):
            if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(gyr_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/{gyr_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not ul_warning_state, ul_done_state, no_update # activating modal -> warning    
        # if everything went fine ...
        return ul_warning_state, not ul_done_state, no_update
    # ========= ACCELERATION  =======
    elif "ul_acc" in button:
        for i in range(len(acc_filenames)):
            if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(acc_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/{acc_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not ul_warning_state, ul_done_state, no_update # activating modal -> warning    
        # if everything went fine ...
        return ul_warning_state, not ul_done_state, no_update
    # ========= BAROMETER  ==========
    elif "ul_bar" in button:
        for i in range(len(bar_filenames)):
            if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(bar_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/{bar_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not ul_warning_state, ul_done_state, no_update # activating modal -> warning    
        # if everything went fine ...
        return ul_warning_state, not ul_done_state, no_update
    # ======== MAGNETOMETER  ========
    elif "ul_mar" in button:
        for i in range(len(mar_filenames)):
            if mar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_decoder(mar_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/{mar_filenames[i]}", "w") as file:
                    file.write(decoded_content)
            else: return not ul_warning_state, ul_done_state, no_update # activating modal -> warning    
        # if everything went fine ...
        return ul_warning_state, not ul_done_state, no_update
    # ====== no button clicked ======
    # this else-section is always activated, when the page refreshes
    else: return ul_warning_state, ul_done_state, _layers(geojson_style) # returning the current Iframe/map

# handling export
@app.callback(
    ### Outputs ###
    # modal
    Output("exp_done", "is_open"),    # export done status
    Output("exp_warn", "is_open"),    # export warning status
    ### Inputs ###
    # modal
    State("exp_done", "is_open"),     # done
    State("exp_warn", "is_open"),     # warning

    # export
    Input("edit_control", "geojson"), # drawn data in geojson format
    Input("exp_btn", "n_clicks")      # export button click status 
)
def export(
    ## modal
    exp_done_state,
    exp_warn_state,
    # export
    data,
    exp_clicks
    ): 
    # getting clicked button
    button = [p["prop_id"] for p in callback_context.triggered][0]
    if "exp_btn" in button:
        if data["features"]:
            export_data(data)
            return not exp_done_state, exp_warn_state # data successfully exported
        return exp_done_state, not exp_warn_state # nothing is drawn -> no data exported
    return exp_done_state, exp_warn_state # nothing is clicked. nothing happens

# handling help
@app.callback(
    ### Outputs ###
    Output("help_cv", "is_open"),    # canvas
    ### Inputs ###
    State("help_cv", "is_open"),     # canvas status
    Input("help_btn", "n_clicks")    # button
)
def help(
    # canvas status
    help_cv_state,
    # button
    help_clicks
    ): 
    # getting clicked button
    button = [p["prop_id"] for p in callback_context.triggered][0]
    if "help_btn" in button: return not help_cv_state     # activate help offcanvas
    else: help_cv_state



# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)

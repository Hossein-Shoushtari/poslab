#### IMPORTS
# dash
from dash import Dash, dcc, html, Output, Input, State, no_update, callback_context
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import assign
# installed packages
from geopandas import GeoDataFrame, read_file
# layouts (ly)
from ly_home import home_card
from ly_simulator import simulator_card
from ly_evaluator import evaluator_card
from ly_coming_soon import coming_soon_card
# utils
from util import upload_encoder, floorplan2layer
from util import export_data, hover_info
from util import upload2layer, csv2marker
# generations/simulations/calculations
from ground_truth_generation import generate_gt


# Geojson rendering logic, must be JavaScript and only initialized once!
geojson_style = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    return style;}"""
)

# ---------------- HTML ---------------- #
# designing the webpage using dash
ex_ss = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=ex_ss)
server = app.server
# title
app.title = "L5IN"

### LAYOUT ###
## Home page ##
home_tab = home_card()  # getting the card content from home.py
## Simulator ##
sim_tab = simulator_card(geojson_style)  # from simulator.py
## Evaluator ##
ev_tab = evaluator_card()  # from evaluator.py
## Comming Soon ##
cs_tab = coming_soon_card()  # from comming_soon.py    

# putting all together
app.layout = html.Div(
    [
        dcc.Tabs(
            value="tab1",
            children=
            [
                dcc.Tab(
                    value="tab1",
                    label="Home",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    selected_style={"color": "#DC6000", "background": "#303030"},
                    children=home_tab),
                dcc.Tab(
                    value="tab2",
                    label="Simulator",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    selected_style={"color": "#DC6000", "background": "#303030"},
                    children=sim_tab),
                dcc.Tab(
                    value="tab3",
                    label="Evaluator",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    selected_style={"color": "#DC6000", "background": "#303030"},
                    children=ev_tab),
                dcc.Tab(
                    value="tab4",
                    label="Coming Soon",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    selected_style={"color": "#AEB5BD", "background": "#303030"},
                    children=cs_tab,
                    disabled=True)
            ],
            colors={
                "background": "#222222"
            }
        )
    ]
)

# ========= handling upload and generation ================================================================================================
@app.callback(
    ### Outputs ###
    # modals
    Output("ul_warn", "is_open"),    # upload warn
    Output("ul_done", "is_open"),    # upload done
    Output("gen_done", "is_open"),   # generation done
    Output("gen_warn", "is_open"),   # generation warn
    # layers
    Output("layers", "children"),    # layers
    # loading (invisible div)
    Output("spin", "children"),      # loading status
    ### Inputs ###
    # modals
    State("ul_warn", "is_open"),
    State("ul_done", "is_open"),
    State("gen_done", "is_open"),
    State("gen_warn", "is_open"),
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
    # generation
    Input("gen_btn", "n_clicks")
)
def upload(
    ## modals
    ul_warn,
    ul_done,
    calc_warn,
    calc_done,
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
    mag_filenames,
    # generation
    gen_btn
    ): 
    # getting clicked button
    button = [p["prop_id"] for p in callback_context.triggered][0]
    # UPLOAD
    #============= MAP =====================================================================================================================
    if "ul_map" in button:
        for i in range(len(map_filenames)):
            if map_filenames[i].split(".")[-1] in ["geojson"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(map_contents[i]) # decoding uploaded base64 file
                converted = GeoDataFrame(read_file(decoded_content), crs=32632).to_crs(4326) # converting EPSG:32632 to WGS84 and saving it in floorplans_converted
                converted.to_file(f"assets/floorplans/{map_filenames[i]}", driver="GeoJSON") # saving converted layer
            else: return not ul_warn, ul_done, calc_warn, calc_done, no_update, no_update # activating modal -> warn    
        # if everything went fine ...
        layers = upload2layer(geojson_style) # uploaded layers
        return ul_warn, not ul_done, calc_warn, calc_done, html.Div(dl.LayersControl(layers)), no_update # returning an html.Iframe with refreshed map
    # ========== WAYPOINTS =================================================================================================================
    elif "ul_way" in button:
        for i in range(len(way_filenames)):
            if way_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(way_contents[i]) # decoding uploaded base64 file
                with open(f"assets/waypoints/{way_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, calc_warn, calc_done, no_update, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, calc_warn, calc_done, no_update, no_update
    # ========== ANTENNAS ==================================================================================================================
    elif "ul_ant" in button:
        for i in range(len(ant_filenames)):
            if ant_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(ant_contents[i]) # decoding uploaded base64 file
                with open(f"assets/antennas/{ant_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, calc_warn, calc_done, no_update, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, calc_warn, calc_done, no_update, no_update
    # ========== GYROSCOPE =================================================================================================================
    elif "ul_gyr" in button:
        for i in range(len(gyr_filenames)):
            if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(gyr_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/gyr.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, calc_warn, calc_done, no_update, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, calc_warn, calc_done, no_update, no_update
    # ========= ACCELERATION  ==============================================================================================================
    elif "ul_acc" in button:
        for i in range(len(acc_filenames)):
            if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(acc_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/acc.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, calc_warn, calc_done, no_update, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, calc_warn, calc_done, no_update, no_update
    # ========= BAROMETER  =================================================================================================================
    elif "ul_bar" in button:
        for i in range(len(bar_filenames)):
            if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(bar_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/bar.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, calc_warn, calc_done, no_update, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, calc_warn, calc_done, no_update, no_update
    # ======== MAGNETOMETER  ===============================================================================================================
    elif "ul_mag" in button:
        for i in range(len(mag_filenames)):
            if mag_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(mag_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/mag.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, calc_warn, calc_done, no_update, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, calc_warn, calc_done, no_update, no_update
    # ======== GENERATION  ================================================================================================================
    elif "gen_btn" in button:
        try:
            gt = generate_gt(geojson_style) # generating ground truth data
            markers = csv2marker(gt[:, 1:3]) # converting crs and making markers
            layers = upload2layer(geojson_style) + [dl.Overlay(dl.LayerGroup(markers), name="GroundTruth", checked=True)] # uploaded layers + markers
            return ul_warn, ul_done, not calc_done, calc_warn, html.Div(dl.LayersControl(layers)), no_update # successful generation
        except: # generation  failed
            return ul_warn, ul_done, calc_done, not calc_warn, no_update, no_update   
    # ====== no button clicked =============================================================================================================
    # this else-section is always activated, when the page refreshes
    else:
        return ul_warn, ul_done, ul_done, calc_done, html.Div(dl.LayersControl(upload2layer(geojson_style))), no_update

# ================ handling export =========================================================================================================
@app.callback(
    ### Outputs ###
    # modal
    Output("exp_done", "is_open"),    # export done status
    Output("exp_warn", "is_open"),    # export warn status
    ### Inputs ###
    # modal
    State("exp_done", "is_open"),     # done
    State("exp_warn", "is_open"),     # warn
    # export
    Input("edit_control", "geojson"), # drawn data in geojson format
    Input("exp_btn", "n_clicks")      # export button click status 
)
def export(
    ## modal
    exp_done,
    exp_warn,
    # export
    data,
    exp_clicks
    ):
    button = [p["prop_id"] for p in callback_context.triggered][0]
    if "exp_btn" in button:
        if data["features"]:
            export_data(data)
            return not exp_done, exp_warn # data successfully exported
        return exp_done, not exp_warn # nothing is drawn -> no data exported
    return exp_done, exp_warn # nothing is clicked. nothing happens

# ================= handling help ==========================================================================================================
@app.callback(
    ### Outputs ###
    Output("help_cv", "is_open"),    # canvas
    ### Inputs ###
    State("help_cv", "is_open"),     # canvas status
    Input("help_btn", "n_clicks")    # button
)
def help(
    # canvas status
    help_cv,
    # button
    help_clicks
    ):
    if help_clicks: return not help_cv     # activate help offcanvas
    else: help_cv

# ====== handling hovering tooltips in layers ==============================================================================================
@app.callback(
    ### Outputs ###
    Output("hover_info", "children"),  # info panel
    ### Inputs ###
    Input("EG", "hover_feature"),      # EG
    Input("1OG", "hover_feature"),     # 1OG
    Input("4OG", "hover_feature"),     # 4OG
)
def hovering(
    # geojson info of all three layers
    feature_eg, feature_1og, feature_4og
    ):
    if feature_eg: return hover_info(feature_eg)       # if EG is clicked
    elif feature_1og: return hover_info(feature_1og)   # if 1OG is clicked
    elif feature_4og: return hover_info(feature_4og)   # if 4OGG is clicked
    else: return hover_info()                          # if nothing is clicked




# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)

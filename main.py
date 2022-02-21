#### IMPORTS
# dash
from dash import Dash, dcc, html, Output, Input, State, no_update, callback_context
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import assign
# built in
from os import listdir
# installed
from geopandas import GeoDataFrame, read_file
# layouts (ly)
from ly_home import home_card
from ly_simulator import simulator_card
from ly_evaluator import evaluator_card
from ly_coming_soon import coming_soon_card
# utils
from util import upload_encoder, floorplan2layer
from util import export_data, hover_info
from util import upload2layer, gt2marker
from util import ref_tab, ref_checked
from util import ref2marker

# generators/simulations/calculations
from ground_truth_generator import generate_gt


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

# =============  upload ============================================================================================================
@app.callback(
    ### Outputs ###
    # modals
    Output("ul_warn", "is_open"),    # upload warn
    Output("ul_done", "is_open"),    # upload done
    # loading (invisible div)
    Output("spin1", "children"),     # loading status
    ### Inputs ###
    # modals
    State("ul_warn", "is_open"),
    State("ul_done", "is_open"),
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
    State("ul_mag", "filename")
)
def upload(
    ## modals
    ul_warn,
    ul_done,
    ## upload
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
    # ========== WAYPOINTS =================================================================================================================
    if "ul_way" in button:
        for i in range(len(way_filenames)):
            if way_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(way_contents[i]) # decoding uploaded base64 file
                with open(f"assets/waypoints/{way_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, no_update
    # ========== ANTENNAS ==================================================================================================================
    elif "ul_ant" in button:
        for i in range(len(ant_filenames)):
            if ant_filenames[i].split(".")[-1] in ["geojson", "txt", "csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(ant_contents[i]) # decoding uploaded base64 file
                with open(f"assets/antennas/{ant_filenames[i]}", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, no_update
    # ========== GYROSCOPE =================================================================================================================
    elif "ul_gyr" in button:
        for i in range(len(gyr_filenames)):
            if gyr_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(gyr_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/gyr.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, no_update
    # ========= ACCELERATION  ==============================================================================================================
    elif "ul_acc" in button:
        for i in range(len(acc_filenames)):
            if acc_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(acc_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/acc.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, no_update
    # ========= BAROMETER  =================================================================================================================
    elif "ul_bar" in button:
        for i in range(len(bar_filenames)):
            if bar_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(bar_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/bar.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, no_update
    # ======== MAGNETOMETER  ===============================================================================================================
    elif "ul_mag" in button:
        for i in range(len(mag_filenames)):
            if mag_filenames[i].split(".")[-1] in ["csv"]: # assuming user uploaded right file format
                decoded_content = upload_encoder(mag_contents[i]) # decoding uploaded base64 file
                with open(f"assets/sensors/mag.csv", "w") as file: file.write(decoded_content) # saving file
            else: return not ul_warn, ul_done, no_update # activating modal -> warn    
        # if everything went fine ...
        return ul_warn, not ul_done, no_update  
    # ====== no button clicked =============================================================================================================
    # this else-section is always activated, when the page refreshes -> no warnings
    else: return ul_warn, ul_done, no_update

# ===========  map display =========================================================================================================
@app.callback(
    ### Outputs ###
    # modals
    Output("map_warn", "is_open"),    # upload/display warn
    Output("map_done", "is_open"),    # upload/display done
    Output("gen_warn", "is_open"),    # gt generator warn
    Output("gen_done", "is_open"),    # gt generator done
    Output("show_warn", "is_open"),   # show ref points warn
    # layers
    Output("layers", "children"),    # layers
    # loading (invisible div)
    Output("spin2", "children"),      # loading status
    ### Inputs ###
    # modals
    State("map_warn", "is_open"),
    State("map_done", "is_open"),
    State("gen_warn", "is_open"),
    State("gen_done", "is_open"),
    State("show_warn", "is_open"),
    # maps
    Input("ul_map", "contents"),
    State("ul_map", "filename"),
    # ground truth generator
    Input("gen_btn", "n_clicks"),
    # reference points
    Input("show_btn", "n_clicks"),
    Input("dd_filename", "data"),
    [Input(f"check{i}", "value") for i in range(100)]
)
def display(
    ## modals
    map_warn,
    map_done,
    gen_warn,
    gen_done,
    show_warn,
    ## upload
    map_contents,  # maps
    map_filenames,
    # gt generator
    gen_btn,
    # ref points
    show_btn,
    name,
    *check
    ):
    button = [p["prop_id"] for p in callback_context.triggered][0]
    #============= MAP =====================================================================================================================
    if "ul_map" in button:
        file_check = [name.split(".")[-1] for name in map_filenames if name.split(".")[-1] not in ["geojson"]] # getting all wrong file formats
        if len(file_check) > 0: return not map_warn, map_done, gen_warn, gen_done, show_warn, no_update, no_update # activating modal -> warn
        for i in range(len(map_filenames)): # only right files were uploaded
            decoded_content = upload_encoder(map_contents[i]) # decoding uploaded base64 file
            converted = GeoDataFrame(read_file(decoded_content), crs=32632).to_crs(4326) # converting EPSG:32632 to WGS84 and saving it in floorplans_converted
            converted.to_file(f"assets/maps/{map_filenames[i]}", driver="GeoJSON") # saving converted layer
        # floorplans + uploaded maps
        layers = floorplan2layer(geojson_style) + upload2layer(geojson_style)
        return map_warn, not map_done, gen_warn, gen_done, show_warn, html.Div(dl.LayersControl(layers)), no_update # returning uploaded layers
    # ========= GT GENERATOR  =================================================================================================================
    elif "gen_btn" in button:
        if name:
            ref = ref_checked(name, check)
            gt = generate_gt(ref) # generating ground truth data
            markers = gt2marker(gt[:, 1:3]) # converting crs and making markers
            # floorplans + uploaded maps + markers
            layers = floorplan2layer(geojson_style) + upload2layer(geojson_style) + [dl.Overlay(dl.LayerGroup(markers), name="GroundTruth", checked=True)]
            return map_warn, map_done, gen_warn, not gen_done, show_warn, html.Div(dl.LayersControl(layers)), no_update # successful generator
    # ========= REF POINTS  =================================================================================================================
    elif "show_btn" in button:
        if name:
            markers = ref2marker(name, check) # converting crs and making markers
            # floorplans + uploaded maps + markers
            layers = floorplan2layer(geojson_style) + upload2layer(geojson_style) + [dl.Overlay(dl.LayerGroup(markers), name="Waypoints", checked=True)]
            return map_warn, map_done, gen_warn, gen_done, show_warn, html.Div(dl.LayersControl(layers)), no_update # successful
        else: return map_warn, map_done, gen_warn, gen_done, not show_warn, no_update, no_update # no data selected
    # ====== no button clicked =============================================================================================================
    # this else-section is always activated, when the page refreshes -> load layers
    else:
        layers = floorplan2layer(geojson_style) + upload2layer(geojson_style)
        return map_warn, map_done, gen_warn, gen_done, show_warn, html.Div(dl.LayersControl(layers)), no_update

# ==============  export ===========================================================================================================
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

# ============  help canvas ========================================================================================================
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

# ====== hovering tooltips in layers ===============================================================================================
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

# ========== ground truth canvas ===================================================================================================
@app.callback(
    ### Outputs ###
    Output("gt_cv", "is_open"),       # canvas
    Output("ref_select", "options"),  # ref points dropdown
    ### Inputs ###
    State("gt_cv", "is_open"),        # canvas status
    Input("gt_btn", "n_clicks")       # button
)
def gt_canvas(
    # canvas status
    gt_cv,
    # button
    gt_clicks
    ):
    if gt_clicks:
        options = [{"label": name.split(".")[0], "value": name.split(".")[0]} for name in listdir("assets/waypoints")]
        return not gt_cv, options     # activate gt offcanvas and filling dropdown with data
    else: return gt_cv, []            # offcanvas is closed

# ======== reference points table ==================================================================================================
@app.callback(
    ### Outputs ###
    Output("ref_tab", "children"),    # table
    Output("invisible", "children"),  # 100 invisible checkboxes
    Output("dd_filename", "data"),    # filename from dropdown
    ### Inputs ###
    Input("ref_select", "value")      # dropdown
)
def ref_table(name):
    if name: # file is selected
        # list of rows filled with selecet coordinates
        tr_list = ref_tab(name)
        # filling table with rows
        table = dbc.Table(
            html.Tbody(tr_list),
            style={"marginTop": "-7px"},
            size="sm",
            bordered=True,
            color="primary"
        )
        # refreshing the invisible checklist
        checklist = [dbc.Checklist(options=[{"value": 1}], value=[1], id=f"check{i}") for i in range(len(tr_list), 100)]
        return table, checklist, name
    # no file selected
    else: return no_update, no_update, name



# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)

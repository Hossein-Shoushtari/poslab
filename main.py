from dash import html, Dash, Output, Input, State, no_update, callback_context
import dash_bootstrap_components as dbc
from simulator_layout import simulator_card
from simulator_func import get_map, upload_decoder, crs32632_converter
from evaluator_layout import evaluator_card
from coming_soon_layout import coming_soon_card
from home_layout import home_card

# ---------------- HTML ---------------- #
# designing the webpage using dash
ex_ss = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=ex_ss)
server = app.server
# title
app.title = 'L5IN'

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
                dbc.Tab(home_tab_content, label='Level 5 Indoor Navigation', active_label_style={"color": "#DC7633"}),
                dbc.Tab(sim_tab_content, label='Simulator', active_label_style={"color": "#DC7633"}),
                dbc.Tab(ev_tab_content, label='Evaluator', active_label_style={"color": "#DC7633"}),
                dbc.Tab(cs_tab_content, label='Coming Soon', disabled=True)
            ]
        )
    ]
)
# ==============================================================================
# handling upload
@app.callback(
    ### Outputs ###
    Output('sim_modal', 'is_open'),   # modal
    Output('map', 'children'),        # map
    Output("ul_cv", "is_open"),       # upload - canvas
    Output("sim_cv", "is_open"),      # simulator - canvas
    ### Inputs ###
    # modal
    State('sim_modal', 'is_open'),
    # canvas
    Input("ul_btn", "n_clicks"),   # upload
    State("ul_cv", "is_open"),     # upload
    Input("sim_btn", "n_clicks"),  # simulator
    State("sim_cv", "is_open"),    # simulator
    # maps
    Input('ul_map', 'contents'),
    State('ul_map', 'filename'),
    # waypoints
    Input('ul_way', 'contents'),
    State('ul_way', 'filename'),
    # antennas
    Input('ul_ant', 'contents'),
    State('ul_ant', 'filename'),
)
def callback(
    # modal
    modal_state,
    # offcanvas
    ul_clicks,  # upload
    ul_state,   # upload
    sim_clicks, # simpulation
    sim_state,  # simpulation
    # upload
    map_contents,  # maps
    map_filenames, # maps
    way_contents,  # waypoints
    way_filenames, # waypoints
    ant_contents,  # antennas
    ant_filenames  # antennas
    ): 
    # getting clicked button
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    # =========== CANVAS ============
    # UPLOAD
    if 'ul_btn' in changed_id: return modal_state, no_update, not ul_state, sim_state     # activate upload offcanvas
    # SIMULATOR
    elif 'sim_btn' in changed_id: return modal_state, no_update, ul_state, not sim_state  # activate simulator offcanvas
    #============= MAP =============
    elif 'ul_map' in changed_id:
        for i in range(len(map_filenames)):
            if map_filenames[i].split('.')[-1] in ['geojson']: # assuming user uploaded right file format
                decoded_content = upload_decoder(map_contents[i]) # decoding uploaded base64 file
                crs32632_converter(map_filenames[i], decoded_content) # converting EPSG:32632 to WGS84 and saving it in floorplans_converted
            else: # activating modal -> warning
                return not modal_state, no_update, ul_state, sim_state
        # if everything went fine ...
        return modal_state, get_map(), ul_state, sim_state # returning an html.Iframe with refreshed map
    # ========== WAYPOINTS ==========
    elif 'ul_way' in changed_id:
        for i in range(len(way_filenames)):
            if way_filenames[i].split('.')[-1] in ['geojson', 'txt', 'csv']: # assuming user uploaded right file format
                decoded_content = upload_decoder(way_contents[i]) # decoding uploaded base64 file
                with open(f'assets/waypoints/{way_filenames[i]}', 'w') as file:
                    file.write(decoded_content)
            else: # activating modal -> warning
                return not modal_state, no_update, ul_state, sim_state
        # if everything went fine ...
        return modal_state, no_update, ul_state, sim_state
    # ========== ANTENNAS ===========
    elif 'ul_ant' in changed_id:
        for i in range(len(ant_filenames)):
            if ant_filenames[i].split('.')[-1] in ['geojson', 'txt', 'csv']: # assuming user uploaded right file format
                decoded_content = upload_decoder(ant_contents[i]) # decoding uploaded base64 file
                with open(f'assets/antennas/{ant_filenames[i]}', 'w') as file:
                    file.write(decoded_content)
            else: # activating modal -> warning
                return not modal_state, no_update, ul_state, sim_state
        # if everything went fine ...
        return modal_state, no_update, ul_state, sim_state
    # ====== no button clicked ======
    # this else-section is always activated, when the page refreshes
    else: return modal_state, get_map(), ul_state, sim_state # returning the current Iframe/map


# pushing the page to the web
if __name__ == '__main__':
    app.run_server(debug=True)

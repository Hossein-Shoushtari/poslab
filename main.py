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
    ### Inputs ###
    # modal
    State('sim_modal', 'is_open'),
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
def callback(is_open, map_contents, map_filenames, way_contents, way_filenames, ant_contents, ant_filenames):
    # getting clicked button
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    #============= MAP =============
    if 'ul_map' in changed_id:
        for i in range(len(map_filenames)):
            if map_filenames[i].split('.')[-1] in ['geojson']: # assuming user uploaded right file format
                decoded_content = upload_decoder(map_contents[i]) # decoding uploaded base64 file
                crs32632_converter(map_filenames[i], decoded_content) # converting EPSG:32632 to WGS84 and saving it in floorplans_converted
            else: # activating modal -> warning
                return not is_open, no_update
        # if everything went fine ...
        return is_open, get_map() # returning an html.Iframe with refreshed map
    #========== WAYPOINTS ==========
    elif 'ul_way' in changed_id:
        for i in range(len(way_filenames)):
            if way_filenames[i].split('.')[-1] in ['geojson', 'txt', 'csv']: # assuming user uploaded right file format
                decoded_content = upload_decoder(way_contents[i]) # decoding uploaded base64 file
                with open(f'assets/waypoints/{way_filenames[i]}', 'w') as file:
                    file.write(decoded_content)
            else: # activating modal -> warning
                return not is_open, no_update
        # if everything went fine ...
        return is_open, no_update
    #========== ANTENNAS ===========
    elif 'ul_ant' in changed_id:
        for i in range(len(ant_filenames)):
            if ant_filenames[i].split('.')[-1] in ['geojson', 'txt', 'csv']: # assuming user uploaded right file format
                decoded_content = upload_decoder(ant_contents[i]) # decoding uploaded base64 file
                with open(f'assets/antennas/{ant_filenames[i]}', 'w') as file:
                    file.write(decoded_content)
            else: # activating modal -> warning
                return not is_open, no_update
        # if everything went fine ...
        return is_open, no_update
    #====== no button clicked ======
    else:
        # this else-section is always activated, when the page refreshes
        return is_open, get_map() # returning the current Iframe/map


# pushing the page to the web
if __name__ == '__main__':
    app.run_server(debug=True)

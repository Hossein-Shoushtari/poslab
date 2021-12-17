import os
from base64 import b64decode
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
from maps import _map
from simulator import simulator_card, GeoJSON
from evaluator import evaluator_card
from coming_soon import coming_soon_card
from home import home_card

# ==============================================================================
# -------- INITIALIZING THE MAP -------- #
geojson = GeoJSON()
# making layers out of existing data
for filename in os.listdir('assets/floorplans_raw'):
    if filename not in os.listdir('assets/floorplans_converted'): # assuming there is no converted version of this GeoJSON file
        geojson.convert_to_crs32632(filename) # making a layer
# adding all layers to the map
geojson.add_layer()
# in case of an empty floorplans_converted directory, a layerless map should be created
if len(os.listdir('assets/floorplans_converted')) == 0: _map()
# ==============================================================================
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
## Simulator page ##
sim_tab_content = simulator_card()  # from simulator.py
## Evaluator page ##
ev_tab_content = evaluator_card()  # from evaluator.py
## Comming Soon page ##
cs_tab_content = coming_soon_card()  # from comming_soon.py    

# putting all together
app.layout = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(home_tab_content, label='Level 5 Indoor Navigation'),
                dbc.Tab(sim_tab_content, label='Simulator'),
                dbc.Tab(ev_tab_content, label='Evaluator'),
                dbc.Tab(cs_tab_content, label='Coming Soon', disabled=True),
            ]
        )
    ]
)
# ==============================================================================
# handling upload
@app.callback(
    ### Outputs ###
    Output('sim_modal', 'is_open'),        # modal
    Output('map', 'children'),             # map
    ### Inputs ###
    # modal
    State('sim_modal', 'is_open'),
    # geojson
    Input('upload_geojson', 'contents'),
    State('upload_geojson', 'filename'),
)
def callback(is_open, content, filename):
    if filename and content is not None: 
        children = GeoJSON(content, filename).upload()
        if children is not None:
            # returning the new Iframe
            return is_open, children
        else:
            # activating modal for warning reasons
            return not is_open, no_update
    else:
        # this else-section is always activated, when the page refreshes
        # returning the current Iframe
        return is_open, html.Iframe(srcDoc=open('index.html').read(),
                                      style={
                                        'width': '100%',
                                        'height': '80vh'
                                      })


# pushing the map to the web
if __name__ == '__main__':
    app.run_server(debug=True)

#### IMPORTS
# dash
from dash_extensions.javascript import assign
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
# users
from user_handling import users_calls
# home
from home.callbacks import home_calls
from home.layout import home_layout
# simulator
from simulator.callbacks import sim_calls
from simulator.layout import sim_layout
# evaluator
from evaluator.callbacks import eval_calls
from evaluator.layout import eval_layout
# coming soon
from datasets.layout import ds_layout
# simulator & evaluator map
from maps.callbacks import maps_calls
from maps.layout import maps_layout
# installed
import nextcloud_client


# ------------- NEXTCLOUD -------------- #
nc = nextcloud_client.Client("https://ann.nl.tab.digital/")
nc.login("cpsimulation2022@gmail.com", "PosLabNEXTCLOUD?*")

# -------------- GEOJSON --------------- #
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
app.title = "L5IN⁺"
# favicon
app._favicon = "assets/images/favicon.ico"

### LAYOUT ###
## Homepage ##
home_tab = home_layout()
## Simulator ##
sim_tab = sim_layout(geojson_style)
## Evaluator ##
eval_tab = eval_layout(geojson_style)
## Datasets ##
ds_tab = ds_layout()

# putting all together
app.layout = html.Div(
    [
        # maps
        maps_layout(),
        # Tabs
        dcc.Tabs(
            id="tabs",
            className="my-tabs",
            value="tab1",
            colors={"background": "#222222"},
            children=
            [
                dcc.Tab(
                    value="tab1",
                    label="Home",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    selected_style={"color": "#DC6000", "background": "#303030"},
                    children=home_tab
                ),
                dcc.Tab(
                    value="tab2",
                    label="Simulator",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    selected_style={"color": "#DC6000", "background": "#303030"},
                    children=sim_tab
                ),
                dcc.Tab(
                    value="tab3",
                    label="Evaluator",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    selected_style={"color": "#DC6000", "background": "#303030"},
                    children=eval_tab
                ),
                dcc.Tab(
                    value="tab4",
                    label="Dataset",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    selected_style={"color": "#DC6000", "background": "#303030"},
                    children=ds_tab
                )
            ]
        )
    ],
    className="main-div"
)

### CALLBACKS ###
home_calls(app)
sim_calls(app, nc)
eval_calls(app, nc)
users_calls(app, nc)
maps_calls(app, geojson_style)

# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)
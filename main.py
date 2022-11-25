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
from coming_soon.layout import com_layout
# simulator & evaluator map
from maps.callbacks import maps_calls
from maps.layout import maps_layout
# installed
import nextcloud_client


# ------------- NEXTCLOUD -------------- #
nc = nextcloud_client.Client('https://cloud.hcu-hamburg.de/nextcloud')
nc.login('hne164', 'NivrokUni2022?')

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
app._favicon = "assets/images/signs/favicon.ico"

### LAYOUT ###
## Home page ##
home_tab = home_layout()
## Simulator ##
sim_tab = sim_layout(geojson_style)
## Evaluator ##
eval_tab = eval_layout(geojson_style)
## Comming Soon ##
cs_tab = com_layout()

# putting all together
app.layout = html.Div(
    [
        # maps
        maps_layout(),
        # Tabs
        dcc.Tabs(
            id="tabs",
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
                    children=eval_tab),
                dcc.Tab(
                    value="tab4",
                    label="Coming Soon",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    selected_style={"color": "#AEB5BD", "background": "#303030"},
                    children=cs_tab,
                    disabled=True)
            ],
            colors={"background": "#222222"}
        )
    ]
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
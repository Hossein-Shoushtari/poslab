#### IMPORTS
# dash
from dash_extensions.javascript import assign
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
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
from maps import map_display


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
        # storage
        dcc.Store(id="unlocked", data={"unlocked": False,"date": 0}, storage_type="memory"),
        dcc.Store(id="layers", data=[], storage_type="memory"),
        # upload and map display done
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/done_sign.svg"))),
            dbc.ModalBody("Successful!")],
            id="display_done",
            size="sm",
            is_open=False
        ),
        # trajectory 500 points limit reached
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/caution_sign.svg"))),
            dbc.ModalBody("500 points limit reached! Trajectory not shown on map but still in system.")],
            id="overflow",
            size="sm",
            is_open=False
        ),
        # unlock hcu maps
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Researcher Login")),
                dbc.ModalBody(
                    html.Div(
                        [
                            dbc.Label("Password"),
                            dbc.Input(id="password", type="password", placeholder="Enter password", style={"color": "white"}),
                            dbc.FormFeedback("Access granted", type="valid"),
                            dbc.FormFeedback("Access denied", type="invalid")
                        ]
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button("Unlock", color="primary", id="unlock")
                ),
            ],
        id="research",
        backdrop="static",
        is_open=False,
        ),
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
            colors={
                "background": "#222222"
            }
        )
    ]
)

### CALLBACKS ###
home_calls(app)
sim_calls(app)
eval_calls(app)
map_display(app, geojson_style)

# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)
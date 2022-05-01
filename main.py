#### IMPORTS
# dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash_extensions.javascript import assign
# layouts
from layout.home import home_card
from layout.simulator import simulator_card
from layout.evaluator import evaluator_card
from layout.coming_soon import coming_soon_card
# callbacks
from callbacks.simulator import sim_calls


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
# favicon
#app._favicon = "favicon.ico"

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

### CALLBACKS ###
sim_calls(app, geojson_style)

# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)

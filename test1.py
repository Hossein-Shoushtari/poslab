
import utils as u
#### IMPORTS
# dash
from dash_extensions.javascript import assign
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
# home
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

eval_map_layers = {
    "layers": True,
    "quantity": 1,
    "bounds": 2,
    "date": 3
}

maps = u.gt2marker(eval_map_layers["quantity"])

# print(maps)


#### IMPORTS
# dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import evaluator.utils as t
import pandas as pd
import numpy as np


# data
gt  = np.loadtxt("gt.csv", delimiter=";", skiprows=1)
traj = np.loadtxt("PDR.csv", delimiter=";")
# interpolation
gt_ip, traj_ip = t.interpolation(gt, traj)
cdf = t.cdf(gt_ip, traj_ip)
df = t.dataframe4graph(cdf, "hallo")


fig = px.line(data_frame=df, x='err', y='cdf', title="CDF", color="Trajectory")
fig.update_traces(mode='lines')

# ---------------- HTML ---------------- #
# designing the webpage using dash
ex_ss = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=ex_ss)
server = app.server
# title
app.title = "L5IN" 

modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("CDF Plot")),
        dbc.ModalBody(
            dcc.Graph(figure=fig, config={
                'staticPlot': False,     # True, False
                'scrollZoom': True,      # True, False
                'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,        # True, False
                'displayModeBar': True,  # True, False, 'hover'
                'watermark': True
                },
                className='six columns')
            )
    ],
    id="exp_done",
    size="xl",
    is_open=True
)

# putting all together
app.layout = html.Div(
    [  
        modal
    ]
)

# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)

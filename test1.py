#### IMPORTS
# dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import evaluator.utils as t
import pandas as pd
import numpy as np

names = ["traj1", "traj2", "traj3", "traj4"]
i = 0
df = []
# data
gt  = np.loadtxt("gt.csv", delimiter=";", skiprows=1)
traj1 = np.loadtxt("traj1.csv", delimiter=";")
traj2 = np.loadtxt("traj2.csv", delimiter=";")
traj3 = np.loadtxt("traj3.csv", delimiter=";")
traj4 = np.loadtxt("traj4.csv", delimiter=";")
# interpolation
interpolations = t.interpolation(gt, [traj1, traj2, traj3, traj4])
for interpolation in interpolations:
    cdf = t.cdf(interpolation[0], interpolation[1])
    df.append(t.dataframe4graph(cdf, names[i]))
    i += 1
fig = px.line(data_frame=pd.concat(df), x='err', y='cdf', title="CDF", color="trajectory")
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

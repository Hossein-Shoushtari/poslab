import dash
import dash_html_components as html
import dash_leaflet as dl
from dash.dependencies import Input, Output

markers = [dl.Marker(children=dl.Tooltip("test"), position=a) for a in [(11,11),(33,33), 
    (55,55)]]
cluster = dl.MarkerClusterGroup(id="markers", children=markers, options={"polygonOptions": 
    {"color": "red"}})

app = dash.Dash(prevent_initial_callbacks=True)
app.layout = html.Div(
        children=[
        html.Div(
            dl.Map([dl.TileLayer(),
                    dl.LayerGroup(id="layer"),
                    cluster
            ],
                   id="map", style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})),
        html.P("EHEE"),
        html.Div(id='clickdata')
    ])

@app.callback(Output("clickdata", "children"),
              [Input("map", "click_lat_lng")])
def map_click(click_lat_lng):
    return "{}".format(click_lat_lng)

if __name__ == '__main__':
    app.run_server()
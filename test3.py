#### IMPORTS
# dash
from dash import Dash, dcc, html, Output, Input, State, no_update, callback_context
import dash_bootstrap_components as dbc
import nextcloud_client
import zipfile
import random
import os

def signin_validation(entry):
    # entry should exist
    if entry == None: return False
    # entry should start with a letter
    is_first_lower = ord('a') <= ord(entry[0]) <= ord('z')
    is_first_upper = ord('A') <= ord(entry[0]) <= ord('Z')
    if not (is_first_lower or is_first_upper):
        return False
    # only consists of letters and numbers
    for character in entry:
        is_lower = ord('a') <= ord(character) <= ord('z')
        is_upper = ord('A') <= ord(character) <= ord('Z')
        is_number = ord('0') <= ord(character) <= ord('9')
        if not (is_lower or is_upper or is_number):
            return False
    # length between 3 and 15 characters
    if len(entry) < 3 or len(entry) > 15:
        return False
    return True

def create_user(nc, username, password):
    assets = ["antennas", "groundtruth", "maps", "sensors", "trajectories", "waypoints"]
    sensors = ["acc", "bar", "gyr", "mag"]
    nc.mkdir(f"L5IN/{username}_{password}")
    for asset in assets:
        nc.mkdir(f"L5IN/{username}_{password}/{asset}")
    for sensor in sensors:
        nc.mkdir(f"L5IN/{username}_{password}/sensors/{sensor}")

def get_user(nc, username, password):
    nc.get_directory_as_zip(f"L5IN/{username}_{password}", f"assets/users/{username}_{password}.zip")
    with zipfile.ZipFile(f"assets/users/{username}_{password}.zip", 'r') as zip_ref:
        zip_ref.extractall("assets/users")
    os.remove(f"assets/users/{username}_{password}.zip")

def update_user_data(nc, username, password, rel_file_path):
    remote_path = f"L5IN/{username}_{password}/{rel_file_path}"
    local_source_file = f"assets/users/{username}_{password}/{rel_file_path}"
    nc.put_file(remote_path, local_source_file)


# ------------- NEXTCLOUD -------------- #
nc = nextcloud_client.Client('https://cloud.hcu-hamburg.de/nextcloud')
nc.login('hne164', 'NivrokUni2022?')

# ---------------- HTML ---------------- #
# designing the webpage using dash
ex_ss = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=ex_ss)
server = app.server
# title
app.title = "Test"
btn1 = html.Div(dbc.Button("REGISTER", id="open_register_btn", color="light", outline=False, style={"border": "0px"}))
btn2 = html.Div(dbc.Button("LOGIN", id="open_login_btn", color="danger", outline=False, style={"border": "0px"}))
spin1 = dbc.Spinner(
    children=[html.Div(id="spin1", style={"display": "none"})],
    type=None,
    fullscreen=True,
    fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
    spinnerClassName="spinner"
)
spin2 = dbc.Spinner(
    children=[html.Div(id="spin2", style={"display": "none"})],
    type=None,
    fullscreen=True,
    fullscreen_style={"opacity": "0.5", "z-index": "10000", "backgroundColor": "transparent"},
    spinnerClassName="spinner"
)
reg_done = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/done_sign.svg"))),
    dbc.ModalBody("Registration successful!")],
    id="reg_done",
    size="sm",
    is_open=False
)
reg_warning = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/caution_sign.svg"))),
        dbc.ModalBody(html.Div([html.P("This user already exists!"), html.P("Please go back and login instead.")]))
    ],
    id="reg_warning",
    size="sm",
    is_open=False
)
registration = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Registration")),
        dbc.ModalBody(
            [
                dbc.Alert(
                    [
                        html.Div(html.Img(src="assets/images/signs/info_sign.svg"), style={"marginRight": "10px"}),
                        "Please enter a prename as well as a surname. Consider them as your unique ID."
                    ],
                    className="d-flex align-items-center",
                    style={"height": "60px", "color": "silver", "background": "#585858", "border-radius": 5, "border": "1px solid silver"}
                ),
                html.Div(
                    [
                        dbc.Label("Prename"),
                        dbc.Input(id="register_pn", placeholder="Enter prename", style={"color": "white"}),
                        dbc.FormFeedback("prename accepted", type="valid"),
                        dbc.FormFeedback("worng prename", type="invalid")
                    ]
                ),
                html.Div(
                    [
                        dbc.Label("Surname", style={"margin-top": "10px"}),
                        dbc.Input(id="register_sn", placeholder="Enter surname", style={"color": "white"}),
                        dbc.FormFeedback("surname accepted", type="valid"),
                        dbc.FormFeedback("wrong surname", type="invalid")
                    ]
                )
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Create Account", color="primary", id="create_acc_btn")
        )
    ],
    id="registration",
    backdrop="static",
    is_open=False
)
login_done = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/done_sign.svg"))),
    dbc.ModalBody("Login successful!")],
    id="login_done",
    size="sm",
    is_open=False
)
login_warning = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle(html.Img(src="assets/images/signs/caution_sign.svg"))),
        dbc.ModalBody(html.Div([html.P("This user doesn't exist!"), html.P("Please go back and register instead.")]))
    ],
    id="login_warning",
    size="sm",
    is_open=False
)
logging_in = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Login")),
        dbc.ModalBody(
            [
                dbc.Alert(
                    [
                        html.Div(html.Img(src="assets/images/signs/info_sign.svg"), style={"marginRight": "10px"}),
                        "Please enter a prename as well as a surname. Consider them as your unique ID."
                    ],
                    className="d-flex align-items-center",
                    style={"height": "60px", "color": "silver", "background": "#585858", "border-radius": 5, "border": "1px solid silver"}
                ),
                html.Div(
                    [
                        dbc.Label("Prename"),
                        dbc.Input(id="login_pn", placeholder="Enter prename", style={"color": "white"}),
                        dbc.FormFeedback("valid", type="valid"),
                        dbc.FormFeedback("invalid", type="invalid")
                    ]
                ),
                html.Div(
                    [
                        dbc.Label("Surname", style={"margin-top": "10px"}),
                        dbc.Input(id="login_sn", placeholder="Enter surname", style={"color": "white"}),
                        dbc.FormFeedback("valid", type="valid"),
                        dbc.FormFeedback("invalid", type="invalid")
                    ]
                )
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Login", color="primary", id="login_btn")
        )
    ],
    id="logging_in",
    backdrop="static",
    is_open=False
)

# putting all together
app.layout = html.Div(
    [  
        html.Div([btn2, btn1, spin1, spin2, registration, reg_done, reg_warning, logging_in, login_done, login_warning])
    ]
)

@app.callback(
    ### Outputs ###
    Output("registration", "is_open"),
    ### Inputs ###
    Input("registration", "is_open"),
    Input("open_register_btn", "n_clicks")
)
def open_registration(registration, register):
    button = [p["prop_id"] for p in callback_context.triggered][0]
    if "open_register_btn" in button: return True
    else: return no_update

@app.callback(
    ### Outputs ###
    Output("register_pn", "valid"),
    Output("register_pn", "invalid"),
    Output("register_sn", "valid"),
    Output("register_sn", "invalid"),
    Output("reg_done", "is_open"),
    Output("reg_warning", "is_open"),
    Output("spin1", "children"),
    ### Inputs ###
    Input("create_acc_btn", "n_clicks"),
    Input("register_pn", "value"),
    Input("register_sn", "value"),
    Input("reg_done", "is_open"),
    Input("reg_warning", "is_open")
)
def registrate(create_acc, username, password, done, warning):
    button = [p["prop_id"] for p in callback_context.triggered][0]
    if "create_acc_btn" in button:
        # checking if username and password are acceptable
        un_valid = signin_validation(username)
        pw_valid = signin_validation(password)
        # one or both are invalid
        if un_valid + pw_valid < 2:
            return un_valid, not un_valid, pw_valid, not pw_valid, False, False, no_update
        else:
            # trying to create account
            try:
                create_user(nc, username, password)
                get_user(nc, username, password)
                # registration successful, user created and then loaded
                return un_valid, not un_valid, pw_valid, not pw_valid, True, False, no_update
            except:
                # same user already exists
                return not un_valid, un_valid, not pw_valid, pw_valid, False, True, no_update
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update
                
@app.callback(
    ### Outputs ###
    Output("logging_in", "is_open"),
    ### Inputs ###
    State("logging_in", "is_open"),
    Input("open_login_btn", "n_clicks")
)
def open_login(logging_in, login):
    button = [p["prop_id"] for p in callback_context.triggered][0]
    if "open_login_btn" in button: return True
    else: return no_update
                
@app.callback(
    ### Outputs ###
    Output("login_pn", "valid"),
    Output("login_pn", "invalid"),
    Output("login_sn", "valid"),
    Output("login_sn", "invalid"),
    Output("login_done", "is_open"),
    Output("login_warning", "is_open"),
    Output("spin2", "children"),
    ### Inputs ###
    Input("login_btn", "n_clicks"),
    Input("login_pn", "value"),
    Input("login_sn", "value"),
    State("login_done", "is_open"),
    State("login_warning", "is_open")
)
def login(login_btn, username, password, done, warning):
    button = [p["prop_id"] for p in callback_context.triggered][0]
    if "login_btn" in button:
        # checking presence of username and password
        un_valid = True if username else False
        pw_valid = True if password else False
        # one or both are invalid
        if un_valid + pw_valid < 2:
            return un_valid, not un_valid, pw_valid, not pw_valid, no_update, no_update, no_update
        # trying to get user's data
        try:
            get_user(nc, username, password)
            # login successful, user loaded
            return un_valid, not un_valid, pw_valid, not pw_valid, True, False, no_update
        except:
            # user doesn't exist
            return not un_valid, un_valid, not pw_valid, pw_valid, False, True, no_update
    else: return no_update, no_update, no_update, no_update, no_update, no_update, no_update


# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)
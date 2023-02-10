##### Callbacks Users
#### IMPORTS
# dash
from dash import html, Output, Input, State, no_update, callback_context
# built in
from os import listdir
# utils
import utils as u



def users_calls(app, nc):
    
    # open user info =========================================================================================================================
    @app.callback(
        ### Outputs ###
        Output("usr_info", "is_open"),
        ### Inputs ###
        State("usr_info", "is_open"),
        Input("info_btn", "n_clicks")
    )
    def open_login(modal, btn):
        trigger = [p["prop_id"] for p in callback_context.triggered][0]
        if "info_btn" in trigger: return True
        else: return no_update

    # registrate/login user ==============================================================================================================
    @app.callback(
        ### Outputs ###
        # register
        Output("register_un", "valid"),     # username
        Output("register_un", "invalid"),   # username
        Output("register_pw", "valid"),     # password
        Output("register_pw", "invalid"),   # password
        Output("reg_done", "is_open"),      # modal done
        Output("reg_warning", "is_open"),   # modal warn
        # login
        Output("login_un", "valid"),        # username
        Output("login_un", "invalid"),      # password
        Output("login_pw", "valid"),        # password
        Output("login_pw", "invalid"),      # username
        Output("login_done", "is_open"),    # modal done
        Output("login_warning", "is_open"), # modal warn
        # welcome text
        Output("welcome_user", "children"),
        # user
        Output("usr_data", "data"),
        # spinner
        Output("usr_spin1", "children"),
        ### Inputs ###
        # register
        Input("register_btn", "n_clicks"),  # button
        Input("register_un", "value"),      # username
        Input("register_pw", "value"),      # password
        State("reg_done", "is_open"),       # modal done
        State("reg_warning", "is_open"),    # modal warn
        # login
        Input("login_btn", "n_clicks"),     # button
        Input("login_un", "value"),         # username
        Input("login_pw", "value"),         # password
        State("login_done", "is_open"),     # modal done
        State("login_warning", "is_open")   # modal warn
    )
    def registrate_login(
        # register
        register_btn,
        register_un,
        register_pw,
        register_done,
        register_warn,
        # login
        login_btn,
        login_un,
        login_pw,
        login_done,
        login_warn
        ):
        # get rid of white spaces at end of strings
        try:
            register_un = register_un.rstrip()
            register_pw = register_pw.rstrip()
            login_un = login_un.rstrip()
            login_pw = login_pw.rstrip()
        except: pass
        # let's go
        trigger = [p["prop_id"] for p in callback_context.triggered][0]
        usr_data = {
            "username": "",
            "password": ""
        }
        welcome = html.P("Register or Login", style={"margin": "0px"})
        # REGISTER --------------------------------------------------------------------------------------------------------
        if "register_btn" in trigger:
            # checking if username and password are acceptable
            register_un_valid = u.signin_validation(register_un)
            register_pw_valid = u.signin_validation(register_pw)
            # one or both are invalid
            if register_un_valid + register_pw_valid < 2:
                return register_un_valid, not register_un_valid, register_pw_valid, not register_pw_valid, False, False, no_update, no_update, no_update, no_update, no_update, no_update, welcome, usr_data, no_update
            else:
                # trying to create account
                try:
                    u.create_user(nc, register_un, register_pw)
                    u.get_user(nc, register_un, register_pw)
                    usr_data["username"] = register_un
                    usr_data["password"] = register_pw
                    welcome = html.P(f"Hello {register_un}!", style={"margin": "0px"})
                    # registration register_un, user created and then loaded
                    return register_un_valid, not register_un_valid, register_pw_valid, not register_pw_valid, True, False, no_update, no_update, no_update, no_update, no_update, no_update, welcome, usr_data, no_update
                except:
                    # same user already exists
                    return not register_un_valid, register_un_valid, not register_pw_valid, register_pw_valid, False, True, no_update, no_update, no_update, no_update, no_update, no_update, welcome, usr_data, no_update
        # LOGIN ------------------------------------------------------------------------------------------------------------
        if "login_btn" in trigger:
            # checking presence of username and password
            login_un_valid = True if login_un else False
            login_pw_valid = True if login_pw else False
            # one or both are invalid
            if login_un_valid + login_pw_valid < 2:
                return no_update, no_update, no_update, no_update, no_update, no_update, login_un_valid, not login_un_valid, login_pw_valid, not login_pw_valid, no_update, no_update, welcome, usr_data, no_update
            # trying to get user's data
            try:
                usr_data["username"] = login_un
                usr_data["password"] = login_pw
                if f"{login_un}_{login_pw}" not in listdir("assets/users"): # user data still only in cloud -> get user's data
                    u.get_user(nc, login_un, login_pw)
                welcome = html.P(f"Hello {login_un}!", style={"margin": "0px"})
                # login successful, user loaded
                return no_update, no_update, no_update, no_update, no_update, no_update, login_un_valid, not login_un_valid, login_pw_valid, not login_pw_valid, True, False, welcome, usr_data, no_update
            except:
                # user doesn't exist
                return no_update, no_update, no_update, no_update, no_update, no_update, not login_un_valid, login_un_valid, not login_pw_valid, login_pw_valid, False, True, welcome, usr_data, no_update
        # LOAD DEMO DATA ----------------------------------------------------------------------------------------------------
        if trigger == ".":
            usr_data["username"] = "demo"
            usr_data["password"] = "data"
            # demo data loaded
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, welcome, usr_data, no_update

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update



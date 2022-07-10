##### Utils general
###IMPORTS
# dash
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import html
# built in
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from base64 import b64decode
import shutil as st
import numpy as np
import math as m
import smtplib
import os

def time():
    # for Hossein's time confusion
    H, M, S = datetime.now().strftime('%H'), datetime.now().strftime('%M'), datetime.now().strftime('%S')
    name = f"{int(H)+2}+{M}+{S}"
    return name

def sending_email():
    """
    FUNCTION
    - sends an email with all uploaded and generated data as zip files to 'cpsimulation2022@gmail.com'
    -------
    RETURN
    nothing... just sending an email
    """
    # creating a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText("Check out the latest uploaded and calculated data!", 'plain')
    msg['Subject'] = f"Uploaded & calculated data -- {datetime.now().strftime('%d.%m.%Y')} - {time()}"
    msg['From'] = "cpsimulation2022@gmail.com"
    msg['To'] = "cpsimulation2022@gmail.com"
    # adding body to email
    msg.attach(body_part)
    # zipping all dirs if not empty
    if len(os.listdir("assets/antennas")): st.make_archive(f"assets/zip/antennas-{time()}", 'zip', "assets/antennas")
    if len(os.listdir("assets/maps")): st.make_archive(f"assets/zip/maps-{time()}", 'zip', "assets/maps")
    if len(os.listdir("assets/sensors/acc")) or len(os.listdir("assets/sensors/bar")) or len(os.listdir("assets/sensors/gyr")) or len(os.listdir("assets/sensors/mag")): st.make_archive(f"assets/zip/sensors-{time()}", 'zip', "assets/sensors")
    if len(os.listdir("assets/waypoints")): st.make_archive(f"assets/zip/waypoints-{time()}", 'zip', "assets/waypoints")
    # attaching all files 
    for zip in os.listdir("assets/zip"):
        # open and read the file in binary
        with open(f"assets/zip/{zip}","rb") as file:
            # attach the file with filename to the email
            msg.attach(MIMEApplication(file.read(), Name=f'{zip}'))
    # creating SMTP object
    smtp_obj = smtplib.SMTP_SSL("smtp.gmail.com")
    # login to the server
    smtp_obj.login("cpsimulation2022@gmail.com", "simulation2evaluation20xx")




sending_email()
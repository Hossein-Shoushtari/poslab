##### Utils general
###IMPORTS
# built in
import numpy as np
import math as m
from base64 import b64decode
from datetime import datetime
import shutil as st
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


def upload_encoder(content: str) -> str:
    """
    FUNCTION
    - encodes uploaded base64 file to originally uploaded file
    -------
    PARAMETER
    content : decoded content
    -------
    RETURN
    encoded content
    """
    # decoding base64 to geojson
    encoded_content = content.split(",")[1]
    decoded_content = b64decode(encoded_content).decode("latin-1")  # should be a geojson like string

    return decoded_content

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
    msg['Subject'] = f"Uploaded & calculated data -- {datetime.now().strftime('%d.%m.%Y - %H:%M:%S')}"
    msg['From'] = "cpsimulation2022@gmail.com"
    msg['To'] = "cpsimulation2022@gmail.com"
    # adding body to email
    msg.attach(body_part)
    # zipping all dirs if not empty
    if len(os.listdir("assets/antennas")): st.make_archive(f"assets/zip/antennas-{datetime.now().strftime('%H_%M')}", 'zip', "assets/antennas")
    if len(os.listdir("assets/maps")): st.make_archive(f"assets/zip/maps-{datetime.now().strftime('%H_%M')}", 'zip', "assets/maps")
    if len(os.listdir("assets/sensors/acc")) or len(os.listdir("assets/sensors/bar")) or len(os.listdir("assets/sensors/gyr")) or len(os.listdir("assets/sensors/mag")): st.make_archive(f"assets/zip/sensors-{datetime.now().strftime('%H_%M')}", 'zip', "assets/sensors")
    if len(os.listdir("assets/waypoints")): st.make_archive(f"assets/zip/waypoints-{datetime.now().strftime('%H_%M')}", 'zip', "assets/waypoints")
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

    # converting the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()

def centroid(lon_raw: list, lat_raw: list) -> tuple:
    """
    FUNCTION
    - calculates center of given geojson file
    -------
    PARAMETER
    lon_raw : longitude
    lat_raw : latitude
    -------
    RETURN
    center : tuple with lat and lon of center
    """
    # calculating mean of lat and lon
    center = (sum(lat_raw)/len(lat_raw), sum(lon_raw)/len(lon_raw))
    return center

def zoom_lvl(lon_raw: list, lat_raw: list) -> int:
    """
    FUNCTION
    - calculates zoom level of given geojson file
    -------
    PARAMETER
    lon_raw : longitude
    lat_raw : latitude
    -------
    RETURN
    zoom : zoom lvl (integer)
    """
    lon = []
    lat = []
    # modify all negative coordinates
    for i in range(len(lon_raw)):
        if lon_raw[i] < 0: lon.append(lon_raw[i]+360)
        else: lon.append(lon_raw[i])
        if lat_raw[i] < 0: lat.append(lat_raw[i]+180)
        else: lat.append(lat_raw[i])
    # finding edge points      
    maxx, minx, maxy, miny = max(lon), min(lon), max(lat), min(lat)
    # calculating distance in x and y direction
    d = (abs(maxx - minx), abs(maxy - miny)*16/9) # y-direction factorized by 16/9 because of screen ratio
    # getting max distance (x or y)
    d = max(d)
    # approximate value of latitude proportion at maximum zoom level (20)
    v = 0.002
    # calculating final zoom factor
    if d == 0: zoom = 20            # d=0  (e.g.: simple point was uploaded)
    else: zoom = 20 - m.log(d/v, 2)     # d>0  (everything else like Polygons, lines, multiple points, etc.)
    if zoom > 20: zoom = 20         # d>20 (zoom level exceeds 20 | e.g.: simple point)
    if zoom > 1: zoom -= 1          # always subtract 1 to make sure everything fits safely
    return zoom

def deleter():
    """
    - emptying all uploaded or generated files before the actuall app starts
    """
    for filename in os.listdir("assets/antennas"): os.remove(f"assets/antennas/{filename}")
    for filename in os.listdir("assets/exports/gt"): os.remove(f"assets/exports/gt/{filename}")
    for filename in os.listdir("assets/exports/sm"): os.remove(f"assets/exports/sm/{filename}")
    for filename in os.listdir("assets/exports/draw"): os.remove(f"assets/exports/draw/{filename}")
    for filename in os.listdir("assets/groundtruth"): os.remove(f"assets/groundtruth/{filename}")
    for filename in os.listdir("assets/maps"): os.remove(f"assets/maps/{filename}")
    for filename in os.listdir("assets/sensors/acc"): os.remove(f"assets/sensors/acc/{filename}")
    for filename in os.listdir("assets/sensors/bar"): os.remove(f"assets/sensors/bar/{filename}")
    for filename in os.listdir("assets/sensors/gyr"): os.remove(f"assets/sensors/gyr/{filename}")
    for filename in os.listdir("assets/sensors/mag"): os.remove(f"assets/sensors/mag/{filename}")
    for filename in os.listdir("assets/trajectories"): os.remove(f"assets/trajectories/{filename}")
    for filename in os.listdir("assets/waypoints"): os.remove(f"assets/waypoints/{filename}")
    for filename in os.listdir("assets/zip"): os.remove(f"assets/zip/{filename}")

def dummy():
    with open("assets/antennas/dummy", "w") as f: f.write("")
    with open("assets/exports/gt/dummy", "w") as f: f.write("")
    with open("assets/exports/sm/dummy", "w") as f: f.write("")
    with open("assets/exports/draw/dummy", "w") as f: f.write("")
    with open("assets/maps/dummy", "w") as f: f.write("")
    with open("assets/groundtruth/dummy", "w") as f: f.write("")
    with open("assets/sensors/acc/dummy", "w") as f: f.write("")
    with open("assets/sensors/bar/dummy", "w") as f: f.write("")
    with open("assets/sensors/gyr/dummy", "w") as f: f.write("")
    with open("assets/sensors/mag/dummy", "w") as f: f.write("")
    with open("assets/trajectories/dummy", "w") as f: f.write("")
    with open("assets/waypoints/dummy", "w") as f: f.write("")
    with open("assets/zip/dummy", "w") as f: f.write("")


if __name__ == "__main__":
    deleter()
    dummy()

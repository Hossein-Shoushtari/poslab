
  

# INDOOR NAVIGATION 5G | Simulation ⟷ Evaluation

  

  

### official website: https://simulation2evaluation.herokuapp.com/

  

  

---

  

## File Navigation -- Overview

  

### DIRECTORIES

  

#### assets

  

>  **exports** : for each user generated ground truth, simulated measurements and drawn data

  

>  **floorplans** : HCU floorplans (EG, 1OG, 4OG)

  

>  **images** : images and icons for the website

  

>  **users** : user data from nextcloud after logged in successfully

  

#### coming soon

  

> Coming-soon tab with all its required python scripts

  

#### evaluator

  

> Evaluator tab with all its required python scripts

  

#### home

  

> Home tab with all its required python scripts

  

#### simulator

  

> Simulator tab with all its required python scripts

  

#### maps

  

> Dash-leaflet maps (simulator & evaluator tab) with all its required python scripts

  

  

### FILES

  

>  **main.py** : self-explanatory :)

  

>  **maps.py** : all logic code related to the two maps in Simulator & Evaluator (unlock HCU maps, show all uploaded/generated, zoom, center etc.)

  

>  **dashExtensions_default.js** : GeoJSON rendering logic. Must be in Java Script. It's used for dash-leaflet. It's only initialized once in the beginning.

  

>  **spinner_styling.css** : CSS styling of the blue spinner/loading sign

  

>  **tabs.css** : CSS styling of the four tabs

  

>  **example_data.zip** : some example data for the user to know how to format his own data

  

>  **util.py** : Required general functions from all tabs

  

>  **user_handling.py** : callbacks for registration and login

  

>  **README.txt** : readme file in exported results zip for user's info

  

>  **.gitignore**, **Procfile**, **requirements.txt** : for heroku deploy

  

  

<br/>

  

<a  href="https://www.paypal.me/KorvinVenzke"><img  src="assets/images/signs/donate_sign.svg"  height="40"></a>

  

If you enjoyed this project — or just feel generous, consider supporting us!
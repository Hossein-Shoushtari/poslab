# Simulation ⟷  Evaluation

### official website: https://simulation2evaluation.herokuapp.com/

---
## File Navigation -- Overview
### DIRECTORIES
#### assets
> **antennas** : uploaded antenna data can be found here  
> **export** : after clicking on 'Get results', drawn geometry types are saved in one geojson file here  
> **floorplans** : already converted floorplans (EG, 1OG, 4OG) can be found here  
> **groundtruth** : Dorians groung truth data can be found here  
> **images** : images for the website can be found here    
> **maps** : all uploaded map data can be found here 
> **sensors** : all uploaded sensor data (acc, bar, gyr, mag) can be found here  
> **waypoints** : uploaded waypoint data can be found here  

### FILES
> **main.py** : self-explanatory :)

> **dashExtensions_default.js** : GeoJSON rendering logic. Must be in Java Script. It's used for dash-leaflet. It's only initialized once in the beginning.

> **spinner_styling.css** : CSS styling of the blue spinner/loading sign

> **tabs.css** : CSS styling of the four tabs

> **coordinate_simulation.py** : Dorian's part

> **ground_truth_generation.py** : Hossein's part

> **measurement_simulation.py** : Georg's part (?)

> **ly_...** : Design and layout of all 4 tabs on web (Home, Simulator, Evaluator, Coming Soon)

> **cb_...** : Callbacks of all 4 tabs for every function (Home, Simulator, Evaluator, Coming Soon)

> **util.py** : Needed functions to run all buttons (converting, encoding, etc.)

> **.gitignore**, **Procfile**, **requirements.txt** : for heroku deploy


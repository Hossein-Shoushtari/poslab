# Simulation ⟷  Evaluation

### official website: https://simulation2evaluation.herokuapp.com/

---
## File Navigation -- Overview
### DIRECTORIES
#### assets
> **antennas** : uploaded antenna data  
> **exports** : generated ground truth and simulated measurements data  
> **floorplans** : already converted HCU floorplans (EG, 1OG, 4OG)  
> **images** : images for the website  
> **maps** : all uploaded map data  
> **sensors** : all uploaded sensor data (acc, bar, gyr, mag)  
> **waypoints** : uploaded waypoints  
#### callbacks
> all callbacks for the respective tabs
#### layout
> Design and layout of all 4 tabs (Home, Simulator, Evaluator, Coming Soon)

### FILES
> **main.py** : self-explanatory :)  
> **dashExtensions_default.js** : GeoJSON rendering logic. Must be in Java Script. It's used for dash-leaflet. It's only initialized once in the beginning.  
> **spinner_styling.css** : CSS styling of the blue spinner/loading sign  
> **tabs.css** : CSS styling of the four tabs  
> **coordinate_simulation.py** : Dorian's part  
> **ground_truth_generator.py** : Hossein's part  
> **measurement_simulation.py** : Georg's part (?)  
> **util.py** : Needed functions to run all buttons (converting, encoding, etc.)  
> **.gitignore**, **Procfile**, **requirements.txt** : for heroku deploy  


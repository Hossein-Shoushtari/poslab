# Simulation ⟷  Evaluation

### official website: https://simulation2evaluation.herokuapp.com/

---
## File Navigation -- Overview
### DIRECTORIES
#### assets
> **antennas** : uploaded antenna data  
> **exports** : generated ground truth and simulated measurements data  
> **floorplans** : already converted HCU floorplans (EG, 1OG, 4OG)  
> **groundturth** : uploaded ground truth for evaluation    
> **images** : images for the website  
> **maps** : all uploaded map data  
> **sensors** : all uploaded sensor data (acc, bar, gyr, mag)  
> **trajectories** : uploaded trajectories for evaluation    
> **waypoints** : uploaded waypoints for ground truth  
> **zip** : zip directories that are either downloaded for the user or sent to us as an attachment in an email  
#### coming soon
> Coming-soon tab with all its required python scripts
#### evaluator
> Evaluator tab with all its required python scripts
#### home
> Home tab with all its required python scripts
#### Simulator
> Simulator tab with all its required python scripts

### FILES
> **main.py** : self-explanatory :)  
> **dashExtensions_default.js** : GeoJSON rendering logic. Must be in Java Script. It's used for dash-leaflet. It's only initialized once in the beginning.  
> **spinner_styling.css** : CSS styling of the blue spinner/loading sign  
> **tabs.css** : CSS styling of the four tabs   
> **util.py** : Required general functions from all tabs  
> **.gitignore**, **Procfile**, **requirements.txt** : for heroku deploy  


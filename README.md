
#   L5IN⁺: Level 5 Indoor-Navigation Plus  

**Website**: https://poslab.herokuapp.com/  
**Papers**:  
**Demo**: https://youtu.be/ABc6WXrFHIs

---
### Requirements   
Website:
```
dash, dash-bootstrap-components, dash-core-components, dash-extensions,
dash-html-components, dash-leaflet, dash-table, plotly, pyncclient
```
Simulation & Evaluation:
```
geojson, geopandas, numpy, pandas, scipy 
```

### Data 

### Usage:

1.  Visit our website
2. Example data can be downloaded in the ```help``` section!
3.  In the **Simulator** tab, you can simulate measurements. To do this:
    1.  Enter your first and last name during registration for easy identification and data restoration.
    2.  Upload your data.
    3.  Generate ground truth trajectories using your waypoints and sensor data.
    4.  Simulate measurements.
    5.  Download your results.
    6.  Refer to the ```help``` section for more detailed instructions.
    7.  Add on: Draw points, lines, polygons and shapes on the map, and access the geojson file in the results!
4. In the **Evaluator** tab, you can evaluate the simulated data. For doing this:
    1.  Either upload additional data or select the previously calculated data.
    2.  Go to ```CDF``` to calculate the cumulative distribution function.
    3.  Optionally select a map to get the percentage of points in corresponding polygons (=pip).
    4.  Safe the plot as .png!
    5.  Open the ```Visual``` modal -- it functions as a minimalistic GIS.
    6. Select the prefered map background, file format and uploaded or generated files.
    7. Safe the plot!
5. In the **Dataset** tab, you can apply for our _L5IN⁺  Dataset_.

### Citation

---
<a  href="https://www.paypal.me/KorvinVenzke"><img  src="assets/images/svg/signs/donate_sign.svg"  height="40"></a>

If you enjoyed this project — or just feel generous, consider supporting us!

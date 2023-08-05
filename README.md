

#   L5IN⁺: Level 5 Indoor-Navigation Plus  

**Website**: https://poslab-24ac1d08a0af.herokuapp.com/  
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
geojson, geopandas, numpy, pandas, scipy, Shapely 
```

### Dash
Our website is built entirely using [Dash](https://plotly.com/dash/) and Python. This means that the entire website, including the layouts, callbacks, and visualizations, are all created and managed using Python. The use of Python also allows for efficient data processing and manipulation, making it an ideal choice for building data-driven websites. Our website demonstrates the versatility of Dash by using it in the context of Geoinformatics and GIS, showing that it can be a valuable tool in these fields as well.


### Data
The  _L5IN⁺  Dataset_ will be available for release on January 26, 2023. To apply for access to this dataset, please visit our website and navigate to the **Dataset** tab. For additional information, please refer to our website or contact [hossein.shoushtari@hcu-hamburg.de](mailto:hossein.shoushtari@hcu-hamburg.de) for further assistance.

### Usage
1.  Visit our website
2. Example data can be downloaded in the ```Help``` section!
3.  In the **Simulator** tab, you can simulate measurements. To do this:
    1.  Enter your first and last name during registration for easy identification and data restoration.
    2.  Upload your data.
    3.  Generate ground truth trajectories using your waypoints and sensor data.
    4.  Simulate measurements.
    5.  Download your results.
    6.  Refer to the ```Help``` section for more detailed instructions.
    7.  Add on: Draw points, lines, polygons and shapes on the map, and access the geojson file in the results!
4. In the **Evaluator** tab, you can evaluate the simulated data. For doing this:
    1.  Either upload additional data or select the previously calculated data.
    2.  Go to ```CDF``` to calculate the cumulative distribution function.
    3.  Optionally select a map to get the percentage of points in (corresponding) polygons (=pip).
    4.  Safe the plot as .png!
    5.  Open the ```Visual``` modal -- it functions as a minimalistic GIS.
    6. Select the prefered map background, file format and uploaded or generated files.
    7. Safe the plot!
5. In the **Dataset** tab, you can apply for our _L5IN⁺  Dataset_.

### Privacy
By using our website and creating an account for uploading data, you consent to the collection, administration, and storage of your data as outlined in this Privacy Policy.  
The data you provide, including registration data, will be collected and managed by us using the Nextcloud platform. The purpose of collecting the data is to create and manage your account, and for any other uses specifically outlined on our website. Should you wish to revoke your consent, we will promptly delete your data from our system.  
The data of all users is open-source and available under this link:  
https://ann.nl.tab.digital/s/9jo9raqZ6p8m5X9

---
<a  href="https://www.paypal.me/KorvinVenzke"><img  src="assets/images/svg/signs/donate_sign.svg"  height="40"></a>

If you enjoyed this project — or just feel generous, consider supporting us!

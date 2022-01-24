from folium import Map, Marker, Icon
from folium.plugins import Fullscreen, MiniMap, MeasureControl, Draw, LocateControl
from geopandas import read_file
from datetime import datetime

def _map():
    '''
    :return: created base map
    '''
    # creating a base map and get an hcu-centered view
    hcu_coordinates = (53.540252, 10.004814073621176)
    base_map = Map(
        location=hcu_coordinates,
        tiles='stamentoner',
        zoom_start=19,
        max_zoom=19,
        control_scale=True
    )
    # plugin for mini map
    # minimap = MiniMap(toggle_display=True)
    # add minimap to map
    # base_map.add_child(minimap)
    # add full screen button to map
    Fullscreen(position='topleft').add_to(base_map)
    # measure control
    # measure_control = MeasureControl(position='topleft', active_color='red', completed_color='green', primary_length_unit='meters')
    # add measure control to map
    # base_map.add_child(measure_control)
    # draw tools | 'export=True' exports the drawn shapes as a geojson file
    draw = Draw(
        filename=f'{datetime.now()}.geojson',
        position='topleft',
        draw_options={'polyline': {'allowIntersection': False}},
        edit_options={'poly': {'allowIntersection': False}}
    )
    # add draw tools to map
    draw.add_to(base_map)
    return base_map
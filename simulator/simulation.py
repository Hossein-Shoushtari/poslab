##### Coordinate Simulation class
### IMPORTS
# built in
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
# installed
from geopandas import GeoSeries
from geojson import Point
# utils
import utils as u


def find_nearest(array, value):
    """
    Find the nearest value in a numpy array.

    Parameters:
    -----------
    array (np.array): A 1D numpy array.
    value (float): The value to find the nearest match of.

    Returns:
    --------
    int, float: The index of the nearest match, and the value of the nearest match.
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]

def closest_value(input_list, input_value):
    """
    return the closest value to a given input value from a list of given values

    Parameters
    ----------
    input_list : list of values - list of floats
    input_value : value for which the closest value is determined - float

    Returns
    -------
    arr[i] : closest value from the list to the given value - float
    """
    arr = np.asarray(input_list)

    i = (np.abs(arr - input_value)).argmin()

    return arr[i]

def semantic_error(number, error_range, intervall_range, time_stamps):
    """
    creating semantic error values. the number of occurences, the error values and the length of each intervall of
    semantic errors is randomly chosen from a given range

    Parameters
    ----------
    number_range : range of number of accurances of semantic errors - tuple of integers
    error_range : range of possible error values for the semantic error - tuple of floats
    intervall_range : range of possible lengths for the semantic errors - tuple of floats
    time_stamps : time stamps from the ground truth data - list of floats

    Returns
    -------
    intervall_lengths : length of all intervalls with semantic error - list of floats
    errors : standard deviations for each semantic error intervall - list of floats
    intervall_starts : start time of each semantic error intervall - list of floats
    """
    number_of_intervalls = number
    intervall_lengths = []
    intervall_starts = []
    errors = []

    for i in range(number_of_intervalls):
        intervall_lengths.append(np.random.uniform(intervall_range[0], intervall_range[
            -1]))  # choose random intervalls (according to number of intervalls) from the timeline
        intervall_starts.append(np.random.choice(time_stamps[:-1]))
        errors.append(np.random.uniform(error_range[0], error_range[-1]))

    return intervall_lengths, errors, intervall_starts

def simulate_positions(user, groundtruth, error, measurement_freq, network_capacity, number_of_users, number_of_intervalls,
                       error_range, intervall_range, semantic):
    """
    creating sample data points for 5G measurements

    Parameters
    ----------
    groundtruth : time stamps and position coordinates of the ground truth data set - array of floats
    error : desired error for 5G positions  - float
    measurement_freq : frequency of 5G measurements in (number of measurements/second)  - float
    query_freq : frequency of possible queries to receive the position information (number of queries/second)  - float
    number_of_users : number of users connected to the %G network simultaneously  - int
    number_of_intervalls : number of time intervalls where a semantic error is specified and used  - int
    error_range : range to randomly draw the semantic error values from  - tuple (list) of floats
    intervall_range : range to randomly draw duration of time intervalls from  - tuple (list) of floats
    semantic : choose if semantic errors are used (True) or not (False) - Boolean


    Returns
    -------
    positions : simulated positions from 5G measurements - array of arrays (tuples) of floats
    time_stamps : timestamps of 5G measurements - array of floats
    error_list : generated error values for every position - list of floats
    qualities_list : estimated qualities for each measurement (as limits of a error intervall) - array of floats
    """
    # user data
    un = user["username"]
    pw = user["password"]
    # getting selected ground truth data
    groundtruth = np.loadtxt(f"assets/users/{un}_{pw}/groundtruth/{groundtruth}.csv", skiprows=1)
    error_list = []
    count = 0
    semantic_active = False


    rows = groundtruth
    ts = rows[0][0]

    measurement_freq = measurement_freq / 1000  # convert from s to ms

    gt_time_stamps = [r[0] for r in rows]

    if number_of_users > network_capacity:
        dt = (number_of_users / network_capacity) * 1000
    else:
        dt = 1 / measurement_freq


    positions = []

    simulatd_timestamps = []
    while ts <= rows[-1][0]:
        simulatd_timestamps.append(ts)
        ts += dt

    intervall_lengths, semantic_errors, intervall_starts = semantic_error(number_of_intervalls, error_range,
                                                                          intervall_range, simulatd_timestamps)


    for i,t in enumerate(simulatd_timestamps):

        if semantic == True:
            if t >= intervall_starts[count] and t <= intervall_starts[count] + \
                    intervall_lengths[count]:
                current_error = semantic_errors[count]
                semantic_active == True

            elif semantic_active == True:
                current_error = semantic_errors[count]
                count += 1
            elif semantic_active == False:
                current_error = error
        else:
            current_error = error

        x_error = np.random.normal(0, current_error)
        y_error = np.random.normal(0, current_error)
        error_list.append(np.sqrt(x_error ** 2 + y_error ** 2))

        id, closest_GT_time =find_nearest(gt_time_stamps, t)

        x_temp = rows[id][1]
        y_temp = rows[id][2]

        positions.append([x_temp + np.random.uniform(-current_error, current_error, 1)[0],
                          y_temp + np.random.uniform(-current_error, current_error, 1)[0]])
    qualities_list = []
    for e in error_list:
        quality = closest_value([error / 5, 2 * error / 5, 3 * error / 5, 4 * error / 5, 5 * error / 5],
                                e)
        qualities_list.append(quality)

    time_stamps = simulatd_timestamps
    return time_stamps, positions, error_list, qualities_list

def azimuth(point1: tuple, point2: tuple) -> float:
    """
    Calculate the azimuth angle between two points on a plane.
    
    Parameters:
    point1 (tuple): Tuple of x and y coordinates of the first point.
    point2 (tuple): Tuple of x and y coordinates of the second point.
    
    Returns:
    float: The azimuth angle in degrees, where 0 <= angle < 360.
    """
    angle = np.arctan2(point2[0] - point1[0], point2[1] - point1[1])
    return np.degrees(angle) if angle >= 0 else np.degrees(angle) + 360

def distance(point1: tuple, point2: tuple) -> float:
    """
    Calculates the Euclidean distance between two points in 2-dimensional space.
    
    Parameters:
    point1 (tuple) : A tuple representing the first point in 2-dimensional space.
    point2 (tuple) : A tuple representing the second point in 2-dimensional space.
    
    Returns:
    float : The Euclidean distance between the two points.
    """
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def export_sim(nc: object, user: dict, time_stamps: list, positions: list, errors: list, qualities: list, name: tuple) -> None:
    """
    Exports simulation data for a user to a CSV file.

    Parameters:
    nc (obj) : Object for cloud storage connection.
    user (dict) : Dictionary containing the user's login information.
    time_stamps (list) : List of timestamps for the simulation data.
    positions (list) : List of positions for the simulation data.
    errors (list) : List of errors for the simulation data.
    qualities (list) : List of qualities for the simulation data.
    name (tuple) : Tuple of parameters (frequency, error, user) that describe the simulation.

    Returns:
    None
    """
    # user data
    un = user["username"]
    pw = user["password"]
    ### as new trajectory
    with open(f"assets/users/{un}_{pw}/trajectories/sim__freq{name[0]}_err{name[1]}_user{name[2]}.csv", "w") as f:
        lines = [[time_stamps[i], positions[i][0], positions[i][1]] for i in range(len(time_stamps))]
        output = "timestamp x y error quality \n"
        for row in lines:
            output += f"{row[0]} {row[1]} {row[2]}\n"
        f.write(output)
    ### export
    # antennas
    if len(os.listdir(f"assets/users/{un}_{pw}/antennas")):
        ant_header = ""
        ants = []
        antennas = np.loadtxt(f"assets/users/{un}_{pw}/antennas/antennas.csv", skiprows=1)
        ant = []
        for i in range(antennas.shape[0]):
            ant_header += f"ant{i+1}_dist ant{i+1}_azim "
            ant_pos = antennas[i]
            liste = [f"{distance(ant_pos, positions[j])} {azimuth(ant_pos, positions[j])} " for j in range(len(time_stamps))]
            ant.append(liste)
        for i in range(len(liste)):
            line = ""
            for j in range(len(ant)):
                line += ant[j][i]
            ants.append(line)
        with open(f"assets/exports/results_{un}_{pw}/sm/sim__freq{name[0]}_err{name[1]}_user{name[2]}.csv", "w") as f:
            lines = [[time_stamps[i], positions[i][0], positions[i][1], errors[i], qualities[i], ants[i]] for i in range(len(time_stamps))]
            output = f"timestamp x y error quality {ant_header[:-1]}\n"
            for row in lines:
                output += f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]}\n"
            f.write(output)
        # push to cloud if not demo data logged in
        if f"{un}_{pw}" != "demo_data":
            u.update_user_data(nc, f"{un}_{pw}/trajectories/sim__freq{name[0]}_err{name[1]}_user{name[2]}.csv")
    # no antennas
    else:
        with open(f"assets/exports/results_{un}_{pw}/sm/sim__freq{name[0]}_err{name[1]}_user{name[2]}.csv", "w") as f:
            lines = [[time_stamps[i], positions[i][0], positions[i][1], errors[i], qualities[i]] for i in range(len(time_stamps))]
            output = "timestamp x y error quality \n"
            for row in lines:
                output += f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}\n"
            f.write(output)
        # push to cloud if not demo data logged in
        if f"{un}_{pw}" != "demo_data":
            u.update_user_data(nc, f"{un}_{pw}/trajectories/sim__freq{name[0]}_err{name[1]}_user{name[2]}.csv")


if __name__ == "__main__":    
    pass
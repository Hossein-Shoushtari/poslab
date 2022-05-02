##### Coordinate Simulation class
### IMPORTS
# built in
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
# installed
from geojson import Point
from geopandas import GeoSeries


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

def simulate_positions(groundtruth, error, measurement_freq, query_freq, number_of_users, number_of_intervalls,
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
    # getting selected ground truth data
    with open(f"assets/exports/gt/{groundtruth}.csv", "r") as f:
        gt = list(csv.reader(f, delimiter=";"))[1:]
        gt = np.array(gt).astype(np.float)

    rows = gt
    positions = []
    time_stamps = []

    error_list = []
        # for row in reader:
            # rows.append([float(row[0].split(' ')[0]), float(row[0].split(' ')[1]), float(row[0].split(' ')[2])])
    original_time_stamps = [r[0] for r in rows]
    intervall_lengths, semantic_errors, intervall_starts = semantic_error(number_of_intervalls, error_range,
                                                                          intervall_range, original_time_stamps)


    # current_intervall_start = intervall_starts[0]
    # current_semantic_error = semantic_errors[0]
    # current_intervall_length = intervall_lengths[0]
    count = 0
    semantic_active = False

    if number_of_users > query_freq:
        #overflow = number_of_users - query_freq
        duration = (number_of_users / query_freq) * 1000
        ts = rows[0][0]
        print(measurement_freq, 'measurement_freq')
        print(query_freq, 'query_freq')
        print(number_of_users, 'number of users')
        print(duration, 'duration')
        measurement_freq = measurement_freq / 1000
        query_freq = query_freq / 1000
        print(rows[1][0] - rows[0][0], 'first sequel')

        for r in range(len(rows)):
            if r == 0:
                time_stamps.append(ts)

                if semantic == True:
                    if rows[r][0] >= intervall_starts[count] and rows[r][0] <= intervall_starts[count] + \
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
                positions.append([rows[r][1] + x_error, rows[r][2] + y_error])
                ts += duration

            else:

                x_error = np.random.normal(0, current_error)
                y_error = np.random.normal(0, current_error)
                error_list.append(np.sqrt(x_error ** 2 + y_error ** 2))
                positions.append([rows[r][1] + x_error, rows[r][2] + y_error])

                ts += duration

            dt = 1 / measurement_freq
            t1 = rows[r][0]
            t2 = rows[r][0] + dt

            if r <= len(rows) - 2:
                dx = ((rows[r + 1][1] - rows[r][1]) / (rows[r + 1][0] - rows[r][0])) * dt
                dy = ((rows[r + 1][2] - rows[r][2]) / (rows[r + 1][0] - rows[r][0])) * dt
                # dz = ((rows[r-1][3] - rows[r][3])/(rows[r-1][0] - rows[r][0]))*dt

                x_temp = rows[r][1] + dx
                y_temp = rows[r][2] + dy
                # z_temp = rows[r][3] + dz

            while t2 < rows[-1][0] and t2 < rows[r + 1][0]:
                time_stamps.append(ts)
                x_error = np.random.normal(0, current_error)
                y_error = np.random.normal(0, current_error)
                error_list.append(np.sqrt(x_error ** 2 + y_error ** 2))
                positions.append([x_temp + dx + np.random.uniform(-current_error, current_error, 1)[0],
                                  y_temp + dy + np.random.uniform(-error, error, 1)[0]])
                t2 = t2 + dt
                x_temp = x_temp + dx
                y_temp = y_temp + dy

                ts += duration


    else:

        for r in range(len(rows)):

            time_stamps.append(rows[r][0])

            if semantic == True:
                if rows[r][0] >= intervall_starts[count] and rows[r][0] <= intervall_starts[count] + \
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
            positions.append([rows[r][1] + x_error, rows[r][2] + y_error])

            dt = 1 / measurement_freq
            t1 = rows[r][0]
            t2 = rows[r][0] + dt

            if r <= len(rows) - 2:
                dx = ((rows[r + 1][1] - rows[r][1]) / (rows[r + 1][0] - rows[r][0])) * dt
                dy = ((rows[r + 1][2] - rows[r][2]) / (rows[r + 1][0] - rows[r][0])) * dt
                # dz = ((rows[r-1][3] - rows[r][3])/(rows[r-1][0] - rows[r][0]))*dt

                x_temp = rows[r][1] + dx
                y_temp = rows[r][2] + dy
                # z_temp = rows[r][3] + dz

            while t2 < rows[-1][0] and t2 < rows[r + 1][0]:
                time_stamps.append(t2)
                x_error = np.random.normal(0, current_error)
                y_error = np.random.normal(0, current_error)
                error_list.append(np.sqrt(x_error ** 2 + y_error ** 2))
                positions.append([x_temp + dx + np.random.uniform(-current_error, current_error, 1)[0],
                                  y_temp + dy + np.random.uniform(-current_error, current_error, 1)[0]])
                t2 = t2 + dt
                x_temp = x_temp + dx
                y_temp = y_temp + dy

        qualities_list = []
        for e in error_list:
            quality = closest_value([error / 5, 2 * error / 5, 3 * error / 5, 4 * error / 5, 5 * error / 5],
                                    e)
            qualities_list.append(quality)

    return time_stamps, positions, error_list, qualities_list

def azimuth(point1: tuple, point2: tuple) -> float:
    '''azimuth between 2 points (interval 0 - 360)'''
    angle = np.arctan2(point2[0] - point1[0], point2[1] - point1[1])
    return np.degrees(angle) if angle >= 0 else np.degrees(angle) + 360

def distance(point1: tuple, point2: tuple) -> float:
    '''distance between 2 points'''
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def export_sim(time_stamps: list, positions: list, errors: list, qualities: list):
    ant_header = ""
    ants = []
    if len(os.listdir("assets/antennas")):
        antennas = np.loadtxt("assets/antennas/antennas.csv")
        ant = []
        for i in range(antennas.shape[0]):
            ant_header += f"ant{i+1}_dist;ant{i+1}_azim;"
            ant_pos = antennas[i][1:]
            liste = [f"{distance(ant_pos, positions[j])};{azimuth(ant_pos, positions[j])};" for j in range(len(time_stamps))]
            ant.append(liste)
        for i in range(len(liste)):
            line = ""
            for j in range(len(ant)):
                line += ant[j][i]
            ants.append(line)

    with open(f"assets/exports/sm/simulated_measurements__{datetime.now().strftime('%H-%M-%S')}.csv", "w") as f:
        lines = [[time_stamps[i], positions[i][0],positions[i][1], errors[i], qualities[i], ants[i]] for i in range(len(time_stamps))]
        output = f"time stamp;x;y;error;quality;{ant_header[:-1]}\n"
        for row in lines:
            output += f"{row[0]};{row[1]};{row[2]};{row[3]};{row[4]};{row[5]}\n"
        f.write(output)


if __name__ == "__main__":    
    ####Coordinate Simulation
    """
    check if the simulate_positions function is working
    """

    filename = 'assets/groundtruth/GroundTruthEight.csv'

    with open(filename, newline='') as f:

        reader = csv.reader(f)

        rows = []

        error_list = []
        for row in reader:
            rows.append([float(row[0].split(' ')[0]), float(row[0].split(' ')[1]), float(row[0].split(' ')[2])])
    grundtruth = rows

    error = 2
    measurement_freq = 1
    number_range = [1, 10] # range of number of occurencies for segments with semantic error
    error_range = [1, 15] # range of possible values for the semantic errors
    intervall_range = [1 * 1000, 20 * 1000] # range of intervall lengths where semantic errors are generated
    semantic_is_used = False # set this to True if semantic errors are used

    time_stamps, positions, errors, qualities = simulate_positions(grundtruth, error, measurement_freq, 500, 1, 1,[1, 15], [1 * 1000, 20 * 1000],semantic_is_used)
    

    print('qualities',qualities)
    print('errors', errors)

    points_positions = []
    for p in positions:
        points_positions.append(Point(p))

    # print(points_positions)
    GeoSeries(points_positions).plot(figsize=(10, 10), color='red', markersize=100, label='5G positions')
    plt.pause(60)
##### Coordinate Simulation class!!!
### IMPORTS
# built in
import csv
import numpy as np
import matplotlib.pyplot as plt
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

def semantic_error(number_range, error_range, intervall_range, time_stamps):
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
    number_of_intervalls = np.random.randint(number_range[0], number_range[-1])
    intervall_lengths = []
    intervall_starts = []
    errors = []

    for i in range(number_of_intervalls):
        intervall_lengths.append(np.random.uniform(intervall_range[0], intervall_range[-1]))  # choose random intervalls (according to number of intervalls) from the timeline
        intervall_starts.append(np.random.choice(time_stamps[:-1]))
        errors.append(np.random.uniform(error_range[0], error_range[-1]))

    return intervall_lengths, errors, intervall_starts

def simulate_positions(filename, error, freq, number_range=[1, 10], error_range=[1, 15], intervall_range=[1 * 1000, 20 * 1000], semantic=False):
    """
        creating sample data points for 5G measurements with defined frequency and measurement error range. Semantic errors are
        generated in rondomly with chosen ranges for the duration, standard deviation and number of accurances

        Parameters
        ----------
        semantic : if True use semantic errors, if False don't use semantic errors - Boolean
        filename : name of csv file containing groundtrouth data points - string
        error : desired error for 5G positions  - float
        freq : frequency of 5G measurements in (number of measurements/second) - float
        number_range : range of number of accurances of semantic errors - tuple of integers
        error_range : range of possible error values for the semantic error - tuple of floats
        intervall_range : range of possible lengths for the semantic errors - tuple of floats

        Returns
        -------
        positions : simulated positions from 5G measurements - array of arrays (tuples) of floats
        time_stamps : timestamps of 5G measurements - array of floats
        error_list : list of the errors for each measurement - array of floats
        qualities_list : estimated qualities for each measurement (as closest value from an list of quality values to the real error) - array of floats
        """
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        rows = []
        positions = []
        time_stamps = []

        freq = freq / 1000

        error_list = []
        for row in reader:
            rows.append([float(row[0].split(' ')[0]), float(row[0].split(' ')[1]), float(row[0].split(' ')[2])])

        original_time_stamps = [r[0] for r in rows]
        intervall_lengths, semantic_errors, intervall_starts = semantic_error(number_range, error_range,
                                                                              intervall_range, original_time_stamps)
        count = 0
        semantic_active = False

        for r in range(len(rows)):

            time_stamps.append(rows[r][0])

            if semantic == True:
                if rows[r][0] >= intervall_starts[count] and rows[r][0] <= intervall_starts[count] + intervall_lengths[
                    count]:
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

            dt = 1 / freq
            #t1 = rows[r][0]
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
            quality = closest_value([error / 5, 2 * error / 5, 3 * error / 5, 4 * error / 5, 5 * error / 5], e)
            qualities_list.append(quality)

        return time_stamps, positions, error_list, qualities_list

if __name__ == "__main__":    
    ####Coordinate Simulation
    """
    check if the simulate_positions function is working
    """

    filename = 'assets/groundtruth/GroundTruthEight.csv'
    error = 2
    freq = 1
    number_range = [1, 10] # range of number of occurencies for segments with semantic error
    error_range = [1, 15] # range of possible values for the semantic errors
    intervall_range = [1 * 1000, 20 * 1000] # range of intervall lengths where semantic errors are generated
    semantic_is_used = False # set this to True if semantic errors are used
    time_stamps, positions, errors, qualities = simulate_positions(filename,2,1)
    print('qualities',qualities)
    print('errors', errors)

    points_positions = []
    for p in positions:
        points_positions.append(Point(p))

    print(points_positions)
    GeoSeries(points_positions).plot(figsize=(10, 10), color='red', markersize=100, label='5G positions')
    plt.pause(60)
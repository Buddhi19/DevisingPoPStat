import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def calculate_interval_variance(time_series_data, interval=14):
    # blocks of time sequence data to analyze for variance
    time_positions = np.arange(1 + len(time_series_data) // interval) * interval

    block_variance = list()

    for interval_start in time_positions:
        interval_stop = interval_start + interval
        interval_stop = min(interval_stop, len(time_series_data))
        block_variance.append(np.std(time_series_data[interval_start: interval_stop]))

    return block_variance


def smooth_time_series_data(time_series_data, interval=14):
    smooth_signal_time_stamps = list()
    smooth_signal = list()

    for index in range(len(time_series_data) - interval + 1):
        signal_window = time_series_data[index: index + interval]
        smooth_signal.append(np.average(signal_window))
        smooth_signal_time_stamps.append(df_covid['time series'][index + interval - 1])

    return smooth_signal, smooth_signal_time_stamps


def detect_waves(data_signal, time_stamps, peak_locations, trough_locations):
    while len(peak_locations) != 0:
        # get the next peak and trough locations in the data signal and store the values
        current_peak, current_trough = peak_locations[0], trough_locations[0]
        current_peak_value, current_trough_value = data_signal[current_peak], data_signal[current_trough]

        # remove the current peak and trough locations from the peak and trough arrays
        peak_locations, trough_locations = np.delets(peak_locations, 0), np.delete(trough_locations, 0)

        while len(peak_locations) != 0:
            # get the next peak and trough values to compare with the previous peak and trough values
            next_peak, next_trough = peak_locations[0], trough_locations[0]
            next_peak_value, next_trough_value = data_signal[next_peak], data_signal[next_trough]

            # remove the respective peak and trough locations from the peak and trough arrays
            peak_locations, trough_locations = np.delete(peak_locations, 0), np.delete(trough_locations, 0)


path = 'population_study/my_files/'
print(os.path.abspath(path))

file_names = os.listdir(path)
first_wave_locations = list()


for file_index in range(360, len(file_names), 2):

    df_covid = pd.read_csv(path+file_names[file_index])

    # time span to separate
    time_span = 28  # days
    tick_positions = len(df_covid['time series'])//time_span
    tick_positions = np.arange(tick_positions + 1) * time_span
    tick_labels = df_covid['time series'][tick_positions].values

    df_population = pd.read_csv(path+file_names[1])

    '''plt.plot(df_covid['time series'], df_covid['new_cases_smoothed'])
    plt.xticks(tick_positions, tick_labels, rotation=90)'''

    std_result = calculate_interval_variance(df_covid['new_cases_smoothed_per_million'], interval=time_span)
    smooth_signal, smooth_signal_time_stamps = smooth_time_series_data(df_covid['new_cases_smoothed_per_million'],
                                                                       interval=time_span)

    plt.figure()
    '''plt.plot(tick_positions, std_result)
    plt.xticks(tick_positions, tick_labels, rotation=90)'''

    # get the peaks and the troughs of the smoothed signal
    peaks = find_peaks(smooth_signal)[0]

    troughs = find_peaks([1/(value+1e-6) for value in smooth_signal])[0]

    plt.plot(smooth_signal)

    for index, trough in enumerate(troughs):
        plt.text(trough, smooth_signal[trough], index)

    plt.title(file_names[file_index].split('_')[0])
    plt.show()

    first_wave_location = input('Enter wave location: ')
    if len(first_wave_location) == 0:
        first_wave_location = len(smooth_signal)
    elif first_wave_location == '*':
        continue
    else:
        first_wave_location = troughs[int(first_wave_location)]
    country_name = file_names[file_index].split('_')[0]
    first_wave_locations.append([country_name, first_wave_location])
    print(f'{len(file_names)//2}||{file_index//2+1}')

    # save first wave locations
    path_save = 'population_study/'
    df = pd.DataFrame(first_wave_locations)
    file_name = path_save + 'first_wave_locations_8.csv'
    df.to_csv(file_name, index=False)

'''for first_wave in first_waves:
    plt.plot(first_wave)
    plt.show()'''

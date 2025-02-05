import statistics


from find_file_function import find_event_files
from functions_for_comparing_data import headbend_vs_majority , aispg_vs_majority
from error_counts_and_full_sleep_functions import error_houers_count , total_sleeping_hours
from creating_plots import plot_sleep_stages
from function_for_reviewing_patients import review_subjects

# Main script execution
hb_vs_mj_sec = []
psgai_vs_mj_sec = []
error_houers = 0
sleeping_houers = 0

# Find event files
headband_files, psg_files = find_event_files('files_for_python_project')

# Iterate over the headband and PSG files to calculate statistics
for headband_file, psg_file in zip(headband_files, psg_files):
    hb_vs_mj_sec.append(headbend_vs_majority(headband_file, psg_file))
    psgai_vs_mj_sec.append(aispg_vs_majority(psg_file))
    error_houers += error_houers_count(headband_file)
    sleeping_houers += total_sleeping_hours(headband_file)

# Filter out None values from hb_vs_mj_sec list
hb_vs_mj_sec = [x for x in hb_vs_mj_sec if x is not None]

# Display results
print(f"We found {round(statistics.mean(hb_vs_mj_sec), 2)}% match between the headband AI and the majority")
print(f"We found {round(statistics.mean(psgai_vs_mj_sec), 2)}% match between the PSG AI and the majority")
print(f"There were {round(error_houers, 2)} hours of missing data out of a total of {round(sleeping_houers, 2)} sleeping hours in the headband experiment")

# Call the review function
review_subjects(headband_files, psg_files)
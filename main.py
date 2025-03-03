import statistics
import logging
#importing the needed functions from different files.
from files_for_python_project.find_file_function import find_event_files
from files_for_python_project.functions_for_comparing_data import headband_vs_majority , aispg_vs_majority
from files_for_python_project.error_counts_and_full_sleep_functions import error_hours_count , total_sleeping_hours
from files_for_python_project.function_for_reviewing_patients import review_subjects

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Main script execution
logging.info("Starting main script...")

# Main script execution
hb_vs_mj_sec = []
psgai_vs_mj_sec = []
error_houers = 0
sleeping_houers = 0

# Find event files
headband_files, psg_files = find_event_files('files_for_python_project')

# Iterate over the headband and PSG files to calculate statistics
for headband_file, psg_file in zip(headband_files, psg_files):
    hb_vs_mj_sec.append(headband_vs_majority(headband_file, psg_file))
    psgai_vs_mj_sec.append(aispg_vs_majority(psg_file))
    error_houers += error_hours_count(headband_file)
    sleeping_houers += total_sleeping_hours(headband_file)

# Filter out None values from hb_vs_mj_sec list
hb_vs_mj_sec = [x for x in hb_vs_mj_sec if x is not None]

# Display results using logger instead of print
logging.info(f"We found {round(statistics.mean(hb_vs_mj_sec), 2)}% match between the headband AI and the majority")
logging.info(f"We found {round(statistics.mean(psgai_vs_mj_sec), 2)}% match between the PSG AI and the majority")
logging.info(f"There were {round(error_houers, 2)} hours of missing data out of a total of {round(sleeping_houers, 2)} DATA hours collected in the headband experiment")

# Call the review function
review_subjects(headband_files, psg_files)

import re
import os
import logging
from creating_plots import plot_sleep_stages

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def review_subjects(headband_files, psg_files):
    """
    Allows the user to review subjects by entering a subject number.
    
    Parameters:
    headband_files (list): A list of paths to the headband event files.
    psg_files (list): A list of paths to the PSG event files.
    """
    while True:
        # Allow the user to input a subject number
        while True:
            subject_id_input = input("Please enter a subject number: ").strip()  # Strip any extra spaces

            logging.info(f"Looking for subject number: '{subject_id_input}'")

            # Check if the input matches any of the headband files
            matching_headband_file = None
            for headband_file in headband_files:
                # Extract subject number from the filename using regex (match 'sub-<number>' format)
                filename = os.path.basename(headband_file)
                match = re.match(r'sub-(\d+)_', filename)
                if match:
                    subject_id_in_filename = match.group(1)  # Get the numeric subject ID

                    if subject_id_input == subject_id_in_filename:
                        matching_headband_file = headband_file
                        break

            # Check if the input matches any of the PSG files
            matching_psg_file = None
            for psg_file in psg_files:
                # Extract subject number from the filename using regex (match 'sub-<number>' format)
                filename = os.path.basename(psg_file)
                match = re.match(r'sub-(\d+)_', filename)
                if match:
                    subject_id_in_filename = match.group(1)  # Get the numeric subject ID

                    if subject_id_input == subject_id_in_filename:
                        matching_psg_file = psg_file
                        break

            if matching_headband_file and matching_psg_file:
                # If both files are found, plot the sleep stages
                logging.info(f"Found matching files for subject {subject_id_input}. Displaying plots...")
                plot_sleep_stages([matching_psg_file], [matching_headband_file])
                break  # Exit the loop after plotting
            else:
                # If no matching files, prompt the user again
                logging.warning(f"The subject number you entered doesn't exist, please enter a new subject number.")
        
        # Ask if the user wants to review another subject's data
        while True:
            review_another = input("Do you want to review another subject's data? (y/n): ").strip().lower()

            if review_another == 'y':
                break  # Continue to the next iteration and ask for a new subject number
            elif review_another == 'n':
                logging.info("Exiting the program.")
                exit()  # Exit the program
            else:
                logging.warning("Invalid input. Please enter 'y' to review another subject or 'n' to exit.")

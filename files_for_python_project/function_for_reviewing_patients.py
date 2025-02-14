import re
import os
import logging
from files_for_python_project.creating_plots import plot_sleep_stages

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_matching_file(subject_id_input, file_list):
    """
    Helper function to get a matching file based on the subject ID.

    Parameters:
    subject_id_input (str): The subject ID to look for.
    file_list (list): List of file paths to check.

    Returns:
    str or None: The matching file path or None if no match is found.
    """
    for file in file_list:
        filename = os.path.basename(file)
        match = re.match(r'sub-(\d+)_', filename)

        if match:
            subject_id_in_filename = match.group(1)
            if subject_id_input == subject_id_in_filename:
                return file
            
    return None

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

            # Handle empty subject input or invalid ID directly
            if not subject_id_input:
                logging.warning("Subject ID cannot be empty. Please enter a valid subject number.")
                continue  # Skip to the next iteration to ask for the subject again
            
            logging.info(f"Looking for subject number: '{subject_id_input}'")


            matching_headband_file = get_matching_file(subject_id_input, headband_files)
            matching_psg_file = get_matching_file(subject_id_input, psg_files)


            if matching_headband_file and matching_psg_file:
                # If both files are found, plot the sleep stages
                logging.info(f"Found matching files for subject {subject_id_input}. Displaying plots...")
                logging.debug("Calling plot_sleep_stages with:", psg_files, headband_files)

                try:
                    print("Attempting to call plot_sleep_stages...")  # Debugging statement
                    plot_sleep_stages([matching_psg_file], [matching_headband_file])
                    print("Successfully called plot_sleep_stages")  # This should appear if it runs
                except Exception as e:
                    print(f"Error calling plot_sleep_stages: {e}")  # Catches and logs the exception

                break  # Exit the loop after plotting
            else:
                # If no matching files, prompt the user again
                logging.warning(f"The subject number you entered doesn't exist, please enter a new subject number.")
        
        # Ask if the user wants to review another subject's data
        while True:
            review_another = input("Do you want to review another subject's data? (y/n): ").strip().lower()

            # Validate user input for 'y' or 'n'
            if review_another == 'y':
                break  # Continue to the next iteration and ask for a new subject number
            elif review_another == 'n':
                logging.info("Exiting the program.")
                return  # Exit the function gracefully
            else:
                logging.warning("Invalid input. Please enter 'y' to review another subject or 'n' to exit.")

import logging
import os

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to find event files within the provided base folder
def find_event_files(base_folder):
    """
    Finds and returns pairs of headband and PSG event files within the given directory structure.
    
    Parameters:
    base_folder (str): The path to the base folder containing the subject data folders.
    
    Returns:
    tuple: A tuple containing two lists - headband_files and psg_files.
    """
    headband_files = []
    psg_files = []

    # Check if base_folder exists and is a valid directory
    if not os.path.isdir(base_folder):
        logging.error(f"'{base_folder}' is not a valid directory.")
        return headband_files, psg_files

    # Iterate through each subfolder in the base folder, if the subfolder is a valid directory, the function will add the subfolder name "eeg" to the folder path
    for entry in os.scandir(base_folder):
        if entry.is_dir():
            eeg_folder_path = os.path.join(entry.path, "eeg")

            if os.path.isdir(eeg_folder_path):
                headband_file, psg_file = None, None

                # Loop through files in "eeg" folder
                for file_entry in os.scandir(eeg_folder_path):
                    if file_entry.is_file():
                        # Identify headband and PSG event files
                        if file_entry.name.endswith("headband_events.tsv"):
                            headband_file = file_entry.path
                        elif file_entry.name.endswith("psg_events.tsv"):
                            psg_file = file_entry.path

                    # If both files are found, exit loop early
                    if headband_file and psg_file:
                        break

                # Only add files if BOTH are found
                if headband_file and psg_file:
                    headband_files.append(headband_file)
                    psg_files.append(psg_file)

    return headband_files, psg_files
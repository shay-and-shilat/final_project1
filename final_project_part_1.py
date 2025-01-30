import os

def find_event_files(base_folder):
    headband_files = []
    psg_files = []

    # Check if base_folder exists and is a directory
    if not os.path.isdir(base_folder):
        print(f"Error: '{base_folder}' is not a valid directory.")
        return headband_files, psg_files

    # Iterate through each subfolder in the base folder
    for entry in os.scandir(base_folder):
        if entry.is_dir():
            eeg_folder_path = os.path.join(entry.path, "eeg")

            if os.path.isdir(eeg_folder_path):
                headband_file, psg_file = None, None

                # Loop through files in "eeg" folder
                for file_entry in os.scandir(eeg_folder_path):
                    if file_entry.is_file():
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


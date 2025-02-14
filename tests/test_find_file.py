import os
import tempfile
import pytest
import sys

# Add the root project directory to sys.path so that the module can be imported.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the function to be tested from the project module.
from files_for_python_project.find_file_function import find_event_files  # Ensure correct module path

def create_test_files(base_path, subject, create_headband=True, create_psg=True, extra_files=False):
    """
    Creates a simulated EEG directory structure with optional headband and PSG event files.

    Parameters:
        base_path (str): The base directory in which the subject directories will be created.
        subject (str): The subject identifier (e.g., "sub-10").
        create_headband (bool): Whether to create a headband events file.
        create_psg (bool): Whether to create a PSG events file.
        extra_files (bool): Whether to create extra unrelated files in the directory.

    Returns:
        tuple: A tuple containing the paths to the headband file and PSG file. 
               If a file is not created, its corresponding value will be None.
    """
    # Construct the EEG directory path for the given subject.
    eeg_path = os.path.join(base_path, subject, "eeg")
    os.makedirs(eeg_path, exist_ok=True)
    
    headband_file = None
    psg_file = None
    
    # Create the headband events file if required.
    if create_headband:
        headband_file = os.path.join(eeg_path, f"{subject}_task-Sleep_acq-headband_events.tsv")
        with open(headband_file, "w") as f:
            f.write("dummy headband data")
    
    # Create the PSG events file if required.
    if create_psg:
        psg_file = os.path.join(eeg_path, f"{subject}_task-Sleep_acq-psg_events.tsv")
        with open(psg_file, "w") as f:
            f.write("dummy psg data")
    
    # Optionally create extra files that should be ignored by the function.
    if extra_files:
        with open(os.path.join(eeg_path, "unrelated_file.txt"), "w") as f:
            f.write("This is an extra file.")
        with open(os.path.join(eeg_path, "random_notes.tsv"), "w") as f:
            f.write("This file should be ignored.")  # Different name format
    
    return headband_file, psg_file

def test_find_event_files(caplog):
    """
    Test the 'find_event_files' function to verify that it correctly identifies matching 
    headband and PSG event files in a directory structure.

    This test creates multiple subject directories with different combinations:
        - Subjects with both headband and PSG files.
        - Subjects with incomplete file pairs.
    
    It then checks:
        - That only subjects with complete file pairs are returned.
        - That the correct file paths are included.
        - That appropriate log messages are generated for missing files.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test data for several subjects.
        headband1, psg1 = create_test_files(temp_dir, "sub-10")
        headband2, psg2 = create_test_files(temp_dir, "sub-20")
        create_test_files(temp_dir, "sub-30", create_headband=True, create_psg=False)  # Incomplete pair: missing PSG file
        create_test_files(temp_dir, "sub-40", create_headband=False, create_psg=True)  # Incomplete pair: missing headband file
        headband3, psg3 = create_test_files(temp_dir, "sub-50")  # Valid pair for sub-50

        # Execute the function to find event files within the temporary directory.
        headband_files, psg_files = find_event_files(temp_dir)

        # Debug: Print out found files to see what was collected (useful during development).
        print("Headband files:", headband_files)
        print("PSG files:", psg_files)

        # Validate results:
        # Expect valid pairs for subjects: sub-10, sub-20, and sub-50.
        # Sorting ensures that order does not affect the comparison.
        assert sorted(headband_files) == sorted([headband1, headband2, headband3])
        assert sorted(psg_files) == sorted([psg1, psg2, psg3])

        # Ensure that only complete pairs are included.
        assert len(headband_files) == len(psg_files)
        
        # Check that the logs contain messages about missing event files for the incomplete pairs.
        assert "Missing PSG file" in caplog.text
        assert "Missing headband file" in caplog.text

def test_empty_directory():
    """
    Test the 'find_event_files' function with an empty directory.
    
    Expectation:
        - No event files (headband or PSG) should be found.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        headband_files, psg_files = find_event_files(temp_dir)
        # Since the directory is empty, both lists should be empty.
        assert headband_files == []
        assert psg_files == []

def test_nonexistent_directory():
    """
    Test the 'find_event_files' function with a directory path that does not exist.

    Expectation:
        - The function should handle the non-existent directory gracefully,
          returning empty lists for both headband and PSG files.
    """
    headband_files, psg_files = find_event_files("nonexistent_path")
    assert headband_files == []
    assert psg_files == []

if __name__ == "__main__":
    # If this script is run directly, execute the tests.
    pytest.main()

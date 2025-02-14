import os
import tempfile
import pytest
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from files_for_python_project.find_file_function import find_event_files  # Ensure correct module path

def create_test_files(base_path, subject, create_headband=True, create_psg=True, extra_files=False):
    """Creates a test EEG directory with optional headband and PSG event files."""
    eeg_path = os.path.join(base_path, subject, "eeg")
    os.makedirs(eeg_path, exist_ok=True)
    
    headband_file = None
    psg_file = None
    
    if create_headband:
        headband_file = os.path.join(eeg_path, f"{subject}_task-Sleep_acq-headband_events.tsv")
        with open(headband_file, "w") as f:
            f.write("dummy headband data")
    
    if create_psg:
        psg_file = os.path.join(eeg_path, f"{subject}_task-Sleep_acq-psg_events.tsv")
        with open(psg_file, "w") as f:
            f.write("dummy psg data")
    
    if extra_files:
        with open(os.path.join(eeg_path, "unrelated_file.txt"), "w") as f:
            f.write("This is an extra file.")
        with open(os.path.join(eeg_path, "random_notes.tsv"), "w") as f:
            f.write("This file should be ignored.")  # Different name format
    
    return headband_file, psg_file

def test_find_event_files(caplog):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test data
        headband1, psg1 = create_test_files(temp_dir, "sub-10")
        headband2, psg2 = create_test_files(temp_dir, "sub-20")
        create_test_files(temp_dir, "sub-30", create_headband=True, create_psg=False)  # Incomplete pair
        create_test_files(temp_dir, "sub-40", create_headband=False, create_psg=True)  # Incomplete pair
        headband3, psg3 = create_test_files(temp_dir, "sub-50")  # Valid pair for sub-50

        # Run function
        headband_files, psg_files = find_event_files(temp_dir)

        # Debug: Print out found files to see what was collected
        print("Headband files:", headband_files)
        print("PSG files:", psg_files)

        # Validate results
        # Expecting sub-10, sub-20, and sub-50 to be valid pairs, so we sort and compare
        assert sorted(headband_files) == sorted([headband1, headband2, headband3])
        assert sorted(psg_files) == sorted([psg1, psg2, psg3])

        # Ensure incomplete pairs are not included
        assert len(headband_files) == len(psg_files)
        
        # Check logs for missing event files
        assert "Missing PSG file" in caplog.text
        assert "Missing headband file" in caplog.text

def test_empty_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        headband_files, psg_files = find_event_files(temp_dir)
        assert headband_files == []
        assert psg_files == []

def test_nonexistent_directory():
    headband_files, psg_files = find_event_files("nonexistent_path")
    assert headband_files == []
    assert psg_files == []

if __name__ == "__main__":
    pytest.main()

import pytest
import pandas as pd
import os
import sys

# Add the root project directory to the sys.path so Python can locate the 'files_for_python_project' module.
# This ensures that modules in the project can be imported even if the test script is run from a different directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the functions to be tested from the project module.
from files_for_python_project.functions_for_comparing_data import headband_vs_majority, aispg_vs_majority  

# Fixture to set up temporary test files for testing.
@pytest.fixture(scope="module")
def setup_test_files():
    """
    Creates temporary test files needed for testing and returns their file paths.
    
    This fixture creates four test files in a dedicated 'test_data' directory:
    - headband_file: A headband events file containing a small dataset with one missing data point (represented by -2).
    - psg_file: A PSG events file containing a small valid dataset.
    - high_error_file: A headband events file where all data points indicate missing data (all values are -2),
      which is used to simulate a high error scenario.
    - empty_file: An empty file to test edge cases (e.g., no data available).
    
    After the tests are executed, the fixture cleans up by deleting the temporary files and the directory.
    
    Yields:
        tuple: A tuple containing the paths to the headband_file, psg_file, high_error_file, and empty_file.
    """
    # Create a directory for test data if it doesn't already exist.
    test_dir = "test_data"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create a valid headband file with one missing data point (-2) in the 'ai_hb' column.
    headband_file = os.path.join(test_dir, "sub-1_headband_events.tsv")
    pd.DataFrame({
        "ai_hb": [1, 2, 3, -2, 2],  # One missing data point (-2)
        "majority": [1, 2, 3, 3, 2]
    }).to_csv(headband_file, sep="\t", index=False)
    
    # Create a valid PSG file.
    psg_file = os.path.join(test_dir, "sub-1_psg_events.tsv")
    pd.DataFrame({
        "ai_psg": [1, 2, 3, 4, 2],
        "majority": [1, 2, 3, 3, 2]
    }).to_csv(psg_file, sep="\t", index=False)

    # Create a headband file with high error rate: all values in 'ai_hb' are -2.
    high_error_file = os.path.join(test_dir, "sub-1_high_error_headband.tsv")
    pd.DataFrame({
        "ai_hb": [-2, -2, -2, -2, -2],
        "majority": [1, 2, 3, 4, 5]
    }).to_csv(high_error_file, sep="\t", index=False)

    # Create an empty file to simulate edge cases.
    empty_file = os.path.join(test_dir, "empty.tsv")
    pd.DataFrame().to_csv(empty_file, sep="\t", index=False)
    
    # Yield the file paths to the tests.
    yield headband_file, psg_file, high_error_file, empty_file
    
    # Cleanup: remove all files created and the test_data directory after tests are completed.
    for file in os.listdir(test_dir):
        os.remove(os.path.join(test_dir, file))
    os.rmdir(test_dir)

# Test function for headband_vs_majority with valid data.
def test_headband_vs_majority_success(setup_test_files):
    """
    Test that headband_vs_majority returns a float value within the expected range [0, 100]
    when provided with valid headband and PSG files.
    """
    # Unpack the file paths from the fixture.
    headband_file, psg_file, _, _ = setup_test_files
    # Call the function with valid test files.
    result = headband_vs_majority(headband_file, psg_file)
    # Assert that the result is a float.
    assert isinstance(result, float)
    # Assert that the result is within the valid range (e.g., a percentage).
    assert 0 <= result <= 100

# Test function for headband_vs_majority with a high error headband file.
def test_headband_vs_majority_high_error(setup_test_files):
    """
    Test that headband_vs_majority returns None when the headband file has a high error rate
    (all values indicating missing data).
    """
    # Unpack the file paths from the fixture.
    _, psg_file, high_error_file, _ = setup_test_files
    # Call the function with the high error headband file.
    result = headband_vs_majority(high_error_file, psg_file)
    # Assert that the function returns None indicating an error or unacceptable error rate.
    assert result is None

# Test function for headband_vs_majority with an empty file.
def test_headband_vs_majority_empty(setup_test_files):
    """
    Test that headband_vs_majority returns None when the headband file is empty.
    """
    # Unpack the file paths from the fixture.
    _, psg_file, _, empty_file = setup_test_files
    # Call the function with the empty headband file.
    result = headband_vs_majority(empty_file, psg_file)
    # Assert that the function returns None.
    assert result is None

# Test function for aispg_vs_majority with valid PSG data.
def test_aispg_vs_majority_success(setup_test_files):
    """
    Test that aispg_vs_majority returns a float value within the expected range [0, 100]
    when provided with valid PSG file data.
    """
    # Unpack the file paths from the fixture.
    _, psg_file, _, _ = setup_test_files
    # Call the function with the valid PSG file.
    result = aispg_vs_majority(psg_file)
    # Assert that the result is a float.
    assert isinstance(result, float)
    # Assert that the result is within the valid range (e.g., a percentage).
    assert 0 <= result <= 100

# Test function for aispg_vs_majority with an empty file.
def test_aispg_vs_majority_empty(setup_test_files):
    """
    Test that aispg_vs_majority returns None when the PSG file is empty.
    """
    # Unpack the file paths from the fixture.
    _, _, _, empty_file = setup_test_files
    # Call the function with the empty file.
    result = aispg_vs_majority(empty_file)
    # Assert that the function returns None.
    assert result is None

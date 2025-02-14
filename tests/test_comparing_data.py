import pytest
import pandas as pd
import os
import sys

# Add the root project directory to the sys.path so Python can find the 'files_for_python_project' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from files_for_python_project.functions_for_comparing_data import headband_vs_majority, aispg_vs_majority  

@pytest.fixture(scope="module")
def setup_test_files():
    """
    Set up temporary test files for testing and return file paths.
    This fixture creates:
    - A valid headband AI file with one missing data point (-2)
    - A valid PSG AI file
    - A high-error headband AI file (all -2 values)
    - An empty file to test edge cases
    
    After the tests are completed, the fixture cleans up the temporary files.
    """
    test_dir = "test_data"
    os.makedirs(test_dir, exist_ok=True)
    
    headband_file = os.path.join(test_dir, "sub-1_headband_events.tsv")
    pd.DataFrame({
        "ai_hb": [1, 2, 3, -2, 2],  # One missing data (-2)
        "majority": [1, 2, 3, 3, 2]
    }).to_csv(headband_file, sep="\t", index=False)
    
    psg_file = os.path.join(test_dir, "sub-1_psg_events.tsv")
    pd.DataFrame({
        "ai_psg": [1, 2, 3, 4, 2],
        "majority": [1, 2, 3, 3, 2]
    }).to_csv(psg_file, sep="\t", index=False)

    high_error_file = os.path.join(test_dir, "sub-1_high_error_headband.tsv")
    pd.DataFrame({
        "ai_hb": [-2, -2, -2, -2, -2],
        "majority": [1, 2, 3, 4, 5]
    }).to_csv(high_error_file, sep="\t", index=False)

    empty_file = os.path.join(test_dir, "empty.tsv")
    pd.DataFrame().to_csv(empty_file, sep="\t", index=False)
    
    yield headband_file, psg_file, high_error_file, empty_file
    
    for file in os.listdir(test_dir):
        os.remove(os.path.join(test_dir, file))
    os.rmdir(test_dir)

def test_headband_vs_majority_success(setup_test_files):
    """Test headband AI comparison with valid data."""
    headband_file, psg_file, _, _ = setup_test_files
    result = headband_vs_majority(headband_file, psg_file)
    assert isinstance(result, float)
    assert 0 <= result <= 100

def test_headband_vs_majority_high_error(setup_test_files):
    """Test headband AI comparison when the error rate is too high (should return None)."""
    _, psg_file, high_error_file, _ = setup_test_files
    result = headband_vs_majority(high_error_file, psg_file)
    assert result is None

def test_headband_vs_majority_empty(setup_test_files):
    """Test headband AI comparison with an empty file (should return None)."""
    _, psg_file, _, empty_file = setup_test_files
    result = headband_vs_majority(empty_file, psg_file)
    assert result is None

def test_aispg_vs_majority_success(setup_test_files):
    """Test PSG AI comparison with valid data."""
    _, psg_file, _, _ = setup_test_files
    result = aispg_vs_majority(psg_file)
    assert isinstance(result, float)
    assert 0 <= result <= 100

def test_aispg_vs_majority_empty(setup_test_files):
    """Test PSG AI comparison with an empty file (should return None)."""
    _, _, _, empty_file = setup_test_files
    result = aispg_vs_majority(empty_file)
    assert result is None

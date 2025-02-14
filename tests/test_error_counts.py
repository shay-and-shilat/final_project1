import pytest
import pandas as pd
from io import StringIO
import os
import sys

# Add the root project directory to sys.path so that the module can be imported.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the functions to be tested from the project's module.
from files_for_python_project.error_counts_and_full_sleep_functions import error_hours_count, total_sleeping_hours

# ------------------------------------------------------------------------------
# MOCK DATA SETUP
# ------------------------------------------------------------------------------

# Define mock data strings representing different scenarios for the headband AI data.
# Each string mimics the content of a TSV file.

# valid_ai_data: Contains a valid "ai_hb" column with a mix of -2 (artifact) and other values.
valid_ai_data = """ai_hb
-2
0
-2
1
-2
"""
# Read the mock data string into a pandas DataFrame.
valid_ai_df = pd.read_csv(StringIO(valid_ai_data), sep="\t")

# invalid_ai_data: Does not contain the expected "ai_hb" column; instead it has a 'missing_column'.
invalid_ai_data = """missing_column
-2
0
-2
1
-2
"""
invalid_ai_df = pd.read_csv(StringIO(invalid_ai_data), sep="\t")

# empty_ai_data: Contains only the header with no data rows.
empty_ai_data = """ai_hb
"""
empty_ai_df = pd.read_csv(StringIO(empty_ai_data), sep="\t")

# all_artifacts_data: Contains only artifact values (-2) in the "ai_hb" column.
all_artifacts_data = """ai_hb
-2
-2
-2
-2
-2
"""
all_artifacts_df = pd.read_csv(StringIO(all_artifacts_data), sep="\t")

# ------------------------------------------------------------------------------
# MOCK read_csv FUNCTION
# ------------------------------------------------------------------------------

def mock_read_csv(file, sep="\t"):
    """
    A mock version of pandas.read_csv that returns pre-defined DataFrames based on the input file name.
    
    Parameters:
        file (str): The name of the mock file.
        sep (str): The separator used in the file (default is tab).
    
    Returns:
        pd.DataFrame: A DataFrame corresponding to the mock file content.
    
    Raises:
        FileNotFoundError: If the file name does not match any of the defined mock data.
    """
    if file == "valid_ai_file":
        return valid_ai_df
    elif file == "invalid_ai_file":
        return invalid_ai_df
    elif file == "empty_ai_file":
        return empty_ai_df
    elif file == "all_artifacts_file":
        return all_artifacts_df
    else:
        raise FileNotFoundError("File not found")

# ------------------------------------------------------------------------------
# TEST FUNCTIONS FOR error_hours_count
# ------------------------------------------------------------------------------

def test_error_hours_count(monkeypatch):
    """
    Tests the error_hours_count function using various mock scenarios.
    
    Uses monkeypatch to override pandas.read_csv with our mock_read_csv function.
    
    Test Scenarios:
    - Valid file: Checks if the returned error hours match the expected value.
    - Invalid file: Checks if the function returns 0 when the required column is missing.
    - Empty file: Checks if the function returns 0 for an empty file.
    - All artifacts file: Checks if the returned error hours match the expected value when all data are artifacts.
    """
    # Override pandas.read_csv with our mock function.
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    # Test with a valid file containing a mix of artifact (-2) and valid data.
    result = error_hours_count("valid_ai_file")
    # The expected result is computed based on the number of -2 values * 30 seconds per value, then converted to hours.
    assert result == pytest.approx(0.025, abs=1e-4), f"Expected 0.025 but got {result}"

    # Test with an invalid file that lacks the required 'ai_hb' column.
    result = error_hours_count("invalid_ai_file")
    assert result == 0, f"Expected 0 but got {result}"

    # Test with an empty file (only header, no data).
    result = error_hours_count("empty_ai_file")
    assert result == 0, f"Expected 0 but got {result}"

    # Test with a file where all rows are artifacts (-2).
    result = error_hours_count("all_artifacts_file")
    # The expected result is computed similarly by converting artifact counts to hours.
    assert result == pytest.approx(0.0417, abs=1e-4), f"Expected 0.0417 but got {result}"

# ------------------------------------------------------------------------------
# TEST FUNCTIONS FOR total_sleeping_hours
# ------------------------------------------------------------------------------

def test_total_sleeping_hours(monkeypatch):
    """
    Tests the total_sleeping_hours function using various mock scenarios.
    
    Uses monkeypatch to override pandas.read_csv with our mock_read_csv function.
    
    Test Scenarios:
    - Valid file: Checks if the function returns the expected number of sleeping hours.
    - Empty file: Checks if the function returns 0 for an empty file.
    - Invalid file: Checks if the function returns 0 when the required column is missing.
    - All artifacts file: Even if all values are artifacts, the total sleep hours are computed based on the number of entries.
    """
    # Override pandas.read_csv with our mock function.
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    # Test with a valid file.
    result = total_sleeping_hours("valid_ai_file")
    # Expected sleep hours are calculated based on the total number of data points (excluding header) 
    # multiplied by 30 seconds and then converted to hours.
    assert result == pytest.approx(0.0333333, abs=1e-4), f"Expected 0.0333333 but got {result}"

    # Test with an empty file.
    result = total_sleeping_hours("empty_ai_file")
    assert result == 0, f"Expected 0 but got {result}"

    # Test with an invalid file that does not have the expected 'ai_hb' column.
    result = total_sleeping_hours("invalid_ai_file")
    assert result == 0, f"Expected 0 but got {result}"

    # Test with a file where all rows are artifacts (-2). The total sleep hours should be the same as long as there are entries.
    result = total_sleeping_hours("all_artifacts_file")
    assert result == pytest.approx(0.0333333, abs=1e-4), f"Expected 0.0333333 but got {result}"

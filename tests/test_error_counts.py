import pytest
import pandas as pd
from io import StringIO
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from files_for_python_project.error_counts_and_full_sleep_functions import error_hours_count, total_sleeping_hours

# Mock data (Fixed valid_ai_data)
valid_ai_data = """ai_hb
-2
0
-2
1
-2
"""
valid_ai_df = pd.read_csv(StringIO(valid_ai_data), sep="\t")

invalid_ai_data = """missing_column
-2
0
-2
1
-2
"""
invalid_ai_df = pd.read_csv(StringIO(invalid_ai_data), sep="\t")

empty_ai_data = """ai_hb
"""
empty_ai_df = pd.read_csv(StringIO(empty_ai_data), sep="\t")

all_artifacts_data = """ai_hb
-2
-2
-2
-2
-2
"""
all_artifacts_df = pd.read_csv(StringIO(all_artifacts_data), sep="\t")

# Mock read_csv function
def mock_read_csv(file, sep="\t"):
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

# Test function for error_hours_count
def test_error_hours_count(monkeypatch):
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    result = error_hours_count("valid_ai_file")
    assert result == pytest.approx(0.025, abs=1e-4), f"Expected 0.025 but got {result}"

    result = error_hours_count("invalid_ai_file")
    assert result == 0, f"Expected 0 but got {result}"

    result = error_hours_count("empty_ai_file")
    assert result == 0, f"Expected 0 but got {result}"

    result = error_hours_count("all_artifacts_file")
    assert result == pytest.approx(0.0417, abs=1e-4), f"Expected 0.0417 but got {result}"

# Test function for total_sleeping_hours
def test_total_sleeping_hours(monkeypatch):
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    result = total_sleeping_hours("valid_ai_file")
    assert result == pytest.approx(0.0333333, abs=1e-4), f"Expected 0.0333333 but got {result}"

    result = total_sleeping_hours("empty_ai_file")
    assert result == 0, f"Expected 0 but got {result}"

    result = total_sleeping_hours("invalid_ai_file")
    assert result == 0, f"Expected 0 but got {result}"

    result = total_sleeping_hours("all_artifacts_file")
    assert result == pytest.approx(0.0333333, abs=1e-4), f"Expected 0.0333333 but got {result}"

import pytest
import pandas as pd
import sys
import logging
import os
from unittest.mock import MagicMock
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from files_for_python_project.function_for_reviewing_patients import review_subjects

@pytest.fixture
def headband_files():
    return ["sub-1_mocked_headband_file.tsv"]

@pytest.fixture
def psg_files():
    return ["sub-1_mocked_psg_file.tsv"]

def test_review_subjects_one_subject(mocker, headband_files, psg_files):
    mocker.patch('builtins.input', side_effect=['1', 'n'])  # Simulate user input
    
    # Correct the side_effect for get_matching_file
    def mock_get_matching_file(subject_id_input, file_list):
        if file_list == headband_files:
            return headband_files[0]  # Return headband file when searching headband list
        elif file_list == psg_files:
            return psg_files[0]  # Return PSG file when searching PSG list
        return None  # Default case if no match found

    mocker.patch(
        'files_for_python_project.function_for_reviewing_patients.get_matching_file',
        side_effect=mock_get_matching_file
    )

    # Mock plot function
    mock_plot_sleep_stages = mocker.patch('files_for_python_project.function_for_reviewing_patients.plot_sleep_stages')

    # Mock file existence check
    mocker.patch('os.path.exists', return_value=True)

    # Run function under test
    review_subjects(headband_files, psg_files)

    # Validate function call with correct parameters
    mock_plot_sleep_stages.assert_called_once_with([psg_files[0]], [headband_files[0]])


def test_review_subjects_no_match(mocker, headband_files, psg_files):
    mocker.patch('builtins.input', side_effect=['999', '999', '999', KeyboardInterrupt])  # No pytest.raises()

    # Ensure get_matching_file always returns None
    mocker.patch('files_for_python_project.function_for_reviewing_patients.get_matching_file', return_value=None)
    mock_plot_sleep_stages = mocker.patch('files_for_python_project.function_for_reviewing_patients.plot_sleep_stages')

    mocker.patch('os.path.exists', return_value=True)

    with pytest.raises(KeyboardInterrupt):  # Expect the function to be interrupted
        review_subjects(headband_files, psg_files)

    mock_plot_sleep_stages.assert_not_called()

def test_review_subjects_empty_input(mocker, headband_files, psg_files):
    # Mock input to return empty input first, then a valid subject ID
    input_mock = mocker.patch('builtins.input', side_effect=[
        '',             # Invalid (empty)
        '',             # Invalid (empty)
        '001',          # Valid subject ID
        'n'             # Exit review
    ])

    # Mock file lookup and existence
    mocker.patch('files_for_python_project.function_for_reviewing_patients.get_matching_file', return_value=headband_files[0])
    mock_plot_sleep_stages = mocker.patch('files_for_python_project.function_for_reviewing_patients.plot_sleep_stages')
    mocker.patch('os.path.exists', return_value=True)

    # Ensure mock DataFrame has valid sleep data
    mock_df = pd.DataFrame({
        'onset': [10, 30, 60],
        'ai_hb': [1, 2, 3],  # Ensure required columns exist
        'ai_psg': [2, 3, 4],  # ✅ Add this missing column
        'majority': [3, 3, 5]
    })
    mocker.patch('pandas.read_csv', return_value=mock_df)

    # Run the function
    review_subjects(headband_files, psg_files)

    # Check that input was called at least 3 times (2 invalid + 1 valid)
    assert input_mock.call_count >= 3

    # Ensure plot function was called
    mock_plot_sleep_stages.assert_called_once()

def test_review_subjects_user_cancel(mocker, headband_files, psg_files):
    mocker.patch('builtins.input', side_effect=['1', 'n'])  # User enters valid ID, then cancels

    # Correct the side_effect for get_matching_file
    def mock_get_matching_file(subject_id_input, file_list):
        if file_list == headband_files:
            return headband_files[0]  # Return headband file when searching headband list
        elif file_list == psg_files:
            return psg_files[0]  # Return PSG file when searching PSG list
        return None  # Default case if no match found

    mocker.patch(
        'files_for_python_project.function_for_reviewing_patients.get_matching_file',
        side_effect=mock_get_matching_file
    )
    mock_plot_sleep_stages = mocker.patch('files_for_python_project.function_for_reviewing_patients.plot_sleep_stages')

    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('pandas.read_csv', return_value=pd.DataFrame())  # Mocking file reading

    review_subjects(headband_files, psg_files)

    # Ensure plot_sleep_stages was called exactly once
    mock_plot_sleep_stages.assert_called_once_with([psg_files[0]], [headband_files[0]])  # Fixing the order

def test_review_subjects_invalid_file(mocker, headband_files, psg_files, caplog):
    mocker.patch('builtins.input', side_effect=['1', 'n'])  # User enters valid ID

    # Return an invalid file path
    mocker.patch('files_for_python_project.function_for_reviewing_patients.get_matching_file', return_value="invalid_path")
    
    # Ensure `os.path.exists` returns False to simulate missing file
    mocker.patch('os.path.exists', return_value=False)

    with caplog.at_level(logging.WARNING):  # Capture log warnings
        review_subjects(headband_files, psg_files)

    # Check if expected warning is logged
    assert "File not found: invalid_path. Skipping plot." in caplog.text

def test_review_subjects_plot_error(mocker, headband_files, psg_files, caplog):
    mocker.patch('builtins.input', side_effect=['001', 'n'])  # Simulate user input

    # Mock file lookup to return valid paths
    mocker.patch('files_for_python_project.function_for_reviewing_patients.get_matching_file',
                 return_value='mocked_headband_file.tsv')

    # Mock os.path.exists to return True for the mocked file
    mocker.patch('os.path.exists', return_value=True)

    # Mock pandas.read_csv to return a DataFrame missing 'ai_hb' column
    mocker.patch('pandas.read_csv', return_value=pd.DataFrame({'onset': [0, 30, 60], 'majority': [1, 2, 3]}))

    with caplog.at_level(logging.WARNING):  # Capture log warnings
        review_subjects(headband_files, psg_files)
    
    # Check if the function logged the expected warning
    assert "No valid data found in mocked_headband_file.tsv. Skipping plot." in caplog.text

import pytest
import pandas as pd
import sys
import logging
import os

# Add the project's root directory to sys.path to ensure we can import the module under test.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the function to be tested.
from files_for_python_project.function_for_reviewing_patients import review_subjects

# ------------------------------------------------------------------------------
# Pytest Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def headband_files():
    """
    Fixture returning a list of mocked headband file paths.
    In this test setup, we use a single mocked file.
    """
    return ["sub-1_mocked_headband_file.tsv"]

@pytest.fixture
def psg_files():
    """
    Fixture returning a list of mocked PSG file paths.
    In this test setup, we use a single mocked file.
    """
    return ["sub-1_mocked_psg_file.tsv"]

# ------------------------------------------------------------------------------
# Test Functions
# ------------------------------------------------------------------------------

def test_review_subjects_one_subject(mocker, headband_files, psg_files):
    """
    Test review_subjects with one subject having valid headband and PSG files.
    
    This test simulates:
    - User input for selecting a subject ('1') and then opting not to review further ('n').
    - A correct lookup of matching files using a custom side_effect for get_matching_file.
    - A successful file existence check and plotting call.
    
    The test asserts that the plot_sleep_stages function is called once with the expected file paths.
    """
    # Simulate user input: subject ID '1' and then 'n' to not continue.
    mocker.patch('builtins.input', side_effect=['1', 'n'])
    
    # Define a custom mock for get_matching_file that returns the correct file from the list.
    def mock_get_matching_file(subject_id_input, file_list):
        if file_list == headband_files:
            return headband_files[0]  # Return headband file if searching in headband list.
        elif file_list == psg_files:
            return psg_files[0]       # Return PSG file if searching in PSG list.
        return None  # Default: no match found.
    
    # Patch the get_matching_file function with our custom mock.
    mocker.patch(
        'files_for_python_project.function_for_reviewing_patients.get_matching_file',
        side_effect=mock_get_matching_file
    )
    
    # Patch the plot function to monitor its call without executing actual plotting.
    mock_plot_sleep_stages = mocker.patch('files_for_python_project.function_for_reviewing_patients.plot_sleep_stages')
    
    # Patch os.path.exists to always return True, simulating that the file exists.
    mocker.patch('os.path.exists', return_value=True)
    
    # Run the function under test.
    review_subjects(headband_files, psg_files)
    
    # Assert that plot_sleep_stages is called once with the expected PSG and headband file paths.
    mock_plot_sleep_stages.assert_called_once_with([psg_files[0]], [headband_files[0]])

def test_review_subjects_no_match(mocker, headband_files, psg_files):
    """
    Test review_subjects when no matching file is found.
    
    This test simulates a scenario where get_matching_file returns None
    (i.e., no file matches the subject ID), and user repeatedly enters invalid input,
    until a KeyboardInterrupt is raised.
    
    It asserts that plot_sleep_stages is not called and that a KeyboardInterrupt is raised.
    """
    # Simulate repeated invalid inputs followed by a KeyboardInterrupt.
    mocker.patch('builtins.input', side_effect=['999', '999', '999', KeyboardInterrupt])
    
    # Ensure get_matching_file always returns None, indicating no match.
    mocker.patch('files_for_python_project.function_for_reviewing_patients.get_matching_file', return_value=None)
    
    # Patch the plot function to monitor its calls.
    mock_plot_sleep_stages = mocker.patch('files_for_python_project.function_for_reviewing_patients.plot_sleep_stages')
    
    # Patch os.path.exists to return True.
    mocker.patch('os.path.exists', return_value=True)
    
    # Expect a KeyboardInterrupt since the user input eventually triggers an interrupt.
    with pytest.raises(KeyboardInterrupt):
        review_subjects(headband_files, psg_files)
    
    # Verify that the plot function was never called due to the lack of matching files.
    mock_plot_sleep_stages.assert_not_called()

def test_review_subjects_empty_input(mocker, headband_files, psg_files):
    """
    Test review_subjects handling empty user input.
    
    This test simulates:
    - Two consecutive empty inputs (invalid),
    - Followed by a valid subject ID ('001'),
    - And then opting to exit review ('n').
    
    It also patches the file lookup, file existence, and file reading operations.
    Finally, it asserts that the input function is called multiple times and that the plot function is called.
    """
    # Patch input to simulate empty entries then a valid subject ID.
    input_mock = mocker.patch('builtins.input', side_effect=[
        '',     # First input: empty, invalid.
        '',     # Second input: empty, invalid.
        '001',  # Third input: valid subject ID.
        'n'     # Fourth input: exit review.
    ])
    
    # Patch get_matching_file to always return the first headband file.
    mocker.patch('files_for_python_project.function_for_reviewing_patients.get_matching_file', return_value=headband_files[0])
    
    # Patch the plot function.
    mock_plot_sleep_stages = mocker.patch('files_for_python_project.function_for_reviewing_patients.plot_sleep_stages')
    
    # Patch os.path.exists to always return True.
    mocker.patch('os.path.exists', return_value=True)
    
    # Create a mock DataFrame representing valid sleep data with required columns.
    mock_df = pd.DataFrame({
        'onset': [10, 30, 60],
        'ai_hb': [1, 2, 3],
        'ai_psg': [2, 3, 4],
        'majority': [3, 3, 5]
    })
    # Patch pandas.read_csv to return the mock DataFrame.
    mocker.patch('pandas.read_csv', return_value=mock_df)
    
    # Run the function under test.
    review_subjects(headband_files, psg_files)
    
    # Assert that the input function was called at least 3 times (2 invalid, then 1 valid).
    assert input_mock.call_count >= 3
    
    # Verify that the plot function was called exactly once.
    mock_plot_sleep_stages.assert_called_once()

def test_review_subjects_user_cancel(mocker, headband_files, psg_files):
    """
    Test review_subjects when the user cancels the review.
    
    This test simulates:
    - Valid subject ID input ('1'),
    - Followed by 'n' to cancel further review.
    
    The test uses a custom mock for get_matching_file to return the appropriate file paths.
    It asserts that plot_sleep_stages is called exactly once with the correct arguments.
    """
    # Simulate valid subject ID input and then cancellation.
    mocker.patch('builtins.input', side_effect=['1', 'n'])
    
    # Custom mock for get_matching_file to return the corresponding file from each list.
    def mock_get_matching_file(subject_id_input, file_list):
        if file_list == headband_files:
            return headband_files[0]
        elif file_list == psg_files:
            return psg_files[0]
        return None
    
    # Patch get_matching_file with our custom behavior.
    mocker.patch(
        'files_for_python_project.function_for_reviewing_patients.get_matching_file',
        side_effect=mock_get_matching_file
    )
    
    # Patch the plot function.
    mock_plot_sleep_stages = mocker.patch('files_for_python_project.function_for_reviewing_patients.plot_sleep_stages')
    
    # Patch os.path.exists to simulate file existence.
    mocker.patch('os.path.exists', return_value=True)
    
    # Patch pandas.read_csv to return an empty DataFrame (simulate file reading).
    mocker.patch('pandas.read_csv', return_value=pd.DataFrame())
    
    # Run the function under test.
    review_subjects(headband_files, psg_files)
    
    # Assert that plot_sleep_stages is called exactly once with the expected order of parameters.
    mock_plot_sleep_stages.assert_called_once_with([psg_files[0]], [headband_files[0]])

def test_review_subjects_invalid_file(mocker, headband_files, psg_files, caplog):
    """
    Test review_subjects behavior when the file returned by get_matching_file is invalid.
    
    This test simulates:
    - A valid subject ID input.
    - get_matching_file returning an invalid file path.
    - os.path.exists returning False (file not found).
    
    The test verifies that a warning is logged indicating the missing file and that no plot is attempted.
    """
    # Simulate valid subject input.
    mocker.patch('builtins.input', side_effect=['1', 'n'])
    
    # Patch get_matching_file to return an invalid file path.
    mocker.patch('files_for_python_project.function_for_reviewing_patients.get_matching_file', return_value="invalid_path")
    
    # Patch os.path.exists to always return False to simulate that the file does not exist.
    mocker.patch('os.path.exists', return_value=False)
    
    # Capture log warnings.
    with caplog.at_level(logging.WARNING):
        review_subjects(headband_files, psg_files)
    
    # Assert that the expected warning message is logged.
    assert "File not found: invalid_path. Skipping plot." in caplog.text

def test_review_subjects_plot_error(mocker, headband_files, psg_files, caplog):
    """
    Test review_subjects when the plotting process encounters an error due to invalid data.
    
    This test simulates:
    - Valid subject input.
    - get_matching_file returning a valid file path.
    - os.path.exists confirming file existence.
    - pandas.read_csv returning a DataFrame missing the required 'ai_hb' column.
    
    The test verifies that a warning is logged regarding the lack of valid data and the plot is skipped.
    """
    # Simulate valid subject ID input.
    mocker.patch('builtins.input', side_effect=['001', 'n'])
    
    # Patch get_matching_file to always return a valid headband file path.
    mocker.patch('files_for_python_project.function_for_reviewing_patients.get_matching_file',
                 return_value='mocked_headband_file.tsv')
    
    # Patch os.path.exists to simulate that the file exists.
    mocker.patch('os.path.exists', return_value=True)
    
    # Patch pandas.read_csv to return a DataFrame missing the required 'ai_hb' column.
    mocker.patch('pandas.read_csv', return_value=pd.DataFrame({'onset': [0, 30, 60], 'majority': [1, 2, 3]}))
    
    # Capture log warnings.
    with caplog.at_level(logging.WARNING):
        review_subjects(headband_files, psg_files)
    
    # Verify that the expected warning is logged.
    assert "No valid data found in mocked_headband_file.tsv. Skipping plot." in caplog.text

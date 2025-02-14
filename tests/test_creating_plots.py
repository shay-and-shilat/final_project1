import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Add the root project directory to the sys.path so Python can find the 'files_for_python_project' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from files_for_python_project.creating_plots import plot_sleep_stages

# Mock data for PSG and headband (ensure 'onset' is in the mock data for PSG)
mock_psg_data = pd.DataFrame({
    'onset': [0, 30, 60],  # Example time in 30-second epochs
    'majority': [1, 2, 3],  # Example for expert's sleep stages
    'ai_psg': [1, 2, 3],  # Example for AI sleep stages
})

# Mock data for headband
mock_headband_data = pd.DataFrame({
    'onset': [0, 30, 60],
    'ai_hb': [1, 2, 3],
})

# Test function
@patch('pandas.read_csv')
@patch('matplotlib.pyplot.show')
@patch('os.path.exists', return_value=True)  # Mock os.path.exists to always return True
def test_plot_sleep_stages(mock_exists, mock_show, mock_read_csv):
    # Mock the return value of pd.read_csv to return predefined mock data
    mock_read_csv.side_effect = [mock_psg_data, mock_headband_data, pd.DataFrame()]  # Empty DataFrame for headband

    # Mock random.choice to avoid picking a random file
    with patch('random.choice', return_value='fake_psg_file.txt') as mock_random_choice:
        psg_files = ['fake_psg_file.txt']
        headband_files = ['fake_headband_file.txt']

        # Ensure 'onset' is present in the PSG data
        mock_psg_data['onset'] = mock_psg_data['onset'].fillna(0)  # Ensure no missing onset data

        # Call the function to test
        plot_sleep_stages(psg_files, headband_files)

        # Check that read_csv was called twice (once for PSG data and once for headband data)
        assert mock_read_csv.call_count == 2

        # Check that the plot was shown
        mock_show.assert_called_once()

        # Check that random.choice was called once (to select the PSG file)
        mock_random_choice.assert_called_once_with(psg_files)

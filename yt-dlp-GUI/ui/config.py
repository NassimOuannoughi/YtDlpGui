"""
    Define constants
"""
# Default Placeholder Values
DEFAULT_URL_PLACEHOLDER = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Placeholder text for the URL input field
DEFAULT_OUTPUT_PLACEHOLDER = 'C:/Downloads/...'  # Placeholder text for the output path input field
# Output Settings
DEFAULT_OUTPUT_FOLDER = './output/'  # Default folder path for downloads if none is specified by the user
# Time Settings
DEFAULT_TIME_FORMAT = "HH:mm:ss"  # Default time format for the time input fields
DEFAULT_TIME = '00:00:00'  # Default time value for the time input fields
# Window and UI Titles
DEFAULT_WINDOW_TITLE = 'YtDlpGUI'  # Title of the main application window
# Error Messages
NETWORK_ERROR_TITLE = 'Network Error'  # Title for the error message box when network connection is lost
URL_FIELD_EMPTY_TITLE = 'Url Field Empty'  # Title for the error message box when URL field is empty
URL_FIELD_EMPTY_MESSAGE = 'You must provide a valid URL.'  # Error message when URL field is empty
INVALID_TIME_RANGE_TITLE = 'Invalid Time Range'  # Title for the error message box when an invalid time range is entered
INVALID_TIME_RANGE_MESSAGE = 'The start time must be earlier than the end time.'  # Error message when an invalid time range is entered
INVALID_URL_MESSAGE = 'The provided URL is not valid. Please enter a valid URL.'  # Error message when an invalid URL is provided
DOWNLOAD_ERROR_TITLE = 'Error'  # Title for the error message box when a download error occurs
DOWNLOAD_ERROR_MESSAGE = 'An error occurred while downloading.'  # Error message when a download error occurs


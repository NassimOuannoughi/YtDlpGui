"""
YtDlpGui.py

This module defines the YtDlpGui class, which implements a simple GUI for
downloading audio or video from YouTube using yt-dlp.
"""

import  os
import  subprocess  # This module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import  requests
from    PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QTimeEdit, QPushButton, QVBoxLayout, QLabel, QRadioButton, QGroupBox, QMessageBox, QFileDialog
from    PyQt6.QtGui import QPixmap
from    PyQt6.QtCore import QThread, pyqtSignal, Qt
from    ui.utils import is_connected
from    ui.config import *

class ThumbnailDownloader(QThread):
    """
    A QThread derived class that initiates a separate thread to download
    thumbnails from YouTube using yt-dlp. This ensures the thumbnail
    retrieval process does not block the main application.
    The class emits a signal with the downloaded thumbnail as a QPixmap
    object once the thumbnail is successfully retrieved.
    """
    thumbnail_downloaded = pyqtSignal(QPixmap)

    def __init__(self, url):
        """
        Initializes a new instance of the ThumbnailDownloader class, setting
        up the necessary attributes for the thumbnail download process.
        """
        super().__init__()
        self.url = url

    def run(self):
        """
        Overrides the QThread.run method to define the actions to be taken 
        when the thread is started. It constructs and executes a yt-dlp 
        command to retrieve the thumbnail URL of the specified YouTube video, 
        downloads the thumbnail image, and emits the thumbnail_downloaded 
        signal with the downloaded thumbnail as a QPixmap object.

        This method is automatically called upon starting the thread and 
        ensures that the thumbnail download process occurs in a separate 
        thread, preventing any blocking of the main application thread.
        """
        command = f'yt-dlp --skip-download --get-thumbnail "{self.url}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        thumbnail_url = stdout.strip()
        if thumbnail_url:
            thumbnail_data = requests.get(thumbnail_url).content
            pixmap = QPixmap()
            pixmap.loadFromData(thumbnail_data)
            self.thumbnail_downloaded.emit(pixmap)

class YtDlpGui(QWidget):
    """
    A QWidget derived class that implements a simple GUI for downloading audio or
    video from YouTube using yt-dlp.
    """

    def __init__(self):
        """
        Initializes the user interface elements of the YtDlpGui instance.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface elements of the YtDlpGui instance.
        """

        # Fields for URL 
        self.url_label = QLabel('Enter YouTube URL:', self)
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText(DEFAULT_URL_PLACEHOLDER)  # Set placeholder text
        self.url_input.textChanged.connect(self.on_url_changed)
        # Thumbnail
        self.thumbnail_label = QLabel(self)
        self.default_pixmap = QPixmap(DEFAULT_THUMBNAIL).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.thumbnail_label.setPixmap(self.default_pixmap)

        #Field for output folder. Give the option to click on a folder icon to choose 
        self.output_path_label = QLabel('Output Folder (optional, will download in "output" if not specified):', self)
        self.output_path_input = QLineEdit(self)
        self.output_path_input.setPlaceholderText(DEFAULT_OUTPUT_PLACEHOLDER)  # Set placeholder text
        self.browse_button = QPushButton( 'Folder Path', self)
        self.browse_button.clicked.connect(self.browse_output_folder)

        # Radio buttons for media type selection
        self.audio_button = QRadioButton('Audio', self)
        self.video_button = QRadioButton('Video', self)
        
        # Group box for audio format selection
        self.audio_format_group = QGroupBox('Audio Format:', self)
        self.mp3_button = QRadioButton('mp3', self.audio_format_group)
        self.wav_button = QRadioButton('wav', self.audio_format_group)
        self.flac_button = QRadioButton('flac', self.audio_format_group)
        self.aac_button = QRadioButton('aac', self.audio_format_group)
        self.mp3_button.setChecked(True) # Set mp3 as default
        #
        audio_format_layout = QVBoxLayout(self.audio_format_group)
        audio_format_layout.addWidget(self.mp3_button)
        audio_format_layout.addWidget(self.wav_button)
        audio_format_layout.addWidget(self.flac_button)
        audio_format_layout.addWidget(self.aac_button)
        #
        self.audio_format_group.setLayout(audio_format_layout)
        self.audio_format_group.setHidden(True)  # Hide the group box initially
        # Toggle visibility of audio format options when Audio/Video selection changes
        self.audio_button.toggled.connect(self.audio_format_group.setVisible)
        
        # Group box for video format selection
        self.video_format_group = QGroupBox('Video Format:', self)
        self.webm_button = QRadioButton('webm', self.video_format_group)
        self.mp4_button = QRadioButton('mp4', self.video_format_group)
        self.webm_button.setChecked(True) # Set webm as default
        video_format_layout = QVBoxLayout(self.video_format_group)
        video_format_layout.addWidget(self.webm_button)
        video_format_layout.addWidget(self.mp4_button)
        #
        self.video_format_group.setLayout(video_format_layout)
        self.video_format_group.setHidden(True)  # Hide the group box initially
        # Toggle visibility of audio format options when Audio/Video selection changes
        self.video_button.toggled.connect(self.video_format_group.setVisible)


        self.output_format = QLabel('Select output type:', self)
        self.audio_button.setChecked(True)  # Set audio as default
        self.audio_format_group.setVisible(self.audio_button.isChecked())  # Manually set visibility based on audio_button state

        # Fields for File Name
        self.file_name = QLabel('Rename the file (optional):', self)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('my-custom-name')  # Set placeholder text

        # Advanced Options:
        # Start & End time
        self.advanced_options_button = QPushButton('Advanced Options', self)
        self.advanced_options_button.clicked.connect(self.toggle_advanced_options)

        # Time fields for starting end ending time
        self.start_time_label = QLabel('Start time (download from the start if not specified):', self)
        self.start_time_input = QTimeEdit(self)        
        self.start_time_input.setDisplayFormat(DEFAULT_TIME_FORMAT)
        self.end_time_label = QLabel('End time (download until the end if not specified):', self)
        self.end_time_input = QTimeEdit(self)
        self.end_time_input.setDisplayFormat(DEFAULT_TIME_FORMAT)
        # Initially hide the start and end time fields
        self.start_time_label.setHidden(True)
        self.start_time_input.setHidden(True)
        self.end_time_label.setHidden(True)
        self.end_time_input.setHidden(True)
        # Download button
        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.start_download)
        
        # Vertical layout to organize widgets
        vbox = QVBoxLayout()
        vbox.addWidget(self.url_label)
        vbox.addWidget(self.url_input)
        vbox.addWidget(self.thumbnail_label)
        vbox.addWidget(self.output_path_label)
        vbox.addWidget(self.output_path_input)
        vbox.addWidget(self.browse_button)        
        vbox.addWidget(self.output_format)
        vbox.addWidget(self.audio_button)
        vbox.addWidget(self.video_button)
        vbox.addWidget(self.audio_format_group)  # Add the group box to the layout
        vbox.addWidget(self.video_format_group)
        vbox.addWidget(self.file_name)
        vbox.addWidget(self.name_input)        
        vbox.addWidget(self.advanced_options_button)
        vbox.addWidget(self.start_time_label)
        vbox.addWidget(self.start_time_input)
        vbox.addWidget(self.end_time_label)
        vbox.addWidget(self.end_time_input)
        vbox.addWidget(self.download_button)
        
        self.setLayout(vbox)
        self.setWindowTitle(DEFAULT_WINDOW_TITLE)
        self.setGeometry(300, 300, 400, 200)

    def on_url_changed(self, url):
        if url.strip():
            self.downloader = ThumbnailDownloader(url)
            self.downloader.thumbnail_downloaded.connect(self.on_thumbnail_downloaded)
            self.downloader.start()
        else:
            self.thumbnail_label.setPixmap(self.default_pixmap)

    def on_thumbnail_downloaded(self, pixmap):
        scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.thumbnail_label.setPixmap(scaled_pixmap)

    def toggle_advanced_options(self):
        """
        Toggles the visibility of the start and end time fields.
        """
        hidden = self.start_time_label.isHidden()
        self.start_time_label.setHidden(not hidden)
        self.start_time_input.setHidden(not hidden)
        self.end_time_label.setHidden(not hidden)
        self.end_time_input.setHidden(not hidden)

    def browse_output_folder(self):
        """
        Opens a file dialog for the user to select an output directory.
        """
        options = QFileDialog.Option.ShowDirsOnly  
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", self.output_path_input.text(), options=options)
        if folder:
            self.output_path_input.setText(folder)

    def start_download(self):
        """
        Initiates the download process based on the current state of the GUI.
        """
        # check connection first
        if not is_connected():
            QMessageBox.critical(self, NETWORK_ERROR_TITLE, 'Please check your internet connection and try again.')
            return
    
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.critical(self, URL_FIELD_EMPTY_TITLE, URL_FIELD_EMPTY_MESSAGE)
            return

        output_folder = self.output_path_input.text().strip() or DEFAULT_OUTPUT_FOLDER
        os.makedirs(output_folder, exist_ok=True)  # Check if directory exists

        output_name = self.name_input.text().strip() or '%(title)s'
        output_path = os.path.join(output_folder, f"{output_name}.%(ext)s")

        format_option = ''
        if self.audio_button.isChecked():
            format_option = '-x --audio-format '
            if self.mp3_button.isChecked():
                format_option += 'mp3'
            elif self.wav_button.isChecked():
                format_option += 'wav'
            elif self.flac_button.isChecked():
                format_option += 'flac'
            elif self.aac_button.isChecked():
                format_option += 'aac'
        elif self.video_button.isChecked():
            video_format = 'webm' if self.webm_button.isChecked() else 'mp4'
            format_option = f'--merge-output-format {video_format}'

        command = f'yt-dlp {format_option} -o "{output_path}" "{url}"'

        start_time = self.start_time_input.text().strip()
        end_time = self.end_time_input.text().strip()

        if start_time != DEFAULT_TIME or end_time != DEFAULT_TIME:
            start_parts = [int(part) for part in start_time.split(':')]
            end_parts = [int(part) for part in end_time.split(':')]
            
            if start_parts > end_parts and end_time != DEFAULT_TIME:
                QMessageBox.critical(self, INVALID_TIME_RANGE_TITLE, INVALID_TIME_RANGE_MESSAGE)
                return
            
            pp_args = []
            if start_time != DEFAULT_TIME:
                pp_args.append(f'-ss {start_time}')
            if end_time != DEFAULT_TIME:
                pp_args.append(f'-to {end_time}')

            if pp_args:
                command += f' --postprocessor-args "{" ".join(pp_args)}"'

        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=False)  
        except subprocess.CalledProcessError as e:
            error_message = str(e.stderr)  # Capture the error output
            if "' is not a valid URL." in error_message:
                QMessageBox.critical(self, 'Invalid URL', INVALID_URL_MESSAGE)
            else:
                QMessageBox.critical(self, DOWNLOAD_ERROR_TITLE, DOWNLOAD_ERROR_MESSAGE)
            print(f"Error occurred: {e}")

def run_app():
    """
    Initializes and runs the QApplication instance.

    This function creates a new QApplication instance, creates an instance of
    the YtDlpGui class, initializes the GUI, shows the GUI, and then
    enters the Qt event loop by calling app.exec().
    """
    app = QApplication([])
    ex = YtDlpGui()
    ex.show()
    app.exec()
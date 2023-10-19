from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QTimeEdit, QPushButton, QVBoxLayout, QLabel, QRadioButton, QGroupBox, QMessageBox, QFileDialog
from PyQt6.QtGui import QIcon
import subprocess  # This module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.


class YtDlpGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Fields for URL 
        self.url_label = QLabel('Enter YouTube URL:', self)
        self.url_input = QLineEdit(self)
        #Field for output folder. Give the option to click on a folder icon to choose 
        self.output_path_label = QLabel('Output Folder (optional):', self)
        self.output_path_input = QLineEdit(self)
        self.output_path_input.setText('../../output/')  # Set default output folder
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

        # Time fields for starting end ending time
        self.start_time_label = QLabel('Start time (download from the start if not specified):', self)
        self.start_time_input = QTimeEdit(self)        
        self.start_time_input.setDisplayFormat("HH:mm:ss")
        self.end_time_label = QLabel('End time (download until the end if not specified):', self)
        self.end_time_input = QTimeEdit(self)
        self.end_time_input.setDisplayFormat("HH:mm:ss")

        # Download button
        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.start_download)
        
        # Vertical layout to organize widgets
        vbox = QVBoxLayout()
        vbox.addWidget(self.url_label)
        vbox.addWidget(self.url_input)
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
        vbox.addWidget(self.start_time_label)
        vbox.addWidget(self.start_time_input)
        vbox.addWidget(self.end_time_label)
        vbox.addWidget(self.end_time_input)
        vbox.addWidget(self.download_button)
        
        self.setLayout(vbox)
        self.setWindowTitle('YtDlpGUI')
        self.setGeometry(300, 300, 400, 200)

    def browse_output_folder(self):
        options = QFileDialog.Option.ShowDirsOnly  # Notice the change here
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", self.output_path_input.text(), options=options)
        if folder:
            self.output_path_input.setText(folder)


    def start_download(self):
        url = self.url_input.text()
        file_name = self.name_input.text()
        start_time = self.start_time_input.text()  # Assume this is a QLineEdit
        end_time = self.end_time_input.text()  # Assume this is a QLineEdit
        output_name = self.name_input.text() or '%(title)s'  # Use the provided name or the video title
        output_folder = self.output_path_input.text()
        output_path = f'{output_folder}/{output_name}.%(ext)s'
        # Determine the output format based on the selected radio button
        output_name = "%(title)s.%(ext)s"  # Default to the video's title
        if file_name:  # If a custom file name is provided
            output_name = f"{file_name}.%(ext)s"

        if not url:
            QMessageBox.critical(self, 'Url field empty', 'You must provide a valid url.')
            return  # Exit the method early to avoid starting the download
        
        if self.audio_button.isChecked():
            if self.mp3_button.isChecked():
                command = f'yt-dlp -x --audio-format mp3 -o "{output_name}" {url}'
            elif self.wav_button.isChecked():
                command = f'yt-dlp -x --audio-format wav -o "{output_name}" {url}'
            elif self.flac_button.isChecked():
                command = f'yt-dlp -x --audio-format flac -o "{output_name}" {url}'
            elif self.aac_button.isChecked():
                command = f'yt-dlp -x --audio-format aac -o "{output_name}" {url}'
        else: # download video format
            video_format = 'webm'  # default to webm
            if self.mp4_button.isChecked():
                video_format = 'mp4'
            command = f'yt-dlp --merge-output-format {video_format} -o "{output_name}" {url}'

        if start_time or end_time:
            start_parts = [int(part) for part in start_time.split(':')]
            end_parts = [int(part) for part in end_time.split(':')]

            # Case 1: Both start and end times are the default (00:00:00), so download the whole video.
            if start_time == '00:00:00' and end_time == '00:00:00':
                pass  # No special postprocessor args needed.
            # Case 2: Only one of them is 00:00:00, so either start from the beginning or go until the end.
            elif start_time == '00:00:00' or end_time == '00:00:00':
                pp_args = []
                if start_time != '00:00:00':
                    pp_args.append(f"-ss {start_time}")
                if end_time != '00:00:00':
                    pp_args.append(f"-to {end_time}")
                command += f' --postprocessor-args "{" ".join(pp_args)}"'
            # Case 3: Neither of them is 00:00:00, so ensure the start time is earlier than the end time.
            elif start_parts >= end_parts:
                QMessageBox.critical(self, 'Invalid Time Range', 'The start time must be earlier than the end time.')
                return  # Exit the method early to avoid starting the download
            else:
                command += f' --postprocessor-args "-ss {start_time} -to {end_time}"'

        
        #export to folder
        command += f' -o "{output_path}"'
        # Run the yt-dlp command
        subprocess.run(command, shell=True)
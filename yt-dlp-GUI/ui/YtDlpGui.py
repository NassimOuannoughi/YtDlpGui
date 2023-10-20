import os
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
        self.url_input.setPlaceholderText('https://www.youtube.com/watch?v=dQw4w9WgXcQ')  # Set placeholder text
        #Field for output folder. Give the option to click on a folder icon to choose 
        self.output_path_label = QLabel('Output Folder (optional):', self)
        self.output_path_input = QLineEdit(self)
        self.output_path_input.setText('./output/')  # Set default output folder
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
        self.name_input.setPlaceholderText('Custom Name')  # Set placeholder text

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
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.critical(self, 'Url Field Empty', 'You must provide a valid URL.')
            return

        output_folder = self.output_path_input.text().strip()
        os.makedirs(output_folder, exist_ok=True)  # Ensure directory exists

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

        if start_time != '00:00:00' or end_time != '00:00:00':
            start_parts = [int(part) for part in start_time.split(':')]
            end_parts = [int(part) for part in end_time.split(':')]
            
            if start_parts > end_parts and end_time != '00:00:00':
                QMessageBox.critical(self, 'Invalid Time Range', 'The start time must be earlier than the end time.')
                return
            
            pp_args = []
            if start_time != '00:00:00':
                pp_args.append(f'-ss {start_time}')
            if end_time != '00:00:00':
                pp_args.append(f'-to {end_time}')

            if pp_args:
                command += f' --postprocessor-args "{" ".join(pp_args)}"'

        print("------------------------------")
        print(f"Command: {command}")

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            QMessageBox.critical(self, 'Error', 'An error occurred while downloading.')

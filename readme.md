# YtDlpGUI

A simple GUI wrapper for `yt-dlp`, created to make the process of downloading YouTube videos easier and more secure than using "youtube to mp3" websites.
It is a practice project, I was curious about learning how to make GUI with PyQt6.

## Motivation

I created this project because, as a musician, I often download backing tracks to practice. However, I wasn't comfortable using "youtube to mp3" websites with minimal security. I discovered `yt-dlp` while browsing, and while I liked the capabilities of the tool, I found myself using the same commands all the time. I made this project as a practice project, and released it as I thought it would be useful for other users to have this tool available.

## Features

- Input YouTube URL for downloading media.
- Choose between downloading audio or video.
- Select specific audio or video formats.
- Specify a custom output folder and filename.
- Set the start and end times for downloading a specific portion of the media.

## Installation

1. **Installing Python**:
    - Download and install Python from the official download page (https://www.python.org/downloads/). Make sure to check the box that says "Add Python to PATH" during the installation process.

2. **Downloading the Project**:
    - Download the project files from the GitHub repository. You can do this by clicking the green "Code" button and selecting "Download ZIP." Extract the ZIP file to a location of your choice.

3. **Running the Program**:
On macOS (expected to work on Linux too but hasn't been tested):
    - open the **Finder** and navigate to the folder where you extracted the project files.
    - Right-click on the folder and select **New Terminal at Folder**. This will open a terminal window in the correct directory.
    - In the terminal, make the `run.sh` script executable by running the command: `chmod +x run.sh`.
    - Now, run the script by executing: `./run.sh`. This script will create a virtual environment, install the necessary dependencies, and launch the program.
Note: I don't have access to a Windows machine. 
You can run the program using main.py but to create a similar script you would need a run.bat file with the appropriate commands.
I added this item to the todo list but don't know when I can complete it.

## Usage

1. Enter the YouTube URL you want to download.
2. (Optional) Specify an output folder. By default, media will be downloaded to the `./output` folder.
3. Choose whether you want to download audio or video.
4. Select the media format.
5. (Optional) Rename the output file.
6. (Optional) Set start and end times if you want to download a specific segment of the video.
   - If you don't specify start and end times, it will download the entire video. 
   - If only a start time is specified, it will download from the start time until the end. 
   - If only an end time is specified, it will download from the beginning until the specified end time.
7. Click the "Download" button.

## If you want to contribute
Please feel free to do so.

## License
This project is licensed under the GNU General Public License (GPL) v3. You are free to use, modify, and distribute this software, but you cannot use it for commercial purposes. The author is not liable for any damages or issues arising from the use of this software.

# YtDlpGUI

A simple GUI wrapper for `yt-dlp`, created to make the process of downloading youtube videos easier and more secure than using "youtube to mp3" websites.
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

Install the required Python packages from the requirements.txt file:

pip install -r requirements.txt

Dependencies included in requirements.txt:

    PyQt6==6.5.3
    PyQt6-Qt6==6.5.3
    PyQt6-sip==13.6.0
    yt-dlp

Run the main.py script to launch the application:

python main.py


## Usage

1. Enter the YouTube URL you wish to download.
2. (Optional) Specify an output folder. By default, media will be downloaded to the `./output` folder.
3. Choose whether you want to download audio or video.
4. Select the desired media format.
5. (Optional) Rename the output file.
6. (Optional) Set start and end times if you wish to download a specific segment of the video or audio. 
   - If you don't specify start and end times, it will download the entire video. 
   - If only a start time is specified, it will download from the start time until the end. 
   - If only an end time is specified, it will download from the beginning until the specified end time.
7. Click the "Download" button.


## TODO

TODO

This is very much a work in progress, and I have plans to add the following features in the future:

**Placeholder Text:**
Add grey placeholder text in empty fields.

**Invalid URL Handling:**
Catch errors from yt-dlp and display error message for invalid URLs.

**Unit Tests:**
Write unit tests to ensure the core functionality works as expected.

**Executable Creation:**
Create executables for Windows and Mac.

**Design Improvements:**
Make UI design improvements.

**Logging:**
Implement logging to record events, transactions, or errors that may occur.

**Configurations:**
Save user preferences in a configuration file.

**Error Handling for Network Issues:**
Implement proper error handling for network-related issues.

**Automated Builds and Testing:**
Set up a CI/CD pipeline for automated builds and testing.


If you wish to contribute, please feel free to do so.

## License

This project is licensed under the GNU General Public License (GPL) v3. 
You are free to use, modify, and distribute this software, but you cannot use it for commercial purposes. 
The author is not liable for any damages or issues arising from the use of this software.

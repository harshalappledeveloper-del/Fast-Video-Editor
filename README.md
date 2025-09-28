# Video and Audio Merger Web App

This is a simple web application that allows you to:
1.  Upload multiple video files.
2.  Upload one audio file.
3.  Merge the videos sequentially.
4.  Replace the audio of the merged video with the uploaded audio.
5.  Download the final combined video.

## Technology Stack
- **Backend**: Python, Flask
- **Video/Audio Processing**: `moviepy`
- **Frontend**: HTML, CSS, JavaScript

## Setup and Installation

### Prerequisites
- Python 3.6+
- `pip` (Python package installer)

### Installation
1.  Clone this repository or download the files into a new directory.
2.  Open a terminal or command prompt in the project directory.
3.  Install the required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application
1.  Make sure you are in the project's root directory in your terminal.
2.  Run the Flask application with the following command:
    ```bash
    python app.py
    ```
3.  Once the server is running, you will see a message like:
    ```
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```
4.  Open your web browser and go to `http://127.0.0.1:5000/`.

## How to Use the Web App
1.  **Select Videos**: Click on the "Choose Files" button under "Select Video Files" to select one or more video files you want to merge.
2.  **Select Audio**: Click on the "Choose File" button under "Select Audio File" to select the audio file you want to add to the merged video.
3.  **Combine**: Click the "Combine Videos and Audio" button.
4.  **Wait**: The processing may take some time depending on the size and number of your files.
5.  **Download**: Once processing is complete, a download link will appear. Click on it to download your final video.
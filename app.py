import os
from flask import Flask, request, render_template, send_from_directory, jsonify
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import time

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_files():
    """Handles file uploads and processing."""
    try:
        # Get uploaded files
        video_files = request.files.getlist('videos')
        audio_file = request.files.get('audio')

        if not video_files or not all(f.filename for f in video_files):
            return jsonify({'error': 'No video files selected!'}), 400
        if not audio_file or not audio_file.filename:
            return jsonify({'error': 'No audio file selected!'}), 400

        # Save video files
        video_paths = []
        for video in video_files:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
            video.save(video_path)
            video_paths.append(video_path)

        # Save audio file
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(audio_path)

        # --- Video and Audio Processing ---
        
        # 1. Concatenate videos
        video_clips = [VideoFileClip(path) for path in video_paths]
        final_video_clip = concatenate_videoclips(video_clips, method="compose")

        # 2. Load the new audio
        new_audio_clip = AudioFileClip(audio_path)

        # 3. Set the audio of the concatenated video to the new audio
        final_video_clip = final_video_clip.set_audio(new_audio_clip)

        # Ensure the duration matches the shorter of the two
        if final_video_clip.duration > new_audio_clip.duration:
            final_video_clip = final_video_clip.set_duration(new_audio_clip.duration)

        # 4. Export the final video
        timestamp = int(time.time())
        output_filename = f'combined_video_{timestamp}.mp4'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        final_video_clip.write_videofile(
            output_path, 
            codec='libx264', 
            audio_codec='aac'
        )

        # Close clips to release resources
        for clip in video_clips:
            clip.close()
        new_audio_clip.close()
        final_video_clip.close()

        # Clean up uploaded files
        for path in video_paths:
            os.remove(path)
        os.remove(audio_path)

        return jsonify({'download_url': f'/output/{output_filename}'})

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred during processing. Please check your files and try again.'}), 500

@app.route('/output/<filename>')
def get_output_file(filename):
    """Serves the processed video for download."""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
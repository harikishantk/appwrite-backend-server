from flask import Flask, jsonify, request
import os

import openai

# logging
import logging
# logging related
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# env variables
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('openai_api_key')
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def convertToText(audio_file_path):
    """
    Convert the audio file to text

    Parameters
    ----------
    audio_file_path : str
        Path to the audio file

    Returns
    -------
    transcript : str
        Transcript of the audio file
    """
    logger.log(logging.INFO, f'convertToText()')
    logger.log(logging.INFO, f'audio_file_path: {audio_file_path}')
    audio_file= open(audio_file_path, "rb")
    logger.log(logging.INFO, f'audio_file: {audio_file}')
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    except Exception as e:
        logger.log(logging.ERROR, f'Exception while converting: {e}')
    logger.log(logging.INFO, f'transcript: {transcript}')
    return transcript


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/getText', methods=['POST'])
def getText():
    # Get the audio file from the frontend
    audio_file = request.files['file']

    logger.log(logging.INFO, f'audio_file: {audio_file}')

    # Check if the audio-files folder exists
    if not os.path.exists('audio-files'):
        os.makedirs('audio-files')
    
    try:
        # Save the audio file in the audio-files folder
        audio_file.save(os.path.join('audio-files', audio_file.filename))
        logger.log(logging.INFO, f'audio_file saved: {audio_file.filename}')
        # Convert the audio file to text
        transcript = convertToText(os.path.join('audio-files', audio_file.filename))
        # Return the transcript
        return transcript
    except:
        return 'An error occurred while saving the audio file', 500


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=8000))

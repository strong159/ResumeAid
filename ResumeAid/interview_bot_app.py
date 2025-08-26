from flask import Flask, request, jsonify
from flask_cors import CORS
from save import save_messages
from audio import transcribe_audio
from generate_questions import generate_interview_questions
from main import upload_resume


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000/"}})

@app.route('/')
def home():
    return "Interview Bot is running!"

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    #print("POST request reached")
    file = request.files['resume']
    # Process the uploaded resume
    #print("Fetched resume")
    questions = generate_interview_questions(file)
    #print("Generated questions")
    #print(questions)
    return jsonify({"questions": questions})

@app.route('/record_response', methods=['POST'])
def record_response():
    data = request.get_json()
    response = data['response']
    # Save and process the response
    save_messages(response)
    return jsonify({"status": "Response recorded"})

@app.route('/listen_audio', methods=['POST'])
def listen_audio_route():
    file = request.files['audio']
    # Process the audio file
    transcription = transcribe_audio(file)
    print(transcription)
    return jsonify({"transcription": [transcription]})

if __name__ == '__main__':
    app.run(debug=True)





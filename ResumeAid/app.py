from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import openai
import os
import json
import requests
import fitz  # PyMuPDF
from flask import Flask, render_template
from flask_cors import CORS
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = Flask(__name__)
CORS(app)



openai.api_key = os.getenv("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")
elevenlabs_key = os.getenv("sk_2dd73a349f57e263657a740a1edb604c328d9a69491c6609")

interview_context = {
    "resume_text": "",
    "questions": [],
    "current_question_index": 0
}

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files['file']
    resume_text = extract_text_from_pdf(file)

    if resume_text:
        interview_context["resume_text"] = resume_text
        questions = generate_interview_questions(resume_text)
        interview_context["questions"] = questions
        interview_context["current_question_index"] = 0

        response_text = "Thank you for the resume. Let's start the interview. Here is the first question: " + interview_context["questions"][0]
        audio_output = text_to_speech(response_text)

        return send_from_directory(directory='', filename='audio_output.mp3', as_attachment=True)
    else:
        response_text = "Failed to extract text from the PDF resume. Please try again."
        audio_output = text_to_speech(response_text)
        return send_from_directory(directory='', filename='audio_output.mp3', as_attachment=True)

@app.route('/interview', methods=['POST'])
def interview_response():
    file = request.files['file']
    user_message = transcribe_audio(file)

    if interview_context["current_question_index"] < len(interview_context["questions"]) - 1:
        interview_context["current_question_index"] += 1
        next_question = interview_context["questions"][interview_context["current_question_index"]]
        response_text = get_chat_response(user_message) + next_question
    else:
        response_text = "Thank you for completing the interview. We will get back to you soon."

    audio_output = text_to_speech(response_text)
    return send_from_directory(directory='', filename='audio_output.mp3', as_attachment=True)

def transcribe_audio(file):
    audio_data = file.read()
    response = openai.Audio.transcribe("whisper-1", audio_data)
    return response["text"]

def get_chat_response(user_message): 
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    parsed_gpt_response = gpt_response.choices[0].message["content"]

    save_messages(user_message, parsed_gpt_response)
    return parsed_gpt_response

def load_messages():
    messages = []
    file = 'database.json'
    
    if os.path.exists(file) and os.stat(file).st_size != 0:
        with open(file) as db_file:
            messages = json.load(db_file)
    else:
        messages.append(
            {"role": "system", "content": "You are interviewing the user for a front-end React developer position. Ask short questions that are relevant to a junior level developer. Your name is ZRecruit. The user is Rahul Perumbali. Keep responses under 30 words."}
        )
    return messages

def save_messages(user_message, gpt_response):
    file = 'database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response})
    with open(file, 'w') as f:
        json.dump(messages, f)

def text_to_speech(text):
    voice_id = "iP95p4xoKVk53GoZ742B"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_key
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open('audio_output.mp3', 'wb') as f:
            f.write(response.content)
        return 'audio_output.mp3'
    else:
        return None

def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

def generate_interview_questions(resume_text):
    messages = [
        {"role": "system", "content": "You are an assistant for an interviewer that needs to generate questions based off of a given resume."},
        {"role": "user", "content": f"Generate three detailed interview questions based on the following resume:\n\n{resume_text}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    questions = response.choices[0].message["content"]
    return questions.split('\n\n')

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
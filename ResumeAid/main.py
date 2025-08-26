# from fastapi import FastAPI, UploadFile
# from fastapi.responses import StreamingResponse
# from dotenv import load_dotenv
# import openai
# from openai import OpenAI
# import os
# import json
# import requests
# import fitz  # PyMuPDF
# from flask import Flask
# from flask import Flask, request, jsonify, send_from_directory
# from flask import Flask, render_template
# from asgiref.wsgi import WsgiToAsgi
# from fastapi.middleware.cors import CORSMiddleware


# load_dotenv()

# app = FastAPI()
# client = OpenAI(
#     api_key = os.getenv("OPENAI_API_KEY"),
#     organization = os.getenv("OPENAI_API_ORG"),
# )
# elevenlabs_key = os.getenv("ELEVENLABS_KEY")

# interview_context = {
#     "resume_text": "",
#     "questions": [],
#     "current_question_index": 0
# }

# @app.post("/intro")
# async def post_audio_intro(file: UploadFile):
#     user_message = transcribe_audio(file)
#     chat_response = get_chat_response(user_message)
#     audio_output = text_to_speech(chat_response)
#     def iterfile():   
#         yield audio_output

#     return StreamingResponse(iter([audio_output]), media_type="audio/mpeg")

# # @app.post("/upload_resume")
# # async def upload_resume(file: UploadFile):
# #     resume_text = extract_text_from_pdf(file.file)
    
# #     if resume_text:
# #         interview_context["resume_text"] = resume_text
# #         questions = generate_interview_questions(resume_text)
# #         # print(questions)
# #         interview_context["questions"] = questions
# #         # print(interview_context["questions"])
# #         interview_context["current_question_index"] = 0

# #         response_text = "Thank you for the resume. Let's start the interview. Here is the first question: " + interview_context["questions"][0]
# #         audio_output = text_to_speech(response_text)

# #         return StreamingResponse(iter([audio_output]), media_type="audio/mpeg")
# #     else:
# #         response_text = "Failed to extract text from the PDF resume. Please try again."
# #         audio_output = text_to_speech(response_text)
# #         return StreamingResponse(iter([audio_output]), media_type="audio/mpeg")

# @app.post("/interview")
# async def interview_response(file: UploadFile):
#     user_message = transcribe_audio(file)

#     if interview_context["current_question_index"] < len(interview_context["questions"]) - 1:
#         interview_context["current_question_index"] += 1
#         next_question = interview_context["questions"][interview_context["current_question_index"]]
#         response_text = get_chat_response(user_message) + next_question
#     else:
#         response_text = "Thank you for completing the interview. We will get back to you soon."

#     audio_output = text_to_speech(response_text)
#     return StreamingResponse(iter([audio_output]), media_type="audio/mpeg")

  
#  # Function
# def transcribe_audio(file):
#     audio_file= open(file.filename, "rb")
#     transcript = client.audio.transcriptions.create(model = "whisper-1", file = audio_file)
#     print(transcript)
#     return transcript

# def get_chat_response(user_message): 
#     messages = load_messages()
#     messages.append({"role": "user", "content": user_message.text})
#     print(messages)
#     #Send to GPT
#     gpt_response = openai.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=messages
# )
#     parsed_gpt_response = gpt_response.choices[0].message.content
   

#     #Save messages
#     save_messages(user_message.text, parsed_gpt_response)
#     return parsed_gpt_response

# def load_messages():
#     messages = []
#     file = 'database.json'
    
#     #if File is empty, add context
#     empty = os.stat(file).st_size == 0

#     if not empty:
#         with open(file) as db_file:
#             data = json.load(db_file)
#             for item in data:
#                 messages.append(item)
#     else:
#         messages.append(
#             {"role": "system", "content": "You are interviewing the user for a front-end React developer position. Ask short questions that are relevant to a junior level developer. Your name is ZRecruit. The user is Rahul Perumbali. Keep responses under 30 words."}

#         )
#     return messages

# def save_messages(user_message, gpt_response):
#     file = 'database.json'
#     messages = load_messages()
#     messages.append({"role": "user", "content": user_message})
#     messages.append({"role": "assistant", "content": gpt_response})
#     with open(file, 'w') as f:
#         json.dump(messages, f)

# def text_to_speech(text):
#     voice_id = "iP95p4xoKVk53GoZ742B"
#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

#     headers = {
#         "accept": "audio/mpeg",
#         "Content-Type": "application/json",
#         "xi-api-key": elevenlabs_key
#     }

#     data = {
#         "text": text,
#         "model_id": "eleven_monolingual_v1",
#         "voice_settings": {
#             "stability": 0.5,
#             "similarity_boost": 0.5
#         }
#     }

#     try:
#         response = requests.post(url, json=data, headers=headers)
#         if response.status_code == 200:
#             return response.content
#         else:
#             print("Something went wrong")
#     except Exception as e:
#         print(e)

# def extract_text_from_pdf(pdf_file):
#     try:
#         text = ""
#         pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
#         for page_num in range(len(pdf_document)):
#             page = pdf_document.load_page(page_num)
#             text += page.get_text()
#         return text
#     except Exception as e:
#         print(f"Error reading PDF file: {e}")
#         return None


# def generate_interview_questions(resume_text):
#     messages = [{"role": "system", "content": "You are an assistant for an interviewer that needs to generate questions based off of a given resume."}, {"role": "user", "content": f"Generate three detailed interview questions based on the following resume:\n\n{resume_text}"}]
    
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#     )
    
#     questions = response.choices[0].message.content
#     return questions.split('\n\n')


# app = Flask(__name__)

# # Your bot's interview logic here
# @app.route('/interview', methods=['POST'])
# def interview():
#     data = request.json
#     # Process the interview data with your bot
#     response = {'message': 'Response from your bot'}
#     return jsonify(response)

# @app.route('/')
# def index():
#     return send_from_directory('', 'index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# # app = Flask(__name__)

# # @app.route('/')
# # def hello():
# #     return render_template("front_end.html")

# # asgi_app = WsgiToAsgi(app)

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(asgi_app, host="127.0.0.1", port=8000)

# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Allow only localhost:3000 for security reasons
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods
#     allow_headers=["*"],  # Allow all headers
# )

# # Your existing FastAPI routes and logic


# @app.post("/upload_resume")
# async def upload_resume(file: UploadFile = File(...)):
#     content = await file.read()
#     # Process the file here
#     return {"filename": file.filename}



# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os
import json
import requests
import fitz  # PyMuPDF
from openai import OpenAI
import logging
from flask import Flask, request, jsonify

client = OpenAI(
    api_key = "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",
    organization = "org-zXbr1KA4CTSCes1EYvFqrQ6J"
)

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = "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"
elevenlabs_key = "sk_2dd73a349f57e263657a740a1edb604c328d9a69491c6609"

interview_context = {
    "resume_text": "",
    "questions": [],
    "current_question_index": 0
}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    # Process the file here
    return {"filename": file.filename}

@app.post("/interview")
async def interview_response(file: UploadFile = File(...)):
    interview_context["questions"] = generate_interview_questions(file)
    if interview_context["current_question_index"] < len(interview_context["questions"]) - 1:
        next_question = interview_context["questions"][interview_context["current_question_index"]]
        interview_context["current_question_index"] += 1
        response_text = next_question
    else:
        response_text = "Thank you for completing the interview. We will get back to you soon."
    
    audio_output = text_to_speech(response_text)
    return StreamingResponse(iter([audio_output]), media_type="audio/mpeg")

def transcribe_audio(file):
    audio_file = open(file.filename, "rb")
    #transcript = openai.Audio.transcribe(model="whisper-1", file= audio_file)
    transcript = client.audio.transcriptions.create(model = "whisper-1", file = audio_file)
    return transcript["text"]

def get_chat_response(user_message):
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    parsed_gpt_response = response.choices[0].message["content"]
    save_messages(user_message, parsed_gpt_response)
    return parsed_gpt_response

def load_messages():
    file = 'database.json'
    if os.stat(file).st_size == 0:
        return [{"role": "system", "content": "You are interviewing the user for a front-end React developer position. Ask short questions that are relevant to a junior level developer. Your name is ZRecruit. The user is Rahul Perumbali. Keep responses under 30 words."}]
    
    with open(file, 'r') as db_file:
        return json.load(db_file)

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
        return response.content
    else:
        raise HTTPException(status_code=500, detail="Text-to-speech conversion failed")

def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF file: {e}")

def generate_interview_questions(resume_text):
    messages = [
        {"role": "system", "content": "You are an assistant for an interviewer that needs to generate questions based off of a given resume."},
        {"role": "user", "content": f"Generate three detailed interview questions based on the following resume:\n\n{resume_text}"}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    questions = response.choices[0].message.content
    return questions.split('\n\n')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


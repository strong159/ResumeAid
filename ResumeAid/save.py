from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import openai
from openai import OpenAI
import os
import json
import requests
import fitz  # PyMuPDF

load_dotenv()

app = FastAPI()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    organization = os.getenv("OPENAI_API_ORG"),
)
elevenlabs_key = os.getenv("ELEVENLABS_KEY")

@app.post("/talk")
async def post_audio(file: UploadFile):
    user_message = transcribe_audio(file)
    chat_response = get_chat_response(user_message)
    audio_output = text_to_speech(chat_response)
    def iterfile():   
        yield audio_output

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
  
 # Function
def transcribe_audio(file):
    audio_file= open(file.filename, "rb")
    transcript = client.audio.transcriptions.create(model = "whisper-1", file = audio_file)
    print(transcript)
    return transcript

def get_chat_response(user_message): 
    messages = load_messages()
    messages.append({"role": "user", "content": user_message.text})
    print(messages)
    #Send to GPT
    gpt_response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)
    parsed_gpt_response = gpt_response.choices[0].message.content
   

    #Save messages
    save_messages(user_message.text, parsed_gpt_response)
    return parsed_gpt_response

def load_messages():
    messages = []
    file = 'database.json'
    
    #if File is empty, add context
    empty = os.stat(file).st_size == 0

    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
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

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            print("Something went wrong")
    except Exception as e:
        print(e)

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        pdf_document = fitz.open(pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None


def generate_interview_questions(resume_text):
    messages = [{"role": "system", "content": "You are an assistant for an interviewer that needs to generate questions based off of a given resume."}, {"role": "user", "content": f"Generate three detailed interview questions based on the following resume:\n\n{resume_text}"}]
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    questions = response.choices[0].message.content
    return questions

async def generate_questions(pdf: UploadFile):
    print("Extracting Resume Text...")
    resume_text = extract_text_from_pdf(pdf)
    
    if resume_text:
        print("Generating Questions...")
        questions = generate_interview_questions(resume_text)
        listOfQuestions = questions.split('\n\n')
        print("Generated Interview Questions:")
        for question in listOfQuestions:
            print(f"{question}\n")
    else:
        print("Failed to extract text from the PDF file.")

        # save.py

# def save_response(response):
#     # Logic to save the response
#     with open('responses.txt', 'a') as f:
#         f.write(response + '\n')
#     return True




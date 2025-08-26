from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import openai
from openai import OpenAI
import os
import json
import requests
import io

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
    print("please")
    #print(chat_response)
    audio_output = text_to_speech(chat_response)
    print("pretty please")
    # user_message = transcribe_audio(file)
    # chat_response = get_chat_response(user_message)   
    def iterfile():  # 
        yield audio_output

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
  
 # Function-Speech to text
def transcribe_audio(file):
    audio_data = file.read()
    buffer = io.BytesIO(audio_data)
    buffer.name = "file.mp3"  # this is the important line
    # print(file.filename.endswith('.mp3'))
    try:
        transcript = client.audio.transcriptions.create(model="whisper-1", file= buffer)
        print(transcript)
        return transcript.text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def get_chat_response(user_message): 
    messages = load_messages()
    messages.append({"role": "user", "content": user_message.text})
    print(messages)
    #gpt_response = {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."}
    #Send to GPT
    gpt_response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)
    parsed_gpt_response = gpt_response.choices[0].message.content
   

    #Save messages
    save_messages(user_message.text, parsed_gpt_response)
    return parsed_gpt_response
    # print("hello?")

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

# Text to speech
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


        # audio.py

# def record_audio():
#     # Logic to record audio
#     pass

# def listen_audio(audio_file):
#     # Logic to process the audio file
#     transcription = "Transcribed text from audio"
#     return transcription

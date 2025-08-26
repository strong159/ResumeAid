from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os
import json
import requests
from azure.storage.blob import BlobServiceClient
import fitz  # PyMuPDF

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
azure_connection_string = os.getenv("AZURE_CONNECTION_STRING")
elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
container_name = "your-container-name"

# Read the stats.json file
with open('stats.json', 'r') as file:
    data = json.load(file)

# Extract necessary information
job_description = data['job']['description']
resume = json.dumps(data['profile'], indent=4)

# Generate interview questions
def generate_interview_questions(job_description, resume, num_questions=5):
    messages = [
        {"role": "system", "content": "You are an assistant for an interviewer that needs to generate questions based off of a given resume and job description."},
        {"role": "user", "content": f"Generate {num_questions} detailed interview questions based on the following resume and job description:\n\nResume:\n{resume}\n\nJob Description:\n{job_description}"}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    questions = response.choices[0].message.content
    return questions.split('\n\n')

questions = generate_interview_questions(job_description, resume)


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

# Upload file to Azure Blob Storage
def upload_to_azure(file_content, file_name):
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    blob_client.upload_blob(file_content, overwrite=True)
    return blob_client.url

questions_json = []

for i, question in enumerate(questions):
    audio_content = text_to_speech(question)
    file_name = f"question_{i+1}.mp3"
    audio_url = upload_to_azure(audio_content, file_name)
    questions_json.append({
        "questionText": question,
        "questionAudioPath": audio_url,
    })

# Save the questions to questions.json
with open('questions.json', 'w') as file:
    json.dump(questions_json, file, indent=4)

print("Interview questions generated and saved to questions.json")

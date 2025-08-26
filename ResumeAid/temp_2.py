from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os
import json
import requests
import fitz  # PyMuPDF

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

openai.api_key = os.getenv("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")
elevenlabs_key = os.getenv("sk_7c45d5b071daa27cd0cbd2ce577ca7f464105416ba5d65b3")

interview_context = {
    "resume_text": "",
    "job_description_text": "",
    "questions": [],
    "current_question_index": 0
}

@app.post("/upload_resume")
async def upload_resume(resume: UploadFile = File(...)):
    try:
        resume_content = await resume.read()
        resume_text = extract_text_from_pdf(resume_content)
        interview_context["resume_text"] = resume_text
        return {"message": "Resume uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {e}")

@app.post("/upload_job_description")
async def upload_job_description(job_description: UploadFile = File(...)):
    try:
        job_description_content = await job_description.read()
        job_description_text = extract_text_from_pdf(job_description_content)
        interview_context["job_description_text"] = job_description_text
        return {"message": "Job description uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing job description: {e}")

@app.post("/submit_response")
async def submit_response(user_response: str = format(...)):
    interview_context["user_responses"].append(user_response)
    if interview_context["current_question_index"] < len(interview_context["questions"]):
        next_question = interview_context["questions"][interview_context["current_question_index"]]
        interview_context["current_question_index"] += 1
        response_text = next_question
    else:
        response_text = "Thank you for completing the interview. We will get back to you soon."
    
    audio_output = text_to_speech(response_text)
    return StreamingResponse(iter([audio_output]), media_type="audio/mpeg")

@app.post("/interview")
async def interview_response():
    resume_text = interview_context["resume_text"]
    job_description_text = interview_context["job_description_text"]
    interview_context["questions"] = generate_interview_questions(resume_text, job_description_text)
    print(interview_context["questions"])
    
    if interview_context["current_question_index"] < len(interview_context["questions"]):
        next_question = interview_context["questions"][interview_context["current_question_index"]]
        interview_context["current_question_index"] += 1
        response_text = next_question
    else:
        response_text = "Thank you for completing the interview. We will get back to you soon."
    
    audio_output = text_to_speech(response_text)
    return StreamingResponse(iter([audio_output]), media_type="audio/mpeg")

def extract_text_from_pdf(pdf_content):
    try:
        text = ""
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF file: {e}")

def generate_interview_questions(resume_text, job_description_text):
    messages = [
        {"role": "system", "content": "You are an assistant for an interviewer that needs to generate questions based off of a given resume and job description."},
        {"role": "user", "content": f"Generate three detailed interview questions based on the following resume and job description:\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description_text}"}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    questions = response.choices[0].message.content
    return questions.split('\n\n')

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

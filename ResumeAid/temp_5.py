from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os
import requests
import fitz  # PyMuPDF
import io
from gtts import gTTS
from pydub import AudioSegment



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
elevenlabs_key = os.getenv("sk_f562b71147555279dbd803fffe96a3313e00d8687447808a")

interview_context = {
    "resume_text": "",
    "job_description_text": "",
    "questions": [],
    "current_question_index": 0,
    "user_responses": []
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
async def submit_response(audio: UploadFile = File(...)):
    try:
        audio_content = await audio.read()
        interview_context["user_responses"].append(audio_content)
        
        if interview_context["current_question_index"] < len(interview_context["questions"]):
            next_question = interview_context["questions"][interview_context["current_question_index"]]
            interview_context["current_question_index"] += 1
            response_text = next_question
        else:
            response_text = "Thank you for completing the interview. We will get back to you soon."
            # Reset interview context after completion
            interview_context["questions"] = []
            interview_context["current_question_index"] = 0
            interview_context["user_responses"] = []

        audio_output = text_to_speech(response_text)
        return StreamingResponse(io.BytesIO(audio_output), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during audio response submission: {e}")

@app.post("/interview")
async def interview_response():
    try:
        resume_text = interview_context["resume_text"]
        job_description_text = interview_context["job_description_text"]
        interview_context["questions"] = generate_interview_questions(resume_text, job_description_text)
        interview_context["current_question_index"] = 0  # Reset for new interview
        interview_context["user_responses"] = []
        
        if interview_context["questions"]:
            next_question = interview_context["questions"][interview_context["current_question_index"]]
            interview_context["current_question_index"] += 1
            response_text = next_question
        else:
            response_text = "No questions were generated. Please check the resume and job description."
        
        audio_output = text_to_speech(response_text)
        return StreamingResponse(io.BytesIO(audio_output), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating interview questions: {e}")

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
    try:
        # Use gTTS to convert text to speech
        tts = gTTS(text=text, lang='en')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert the audio to mp3 format using pydub
        audio = AudioSegment.from_file(audio_buffer, format="mp3")
        output_buffer = io.BytesIO()
        audio.export(output_buffer, format="mp3")
        output_buffer.seek(0)
        
        return output_buffer.read()
    except Exception as e:
        print(f"Text-to-speech conversion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {e}")

# Ensure ffmpeg is installed for pydub
AudioSegment.ffmpeg = "/usr/local/bin/ffmpeg"
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

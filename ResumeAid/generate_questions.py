import openai
from openai import OpenAI
import os
import fitz  # PyMuPDF

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
    messages = [{"role": "system", "content": "You are an assistant for an interviewer that needs to generate questions based off of a given resume."}, {"role": "user", "content": f"Generate three detailed interview questions based on the following resume:\n\n{resume_text}"}]
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    questions = response.choices[0].message.content
    return questions

def main():
    pdf_path = input("Please enter the path to the PDF resume file: ")
    #pdf_path = "/Users/sanjaysaravanakumaran/interview_Bot/zillion_resume.pdf"

    if not os.path.isfile(pdf_path):
        print("The provided path is invalid. Please make sure the file exists.")
        return
    
    print("Extracting Resume Text...")
    resume_text = extract_text_from_pdf(pdf_path)
    
    if resume_text:
        print("Generating Questions...")
        questions = generate_interview_questions(resume_text)
        listOfQuestions = questions.split('\n\n')
        print("Generated Interview Questions:")
        for question in listOfQuestions:
            print(f"{question}\n")
        # for i, question in enumerate(questions, 1):
        #     print(f"Question {i}: {question}")
    else:
        print("Failed to extract text from the PDF file.")

if __name__ == "__main__":
    main()


# generate_questions.py

# def generate_questions(resume_file):
#     # Logic to generate questions from the resume file
#     #questions = ["Tell me about yourself", "What are your strengths?"]
#     resume_text = extract_text_from_pdf(resume_file)
#     questions = generate_interview_questions(resume_text)
#     return questions.split('\n\n')

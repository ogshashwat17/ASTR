from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from groq import Groq
from pypdf import PdfReader

# Configure Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def get_llm_response(job_description, resume_text, prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
{prompt}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""
            }
        ],
    )
    return response.choices[0].message.content


# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

job_description = st.text_area("Job Description")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Percentage Match")

prompt_review = """
You are an experienced Technical HR.
Evaluate the resume against the job description.
Highlight strengths and weaknesses.
"""

prompt_ats = """
You are an ATS scanner.
Return:
1. Percentage match
2. Missing keywords
3. Final verdict
"""

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

    if submit1:
        st.subheader("HR Review")
        st.write(get_llm_response(job_description, resume_text, prompt_review))

    if submit2:
        st.subheader("ATS Match")
        st.write(get_llm_response(job_description, resume_text, prompt_ats))

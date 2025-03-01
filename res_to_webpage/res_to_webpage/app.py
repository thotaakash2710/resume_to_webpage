import os
import openai
import streamlit as st
import pdfplumber
from dotenv import load_dotenv
import docx


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OpenAI API key is missing. Please set it in your environment variables.")
    st.stop()

openai.api_key = OPENAI_API_KEY

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = [paragraph.text for paragraph in doc.paragraphs]
    return "\n".join(full_text)

def generate_resume_summary(resume_text):
    prompt = f"""
    Format the following resume into a structured markdown layout with sections:
    - **Summary**: A concise overview of the candidate's expertise.
    - **Experience**: Bullet points with job roles, companies, and key accomplishments.
    - **Education**: Degrees, universities, and graduation years.
    - **Skills**: A list of technical and soft skills.
    - **Projects**: Highlight notable projects (if any).

    Ensure clarity, conciseness, and a professional tone.
    Resume Text:
    {resume_text}
    """

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert resume formatter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        formatted_resume = response.choices[0].message.content
        return formatted_resume

    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Resume to Webpage Builder (File Upload Version)")
    st.markdown("Upload your PDF or DOCX resume below, and let AI generate an impressive webpage layout:")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a PDF or DOCX.")
            return

        with st.expander("Preview Extracted Text"):
            st.write(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)

        
        if st.button("Build My Webpage"):
            if resume_text.strip():
                with st.spinner("Generating your resume webpage..."):
                    result_markdown = generate_resume_summary(resume_text)

                
                st.session_state["generated_resume"] = result_markdown

                
                st.switch_page("pages/resume_page.py")

            else:
                st.warning("No text was found in the uploaded file.")

    else:
        st.info("Please upload a PDF or DOCX file to get started.")

if __name__ == "__main__":
    main()

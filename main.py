import streamlit as st
from markitdown import MarkItDown
import tempfile
import argparse
import os
from utils import html_tamplate, swot_analyzer, resume_parsing

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run the Streamlit app.')
    parser.add_argument('--environment', 
                        type=str, 
                        choices=['local', 'cloud'], 
                        default='cloud',
                        help='Specify the environment: "local" or "cloud".')
    args = parser.parse_args()
    
    if args.environment == 'cloud':
        # Access secret values
        groq_key = st.secrets["GROQ_KEY"]
    else:
        from dotenv import load_dotenv
        load_dotenv()
        # Access secret values
        groq_key = os.getenv("GROQ_KEY")
    
    st.set_page_config(
          layout="wide"  # This makes the app take the full page width
      )
    
    uploaded_file = st.file_uploader("🚀 Upload your resume here 📄✨", type=["pdf", "docx"])
    job_description = st.text_area("📝 Enter the job description here 💼")

    if uploaded_file is not None and job_description:
      if st.button('Analyze'):
          parsed_resume = resume_parsing(uploaded_file)
          swot_analysis = swot_analyzer(api_key = groq_key,
                                        parsed_resume = parsed_resume, 
                                        job_description = job_description)
          html_content = html_tamplate(swot_analysis = swot_analysis)
          st.components.v1.html(f"""{html_content}""", width=1000, height=1000)
if __name__ == "__main__":
    main()

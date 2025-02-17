import streamlit as st
from markitdown import MarkItDown
import tempfile
from utils import html_tamplate, swot_analyzer
def resume_parsing(uploaded_file):
  suffix = uploaded_file.name.split(".")[-1].lower()
  with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
      temp_file.write(uploaded_file.read())
      file_path = temp_file.name
  md = MarkItDown() 
  result = md.convert(file_path)
  return result.text_content
  

def main():
    st.title("File Uploader and Text Zone")
    
    uploaded_file = st.file_uploader("🚀 Upload your resume here 📄✨", type=["pdf", "docx"])
    job_description = st.text_area("📝 Enter the job description here 💼")

    if uploaded_file is not None and job_description:
      if st.button('Analyze'):
          parsed_resume = resume_parsing(uploaded_file)
          swot_analysis = swot_analyzer(parsed_resume, job_description)
          html_content = html_tamplate(swot_analysis)
          st.components.v1.html(f"""{html_content}""", width=1000, height=1000)
if __name__ == "__main__":
    main()

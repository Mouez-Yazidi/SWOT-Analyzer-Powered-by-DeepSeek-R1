import streamlit as st
from markitdown import MarkItDown
import tempfile

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
    
    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])
    text_input = st.text_area("Enter additional text here:")
    
    if uploaded_file is not None:
        extracted_text = resume_parsing(uploaded_file)
        
        st.subheader("Extracted Text:")
        st.text_area("", extracted_text, height=300)
    
    if text_input:
        st.subheader("Entered Text:")
        st.write(text_input)

if __name__ == "__main__":
    main()

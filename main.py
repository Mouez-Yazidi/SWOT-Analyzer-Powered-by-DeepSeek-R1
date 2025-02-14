import streamlit as st
from markitdown import MarkItDown

def resume_parsing(uploaded_file):
  md = MarkItDown() 
  result = md.convert(uploaded_file)
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

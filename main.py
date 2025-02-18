import streamlit as st
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
          layout="wide", # This makes the app take the full page width
      )
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3997/3997521.png")
    st.sidebar.markdown("## 🏆 Unlock Your Career Potential with DeepSeek R1!")
    st.sidebar.write(
        """   
        Transform your job search and hiring process with our cutting-edge AI that analyzes **CVs** and **Job Descriptions** to deliver a **personalized SWOT Analysis** (Strengths, Weaknesses, Opportunities, and Threats).
    
        **Why DeepSeek R1 Stands Out:**
        - **Deep Insights & Customization:** Tailors the analysis to your unique career profile and job market trends.
        - **Actionable Recommendations:** Identifies not just what you’re good at, but also strategic areas for growth and improvement.
        - **Efficiency & Precision:** Streamlines decision-making for both job seekers and recruiters, saving you time and reducing bias.
    
        **How It Works:**
        1. **Upload:** Simply upload your **CV** and **Job Description**.
        2. **Analyze:** Our advanced AI compares skills, experience, and job requirements.
        3. **Strategize:** Receive a comprehensive **SWOT Analysis** that pinpoints your key strengths and areas needing attention.
    
        🔍 **Ideal For:** Job seekers aiming to align their skills with market demands and recruiters focused on bridging talent gaps with precision.
        """
    )
    uploaded_file = st.file_uploader("🚀 Upload your resume here 📄✨", type=["pdf", "docx"])
    job_description = st.text_area("📝 Enter the job description here 💼")

    if uploaded_file is not None and job_description:
      if st.button('Analyze'):
          parsed_resume = resume_parsing(uploaded_file)
          swot_analysis = swot_analyzer(api_key = groq_key,
                                        resume_content = parsed_resume, 
                                        job_description = job_description)
          html_content = html_tamplate(swot_analysis = swot_analysis)
          st.components.v1.html(f"""{html_content}""", width=1000, height=1000)
if __name__ == "__main__":
    main()

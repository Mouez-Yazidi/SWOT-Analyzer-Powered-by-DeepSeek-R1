from groq import Groq
from markitdown import MarkItDown
import tempfile
from typing import Dict, Any

def resume_parsing(uploaded_file: Any) -> str:
    """
    Parses a resume file and extracts text content.

    Args:
        uploaded_file (Any): The uploaded file object, typically from a web framework like Streamlit.

    Returns:
        str: The extracted text content from the resume.
    """
    suffix = uploaded_file.name.split(".")[-1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name
    
    md = MarkItDown() 
    result = md.convert(file_path)
    
    return result.text_content

def swot_analyzer(api_key: str, resume_content: str, job_description: str) -> Dict[str, Any]:
    """
    Performs a SWOT analysis by comparing a candidate’s resume to a given job description 
    using an AI model.

    Args:
        api_key (str): The API key for the Groq client.
        resume_content (str): The text content of the candidate's resume.
        job_description (str): The job description to compare against.

    Returns:
        Dict[str, Any]: A dictionary containing SWOT analysis results with categories:
                        - strengths
                        - weaknesses
                        - opportunities
                        - threats
    """
  
    client = Groq(api_key=api_key)
    
    PROMPT = """
    Role: You are a professional career advisor specializing in resume optimization and job alignment. Your task is to perform a detailed, evidence-based SWOT analysis comparing a candidate’s resume to a specific job description.
    
    Instructions
    Input Analysis:
    
    Resume: Extract technical skills, soft skills, certifications, work experience (including tenure and achievements), education, projects, and industry-specific keywords.
    
    Job Description: Identify explicit requirements (e.g., “5+ years in Python”), implicit expectations (e.g., leadership in team-based environments), preferred qualifications, company culture cues, and industry trends.
    
    SWOT Analysis Criteria:
    
    Strengths: Direct matches between resume items and job requirements (e.g., “Certified AWS DevOps Engineer aligns with cloud infrastructure role”).
    
    Weaknesses: Gaps in skills/experience, ambiguous wording (e.g., “Led projects” without metrics), or missing credentials.
    
    Opportunities: Undersold transferable skills (e.g., volunteer leadership for management roles), industry trends the candidate could address (e.g., AI familiarity for tech roles), or certifications to bridge minor gaps.
    
    Threats: Risks like competing candidates with niche certifications, automation impacting the role, or overqualification mismatches.
    
    
    Output Format
    Return strictly valid JSON with this structure:
    ```json
    {  
      "strengths": ["Concise bullet tied to job requirements (e.g., 'Advanced Python skills mirror job’s core demand for backend development')"],  
      "weaknesses": ["Specific gaps (e.g., 'No experience with Kubernetes, listed as required in job description')"],  
      "opportunities": ["Actionable leverage points (e.g., '3 years of Agile experience could position candidate for Scrum Master opportunities')"],  
      "threats": ["External risks (e.g., 'Job emphasizes AI/ML, which is not addressed in resume')"]
      }
    ```
    
    Rules
    * Prioritize quality over quantity (3-5 bullets per category max).
    * Use job-specific terminology (e.g., “Proficiency in React.js” vs. “frontend skills”).
    * Flag ambiguities in weaknesses (e.g., “Achieved ‘excellent results’ lacks quantifiable metrics”).
    * Never include markdown, explanations, or placeholder text. 
     
    """
    full_prompt = f"{PROMPT}\n\nResume Content:\n{resume_content}\n\nJob Description:\n{job_description}"
    
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-qwen-32b",
        messages=[{
                "role": "user",
                "content": full_prompt
            }],
        temperature=0,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=False,
        response_format={
            "type": "json_object"
        }
    )
    return completion.choices[0].message.content

def html_tamplate(swot_analysis):
    html_content =  f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />
        <title>SWOT Analysis</title>
        <!-- Google Fonts: Poppins -->
        <link
          href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap"
          rel="stylesheet"
        />
        <style>
          * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }}
    
          body {{
            font-family: "Poppins", sans-serif;
            background-color: #fffff;
            color: #333;
            line-height: 1.6;
            padding: 20px;
          }}
    
          h1 {{
            text-align: center;
            font-size: 2rem;
            margin-bottom: 30px;
            font-weight: 600;
          }}
    
          .swot-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            max-width: 1000px;
            margin: 0 auto;
          }}
    
          .swot-card {{
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
          }}
    
          .swot-card h2 {{
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 15px;
          }}
    
          .strengths {{
            background-color: #ffd5d5;
          }}
          .weaknesses {{
            background-color: #cde4ff;
          }}
          .opportunities {{
            background-color: #d2ffcc;
          }}
          .threats {{
            background-color: #fff1cc;
          }}
    
          .swot-card ul {{
            list-style: none;
            padding-left: 0;
            margin-top: 10px;
          }}
    
          .swot-card li {{
            background-color: rgba(255, 255, 255, 0.4);
            margin-bottom: 8px;
            padding: 8px 12px;
            border-radius: 4px;
            font-weight: 300;
            transition: background-color 0.3s ease;
          }}
          .swot-card li:hover {{
            background-color: rgba(255, 255, 255, 0.6);
          }}
    
          @media (max-width: 768px) {{
            .swot-grid {{
              grid-template-columns: 1fr;
            }}
          }}
        </style>
      </head>
      <body>
        <div class="swot-grid">
          <div class="swot-card strengths">
            <h2>Strengths</h2>
            <ul id="strengths-list"></ul>
          </div>
    
          <div class="swot-card weaknesses">
            <h2>Weaknesses</h2>
            <ul id="weaknesses-list"></ul>
          </div>
    
          <div class="swot-card opportunities">
            <h2>Opportunities</h2>
            <ul id="opportunities-list"></ul>
          </div>
    
          <div class="swot-card threats">
            <h2>Threats</h2>
            <ul id="threats-list"></ul>
          </div>
        </div>
    
        <script>
          const swotData = {swot_analysis};
    
          function populateSwot(swot) {{
            const strengthsList = document.getElementById("strengths-list");
            const weaknessesList = document.getElementById("weaknesses-list");
            const opportunitiesList = document.getElementById("opportunities-list");
            const threatsList = document.getElementById("threats-list");
    
            const createListItems = (items, parent) => {{
              items.forEach((item) => {{
                const li = document.createElement("li");
                li.textContent = item;
                parent.appendChild(li);
              }});
            }};
    
            createListItems(swot.strengths, strengthsList);
            createListItems(swot.weaknesses, weaknessesList);
            createListItems(swot.opportunities, opportunitiesList);
            createListItems(swot.threats, threatsList);
          }}
    
          populateSwot(swotData);
        </script>
      </body>
    </html>
    """
    html_content = html_content.replace("{{","{")
    html_content = html_content.replace("}}","}")
    return html_content

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
    
    uploaded_file = st.file_uploader("🚀 Upload your resume here 📄✨", type=["pdf", "docx"])
    text_input = st.text_area("📝 Enter the job description here 💼")

    if uploaded_file is not None and text_input:
      if st.button('Analyze'):
          extracted_text = resume_parsing(uploaded_file)
          st.text_area("", extracted_text, height=300)
          st.components.v1.html("""
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
    /* Global reset */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: "Poppins", sans-serif;
      background-color: #f0f2f5;
      color: #333;
      line-height: 1.6;
      padding: 20px;
      height: 100%;
      width: 100%;
      overflow: hidden;
    }

    /* Main title */
    h1 {
      text-align: center;
      font-size: 2rem;
      margin-bottom: 30px;
      font-weight: 600;
    }

    /* Container for the 2×2 grid */
    .swot-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: auto auto;
      gap: 20px;
      max-width: 1000px;
      margin: 0 auto; /* center the grid */
    }

    /* Each card container sets the perspective for 3D flip */
    .swot-card {
      perspective: 1000px; /* Needed for 3D flipping */
      min-height: 220px;   /* Ensure enough space for content */
      border-radius: 8px;
      position: relative;
    }

    /* The inner wrapper that will actually flip */
    .swot-card-inner {
      width: 100%;
      height: 100%;
      transition: transform 0.6s;
      transform-style: preserve-3d; /* 3D space for flipping */
      border-radius: 8px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      position: relative;
    }

    /* Front and back faces */
    .swot-card-front,
    .swot-card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden; /* Hide reversed side */
      border-radius: 8px;
      padding: 20px;
      box-sizing: border-box;
    }

    /* The back side is initially hidden by rotating 180deg */
    .swot-card-back {
      transform: rotateY(180deg);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }

    /* When the .flip class is applied, rotate the card 180deg */
    .flip {
      transform: rotateY(180deg);
    }

    /* Card headings */
    .swot-card-front h2,
    .swot-card-back h2 {
      font-size: 1.4rem;
      font-weight: 600;
      margin-bottom: 15px;
    }

    /* 2×2 color scheme (front side) */
    .strengths .swot-card-front {
      background-color: #ffd5d5; /* Soft Pink */
    }
    .weaknesses .swot-card-front {
      background-color: #cde4ff; /* Light Blue */
    }
    .opportunities .swot-card-front {
      background-color: #d2ffcc; /* Light Green */
    }
    .threats .swot-card-front {
      background-color: #fff1cc; /* Light Yellow */
    }

    /* A different (or same) color for the back side (optional) */
    /* You can keep it the same color or change it to something else. */
    .strengths .swot-card-back {
      background-color: #ffc5c5; /* Slightly darker pink */
    }
    .weaknesses .swot-card-back {
      background-color: #bcd4f9; /* Slightly darker blue */
    }
    .opportunities .swot-card-back {
      background-color: #c2fcbc; /* Slightly darker green */
    }
    .threats .swot-card-back {
      background-color: #ffe4b3; /* Slightly darker yellow */
    }

    /* List styling on the front side */
    .swot-card-front ul {
      list-style: none;
      padding-left: 0;
      margin-top: 10px;
    }
    .swot-card-front li {
      background-color: rgba(255, 255, 255, 0.4);
      margin-bottom: 8px;
      padding: 8px 12px;
      border-radius: 4px;
      font-weight: 300;
      transition: background-color 0.3s ease;
    }
    .swot-card-front li:hover {
      background-color: rgba(255, 255, 255, 0.6);
    }

    /* Back side link styling */
    .swot-card-back a {
      display: inline-block;
      margin-top: 10px;
      padding: 8px 16px;
      background-color: #fff;
      color: #333;
      text-decoration: none;
      border-radius: 4px;
      font-weight: 400;
      transition: background-color 0.3s ease;
    }
    .swot-card-back a:hover {
      background-color: #eee;
    }

    /* Responsive design for smaller screens */
    @media (max-width: 768px) {
      .swot-grid {
        grid-template-columns: 1fr;
        grid-template-rows: auto;
      }
    }
  </style>
</head>
<body>

<h1>What's in a SWOT analysis?</h1>

<div class="swot-grid">
  <!-- STRENGTHS -->
  <div class="swot-card strengths" onclick="flipCard('strengths-card')">
    <div class="swot-card-inner" id="strengths-card">
      <div class="swot-card-front">
        <h2>Strengths</h2>
        <ul id="strengths-list"></ul>
      </div>
      <div class="swot-card-back">
        <h2>More Info on Strengths</h2>
        <!-- You can place any content or link here -->
        <a href="#" onclick="event.stopPropagation(); unflipCard('strengths-card'); return false;">Back</a>
      </div>
    </div>
  </div>

  <!-- WEAKNESSES -->
  <div class="swot-card weaknesses" onclick="flipCard('weaknesses-card')">
    <div class="swot-card-inner" id="weaknesses-card">
      <div class="swot-card-front">
        <h2>Weaknesses</h2>
        <ul id="weaknesses-list"></ul>
      </div>
      <div class="swot-card-back">
        <h2>More Info on Weaknesses</h2>
        <a href="#" onclick="event.stopPropagation(); unflipCard('weaknesses-card'); return false;">Back</a>
      </div>
    </div>
  </div>

  <!-- OPPORTUNITIES -->
  <div class="swot-card opportunities" onclick="flipCard('opportunities-card')">
    <div class="swot-card-inner" id="opportunities-card">
      <div class="swot-card-front">
        <h2>Opportunities</h2>
        <ul id="opportunities-list"></ul>
      </div>
      <div class="swot-card-back">
        <h2>More Info on Opportunities</h2>
        <a href="#" onclick="event.stopPropagation(); unflipCard('opportunities-card'); return false;">Back</a>
      </div>
    </div>
  </div>

  <!-- THREATS -->
  <div class="swot-card threats" onclick="flipCard('threats-card')">
    <div class="swot-card-inner" id="threats-card">
      <div class="swot-card-front">
        <h2>Threats</h2>
        <ul id="threats-list"></ul>
      </div>
      <div class="swot-card-back">
        <h2>More Info on Threats</h2>
        <a href="#" onclick="event.stopPropagation(); unflipCard('threats-card'); return false;">Back</a>
      </div>
    </div>
  </div>
</div>

<script>
  // Example JSON data; replace this with your actual SWOT data
  const swotData = {
  "strengths": [
    "Solid technical background with relevant skills in SQL, databases, and programming.",
    "Versatile experience in web and app development.",
    "Proficiency in multiple languages, including English and French, meeting the job's language requirements.",
    "Hands-on experience with data analysis and machine learning.",
    "Projects demonstrate strong problem-solving skills."
  ],
  "weaknesses": [
    "Lacks the required 5 years of PL/SQL experience.",
    "No mention of Oracle expertise on the resume.",
    "Limited direct experience in performance tuning and query optimization.",
    "Currently a student with limited full-time work experience.",
    "No indication of willingness to relocate to Portugal."
  ],
  "opportunities": [
    "Data science background could enhance data-driven roles.",
    "Transferable web development skills to other technical areas.",
    "Potential to grow into roles requiring SQL and database management.",
    "Language skills open opportunities in multilingual environments."
  ],
  "threats": [
    "Lack of specific experience makes the role competitive.",
    "Missing industry-specific knowledge in target sectors.",
    "Relocation to Portugal could be a barrier."
  ]};

  // Populate each list from the JSON data
  function populateSwot(swot) {
    const strengthsList = document.getElementById("strengths-list");
    const weaknessesList = document.getElementById("weaknesses-list");
    const opportunitiesList = document.getElementById("opportunities-list");
    const threatsList = document.getElementById("threats-list");

    const createListItems = (items, parent) => {
      items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        parent.appendChild(li);
      });
    };

    createListItems(swot.strengths, strengthsList);
    createListItems(swot.weaknesses, weaknessesList);
    createListItems(swot.opportunities, opportunitiesList);
    createListItems(swot.threats, threatsList);
  }

  // Flip and unflip card functions
  function flipCard(cardId) {
    const card = document.getElementById(cardId);
    // If already flipped, do nothing. Otherwise, add the flip class.
    if (!card.classList.contains("flip")) {
      card.classList.add("flip");
    }
  }

  function unflipCard(cardId) {
    const card = document.getElementById(cardId);
    // Remove the flip class to show the front side again
    card.classList.remove("flip");
  }

  // Initialize
  populateSwot(swotData);
</script>

</body>
</html>
""", width=1000, height=1000)
if __name__ == "__main__":
    main()

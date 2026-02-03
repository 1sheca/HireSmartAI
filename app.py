import streamlit as st
import json
import re
import os
import hashlib
from pathlib import Path
from groq import Groq
import PyPDF2
import io
import pandas as pd
from dotenv import load_dotenv
from docx import Document
from fpdf import FPDF
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Page config
st.set_page_config(
    page_title="HireSmartAI - Recruitment OS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI with purple theme
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main background */
    .stApp {
        background: #f8f9fc;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e5e7eb;
        padding-top: 1rem;
    }

    [data-testid="stSidebar"] .stMarkdown {
        padding: 0 1rem;
    }

    /* Logo and brand */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .brand-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
    }

    .brand-text {
        font-weight: 700;
        font-size: 1.1rem;
        color: #1f2937;
    }

    .brand-subtitle {
        font-size: 0.75rem;
        color: #6b7280;
    }

    /* Navigation items */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        cursor: pointer;
        transition: all 0.2s;
        color: #4b5563;
        text-decoration: none;
    }

    .nav-item:hover {
        background: #f3f4f6;
    }

    .nav-item.active {
        background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
        color: #7c3aed;
        font-weight: 600;
    }

    /* Main content area */
    .main-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }

    .main-subtitle {
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Cards */
    .upload-card, .jd-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px dashed #e5e7eb;
        min-height: 200px;
    }

    .jd-card {
        border: 1px solid #e5e7eb;
        border-radius: 16px;
    }

    /* File chip */
    .file-chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        margin: 0.25rem;
        font-size: 0.85rem;
        color: #374151;
    }

    /* Results section */
    .results-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 2rem 0 1rem 0;
    }

    .results-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .match-count {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Category section headers */
    .category-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }

    .category-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
    }

    .category-count {
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Skill tags */
    .skill-matched {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin: 0.1rem;
        border: 1px solid #bbf7d0;
    }

    .skill-missing {
        display: inline-block;
        background: #fee2e2;
        color: #991b1b;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin: 0.1rem;
        border: 1px solid #fecaca;
    }

    .skill-nice {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin: 0.1rem;
        border: 1px solid #c7d2fe;
    }

    /* Section labels */
    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    /* Custom streamlit overrides */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        padding: 1rem;
        font-size: 0.95rem;
    }

    .stTextArea textarea:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
    }

    div[data-testid="stFileUploader"] {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        border: 2px dashed #ddd6fe;
    }

    div[data-testid="stFileUploader"]:hover {
        border-color: #8b5cf6;
    }

    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.25);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    }

    .stProgress > div > div {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    }

    /* Keyword tags */
    .keyword-tag {
        display: inline-block;
        background: #ede9fe;
        color: #7c3aed;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        margin: 0.2rem;
        border: 1px solid #ddd6fe;
    }

    /* User profile in sidebar */
    .user-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 1rem;
        border-top: 1px solid #e5e7eb;
        margin-top: auto;
    }

    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
    }

    .user-name {
        font-weight: 600;
        color: #1f2937;
        font-size: 0.9rem;
    }

    .user-plan {
        font-size: 0.75rem;
        color: #8b5cf6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = []
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'folder_pdf_paths' not in st.session_state:
    st.session_state.folder_pdf_paths = []
if 'duplicates_count' not in st.session_state:
    st.session_state.duplicates_count = 0
if 'total_files_processed' not in st.session_state:
    st.session_state.total_files_processed = 0
if 'suggested_keywords' not in st.session_state:
    st.session_state.suggested_keywords = []
if 'job_title' not in st.session_state:
    st.session_state.job_title = ""

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_from_pdf_path(pdf_path):
    """Extract text from PDF file path (for folder upload)"""
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            text = re.sub(r'\s+', ' ', text).strip()
            return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_from_docx(docx_file):
    """Extract text from uploaded DOCX file"""
    try:
        doc = Document(io.BytesIO(docx_file.read()))
        text = ""
        for para in doc.paragraphs:
            text += para.text + " "
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + " "
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_from_docx_path(docx_path):
    """Extract text from DOCX file path (for folder upload)"""
    try:
        doc = Document(docx_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + " "
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + " "
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def get_content_hash(text):
    """Generate hash of resume content for duplicate detection"""
    normalized = re.sub(r'\s+', ' ', text.lower().strip())
    return hashlib.md5(normalized.encode()).hexdigest()

def extract_keywords_from_jd(client, job_description):
    """Extract suggested keywords from job description using AI"""
    prompt = f"""Analyze the following job description and extract key skills, technologies, and qualifications.

Return ONLY valid JSON in this exact format:
{{
    "job_title": "<extracted job title>",
    "must_have_skills": ["skill1", "skill2", "skill3"],
    "nice_to_have_skills": ["skill1", "skill2"],
    "technologies": ["tech1", "tech2"],
    "qualifications": ["qual1", "qual2"],
    "experience_required": "<e.g., 3-5 years>"
}}

JOB DESCRIPTION:
{job_description[:3000]}

Return ONLY the JSON object."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800
        )
        result_text = response.choices[0].message.content.strip()

        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]

        return json.loads(result_text)
    except:
        return {"job_title": "", "must_have_skills": [], "nice_to_have_skills": [], "technologies": [], "qualifications": [], "experience_required": ""}

def calculate_verdict_from_score(score):
    """Calculate verdict deterministically from score - NO LLM involvement"""
    score = max(0, min(100, score))  # Clamp between 0-100

    if score >= 85:
        return "Best Fit", "Recommend for Interview"
    elif score >= 70:
        return "Strong Fit", "Recommend for Interview"
    elif score >= 50:
        return "Average", "Consider for Interview"
    else:
        return "Not a Fit", "Do Not Recommend"

def analyze_resume(client, resume_text, job_description, nice_to_have_skills, candidate_name, job_title):
    """Analyze a single resume against job description using Groq with DETERMINISTIC scoring"""

    nice_to_have_text = ", ".join(nice_to_have_skills) if nice_to_have_skills else "None specified"

    prompt = f"""You are an expert technical recruiter. Analyze this resume against the job description.

SCORING RULES (Follow EXACTLY - calculate each component):
1. SKILLS MATCH (0-40 points):
   - List ALL required skills from JD
   - Count how many the candidate has
   - Score = (matched_skills / total_required_skills) * 40

2. EXPERIENCE (0-25 points):
   - Check years of experience vs required
   - Check if roles are relevant
   - Full points if meets/exceeds, partial if close

3. NICE-TO-HAVE (0-15 points):
   - Check for bonus skills: {nice_to_have_text}
   - 5 points per nice-to-have skill found (max 15)

4. EDUCATION (0-10 points):
   - Relevant degree = 10, Related field = 7, Any degree = 5

5. PRESENTATION (0-10 points):
   - Clear formatting, no errors = 10

FINAL SCORE = Sum of all components (0-100)

Return ONLY this JSON (no other text):
{{
    "score_breakdown": {{
        "skills_score": <0-40>,
        "experience_score": <0-25>,
        "nice_to_have_score": <0-15>,
        "education_score": <0-10>,
        "presentation_score": <0-10>
    }},
    "fit_score": <SUM of above scores>,
    "email": "<extracted email or 'Not provided'>",
    "phone": "<extracted phone or 'Not provided'>",
    "location": "<city/state or 'Not provided'>",
    "skills_matched": ["skill1", "skill2"],
    "skills_missing": ["skill1", "skill2"],
    "nice_to_have_matched": ["skill1"],
    "current_role": "<current job title or 'Not specified'>",
    "experience_years": <number>,
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1"],
    "summary": "<2 sentence evaluation>"
}}

JOB TITLE: {job_title}

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{job_description[:2000]}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,  # ZERO temperature for maximum consistency
            max_tokens=1200
        )
        result_text = response.choices[0].message.content.strip()

        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]

        result = json.loads(result_text)

        # VALIDATE and RECALCULATE score from breakdown
        breakdown = result.get('score_breakdown', {})
        calculated_score = (
            min(40, max(0, breakdown.get('skills_score', 0))) +
            min(25, max(0, breakdown.get('experience_score', 0))) +
            min(15, max(0, breakdown.get('nice_to_have_score', 0))) +
            min(10, max(0, breakdown.get('education_score', 0))) +
            min(10, max(0, breakdown.get('presentation_score', 0)))
        )

        # Use calculated score (not LLM's fit_score) for consistency
        result['fit_score'] = calculated_score

        # DETERMINISTIC verdict based on score
        verdict, recommendation = calculate_verdict_from_score(calculated_score)
        result['verdict'] = verdict
        result['recommendation'] = recommendation

        result['candidate_name'] = candidate_name
        result['job_title'] = job_title
        return result

    except json.JSONDecodeError as e:
        return {
            "candidate_name": candidate_name,
            "job_title": job_title,
            "fit_score": 0,
            "email": "Not provided",
            "phone": "Not provided",
            "location": "Not provided",
            "skills_matched": [],
            "skills_missing": [],
            "nice_to_have_matched": [],
            "current_role": "Unknown",
            "experience_years": 0,
            "strengths": [],
            "weaknesses": ["Could not parse resume"],
            "summary": "Error analyzing resume. Please try again.",
            "verdict": "Not a Fit",
            "recommendation": "Review Manually",
            "error": str(e)
        }
    except Exception as e:
        return {
            "candidate_name": candidate_name,
            "job_title": job_title,
            "fit_score": 0,
            "email": "Not provided",
            "phone": "Not provided",
            "location": "Not provided",
            "current_role": "Unknown",
            "skills_matched": [],
            "skills_missing": [],
            "nice_to_have_matched": [],
            "error": str(e),
            "verdict": "Not a Fit",
            "summary": f"API Error: {str(e)}"
        }

def get_category_color(category):
    colors = {
        "Best Fit": ("#7c3aed", "#ede9fe"),
        "Strong Fit": ("#059669", "#d1fae5"),
        "Average": ("#d97706", "#fef3c7"),
        "Not a Fit": ("#dc2626", "#fee2e2")
    }
    return colors.get(category, ("#6b7280", "#f3f4f6"))


def create_excel_report(results, categories, total_files, duplicates, job_title):
    """Create Excel report with all candidate data"""
    data = []
    for result in results:
        data.append({
            "Candidate Name": result.get('candidate_name', 'Unknown'),
            "Fit Score": result.get('fit_score', 0),
            "Verdict": result.get('verdict', 'N/A'),
            "Job Title Applied": job_title,
            "Current Role": result.get('current_role', 'N/A'),
            "Experience (Years)": result.get('experience_years', 0),
            "Location": result.get('location', 'Not provided'),
            "Email": result.get('email', 'Not provided'),
            "Phone": result.get('phone', 'Not provided'),
            "Skills Matched": ", ".join(result.get('skills_matched', [])),
            "Skills Missing": ", ".join(result.get('skills_missing', [])),
            "Nice-to-Have Skills": ", ".join(result.get('nice_to_have_matched', [])),
            "Strengths": ", ".join(result.get('strengths', [])),
            "Weaknesses": ", ".join(result.get('weaknesses', [])),
            "Summary": result.get('summary', 'N/A'),
            "Recommendation": result.get('recommendation', 'N/A')
        })

    df = pd.DataFrame(data)
    return df

def generate_pdf_report(results, job_title, categories, total_files, duplicates):
    """Generate PDF Report for Resume Analysis"""

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "AI Resume Shortlisting Report", ln=True, align="C")
    pdf.ln(10)

    # Job Title
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Job Title: {job_title}", ln=True)
    pdf.ln(5)

    # Summary Section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Processing Summary", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(200, 8, f"Total Files Uploaded: {total_files}", ln=True)
    pdf.cell(200, 8, f"Unique Resumes Analyzed: {len(results)}", ln=True)
    pdf.cell(200, 8, f"Duplicates Skipped: {duplicates}", ln=True)
    pdf.ln(8)

    # Category Breakdown
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Results Breakdown", ln=True)

    pdf.set_font("Arial", "", 11)
    for cat, cat_results in categories.items():
        pdf.cell(200, 8, f"{cat}: {len(cat_results)} candidates", ln=True)

    pdf.ln(10)

    # Top Candidates
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Top Candidates", ln=True)

    pdf.set_font("Arial", "", 10)
    for result in results[:10]:
        pdf.multi_cell(
            0,
            7,
            f"Name: {result.get('candidate_name')}\n"
            f"Score: {result.get('fit_score')}%\n"
            f"Role: {result.get('current_role')}\n"
            f"Location: {result.get('location')}\n"
            f"Recommendation: {result.get('recommendation')}\n"
            "----------------------------------------"
        )

    # ✅ Return PDF bytes
    return pdf.output(dest="S").encode("latin-1")

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="brand-container">
        <div class="brand-icon">🎯</div>
        <div>
            <div class="brand-text">HireSmartAI</div>
            <div class="brand-subtitle">Recruitment OS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nav-item active">
        <span>📊</span>
        <span>Dashboard</span>
    </div>
    <div class="nav-item">
        <span>🕐</span>
        <span>History</span>
    </div>
    <div class="nav-item">
        <span>⚙️</span>
        <span>Settings</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<p class="section-label">API Status</p>', unsafe_allow_html=True)
    if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
        st.markdown("""
        <div style="background: #d1fae5; padding: 0.5rem 1rem; border-radius: 8px; display: flex; align-items: center; gap: 8px;">
            <span style="color: #059669;">✓</span>
            <span style="color: #059669; font-size: 0.85rem;">API Key Configured</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #fee2e2; padding: 0.5rem 1rem; border-radius: 8px;">
            <span style="color: #dc2626; font-size: 0.85rem;">⚠️ API Key Missing</span>
            <p style="color: #dc2626; font-size: 0.75rem; margin: 0.25rem 0 0 0;">Add to .env file</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="section-label">Quick Links</p>', unsafe_allow_html=True)
    st.markdown("[🔗 Get Free API Key](https://console.groq.com)")

    st.markdown("---")
    st.markdown("""
    <div class="user-profile">
        <div class="user-avatar">HR</div>
        <div>
            <div class="user-name">HR Manager</div>
            <div class="user-plan">Pro Plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="main-header">New Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Upload resumes and define job context to find your perfect match.</p>', unsafe_allow_html=True)

# Two column layout for upload and JD
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-label">Source Files</p>', unsafe_allow_html=True)

    upload_method = st.radio(
        "Upload Method",
        ["📄 Upload Files", "📁 Select Folder"],
        horizontal=True,
        label_visibility="collapsed"
    )

    uploaded_files = []

    if upload_method == "📄 Upload Files":
        uploaded_files = st.file_uploader(
            "Upload Resumes",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            label_visibility="collapsed",
            help="Drag & drop PDF/DOCX files here (supports 250+ files)"
        )

        if uploaded_files:
            st.markdown(f"**{len(uploaded_files)} file(s) selected:**")
            file_chips = ""
            for f in uploaded_files[:3]:
                file_chips += f'<span class="file-chip">📄 {f.name}</span>'
            if len(uploaded_files) > 3:
                file_chips += f'<span class="file-chip">+{len(uploaded_files)-3} others</span>'
            st.markdown(file_chips, unsafe_allow_html=True)

    else:
        # Check if running on Streamlit Cloud
        is_cloud = os.getenv("STREAMLIT_SHARING_MODE") or "streamlit.app" in os.getenv("HOSTNAME", "") or not os.path.exists("C:\\")

        if is_cloud:
            st.warning("⚠️ **Folder selection only works when running locally.** On Streamlit Cloud, please use 'Upload Files' instead.")

        st.markdown("""
        <div style="background: #f9fafb; border: 2px dashed #ddd6fe; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
            <p style="color: #6b7280; font-size: 0.9rem; margin: 0;">
                📁 Enter the full path to your resumes folder (Local only)
            </p>
        </div>
        """, unsafe_allow_html=True)

        folder_path_input = st.text_input(
            "Folder Path",
            placeholder=r"C:\Users\HR\Resumes or /home/hr/resumes",
            label_visibility="collapsed",
            key="folder_path_input"
        )

        if folder_path_input:
            # Clean the path - remove quotes, extra spaces, and normalize
            folder_path_clean = folder_path_input.strip().strip('"').strip("'").strip()

            # Handle escaped backslashes (when copied from some sources)
            folder_path_clean = folder_path_clean.replace("\\\\", "\\")

            # Remove any invisible/control characters (keep printable + space)
            folder_path_clean = ''.join(c for c in folder_path_clean if c.isprintable())

            # Handle HTML entities that might come from browser copy
            folder_path_clean = folder_path_clean.replace("&amp;", "&")
            folder_path_clean = folder_path_clean.replace("%20", " ")

            # Remove leading/trailing whitespace again after all cleaning
            folder_path_clean = folder_path_clean.strip()

            # Debug info - show character codes for troubleshooting
            st.caption(f"📂 Path: `{folder_path_clean}` ({len(folder_path_clean)} chars)")

            try:
                folder_path = Path(folder_path_clean)
            except Exception as path_err:
                st.error(f"❌ Invalid path format: {path_err}")
                st.session_state.folder_pdf_paths = []
                folder_path = None

            if folder_path and folder_path.exists() and folder_path.is_dir():
                resume_files = (
                    list(folder_path.glob("*.pdf")) +
                    list(folder_path.glob("*.PDF")) +
                    list(folder_path.glob("*.docx")) +
                    list(folder_path.glob("*.DOCX")) +
                    list(folder_path.glob("*.doc")) +
                    list(folder_path.glob("*.DOC"))
                )

                if resume_files:
                    pdf_count = len([f for f in resume_files if f.suffix.lower() == '.pdf'])
                    docx_count = len([f for f in resume_files if f.suffix.lower() in ['.docx', '.doc']])
                    st.success(f"✅ Found {len(resume_files)} files ({pdf_count} PDF, {docx_count} DOCX/DOC)")
                    st.session_state.folder_pdf_paths = resume_files

                    file_chips = ""
                    for f in resume_files[:3]:
                        file_chips += f'<span class="file-chip">📄 {f.name}</span>'
                    if len(resume_files) > 3:
                        file_chips += f'<span class="file-chip">+{len(resume_files)-3} others</span>'
                    st.markdown(file_chips, unsafe_allow_html=True)

                    include_subfolders = st.checkbox("Include subfolders", value=False)
                    if include_subfolders:
                        resume_files = (
                            list(folder_path.rglob("*.pdf")) +
                            list(folder_path.rglob("*.PDF")) +
                            list(folder_path.rglob("*.docx")) +
                            list(folder_path.rglob("*.DOCX")) +
                            list(folder_path.rglob("*.doc")) +
                            list(folder_path.rglob("*.DOC"))
                        )
                        st.session_state.folder_pdf_paths = resume_files
                        st.info(f"📂 Total with subfolders: {len(resume_files)} files")
                else:
                    st.warning("⚠️ No PDF/DOCX files found in this folder")
                    st.session_state.folder_pdf_paths = []
            elif folder_path:
                # More helpful error message
                if not folder_path.exists():
                    st.error(f"❌ Path does not exist: `{folder_path_clean}`")
                    st.info("💡 Tip: Copy the path from Windows Explorer address bar")
                elif not folder_path.is_dir():
                    st.error(f"❌ Path is not a folder (it's a file): `{folder_path_clean}`")
                else:
                    st.error("❌ Folder not found. Please check the path.")
                st.session_state.folder_pdf_paths = []

with col2:
    st.markdown('<p class="section-label">Job Description</p>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description",
        height=150,
        placeholder="Enter the job description here...\n\nInclude:\n- Role title\n- Required skills\n- Experience requirements\n- Responsibilities",
        label_visibility="collapsed"
    )

    # Nice to Have Skills input (Feature 1)
    st.markdown('<p class="section-label">Nice-to-Have Skills (Optional)</p>', unsafe_allow_html=True)
    nice_to_have_input = st.text_input(
        "Nice-to-Have Skills",
        placeholder="e.g., AWS, Docker, Kubernetes, GraphQL (comma-separated)",
        label_visibility="collapsed"
    )
    nice_to_have_skills = [s.strip() for s in nice_to_have_input.split(",") if s.strip()] if nice_to_have_input else []

# Feature 6: Suggest Keywords Button
if job_description and GROQ_API_KEY:
    col_kw1, col_kw2, col_kw3 = st.columns([1, 1, 1])
    with col_kw2:
        if st.button("🔍 Extract Keywords from JD", use_container_width=True):
            with st.spinner("Analyzing job description..."):
                client = Groq(api_key=GROQ_API_KEY)
                keywords = extract_keywords_from_jd(client, job_description)
                st.session_state.suggested_keywords = keywords
                st.session_state.job_title = keywords.get('job_title', '')

# Display suggested keywords
if st.session_state.suggested_keywords:
    keywords = st.session_state.suggested_keywords
    st.markdown("---")
    st.markdown("### 📋 Suggested Keywords from JD")

    kw_col1, kw_col2 = st.columns(2)

    with kw_col1:
        if keywords.get('job_title'):
            st.markdown(f"**Job Title:** {keywords['job_title']}")
        if keywords.get('experience_required'):
            st.markdown(f"**Experience Required:** {keywords['experience_required']}")

        if keywords.get('must_have_skills'):
            st.markdown("**Must-Have Skills:**")
            skills_html = "".join([f'<span class="keyword-tag">{s}</span>' for s in keywords['must_have_skills']])
            st.markdown(skills_html, unsafe_allow_html=True)

    with kw_col2:
        if keywords.get('nice_to_have_skills'):
            st.markdown("**Nice-to-Have Skills:**")
            skills_html = "".join([f'<span class="keyword-tag">{s}</span>' for s in keywords['nice_to_have_skills']])
            st.markdown(skills_html, unsafe_allow_html=True)

        if keywords.get('technologies'):
            st.markdown("**Technologies:**")
            tech_html = "".join([f'<span class="keyword-tag">{t}</span>' for t in keywords['technologies']])
            st.markdown(tech_html, unsafe_allow_html=True)

# Analyze button
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    analyze_clicked = st.button("✨ Analyze Candidates", use_container_width=True)

# Process analysis
if analyze_clicked:
    files_to_process = []
    use_folder = upload_method == "📁 Select Folder"

    if use_folder:
        folder_paths = st.session_state.get('folder_pdf_paths', [])
        files_to_process = folder_paths
    else:
        files_to_process = uploaded_files if uploaded_files else []

    # Get job title
    job_title = st.session_state.get('job_title', '')
    if not job_title and st.session_state.suggested_keywords:
        job_title = st.session_state.suggested_keywords.get('job_title', 'Not specified')
    if not job_title:
        job_title = "Not specified"

    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        st.error("⚠️ API key not configured. Please add your Groq API key to the .env file")
    elif not job_description:
        st.error("⚠️ Please enter a job description")
    elif not files_to_process:
        st.error("⚠️ Please upload resumes or select a folder with PDF/DOCX files")
    else:
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            time_estimate = st.empty()
            duplicate_info = st.empty()

            total = len(files_to_process)

            # Parallel processing settings
            MAX_WORKERS = min(5, total)  # Limit to 5 parallel requests (Groq rate limit friendly)

            if total > 10:
                est_time = (total // MAX_WORKERS) * 2  # Much faster with parallel
                time_estimate.info(f"⚡ Parallel processing: ~{est_time // 60}m {est_time % 60}s for {total} resumes ({MAX_WORKERS} parallel workers)")

            # Step 1: Extract text from all files first (fast, can be parallelized)
            status_text.text("📄 Extracting text from resumes...")

            extracted_data = []
            seen_hashes = {}
            duplicates_skipped = 0

            for idx, file_item in enumerate(files_to_process):
                if use_folder:
                    file_path = file_item
                    file_name = file_path.name
                    file_ext = file_path.suffix.lower()

                    if file_ext == '.pdf':
                        resume_text = extract_text_from_pdf_path(file_path)
                    elif file_ext in ['.docx', '.doc']:
                        resume_text = extract_text_from_docx_path(file_path)
                    else:
                        resume_text = "Error: Unsupported file format"
                else:
                    file_name = file_item.name
                    file_ext = Path(file_name).suffix.lower()

                    if file_ext == '.pdf':
                        resume_text = extract_text_from_pdf(file_item)
                    elif file_ext in ['.docx', '.doc']:
                        resume_text = extract_text_from_docx(file_item)
                    else:
                        resume_text = "Error: Unsupported file format"

                clean_name = file_name
                for ext in ['.pdf', '.PDF', '.docx', '.DOCX', '.doc', '.DOC']:
                    clean_name = clean_name.replace(ext, '')

                if resume_text.startswith("Error"):
                    extracted_data.append({
                        "candidate_name": clean_name,
                        "job_title": job_title,
                        "fit_score": 0,
                        "error": resume_text,
                        "verdict": "Error",
                        "current_role": "Unknown",
                        "location": "Not provided",
                        "skills_matched": [],
                        "skills_missing": [],
                        "nice_to_have_matched": [],
                        "summary": "Could not extract text from file",
                        "is_error": True
                    })
                else:
                    content_hash = get_content_hash(resume_text)

                    if content_hash in seen_hashes:
                        duplicates_skipped += 1
                    else:
                        seen_hashes[content_hash] = file_name
                        extracted_data.append({
                            "resume_text": resume_text,
                            "candidate_name": clean_name,
                            "is_error": False
                        })

                progress_bar.progress((idx + 1) / total * 0.3)  # 30% for extraction

            if duplicates_skipped > 0:
                duplicate_info.success(f"✅ Found {duplicates_skipped} duplicate(s) - will be skipped")

            # Step 2: Parallel API calls for analysis
            status_text.text(f"🚀 Analyzing {len([d for d in extracted_data if not d.get('is_error')])} resumes in parallel...")

            results = []
            resumes_to_analyze = [d for d in extracted_data if not d.get('is_error')]
            error_results = [d for d in extracted_data if d.get('is_error')]

            # Add error results directly
            for err in error_results:
                del err['is_error']
                results.append(err)

            # Thread-safe counter for progress
            completed_count = [0]
            lock = threading.Lock()

            def analyze_single_resume(data):
                """Analyze a single resume - called in parallel"""
                client = Groq(api_key=GROQ_API_KEY)  # Each thread gets its own client
                result = analyze_resume(
                    client,
                    data['resume_text'],
                    job_description,
                    nice_to_have_skills,
                    data['candidate_name'],
                    job_title
                )

                with lock:
                    completed_count[0] += 1

                return result

            # Parallel execution
            if resumes_to_analyze:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    futures = {executor.submit(analyze_single_resume, data): data for data in resumes_to_analyze}

                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            results.append(result)

                            # Update progress (30% extraction + 70% analysis)
                            progress = 0.3 + (completed_count[0] / len(resumes_to_analyze)) * 0.7
                            progress_bar.progress(progress)
                            status_text.text(f"🔍 Analyzed {completed_count[0]}/{len(resumes_to_analyze)} resumes...")

                        except Exception as e:
                            data = futures[future]
                            results.append({
                                "candidate_name": data['candidate_name'],
                                "job_title": job_title,
                                "fit_score": 0,
                                "error": str(e),
                                "verdict": "Error",
                                "current_role": "Unknown",
                                "location": "Not provided",
                                "skills_matched": [],
                                "skills_missing": [],
                                "nice_to_have_matched": [],
                                "summary": f"Error: {str(e)}"
                            })

            progress_bar.progress(1.0)

            results.sort(key=lambda x: x.get('fit_score', 0), reverse=True)
            st.session_state.results = results
            st.session_state.analyzed = True
            st.session_state.job_title = job_title

            status_text.empty()
            progress_bar.empty()
            time_estimate.empty()

            st.session_state.duplicates_count = duplicates_skipped
            st.session_state.total_files_processed = total

            if duplicates_skipped > 0:
                duplicate_info.success(f"✅ Processed {len(results)} unique resumes. Skipped {duplicates_skipped} duplicate(s).")
            else:
                duplicate_info.empty()

            st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ✅ Display results ONLY after analysis
if st.session_state.analyzed and st.session_state.results:

    results = st.session_state.results
    job_title = st.session_state.get("job_title", "Not specified")

    st.markdown("---")

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
                padding: 1rem 1.5rem;
                border-radius: 12px;
                margin-bottom: 1rem;">
        <div style="color: white; font-size: 0.8rem;">Analyzing for Position</div>
        <div style="color: white; font-size: 1.25rem; font-weight: 700;">
            {job_title}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ Filtering UI
    st.markdown("### 🔍 Filter Results")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        min_score = st.slider("Minimum Score", 0, 100, 0)

    with filter_col2:
        filter_verdict = st.multiselect(
            "Verdict",
            ["Best Fit", "Strong Fit", "Average", "Not a Fit"],
            default=["Best Fit", "Strong Fit", "Average", "Not a Fit"]
        )

    # ✅ Apply filters safely
    filtered_results = [
        r for r in results
        if r.get("fit_score", 0) >= min_score
        and r.get("verdict", "Not a Fit") in filter_verdict
    ]

    # ✅ Stats
    total_files = st.session_state.get("total_files_processed", len(results))
    duplicates = st.session_state.get("duplicates_count", 0)

    # ✅ Categorize results
    categories = {
        "Best Fit": [],
        "Strong Fit": [],
        "Average": [],
        "Not a Fit": []
    }

    for res in filtered_results:
        verdict = res.get("verdict", "Not a Fit")

        if "Best" in verdict:
            categories["Best Fit"].append(res)
        elif "Strong" in verdict:
            categories["Strong Fit"].append(res)
        elif "Average" in verdict:
            categories["Average"].append(res)
        else:
            categories["Not a Fit"].append(res)

    # ✅ Show candidates
    for category, category_results in categories.items():

        if not category_results:
            continue

        st.markdown(f"## ✅ {category} ({len(category_results)})")

        for candidate in category_results:

            st.markdown(f"""
            **👤 {candidate.get("candidate_name","Unknown")}**  
            ✅ Score: {candidate.get("fit_score",0)}%  
            📍 Location: {candidate.get("location","N/A")}  
            💼 Role: {candidate.get("current_role","N/A")}  
            🎯 Recommendation: {candidate.get("recommendation","N/A")}
            """)
            st.markdown("---")

    # ✅ ---------------- DOWNLOAD REPORTS SECTION ----------------
    st.markdown("## 📥 Download Reports")

    download_col1, download_col2, download_col3 = st.columns(3)

    # ✅ Create DataFrame safely
    df = create_excel_report(results, categories, total_files, duplicates, job_title)

    # ✅ CSV Download
    with download_col1:
        st.download_button(
            "📄 Download CSV",
            df.to_csv(index=False),
            "resume_analysis_report.csv",
            "text/csv"
        )

    # ✅ Excel Download
    with download_col2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        excel_buffer.seek(0)

        st.download_button(
            "📊 Download Excel",
            excel_buffer,
            "resume_analysis_report.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # ✅ PDF Download
    with download_col3:
        pdf_bytes = generate_pdf_report(
            results,
            job_title,
            categories,
            total_files,
            duplicates
        )

        st.download_button(
            "📑 Download PDF",
            pdf_bytes,
            "resume_analysis_report.pdf",
            "application/pdf"
        )


# ✅ Footer ALWAYS outside block
st.markdown("""
<div style="text-align: center; padding: 2rem;
            color: #9ca3af; font-size: 0.85rem;">
    Built for Mamsys Hackathon 2025 | Powered by Groq AI
</div>
""", unsafe_allow_html=True)

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

def analyze_resume(client, resume_text, job_description, nice_to_have_skills, candidate_name, job_title):
    """Analyze a single resume against job description using Groq with improved scoring"""

    nice_to_have_text = ", ".join(nice_to_have_skills) if nice_to_have_skills else "None specified"

    prompt = f"""You are an expert technical recruiter with 15 years of experience.
Evaluate the following resume against the job description with STRICT and ACCURATE scoring.

SCORING CRITERIA (Be precise and fair):
- Must-Have Skills Match: 40% weight (each missing critical skill = -10 points)
- Experience Relevance: 25% weight (years + role alignment)
- Nice-to-Have Skills: 15% weight (bonus points for having these)
- Education/Certifications: 10% weight
- Overall Presentation: 10% weight

IMPORTANT: Return ONLY valid JSON, no other text. Use this exact structure:
{{
    "fit_score": <number 0-100 based on above criteria>,
    "email": "<extracted email or 'Not provided'>",
    "phone": "<extracted phone number or 'Not provided'>",
    "location": "<extracted city/location or 'Not provided'>",
    "skills_matched": ["skill1", "skill2", "skill3"],
    "skills_missing": ["skill1", "skill2"],
    "nice_to_have_matched": ["skill1", "skill2"],
    "current_role": "<extracted current job title or 'Not specified'>",
    "experience_years": <number or 0>,
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2"],
    "summary": "<2-3 sentence evaluation>",
    "verdict": "<Best Fit OR Strong Fit OR Average OR Not a Fit>",
    "recommendation": "<Recommend for Interview OR Consider for Interview OR Do Not Recommend>",
    "score_breakdown": {{
        "skills_score": <0-40>,
        "experience_score": <0-25>,
        "nice_to_have_score": <0-15>,
        "education_score": <0-10>,
        "presentation_score": <0-10>
    }}
}}

Verdict Guidelines (STRICT):
- Best Fit (85-100): Exceeds requirements, has most must-have skills + nice-to-have
- Strong Fit (70-84): Meets most requirements, minor gaps
- Average (50-69): Meets some requirements, needs training
- Not a Fit (0-49): Missing critical requirements

JOB TITLE: {job_title}

NICE-TO-HAVE SKILLS: {nice_to_have_text}

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{job_description[:2000]}

Return ONLY the JSON object, nothing else."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1200
        )
        result_text = response.choices[0].message.content.strip()

        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]

        result = json.loads(result_text)
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
            "verdict": "Error",
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
        st.markdown("""
        <div style="background: #f9fafb; border: 2px dashed #ddd6fe; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
            <p style="color: #6b7280; font-size: 0.9rem; margin: 0;">
                📁 Enter the full path to your resumes folder
            </p>
        </div>
        """, unsafe_allow_html=True)

        folder_path = st.text_input(
            "Folder Path",
            placeholder=r"C:\Users\HR\Resumes or /home/hr/resumes",
            label_visibility="collapsed"
        )

        if folder_path:
            folder_path = Path(folder_path)
            if folder_path.exists() and folder_path.is_dir():
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
            client = Groq(api_key=GROQ_API_KEY)
            progress_bar = st.progress(0)
            status_text = st.empty()
            time_estimate = st.empty()
            duplicate_info = st.empty()

            results = []
            seen_hashes = {}
            duplicates_skipped = 0
            total = len(files_to_process)

            if total > 10:
                est_time = total * 2
                time_estimate.info(f"⏱️ Estimated time: {est_time // 60}m {est_time % 60}s for {total} resumes")

            for idx, file_item in enumerate(files_to_process):
                if use_folder:
                    file_path = file_item
                    file_name = file_path.name
                    file_ext = file_path.suffix.lower()
                    status_text.text(f"🔍 Analyzing {file_name}... ({idx + 1}/{total})")

                    if file_ext == '.pdf':
                        resume_text = extract_text_from_pdf_path(file_path)
                    elif file_ext in ['.docx', '.doc']:
                        resume_text = extract_text_from_docx_path(file_path)
                    else:
                        resume_text = "Error: Unsupported file format"
                else:
                    file_name = file_item.name
                    file_ext = Path(file_name).suffix.lower()
                    status_text.text(f"🔍 Analyzing {file_name}... ({idx + 1}/{total})")

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
                    results.append({
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
                        "summary": "Could not extract text from file"
                    })
                else:
                    content_hash = get_content_hash(resume_text)

                    if content_hash in seen_hashes:
                        duplicates_skipped += 1
                        duplicate_info.warning(f"⚠️ Skipped {duplicates_skipped} duplicate(s) - '{file_name}' same as '{seen_hashes[content_hash]}'")
                    else:
                        seen_hashes[content_hash] = file_name
                        result = analyze_resume(
                            client,
                            resume_text,
                            job_description,
                            nice_to_have_skills,
                            clean_name,
                            job_title
                        )
                        results.append(result)

                progress_bar.progress((idx + 1) / total)

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

# Display results
if st.session_state.analyzed and st.session_state.results:
    results = st.session_state.results
    job_title = st.session_state.get('job_title', 'Not specified')

    st.markdown("---")

    # Feature 3: Job Designation Display
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
        <div style="color: white; font-size: 0.8rem; opacity: 0.9;">Analyzing for Position</div>
        <div style="color: white; font-size: 1.25rem; font-weight: 700;">{job_title}</div>
    </div>
    """, unsafe_allow_html=True)

    # Feature 7: Filter Section
    st.markdown("### 🔍 Filter Results")
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        filter_verdict = st.multiselect(
            "Verdict",
            ["Best Fit", "Strong Fit", "Average", "Not a Fit"],
            default=["Best Fit", "Strong Fit", "Average", "Not a Fit"]
        )

    with filter_col2:
        min_score = st.slider("Minimum Score", 0, 100, 0)

    with filter_col3:
        # Get unique locations
        all_locations = list(set([r.get('location', 'Not provided') for r in results]))
        filter_location = st.multiselect("Location", all_locations, default=all_locations)

    with filter_col4:
        # Get all skills for filtering
        all_skills = set()
        for r in results:
            all_skills.update(r.get('skills_matched', []))
        filter_skills = st.multiselect("Has Skill", list(all_skills))

    # Apply filters
    filtered_results = [
        r for r in results
        if r.get('verdict', 'Not a Fit') in filter_verdict
        and r.get('fit_score', 0) >= min_score
        and r.get('location', 'Not provided') in filter_location
        and (not filter_skills or any(s in r.get('skills_matched', []) for s in filter_skills))
    ]

    st.markdown(f"""
    <div class="results-header">
        <div class="results-title">
            Results <span class="match-count">{len(filtered_results)} of {len(results)} Candidates</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_files = st.session_state.get('total_files_processed', len(results))
    duplicates = st.session_state.get('duplicates_count', 0)

    # Categorize filtered results
    categories = {
        "Best Fit": [],
        "Strong Fit": [],
        "Average": [],
        "Not a Fit": []
    }

    for result in filtered_results:
        verdict = result.get('verdict', 'Not a Fit')
        if "Best" in verdict:
            categories["Best Fit"].append(result)
        elif "Strong" in verdict:
            categories["Strong Fit"].append(result)
        elif "Average" in verdict:
            categories["Average"].append(result)
        else:
            categories["Not a Fit"].append(result)

    # Summary metrics - 5 columns including duplicates
    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    with col_m1:
        st.markdown(f"""
        <div style="background: #ede9fe; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #7c3aed;">{len(categories['Best Fit'])}</div>
            <div style="font-size: 0.8rem; color: #7c3aed;">Best Fit</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div style="background: #d1fae5; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #059669;">{len(categories['Strong Fit'])}</div>
            <div style="font-size: 0.8rem; color: #059669;">Strong Fit</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div style="background: #fef3c7; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #d97706;">{len(categories['Average'])}</div>
            <div style="font-size: 0.8rem; color: #d97706;">Average</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div style="background: #fee2e2; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #dc2626;">{len(categories['Not a Fit'])}</div>
            <div style="font-size: 0.8rem; color: #dc2626;">Not a Fit</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m5:
        st.markdown(f"""
        <div style="background: #e0e7ff; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #4338ca;">{duplicates}</div>
            <div style="font-size: 0.8rem; color: #4338ca;">Duplicates Skipped</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Display each category
    for category, category_results in categories.items():
        if not category_results:
            continue

        text_color, bg_color = get_category_color(category)

        st.markdown(f"""
        <div class="category-header">
            <span class="category-title">{category}</span>
            <span class="category-count" style="background: {bg_color}; color: {text_color};">
                {len(category_results)} candidate{'s' if len(category_results) != 1 else ''}
            </span>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        for idx, result in enumerate(category_results):
            col_idx = idx % 3

            score = result.get('fit_score', 0)
            name = result.get('candidate_name', 'Unknown')
            role = result.get('current_role', 'Not specified')
            location = result.get('location', 'Not provided')
            email = result.get('email', 'Not provided')
            phone = result.get('phone', 'Not provided')
            summary = result.get('summary', 'N/A')
            matched = result.get('skills_matched', [])
            missing = result.get('skills_missing', [])
            nice_matched = result.get('nice_to_have_matched', [])
            strengths = result.get('strengths', [])
            weaknesses = result.get('weaknesses', [])
            recommendation = result.get('recommendation', 'N/A')

            if score >= 85:
                score_bg = "#7c3aed"
            elif score >= 70:
                score_bg = "#059669"
            elif score >= 50:
                score_bg = "#d97706"
            else:
                score_bg = "#dc2626"

            with cols[col_idx]:
                # Candidate card with Location (Feature 2)
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 1rem; border: 1px solid #e5e7eb; border-left: 4px solid {score_bg}; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 50px; height: 50px; border-radius: 50%; background: {score_bg}; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 0.9rem;">{score}%</div>
                        <div style="flex: 1; min-width: 0;">
                            <div style="font-weight: 600; color: #1f2937; font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{name}</div>
                            <div style="font-size: 0.75rem; color: #6b7280; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{role}</div>
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem; font-size: 0.7rem; color: #6b7280;">
                        <div>📍 {location}</div>
                        <div>📧 {email if email != 'Not provided' else 'N/A'}</div>
                        <div>📱 {phone if phone != 'Not provided' else 'N/A'}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("📊 View Analysis"):
                    # Feature 4: Highlighted Skills with colored tags
                    st.caption("**Skills Analysis**")

                    if matched:
                        matched_html = "".join([f'<span class="skill-matched">✓ {s}</span>' for s in matched[:6]])
                        st.markdown(f"**Matched:** {matched_html}", unsafe_allow_html=True)

                    if missing:
                        missing_html = "".join([f'<span class="skill-missing">✗ {s}</span>' for s in missing[:6]])
                        st.markdown(f"**Missing:** {missing_html}", unsafe_allow_html=True)

                    if nice_matched:
                        nice_html = "".join([f'<span class="skill-nice">★ {s}</span>' for s in nice_matched[:4]])
                        st.markdown(f"**Nice-to-Have:** {nice_html}", unsafe_allow_html=True)

                    st.markdown("---")

                    sw1, sw2 = st.columns(2)
                    with sw1:
                        st.caption("💪 **Strengths**")
                        if strengths:
                            for s in strengths[:3]:
                                st.write(f"• {s}")
                        else:
                            st.write("None")
                    with sw2:
                        st.caption("⚠️ **Concerns**")
                        if weaknesses:
                            for w in weaknesses[:3]:
                                st.write(f"• {w}")
                        else:
                            st.write("None")

                    st.caption("📝 **Summary**")
                    st.write(summary)
                    st.info(f"🎯 {recommendation}")

        st.markdown("<br>", unsafe_allow_html=True)

    # Feature 5: Download reports section
    st.markdown("---")
    st.markdown("### 📥 Download Reports")

    download_col1, download_col2, download_col3 = st.columns(3)

    # Create DataFrame for Excel/CSV
    df = create_excel_report(results, categories, total_files, duplicates, job_title)

    with download_col1:
        # CSV Download
        csv_data = df.to_csv(index=False)
        st.download_button(
            "📄 Download CSV",
            csv_data,
            "resume_analysis_report.csv",
            "text/csv",
            use_container_width=True
        )

    with download_col2:
        # Excel Download
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='All Candidates')

            # Add separate sheets for each category
            for cat_name, cat_results in categories.items():
                if cat_results:
                    cat_df = create_excel_report(cat_results, {}, 0, 0, job_title)
                    cat_df.to_excel(writer, index=False, sheet_name=cat_name[:31])

        excel_buffer.seek(0)
        st.download_button(
            "📊 Download Excel",
            excel_buffer,
            "resume_analysis_report.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with download_col3:
        # Text Report
        report_text = "AI RESUME SHORTLISTING REPORT\n" + "="*50 + "\n\n"
        report_text += f"JOB TITLE: {job_title}\n\n"
        report_text += "PROCESSING SUMMARY\n"
        report_text += f"Total Files Uploaded: {total_files}\n"
        report_text += f"Unique Resumes Analyzed: {len(results)}\n"
        report_text += f"Duplicates Skipped: {duplicates}\n\n"
        report_text += "RESULTS BREAKDOWN\n"
        report_text += f"Best Fit: {len(categories['Best Fit'])}\n"
        report_text += f"Strong Fit: {len(categories['Strong Fit'])}\n"
        report_text += f"Average: {len(categories['Average'])}\n"
        report_text += f"Not a Fit: {len(categories['Not a Fit'])}\n\n"
        report_text += "="*50 + "\n\n"

        for category, category_results in categories.items():
            if category_results:
                report_text += f"\n--- {category.upper()} ---\n\n"
                for result in category_results:
                    report_text += f"Name: {result.get('candidate_name', 'Unknown')}\n"
                    report_text += f"Score: {result.get('fit_score', 0)}/100\n"
                    report_text += f"Role: {result.get('current_role', 'N/A')}\n"
                    report_text += f"Location: {result.get('location', 'N/A')}\n"
                    report_text += f"Email: {result.get('email', 'N/A')}\n"
                    report_text += f"Phone: {result.get('phone', 'N/A')}\n"
                    report_text += f"Matched Skills: {', '.join(result.get('skills_matched', []))}\n"
                    report_text += f"Missing Skills: {', '.join(result.get('skills_missing', []))}\n"
                    report_text += f"Nice-to-Have: {', '.join(result.get('nice_to_have_matched', []))}\n"
                    report_text += f"Summary: {result.get('summary', 'N/A')}\n"
                    report_text += f"Recommendation: {result.get('recommendation', 'N/A')}\n"
                    report_text += "-"*30 + "\n\n"

        st.download_button(
            "📝 Download TXT",
            report_text,
            "resume_analysis_report.txt",
            "text/plain",
            use_container_width=True
        )

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #9ca3af; font-size: 0.85rem;">
    Built for Mamsys Hackathon 2025 | Powered by Groq AI
</div>
""", unsafe_allow_html=True)

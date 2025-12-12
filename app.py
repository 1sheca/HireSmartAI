import streamlit as st
import json
import re
import os
from pathlib import Path
from groq import Groq
import PyPDF2
import io
from dotenv import load_dotenv

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

    /* Upload area */
    .upload-area {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        text-align: center;
    }

    .upload-icon {
        width: 60px;
        height: 60px;
        background: #f3f4f6;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        font-size: 24px;
    }

    .upload-title {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }

    .upload-subtitle {
        color: #9ca3af;
        font-size: 0.85rem;
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

    /* Analyze button */
    .analyze-btn {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.25);
    }

    .analyze-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
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

    /* Candidate card */
    .candidate-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #f3f4f6;
        transition: all 0.2s;
        height: 100%;
    }

    .candidate-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }

    /* Score circle */
    .score-circle {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        font-weight: 700;
        margin-right: 1rem;
    }

    .score-high {
        background: conic-gradient(#8b5cf6 var(--score-percent), #e5e7eb var(--score-percent));
        position: relative;
    }

    .score-inner {
        width: 54px;
        height: 54px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #1f2937;
    }

    /* Badges */
    .badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    .badge-best {
        background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
        color: #7c3aed;
        border: 1px solid #c4b5fd;
    }

    .badge-strong {
        background: #dcfce7;
        color: #166534;
    }

    .badge-average {
        background: #fef3c7;
        color: #92400e;
    }

    .badge-weak {
        background: #fee2e2;
        color: #991b1b;
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

    /* Small candidate placards */
    .candidate-placard {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        transition: all 0.2s;
        margin-bottom: 0.75rem;
    }

    .candidate-placard:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: #ddd6fe;
    }

    .placard-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }

    .placard-score {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.95rem;
        color: white;
    }

    .placard-info {
        flex: 1;
        margin-left: 0.75rem;
    }

    .placard-name {
        font-weight: 600;
        color: #1f2937;
        font-size: 0.95rem;
    }

    .placard-role {
        font-size: 0.8rem;
        color: #6b7280;
    }

    .placard-contact {
        display: flex;
        gap: 1rem;
        margin-top: 0.5rem;
        font-size: 0.75rem;
        color: #6b7280;
    }

    .placard-contact span {
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Skill tags */
    .skill-tag {
        display: inline-block;
        background: #f3f4f6;
        color: #374151;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8rem;
        margin: 0.2rem;
        border: 1px solid #e5e7eb;
    }

    .skill-tag-matched {
        background: #ede9fe;
        color: #7c3aed;
        border-color: #ddd6fe;
    }

    /* Candidate name and info */
    .candidate-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }

    .candidate-role {
        font-size: 0.85rem;
        color: #6b7280;
    }

    /* Summary text */
    .candidate-summary {
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 1rem 0;
    }

    /* View full analysis link */
    .view-link {
        color: #7c3aed;
        font-weight: 500;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 4px;
        cursor: pointer;
        text-decoration: none;
    }

    .view-link:hover {
        text-decoration: underline;
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

    /* Auto-generate button */
    .auto-gen-btn {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
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

    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f9fafb;
        border-radius: 8px;
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

    /* Card container for results */
    .results-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
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

def analyze_resume(client, resume_text, job_description, candidate_name):
    """Analyze a single resume against job description using Groq"""
    prompt = f"""You are an expert technical recruiter with 15 years of experience.
Evaluate the following resume against the job description.

IMPORTANT: Return ONLY valid JSON, no other text. Use this exact structure:
{{
    "fit_score": <number 0-100>,
    "email": "<extracted email or 'Not provided'>",
    "phone": "<extracted phone number or 'Not provided'>",
    "skills_matched": ["skill1", "skill2", "skill3"],
    "skills_missing": ["skill1", "skill2"],
    "current_role": "<extracted current job title or 'Not specified'>",
    "experience_years": <number or 0>,
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2"],
    "summary": "<2-3 sentence evaluation>",
    "verdict": "<Best Fit OR Strong Fit OR Average OR Not a Fit>",
    "recommendation": "<Recommend for Interview OR Consider for Interview OR Do Not Recommend>"
}}

Verdict Guidelines:
- Best Fit (90-100): Exceeds all requirements, ideal candidate
- Strong Fit (70-89): Meets most requirements, good candidate
- Average (50-69): Meets some requirements, potential with training
- Not a Fit (0-49): Does not meet key requirements

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{job_description[:2000]}

Return ONLY the JSON object, nothing else."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )
        result_text = response.choices[0].message.content.strip()

        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]

        result = json.loads(result_text)
        result['candidate_name'] = candidate_name
        return result
    except json.JSONDecodeError as e:
        return {
            "candidate_name": candidate_name,
            "fit_score": 0,
            "email": "Not provided",
            "phone": "Not provided",
            "skills_matched": [],
            "skills_missing": [],
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
            "fit_score": 0,
            "email": "Not provided",
            "phone": "Not provided",
            "current_role": "Unknown",
            "skills_matched": [],
            "skills_missing": [],
            "error": str(e),
            "verdict": "Error",
            "summary": f"API Error: {str(e)}"
        }

def get_badge_class(verdict):
    if "Best" in verdict:
        return "badge-best"
    elif "Strong" in verdict:
        return "badge-strong"
    elif "Average" in verdict:
        return "badge-average"
    else:
        return "badge-weak"

def get_category_color(category):
    colors = {
        "Best Fit": ("#7c3aed", "#ede9fe"),
        "Strong Fit": ("#059669", "#d1fae5"),
        "Average": ("#d97706", "#fef3c7"),
        "Not a Fit": ("#dc2626", "#fee2e2")
    }
    return colors.get(category, ("#6b7280", "#f3f4f6"))

# Sidebar
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="brand-container">
        <div class="brand-icon">🎯</div>
        <div>
            <div class="brand-text">HireSmartAI</div>
            <div class="brand-subtitle">Recruitment OS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
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

    # API Status
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

    # Help section
    st.markdown('<p class="section-label">Quick Links</p>', unsafe_allow_html=True)
    st.markdown("[🔗 Get Free API Key](https://console.groq.com)")

    # User profile at bottom
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

    # Upload method selection
    upload_method = st.radio(
        "Upload Method",
        ["📄 Upload Files", "📁 Select Folder"],
        horizontal=True,
        label_visibility="collapsed"
    )

    uploaded_files = []
    folder_files = []

    if upload_method == "📄 Upload Files":
        uploaded_files = st.file_uploader(
            "Upload Resumes",
            type=['pdf'],
            accept_multiple_files=True,
            label_visibility="collapsed",
            help="Drag & drop PDF files here (supports 250+ files)"
        )

        if uploaded_files:
            st.markdown(f"**{len(uploaded_files)} file(s) selected:**")
            file_chips = ""
            for f in uploaded_files[:3]:
                file_chips += f'<span class="file-chip">📄 {f.name}</span>'
            if len(uploaded_files) > 3:
                file_chips += f'<span class="file-chip">+{len(uploaded_files)-3} others</span>'
            st.markdown(file_chips, unsafe_allow_html=True)

    else:  # Folder selection
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
                pdf_files = list(folder_path.glob("*.pdf")) + list(folder_path.glob("*.PDF"))

                if pdf_files:
                    st.success(f"✅ Found {len(pdf_files)} PDF files in folder")

                    # Store folder files info in session state
                    st.session_state.folder_pdf_paths = pdf_files

                    # Show preview
                    file_chips = ""
                    for f in pdf_files[:3]:
                        file_chips += f'<span class="file-chip">📄 {f.name}</span>'
                    if len(pdf_files) > 3:
                        file_chips += f'<span class="file-chip">+{len(pdf_files)-3} others</span>'
                    st.markdown(file_chips, unsafe_allow_html=True)

                    # Option to include subfolders
                    include_subfolders = st.checkbox("Include subfolders", value=False)
                    if include_subfolders:
                        pdf_files = list(folder_path.rglob("*.pdf")) + list(folder_path.rglob("*.PDF"))
                        st.session_state.folder_pdf_paths = pdf_files
                        st.info(f"📂 Total with subfolders: {len(pdf_files)} PDFs")
                else:
                    st.warning("⚠️ No PDF files found in this folder")
                    st.session_state.folder_pdf_paths = []
            else:
                st.error("❌ Folder not found. Please check the path.")
                st.session_state.folder_pdf_paths = []

with col2:
    st.markdown('<p class="section-label">Job Description</p>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description",
        height=200,
        placeholder="Enter the job description here...\n\nInclude:\n- Role title\n- Required skills\n- Experience requirements\n- Responsibilities",
        label_visibility="collapsed"
    )

# Analyze button
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    analyze_clicked = st.button("✨ Analyze Candidates", use_container_width=True)

# Process analysis
if analyze_clicked:
    # Determine which files to process
    files_to_process = []
    use_folder = upload_method == "📁 Select Folder"

    if use_folder:
        folder_paths = st.session_state.get('folder_pdf_paths', [])
        files_to_process = folder_paths
    else:
        files_to_process = uploaded_files if uploaded_files else []

    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        st.error("⚠️ API key not configured. Please add your Groq API key to the .env file")
    elif not job_description:
        st.error("⚠️ Please enter a job description")
    elif not files_to_process:
        st.error("⚠️ Please upload resumes or select a folder with PDFs")
    else:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            progress_bar = st.progress(0)
            status_text = st.empty()
            time_estimate = st.empty()

            results = []
            total = len(files_to_process)

            # Show estimate for large batches
            if total > 10:
                est_time = total * 2  # ~2 seconds per resume
                time_estimate.info(f"⏱️ Estimated time: {est_time // 60}m {est_time % 60}s for {total} resumes")

            for idx, pdf_item in enumerate(files_to_process):
                if use_folder:
                    # Processing from folder path
                    pdf_path = pdf_item
                    file_name = pdf_path.name
                    status_text.text(f"🔍 Analyzing {file_name}... ({idx + 1}/{total})")
                    resume_text = extract_text_from_pdf_path(pdf_path)
                else:
                    # Processing uploaded file
                    file_name = pdf_item.name
                    status_text.text(f"🔍 Analyzing {file_name}... ({idx + 1}/{total})")
                    resume_text = extract_text_from_pdf(pdf_item)

                if resume_text.startswith("Error"):
                    results.append({
                        "candidate_name": file_name.replace('.pdf', '').replace('.PDF', ''),
                        "fit_score": 0,
                        "error": resume_text,
                        "verdict": "Error",
                        "current_role": "Unknown",
                        "skills_matched": [],
                        "skills_missing": [],
                        "summary": "Could not extract text from PDF"
                    })
                else:
                    result = analyze_resume(
                        client,
                        resume_text,
                        job_description,
                        file_name.replace('.pdf', '').replace('.PDF', '')
                    )
                    results.append(result)

                progress_bar.progress((idx + 1) / total)

            results.sort(key=lambda x: x.get('fit_score', 0), reverse=True)
            st.session_state.results = results
            st.session_state.analyzed = True

            status_text.empty()
            progress_bar.empty()
            time_estimate.empty()
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display results
if st.session_state.analyzed and st.session_state.results:
    results = st.session_state.results

    # Results header
    st.markdown("---")
    st.markdown(f"""
    <div class="results-header">
        <div class="results-title">
            Results <span class="match-count">{len(results)} Candidates</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Categorize results
    categories = {
        "Best Fit": [],
        "Strong Fit": [],
        "Average": [],
        "Not a Fit": []
    }

    for result in results:
        verdict = result.get('verdict', 'Not a Fit')
        if "Best" in verdict:
            categories["Best Fit"].append(result)
        elif "Strong" in verdict:
            categories["Strong Fit"].append(result)
        elif "Average" in verdict:
            categories["Average"].append(result)
        else:
            categories["Not a Fit"].append(result)

    # Summary metrics
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
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

    st.markdown("<br>", unsafe_allow_html=True)

    # Display each category
    for category, category_results in categories.items():
        if not category_results:
            continue

        text_color, bg_color = get_category_color(category)

        # Category header
        st.markdown(f"""
        <div class="category-header">
            <span class="category-title">{category}</span>
            <span class="category-count" style="background: {bg_color}; color: {text_color};">
                {len(category_results)} candidate{'s' if len(category_results) != 1 else ''}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Display candidates in a grid (3 columns)
        cols = st.columns(3)
        for idx, result in enumerate(category_results):
            col_idx = idx % 3

            score = result.get('fit_score', 0)
            name = result.get('candidate_name', 'Unknown')
            role = result.get('current_role', 'Not specified')
            email = result.get('email', 'Not provided')
            phone = result.get('phone', 'Not provided')
            summary = result.get('summary', 'N/A')
            matched = result.get('skills_matched', [])
            missing = result.get('skills_missing', [])
            strengths = result.get('strengths', [])
            weaknesses = result.get('weaknesses', [])
            recommendation = result.get('recommendation', 'N/A')

            # Score color
            if score >= 90:
                score_bg = "#7c3aed"
            elif score >= 70:
                score_bg = "#059669"
            elif score >= 50:
                score_bg = "#d97706"
            else:
                score_bg = "#dc2626"

            with cols[col_idx]:
                # Candidate card
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
                        <div>📧 {email if email != 'Not provided' else 'N/A'}</div>
                        <div>📱 {phone if phone != 'Not provided' else 'N/A'}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Compact collapsable analysis using expander
                with st.expander("📊 View Analysis"):
                    # Skills in two columns
                    sk1, sk2 = st.columns(2)
                    with sk1:
                        st.caption("✅ **Matched Skills**")
                        if matched:
                            st.write(", ".join(matched[:5]) + ("..." if len(matched) > 5 else ""))
                        else:
                            st.write("None")
                    with sk2:
                        st.caption("❌ **Missing Skills**")
                        if missing:
                            st.write(", ".join(missing[:5]) + ("..." if len(missing) > 5 else ""))
                        else:
                            st.write("None")

                    # Strengths & Weaknesses
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

    # Download report
    st.markdown("---")
    report_text = "AI RESUME SHORTLISTING REPORT\n" + "="*50 + "\n\n"
    report_text += f"Total Candidates: {len(results)}\n"
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
                report_text += f"Email: {result.get('email', 'N/A')}\n"
                report_text += f"Phone: {result.get('phone', 'N/A')}\n"
                report_text += f"Summary: {result.get('summary', 'N/A')}\n"
                report_text += f"Recommendation: {result.get('recommendation', 'N/A')}\n"
                report_text += "-"*30 + "\n\n"

    st.download_button("📄 Download Full Report", report_text, "resume_analysis_report.txt", "text/plain")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #9ca3af; font-size: 0.85rem;">
    Built with 💜 for Hackathon 2024 | Powered by Groq AI
</div>
""", unsafe_allow_html=True)

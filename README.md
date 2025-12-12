# HireSmartAI - AI Resume Shortlister

AI-powered resume screening tool that analyzes resumes against job descriptions and provides instant rankings with match scores.

## Features

- Upload multiple PDF resumes (up to 10)
- AI-powered analysis using Groq LLM
- Fit score (0-100) for each candidate
- Skills matching and gap analysis
- Strengths and weaknesses identification
- Ranked results with recommendations
- Downloadable reports
- Bias-free screening (evaluates skills only)

## Tech Stack

- **Frontend:** Streamlit
- **AI Engine:** Groq API (Free)
- **PDF Parser:** PyPDF2
- **Deployment:** Streamlit Cloud

## Quick Start

### 1. Get Groq API Key (Free)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free
3. Generate an API key
4. Copy the key

### 2. Configure API Key

Open the `.env` file and add your API key:

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**Important:** Never commit your `.env` file to git!

### 3. Run Locally

```bash
# Clone or navigate to project folder
cd ai-resume-shortlister

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### 4. Open in Browser

The app will open at `http://localhost:8501`

## Deploy to Streamlit Cloud (Free)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-resume-shortlister.git
git push -u origin main
```

### Step 2: Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Click "Deploy"

Your app will be live in ~2 minutes!

## Usage

1. Enter your Groq API key in the sidebar
2. Paste the job description in the left panel
3. Upload PDF resumes in the right panel
4. Click "Analyze Resumes"
5. View ranked results with scores
6. Download the report

## How It Works

```
Upload PDFs → Extract Text → AI Analysis → Ranked Results
     ↓              ↓             ↓              ↓
  PyPDF2       Clean Text      Groq API     Fit Scores
```

## AI Output Format

For each resume, the AI returns:

| Field | Description |
|-------|-------------|
| fit_score | 0-100 match score |
| skills_matched | Skills found in resume |
| skills_missing | Required skills not found |
| strengths | Candidate's strong points |
| weaknesses | Areas of concern |
| summary | 2-3 sentence evaluation |
| verdict | Strong Fit / Average Fit / Not a Fit |
| recommendation | Interview recommendation |

## Project Structure

```
ai-resume-shortlister/
├── app.py              # Main application
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## Privacy & Security

- No data is stored permanently
- All processing happens in-memory
- Resumes are deleted after session
- No login required

## Built For

Hackathon 2024 - AI Productivity Tools

## License

MIT License

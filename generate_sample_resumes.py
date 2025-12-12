"""
Generate 10 Sample Data Scientist Resumes for Testing
Run: py generate_sample_resumes.py
"""

from fpdf import FPDF
import os

# Create samples folder
os.makedirs("sample_resumes", exist_ok=True)

resumes = [
    {
        "name": "Alice Chen",
        "email": "alice.chen@email.com",
        "phone": "+1-555-0101",
        "summary": "Senior Data Scientist with 6 years of experience in machine learning, deep learning, and statistical modeling. Expert in Python, TensorFlow, and cloud platforms.",
        "skills": "Python, R, SQL, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, AWS SageMaker, Spark, Docker, Git, Tableau, A/B Testing, NLP, Computer Vision",
        "experience": """Senior Data Scientist | Google | 2021-Present
- Built recommendation system improving user engagement by 23%
- Led team of 4 data scientists on NLP project
- Deployed ML models serving 10M+ daily predictions

Data Scientist | Amazon | 2018-2021
- Developed demand forecasting models reducing inventory costs by $2M
- Created customer segmentation using clustering algorithms
- Built real-time fraud detection system with 99.2% accuracy""",
        "education": "Ph.D. in Computer Science, Stanford University\nM.S. Statistics, UC Berkeley"
    },
    {
        "name": "Bob Martinez",
        "email": "bob.martinez@email.com",
        "phone": "+1-555-0102",
        "summary": "Data Scientist with 4 years of experience specializing in predictive analytics and business intelligence. Strong background in statistical analysis and data visualization.",
        "skills": "Python, SQL, R, Scikit-learn, Pandas, Tableau, Power BI, Excel, SPSS, Regression Analysis, Classification, Time Series",
        "experience": """Data Scientist | Microsoft | 2020-Present
- Developed churn prediction model with 87% accuracy
- Created automated reporting dashboards for executives
- Reduced data processing time by 40% through optimization

Junior Data Analyst | IBM | 2019-2020
- Performed exploratory data analysis on customer datasets
- Built SQL queries for data extraction and reporting""",
        "education": "M.S. Data Science, Columbia University\nB.S. Mathematics, NYU"
    },
    {
        "name": "Carol Williams",
        "email": "carol.williams@email.com",
        "phone": "+1-555-0103",
        "summary": "Machine Learning Engineer with 5 years of experience building production ML systems. Expertise in deep learning, MLOps, and scalable data pipelines.",
        "skills": "Python, TensorFlow, PyTorch, Keras, AWS, GCP, Kubernetes, Docker, MLflow, Airflow, Spark, Kafka, SQL, NoSQL, CI/CD",
        "experience": """ML Engineer | Netflix | 2020-Present
- Built content recommendation engine serving 200M users
- Implemented A/B testing framework for ML experiments
- Reduced model training time by 60% using distributed computing

Data Scientist | Uber | 2018-2020
- Developed surge pricing prediction models
- Created ETL pipelines processing 1TB+ daily data""",
        "education": "M.S. Machine Learning, Carnegie Mellon\nB.S. Computer Science, MIT"
    },
    {
        "name": "David Kim",
        "email": "david.kim@email.com",
        "phone": "+1-555-0104",
        "summary": "Entry-level Data Scientist with strong academic background. Recent graduate with internship experience in data analysis and machine learning projects.",
        "skills": "Python, R, SQL, Pandas, NumPy, Scikit-learn, Matplotlib, Jupyter, Basic TensorFlow, Statistics, Linear Algebra",
        "experience": """Data Science Intern | Startup XYZ | Summer 2023
- Analyzed customer behavior data using Python
- Created visualizations for stakeholder presentations
- Assisted in building basic classification models

Research Assistant | University Lab | 2022-2023
- Collected and cleaned research datasets
- Performed statistical analysis using R""",
        "education": "B.S. Data Science, UCLA\nGPA: 3.7"
    },
    {
        "name": "Emma Thompson",
        "email": "emma.thompson@email.com",
        "phone": "+1-555-0105",
        "summary": "NLP Specialist and Data Scientist with 7 years of experience in natural language processing, text analytics, and conversational AI systems.",
        "skills": "Python, NLP, BERT, GPT, Transformers, Hugging Face, spaCy, NLTK, TensorFlow, PyTorch, SQL, AWS, Elasticsearch, LLMs, RAG",
        "experience": """Principal Data Scientist | OpenAI | 2021-Present
- Led development of text classification systems
- Fine-tuned large language models for enterprise clients
- Built RAG systems for document Q&A applications

Senior NLP Engineer | Salesforce | 2017-2021
- Developed chatbot understanding 50+ intents with 94% accuracy
- Created sentiment analysis pipeline for social media""",
        "education": "Ph.D. Computational Linguistics, MIT\nM.S. Computer Science, Stanford"
    },
    {
        "name": "Frank Johnson",
        "email": "frank.johnson@email.com",
        "phone": "+1-555-0106",
        "summary": "Business Analyst transitioning to Data Science. 3 years of experience in analytics with growing technical skills in Python and machine learning.",
        "skills": "Excel, SQL, Tableau, Power BI, Basic Python, Basic R, Statistics, Business Analysis, Data Visualization, Reporting",
        "experience": """Business Analyst | Deloitte | 2021-Present
- Created business reports and dashboards
- Performed data analysis using Excel and SQL
- Learning Python and machine learning on the side

Junior Analyst | Accenture | 2020-2021
- Supported senior analysts with data gathering
- Built Excel models for financial forecasting""",
        "education": "MBA, University of Chicago\nB.S. Business Administration"
    },
    {
        "name": "Grace Lee",
        "email": "grace.lee@email.com",
        "phone": "+1-555-0107",
        "summary": "Computer Vision Data Scientist with 5 years of experience in image recognition, object detection, and autonomous systems.",
        "skills": "Python, OpenCV, TensorFlow, PyTorch, YOLO, CNN, Image Processing, AWS, Docker, C++, CUDA, Deep Learning, GANs",
        "experience": """Senior CV Engineer | Tesla | 2021-Present
- Developed object detection models for autonomous driving
- Improved pedestrian detection accuracy by 15%
- Optimized models for edge deployment

Data Scientist | NVIDIA | 2019-2021
- Built image classification systems for medical imaging
- Created synthetic data generation pipelines using GANs""",
        "education": "M.S. Computer Vision, Georgia Tech\nB.S. Electrical Engineering, UC San Diego"
    },
    {
        "name": "Henry Brown",
        "email": "henry.brown@email.com",
        "phone": "+1-555-0108",
        "summary": "Marketing professional with no data science experience. Looking to transition into analytics role.",
        "skills": "Marketing, Social Media, Content Creation, Basic Excel, PowerPoint, Communication, Project Management",
        "experience": """Marketing Manager | Brand Agency | 2019-Present
- Managed social media campaigns
- Created marketing content and strategies
- Analyzed campaign performance using basic metrics

Marketing Coordinator | Retail Company | 2017-2019
- Supported marketing team with administrative tasks
- Organized promotional events""",
        "education": "B.A. Marketing, State University"
    },
    {
        "name": "Isabella Garcia",
        "email": "isabella.garcia@email.com",
        "phone": "+1-555-0109",
        "summary": "Data Engineer with strong data science skills. 4 years of experience building data infrastructure and analytics pipelines.",
        "skills": "Python, SQL, Spark, Hadoop, Airflow, AWS, GCP, Snowflake, dbt, Kafka, ETL, Data Modeling, Basic ML, Pandas, Docker",
        "experience": """Senior Data Engineer | Airbnb | 2021-Present
- Built data pipelines processing 5TB daily
- Created feature stores for ML teams
- Implemented data quality monitoring systems

Data Engineer | Spotify | 2019-2021
- Developed ETL jobs using Spark and Airflow
- Collaborated with data scientists on model deployment""",
        "education": "M.S. Computer Science, University of Washington\nB.S. Information Systems"
    },
    {
        "name": "James Wilson",
        "email": "james.wilson@email.com",
        "phone": "+1-555-0110",
        "summary": "Experienced Data Scientist specializing in financial modeling, risk analytics, and quantitative analysis. 8 years in fintech and banking.",
        "skills": "Python, R, SQL, SAS, Quantitative Modeling, Risk Analysis, Time Series, Monte Carlo, VaR, Machine Learning, Bloomberg, Financial Modeling",
        "experience": """Lead Data Scientist | Goldman Sachs | 2019-Present
- Built credit risk models saving $50M annually
- Developed algorithmic trading strategies
- Led team of 6 quantitative analysts

Quantitative Analyst | JPMorgan | 2016-2019
- Created fraud detection system with 98% precision
- Built time series models for market prediction""",
        "education": "Ph.D. Financial Engineering, Princeton\nM.S. Applied Mathematics, Columbia"
    }
]

def create_resume_pdf(resume_data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)

    # Name
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, resume_data["name"], new_x="LMARGIN", new_y="NEXT", align='C')

    # Contact
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f'{resume_data["email"]} | {resume_data["phone"]}', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)

    # Summary
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'PROFESSIONAL SUMMARY', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(0, 5, resume_data["summary"])
    pdf.ln(3)

    # Skills
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'SKILLS', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(0, 5, resume_data["skills"])
    pdf.ln(3)

    # Experience
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'EXPERIENCE', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(0, 5, resume_data["experience"])
    pdf.ln(3)

    # Education
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'EDUCATION', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(0, 5, resume_data["education"])

    pdf.output(filename)

print("Generating 10 sample resumes...")

for i, resume in enumerate(resumes):
    filename = f"sample_resumes/{i+1:02d}_{resume['name'].replace(' ', '_')}.pdf"
    create_resume_pdf(resume, filename)
    print(f"Created: {filename}")

print("\n" + "="*50)
print("Done! Check the 'sample_resumes' folder.")
print("="*50)
print("\nResume Quality Guide:")
print("  1. Alice Chen      -> STRONG FIT (Senior, all skills)")
print("  2. Bob Martinez    -> AVERAGE FIT (Mid-level)")
print("  3. Carol Williams  -> STRONG FIT (ML Engineer)")
print("  4. David Kim       -> AVERAGE FIT (Entry-level)")
print("  5. Emma Thompson   -> STRONG FIT (NLP specialist)")
print("  6. Frank Johnson   -> WEAK FIT (Transitioning)")
print("  7. Grace Lee       -> STRONG FIT (Computer Vision)")
print("  8. Henry Brown     -> NOT A FIT (Marketing only)")
print("  9. Isabella Garcia -> AVERAGE FIT (Data Engineer)")
print(" 10. James Wilson    -> STRONG FIT (Fintech DS)")

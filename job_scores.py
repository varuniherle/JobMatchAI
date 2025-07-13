import pandas as pd
import json
import requests
import time
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types # Keep this for GenerateContentConfig
from google.generativeai.types import GenerationConfig

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])



def build_prompt(job_text):
  resume_text = """
SUMMARY
Proficient software engineer with 3 years of experience in developing Python Systems or Services. Experienced in enhancing applications and managing full-cycle deployments using Azure DevOps. Currently exploring AI-based solutions and automation tools like n8n, OpenAI to drive continuous improvement and efficiency.

PROFESSIONAL EXPERIENCE
ARM Embedded Technologies | Sept 2024 - Present  | Support Specialist: Digital Platform Full Stack
  - Created a simple web application using Flask where users can upload Excel files to automatically update desk details, making the process faster and more accurate.
  - Created many alerts in Azure using KQL for proactive issue detection. 
  - Deployed application code to production and pre-production environments using Azure DevOps.
  - Implemented the Power BI dashboard to get an overview of the application performance, reducing monitoring effort by over 80%.  
  - Worked on UI enhancements and feature development using React JS based on requirements.
  - Built Log anomaly detection using ML models and OpenAI, reducing the manual effort by 40%. 

Tata Consultancy Services | Systems Engineer | Oct 2021 - Sept 2024
- Created numerous file-processing and database services using Python based on business needs.
- Scheduled cron jobs in Azure DevOps using Python.
- Implemented new features and functionalities in React JS.
- Built dashboards for application performance monitoring using React JS.
- Managed deployment of code to production environments using Azure DevOps.
- Analyzed reports, identified root causes, monitored application stability, and addressed bugs.
- Used KQL extensively to analyze logs and diagnose system issues.
- Awarded Star of the Quarter (Oct 2022). Top 10 in Tata Neu app ideathon.

TECHNICAL SKILLS
- Programming: Python, JavaScript
- Web: HTML5, CSS, React JS, Flask
- Database: MySQL, PL/SQL (basic)
- Competencies: Problem-Solving, Data Structures & Algorithms, Troubleshooting, System Monitoring, Unit Testing
- Methodologies: Agile, DevOps, CI/CD

EDUCATION
SJB Institute of Technology | B.E. in Computer Science | 8.38 CGPA | Aug 2017 - Aug 2021
"""
  return f"""
You are an expert career assistant.

Given:
1. A candidate's resume
2. A job description in json format

Assess how well the resume matches the job description and return a [JSON object ONLY in this format]:
{{
  "score": float (between 0 and 1),
  "fit": "Good" or "Bad",
  "reason": "Brief reason for the match"
}}

Resume:
{resume_text}

Job Description:
{job_text}
"""
def get_match(job_desc: str):
    prompt = build_prompt(job_desc)
    
    # Directly get the model instance
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

    response = model.generate_content(
        contents=prompt
        )
    
    return response.text


def get_job_match_score(df):
    df['score'] = ''
    df['fit'] = 'no idea'
    df['reason'] =''
    for idx, row in df.iterrows():
        if idx%10 == 0:
          time.sleep(66)
        res = get_match(row['desc'])
        print(idx, res)
        try:
        # Safely extract JSON substring
            json_part = res[res.find('{'):res.rfind('}')+1]
            data = json.loads(json_part)
            df.at[idx, 'score'] = data.get('score', '')
            df.at[idx, 'fit'] = data.get('fit', '')
            df.at[idx, 'reason'] = data.get('reason', '')
        except Exception as e:
            print(f"Error at row {idx}: {e}")     
    print(df)
    return df


# def get_job_match_score(df):
    # df['score'] = -1
    # df['fit'] = 'no idea'
    # df['reason'] =''

    # OLLAMA_URL='http://localhost:11434/api/generate'
    # for idx, row in df.iterrows():
    #     prompt = build_prompt(row['desc'])
    #     data = {
    #     "model": "mistral:7b-instruct",
    #     "prompt": prompt,
    #     "stream": False
    # }
    #     # print(prompt)
    #     try:
    #         response = requests.post(OLLAMA_URL, json=data)
    #         result = response.json().get('response', '')

    #         # print(type(result), result)
    #         result_json = json.loads(result)
    #         # print(type(result_json))
    #         df.at[idx, 'score'] = result_json.get('score', -1)
    #         df.at[idx,'fit'] = result_json.get('fit','no idea')
    #         df.at[idx,'reason'] = result_json.get('reason','')
    #     except:
    #         print("")
    #         continue 
    # return df    

            


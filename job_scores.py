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
add your resume
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

            


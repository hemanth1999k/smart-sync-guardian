import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyBqVV87NPISUo8MyuLLkaRQE8lMVjLmr6Y"))

def analyze_error(logs):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    prompt = f"""Analyze this data sync error log. Respond in format:
    
    **Category**: [Type]
    **Analysis**: [Explanation]
    **Solution**: 
    - [Step 1]
    - [Step 2]
    - [Step 3]
    
    Logs: {logs[:3000]}"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Analysis failed: {str(e)}"
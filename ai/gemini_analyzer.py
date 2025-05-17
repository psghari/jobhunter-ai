import google.generativeai as genai
import os
from utils.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def bulk_analyze_jobs(jobs):
    model = genai.GenerativeModel("gemini-pro")
    flagged_jobs = []

    for job in jobs:
        prompt = f"""
        You are a job-matching assistant. Evaluate the following job listing and return:
        - Suitability: High / Medium / Low
        - One-sentence Reason
        
        Job Title: {job['title']}
        Company: {job['company']}
        Location: {job.get('location', 'Unknown')}
        Description: {job['summary']}
        URL: {job['url']}

        The ideal candidate has: 16 years experience in ITSM, SIAM, Incident/Problem/Change Management, ServiceNow, RCA, CAB, SLAs, operational governance.
        """

        try:
            res = model.generate_content(prompt)
            text = res.text.strip()

            if "High" in text:
                job["gemini_verdict"] = text
                flagged_jobs.append(job)
        except Exception as e:
            print(f"Gemini error: {e}")

    return flagged_jobs

import openai
import os
from utils.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def escalate_job(job):
    prompt = f"""
    Job Title: {job['title']}
    Company: {job['company']}
    Location: {job.get('location', 'N/A')}
    Description: {job['summary']}

    Profile:
    - 16 years experience in IT delivery, process maturity, vendor coordination
    - Expertise in SIAM, ServiceNow, RCA, ITSM, MIM, CAB, SLAs

    Tasks:
    1. Give a match score from 1 to 10
    2. Write a short, confident cover letter (3–5 sentences) that can be pasted into an email or job portal
    3. Add a verdict label: Strong Fit / Decent Fit / Not Recommended
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()

        # naive parser (you can improve this later)
        job["gpt_output"] = content
        job["score"] = extract_score(content)
        job["cover_letter"] = extract_cover(content)
        job["verdict"] = extract_verdict(content)
        return job
    except Exception as e:
        print(f"GPT error: {e}")
        return None


def extract_score(text):
    import re
    match = re.search(r"(?i)score[:\s]*([0-9]{1,2})", text)
    return match.group(1) if match else "N/A"

def extract_cover(text):
    # Naively split by sections, assuming cover letter is after score
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "cover letter" in line.lower():
            return "\n".join(lines[i+1:i+5]).strip()
    return "Cover letter not found"

def extract_verdict(text):
    for verdict in ["Strong Fit", "Decent Fit", "Not Recommended"]:
        if verdict.lower() in text.lower():
            return verdict
    return "Unknown"

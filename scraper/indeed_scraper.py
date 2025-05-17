import requests
from bs4 import BeautifulSoup
import time

JOB_TITLES = [
    "Service Delivery Manager",
    "ITSM Lead",
    "Problem Manager",
    "Major Incident Manager",
    "Change Manager",
    "Knowledge Manager",
    "SIAM Consultant",
    "IT Operations Manager",
    "ITIL Process Manager",
    "Service Management Lead",
    "Infrastructure Delivery Manager",
    "Application Delivery Manager"
]

LOCATIONS = [
    "Bangalore", "Hyderabad", "Pune", "Chennai", "Noida",
    "Gurgaon", "Coimbatore", "Remote"
]

def scrape_indeed():
    jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for title in JOB_TITLES:
        for location in LOCATIONS:
            query = title.replace(" ", "+")
            base_url = f"https://www.indeed.com/jobs?q={query}&l={location}&remotejob=1"

            try:
                resp = requests.get(base_url, headers=headers)
                soup = BeautifulSoup(resp.text, "html.parser")

                for card in soup.find_all("a", class_="tapItem"):
                    title_text = card.find("h2").text.strip() if card.find("h2") else "N/A"
                    company = card.find("span", class_="companyName").text.strip() if card.find("span", class_="companyName") else "N/A"
                    link = "https://www.indeed.com" + card.get("href")
                    summary = card.find("div", class_="job-snippet").text.strip() if card.find("div", class_="job-snippet") else ""

                    jobs.append({
                        "title": title_text,
                        "company": company,
                        "url": link,
                        "summary": summary,
                        "search_term": title,
                        "location": location
                    })
                time.sleep(1)  # Be polite to their servers
            except Exception as e:
                print(f"Failed to scrape for {title} in {location}: {e}")

    return jobs

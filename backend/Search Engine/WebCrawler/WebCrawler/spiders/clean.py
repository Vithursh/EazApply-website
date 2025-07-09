import requests
from bs4 import BeautifulSoup
import os
import csv


# def fetch_job_title(url: str) -> str:
#     resp = requests.get(url, headers={"User-Agent": "job-scraper/1.0"})
#     resp.raise_for_status()
#     soup = BeautifulSoup(resp.text, "html.parser")

#     # 1. Try Open Graph title
#     og = soup.find("meta", property="og:title")
#     if og and og.get("content"):
#         return og["content"].strip()

#     # 2. Try <title>
#     if soup.title and soup.title.string:
#         return soup.title.string.strip()

#     # 3. Try first <h1>
#     h1 = soup.find("h1")
#     if h1 and h1.get_text(strip=True):
#         return h1.get_text(strip=True)

#     # 4. Try common CSS classes (you may need to customize per site)
#     for cls in ["job-title", "posting-title", "position-title", "title"]:
#         el = soup.select_one(f".{cls}")
#         if el and el.get_text(strip=True):
#             return el.get_text(strip=True)

#     raise ValueError("Job title not found with default heuristics")


def receiveJobData():
    data = []
    index = 0
    # Read data from the CSV file
    path_to_file = "/home/vithursh/Coding/EazApply/backend/File Data/job_data.csv"
    with open(path_to_file, 'r', newline='') as file:
        # Create a csv.reader object with '|' as delimiter
        csv_reader = csv.reader(file, delimiter='|')

        # Optionally, skip the header row if present
        header = next(csv_reader)
        print(f"Header: {header}")

        # Iterate over each row in the CSV file
        for row in csv_reader:
            index += 1
            url = row[1]
            data.append({"id": index, "rank": row[0], "url": url, "paragraph": row[2], "title": row[3]})
            # Add the title of each job by scraping webpage and asking gemini to extract the title
    
    return data
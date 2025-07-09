from httpcore import TimeoutException
import scrapy
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import urljoin
from functools import partial
from collections import deque
from threading import Lock
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from json import JSONDecodeError
import unicodedata
import time
import os
import shutil
import logging
import re
import csv
import ctypes
import json
import requests
import google.generativeai as genai

from scrapy.crawler import Crawler

class EazApplySpider(scrapy.Spider):
    name = 'EazApplybot'
    # 'https://lifeattiktok.com/search?job_category_id_list=6704215862603155720&keyword=&limit=12&recruitment_id_list=&location_code_list=&subject_id_list=&offset=0'
    start_urls = ['https://cibc.wd3.myworkdayjobs.com/en-US/search/details/Analyst--Product-Development--Alternate-Solutions-Group_2505274']
    sub_urls = deque(start_urls)
    crawled_urls = set()

    raw_pages_path = "Raw HTML Pages"
    indexed_pages = "Indexed HTML Pages"

    csv_urls = []

    new_links = []

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model (useful for Linux)
    chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems


    # Initialize the bucket with capacity, refill time, and refill amount
    def __init__(self, capacity, refill_time, refill_amount, *args, **kwargs):
        super(EazApplySpider, self).__init__(*args, **kwargs)
        self.capacity = capacity
        self.tokens = capacity  # Start with a full bucket
        self.refill_time = refill_time  # Time interval for refilling tokens
        self.refill_amount = refill_amount  # Number of tokens to add per refill
        self.last_refill = time.time()  # Timestamp of the last refill
        self.lock = Lock()  # Lock to ensure thread safety
        self.db = {}  # Dictionary to store tokens for different keys


    # createBucket function
    def createBucket(self, key):
        self.db[key] = self.capacity  # Initialize the bucket for the key with full capacity
        return self.db[key]  # Return the initial token count


    # Downloads the seed URL webpages
    def crawl_start_urls(self, response, new_start_urls):        
        # Takes away the "https//"
        page = new_start_urls.split("//")[-1].split("/")[0]
        filename = f'/home/vithursh/Coding/EazApply/backend/File Data/{self.raw_pages_path}/{page}.html'
        
        # Split the URL at ".com" or ".ca" to get the website name
        if ".com" in new_start_urls:
            website_name = new_start_urls.split("//")[-1].split(".com")[0]
        elif ".ca" in new_start_urls:
            website_name = new_start_urls.split("//")[-1].split(".ca")[0]
        
        # print("The filename variable contains:",filename,"before it starts scraping the sub links")      
        
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        # print("The URL is:", page,"\n and the url is:", filename)
        
        # Crawler loop
        yield from self.crawl_loop(response, new_start_urls)


    # refillBucket function
    def refillBucket(self, key):
        print("refillBucket called with key:", key)
        with self.lock:
            current_time = time.time()
            elapsed_time = current_time - self.last_refill
            print("last_refill is:", self.last_refill)
            print("tokens is:", self.tokens)
            if elapsed_time > self.refill_time:
                tokens_to_add = int(elapsed_time / self.refill_time) * self.refill_amount
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = current_time
                self.db[key] = self.tokens
                print("Tokens after refill:", self.db[key])            
            else:
                print("Tokens after no refill:", self.db[key]) 
            return self.db[key]


    # handleRequest function
    def handleRequest(self, key):
        print("handleRequest called with key:", key)
        self.refillBucket(key)
        print("Token count after refill:", self.db[key])
        if self.db[key] > 0:
            self.db[key] -= 1
            print("Token deducted. New count:", self.db[key])
            print("handleRequest returns True")
            return True
        else:
            print("No tokens left to handle request.")
            print("handleRequest returns False")
            return False


    # Loops through all links until all webpages have been visited
    def crawl_loop(self, response, link):
        # Get all hyperlinks
        self.get_hyperlinks(response, link)

        # Uses the BFS algorithm to vist each link in the books.toscrape website
        if self.sub_urls:
            while self.sub_urls:
                if self.handleRequest('server'):
                    try:
                        print("The length of sub_urls is:", len(self.sub_urls))
                        next_url = self.sub_urls.popleft()
                        self.crawled_urls.add(next_url)
                        print("The next_url is:", next_url)
                        self.csv_urls.append(next_url)
                        yield scrapy.Request(next_url, callback=partial(self.crawl_sub_urls, url=next_url))
                    except Exception as e:
                        self.logger.error(f"Error processing URL {next_url}: {str(e)}")
                else:
                    print("Ran out of tokens!!!")
            print("sub_urls has", len(self.sub_urls), "now")
        else:
            self.logger.info('All URLs have been processed.')
            
            df = pd.DataFrame({"Title": self.csv_urls})
            # print(df)
            df.to_csv('/home/vithursh/Coding/EazApply/backend/File Data/LinkInBooksToScrapeWebsite.csv', index=False)


    # Gets all sub URLS in a webpage
    def get_hyperlinks(self, response, link):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        driver.get(link)
        
        print("The link is:", link)
        time.sleep(20)

        # Anchor Tags
        anchor_tags = driver.find_elements(By.CSS_SELECTOR, 'a[href]')

        if not anchor_tags:
            print("No anchor tags found.")
        # else:
            # for anchor_tag in anchor_tags:
                # print(anchor_tag.get_attribute('href'))
        
        # time.sleep(60)

        # Adds the sub links to the sub_urls array
        for anchor_tag in anchor_tags:
            official_Link = anchor_tag.get_attribute('href')
            if official_Link not in self.crawled_urls and official_Link not in self.sub_urls:
                self.sub_urls.append(official_Link)

            # Removes repetitive sub-links and blacklist certain websites
            if ".com/index.html" in official_Link or "facebook.com" in official_Link or "linkedin.com" in official_Link or "forum.bell.ca" in official_Link or "youtube.com" in official_Link or "x.com" in official_Link:
                # print("Contains '.com/index.html'")
                if official_Link in self.sub_urls:
                    self.sub_urls.remove(official_Link)
                    print(official_Link, "is being removed from the sub_urls array")
            # else:
            #     print(official_Link, "will not be put into the seed URL array")
        # print("\n\n\n The urls that are being pushed out:")

        # for next_page in response.xpath("//a[contains(text(), 'next') or contains(text(), 'Next') or contains(text(), '>>')]/@href").getall():
            # yield response.follow(next_page, self.get_hyperlinks)
        #     print("The Xpath is:", next_page)


    # Downloads the sub URL webpages
    def crawl_sub_urls(self, response, url):
        print("The sub url is:", url)

        # Get the urls in the "sub_urls" array and analyze it
        page = response.url.split("//")[-1]
        # print("The page contains:", page)

        # Turns "/" to "_" in each link 
        url_without_link = ""
        for i in page:
            if i == "/":
                url_without_link = url_without_link + i.replace("/", "_")
            else:
                url_without_link = url_without_link + i

        # print("The new string is:", url_without_link)

        # print("The page variable contains:",page)
        filename = f'/home/vithursh/Coding/EazApply/backend/File Data/{self.raw_pages_path}/{url_without_link}'

        # print("The website_name variable contains:",website_name)  # Outputs: "https://jobs.bell.ca"

        # print("The filename variable contains:",filename)

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        # print("\nAll of the urls in the 'new_links' array:")
        # for i in self.new_links:
        #     print("All the links in the new_links are:",i)
        
        yield from self.analyzer(response, url, filename)


    # This is the second line of defense to check if the webpage is a job application webpage
    def is_job_app_LLM(self, text: str) -> bool:
        api_key = os.getenv("GEMINI_API_KEY")
        instruction = (
            "You are a page classifier for job sites.  Decide if the given page text "
            "contains a **detailed job posting** (one individual job) with sections like:\n"
            "  • Job title AND at least one of: “Responsibilities”, “Qualifications”, “Job Description”, or “How to Apply”\n"
            "  • A paragraph (not just a list) describing the role’s duties\n"
            "  • Application instructions or an application form\n"
            "If you see only a list of positions or links (e.g. a homepage or careers listing), "
            "that is **not** a detailed job posting.\n\n"
            "If it **is** a detailed job posting page, respond with exactly:\n"
            "  Yes\n"
            "Otherwise respond with exactly:\n"
            "  No\n"
            "Do not output anything else—no punctuation, no extra words, no JSON."
        )

        payload = {
            "contents": [
                {"parts": [{"text": instruction}, {"text": text}]}
            ],
            "generationConfig": {
                "maxOutputTokens": 3,
                "temperature": 0.0
            }
        }

        resp = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        resp.raise_for_status()
        raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        print("The LLM says:", raw)
        time.sleep(20)

        return raw.lower() == "yes"  # Return True if the response is "Yes", otherwise False


    # Checks how weather to index its text by giving it to gemini to check to see if it's a job application or not
    def is_job_application_page(self, url: str) -> bool:
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
            driver.get(url)
            print("Successfully loaded the webpage")
            time.sleep(20)
    
            try:
                html_content = driver.page_source
                print("Successfully retrieved page source")
                time.sleep(20)
            except Exception as e:
                print(f"Error getting page source: {str(e)}")
                time.sleep(20)
                return False
            finally:
                driver.quit()
    
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
                print("Successfully parsed HTML content")
                time.sleep(20)
            except Exception as e:
                print(f"Error parsing HTML with BeautifulSoup: {str(e)}")
                time.sleep(20)
                return False

            if soup.select('script[type="application/ld+json"]'):
                for tag in soup.select('script[type="application/ld+json"]'):
                    print("It made it here!!!")
                    print("The tag is:", tag)
                    try:
                        raw = tag.string or tag.text
                        data = json.loads(raw)
                        print("Successfully parsed JSON-LD data")
                        time.sleep(20)
                    except JSONDecodeError as e:
                        print(f"JSON decode error: {str(e)}")
                        time.sleep(20)
                        continue
                    except Exception as e:
                        print(f"Error processing JSON-LD tag: {str(e)}")
                        time.sleep(20)
                        continue
        
                    try:
                        entries = data if isinstance(data, list) else [data]
                        for entry in entries:
                            if entry.get("@type") == "JobPosting" or "application" in entry.get("@type", "").lower():
                                print(f"Found job posting: {entry.get('@type')}")
                                time.sleep(20)
                                return True
                    except Exception as e:
                        print(f"Error processing entries: {str(e)}")
                        time.sleep(20)
                        continue
            else:
                print("No script tags with type 'application/ld+json' found")
                # time.sleep(20)
    
        except Exception as e:
            print(f"Unexpected error in is_job_application_page: {str(e)}")
            time.sleep(20)
            return False
    
        print("No job posting found in page")
        time.sleep(20)
        # Further processing
        return self.is_job_app_LLM(self.scrape_page(url))


    def clean_and_chunk(self, rawText: str) -> list[str]:
        api_key = os.getenv("GEMINI_API_KEY")
        url = (
            # "https://generativelanguage.googleapis.com/v1beta/models/"
            # "gemini-2.5-flash:generateContent"
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.0-flash:generateContent"
            f"?key={api_key}"
        )
    
        instruction = (
            "You are a web‐page summarization assistant for job listings.\n"
            "1) Remove all navigation menus, advertisements, footers, scripts, and any HTML artifacts.\n"
            "2) Merge broken lines into full, grammatically correct sentences.\n"
            "3) Summarize the entire page’s content into a single cohesive paragraph "
            "that covers the key details: job title, company name, location, main responsibilities, "
            "qualifications, application deadline/contact info, and any other critical info.\n"
            "4) Return **only** that one paragraph in plain English. No JSON, no lists, no additional commentary—just the summary."
        )

        payload = {
            "contents": [
                {"parts": [{"text": instruction}, {"text": rawText}]}
            ],
            "generationConfig": {
                "maxOutputTokens": 2048,
                "temperature": 0.0
            }
        }

        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, headers=headers, json=payload)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Error:", err)
            print("Response text:", resp.text)
            return ""
    
        body = resp.json()
        print("Gemini API response:", json.dumps(body, indent=2))
    
        try:
            raw = body["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            print("Error: Gemini API response missing expected fields:", e)
            print("Full response:", json.dumps(body, indent=2))
            return ""
    
        paragraphs = [p.strip() for p in raw.split("\n\n") if p.strip()]
        return paragraphs


    def fetch_job_title(self, description: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        instruction = (
            "You are an expert at reading job postings. Given the raw job posting below, "
            "extract **only** the job title. Respond with exactly the title—no additional text."
        )
    
        if isinstance(description, list):
            print("The description is a list, converting to string...")
            description = "\n\n".join(description)
    
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        full_prompt = instruction + "\n\n" + description
    
        try:
            result = model.generate_content(full_prompt)
            print("Gemini SDK result:", result)
            # Check if the result has a 'candidates' attribute and it's not empty
            if hasattr(result, "candidates") and result.candidates:
                candidate = result.candidates[0]
                # Check if the candidate has 'content' and 'parts', and 'parts' is not empty
                if hasattr(candidate, "content") and hasattr(candidate.content, "parts") and candidate.content.parts:
                    text = candidate.content.parts[0].text
                    return text.strip()  # Return the extracted job title, stripped of whitespace
                else:
                    print("No parts in candidate content.")  # Log if 'parts' is missing or empty
                    return ""
            else:
                print("No candidates returned from Gemini.")  # Log if 'candidates' is missing or empty
                return ""
        except Exception as err:
            print("Error fetching title:", err)  # Log any other exception that occurs
            return ""  # Return the error message as a string


    # Function to append a string to a CSV file(debugging purposes)
    def website_text_logs(self, URL, text):
        file_path = "/home/vithursh/Coding/EazApply/backend/File Data/log_website_text.csv"
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Check if the file exists to determine if we need to write the header
        file_exists = os.path.isfile(file_path)
        
        # Open the file in append mode and write the text
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            # Write the header only if the file does not exist
            if not file_exists:
                writer.writerow(["Website name", "Website text"])
            writer.writerow([URL, text])


    def scrape_page(self, url: str, headless: bool = True, timeout: int = 30, poll_interval: float = 0.5) -> str:
        print(f"Attempting to scrape before URL: {url}")  # Add this line
        time.sleep(20)

        """
        Loads a URL in Selenium, waits until the rendered text stabilizes, then returns all text.
        This works whether the page content comes from initial HTML, XHR, infinite scroll, or Shadow DOM.
        """

        opts = Options()
        if headless:
            opts.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        if not isinstance(url, str):
            url = str(url)  # coerce to string (but better to pass the correct type upstream)
        print(f"Attempting to scrape URL: {url}")  # Add this line
        time.sleep(20)
        driver.get(url)

        # 1) Give the page a little time to start loading
        time.sleep(1)

        # 2) Poll page_source length until it stops increasing (or we hit timeout)
        start = time.time()
        last_len = 0
        while True:
            html = driver.page_source
            curr_len = len(html)
            if curr_len == last_len:
                # page_source has stabilized
                break
            last_len = curr_len
            if time.time() - start > timeout:
                # timed out waiting for stabilization
                break
            time.sleep(poll_interval)

        # 3) Try to extract shadow-root content generically
        #    (many dynamic frameworks inject into shadow DOM)
        #    We execute JS to grab all textContent from document and any shadow roots
        js = """
        function getAllText(el) {
        if (el.shadowRoot) {
            return getAllText(el.shadowRoot);
        }
        let txt = el.textContent || "";
        for (let c of el.children) {
            txt += "\\n" + getAllText(c);
        }
        return txt;
        }
        return getAllText(document);
        """
        full_text = driver.execute_script(js)

        driver.quit()
        return full_text


    # Extracts HTML tags from each webpage
    def analyzer(self, response, URL, URLFilePathName):
        print("The analyzer function has been called!!!")
        with open(URLFilePathName, 'r') as f:
            print("The URL is:", URL)
            time.sleep(20)
            # Extract all text
            text = self.scrape_page(URL)

            # If it is a job application webpage 
            if self.is_job_application_page(URL):
                print("The chunk before cleaning is:", text)
                time.sleep(20)

                clean_text = ""
                time_increment = 1

                # If the Gemini api is overloaded, try again after a minute + 1
                while not clean_text:
                    clean_text = self.clean_and_chunk(text)
                    if clean_text == "":
                        print(f'The Gemini API is overloaded after calling the "clean_and_chunk" functions, trying again after {60*time_increment} seconds...')
                        time.sleep(60*time_increment)
                        time_increment += 1
                
                # Reset time_increment to 1 for the next loop
                time_increment = 1

                title = ""

                # If the Gemini api is overloaded, try again after a minute + 1
                while not title:
                    title = self.fetch_job_title(clean_text)
                    if title == "":
                        print(f'The Gemini API is overloaded after calling the "fetch_job_title" functions, trying again after {60*time_increment} seconds...')
                        time.sleep(60*time_increment)
                        time_increment += 1
                
                print("The URL is: ", URL)
                print("The title of the job is:", title)
                print("The chunk after cleaning is:", clean_text)
                time.sleep(100)

                # Define the path to the shared library
                lib_path = os.path.join(os.path.dirname(__file__), '/home/vithursh/Coding/EazApply/backend/Search Engine/Indexer/libIndex.so')

                # Load the shared library
                shared_library = ctypes.CDLL(lib_path)

                # Define the argument and return types
                shared_library.indexDocument.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
                shared_library.indexDocument.restype = ctypes.c_void_p

                # Using 'with' to open and write to the file
                with open('/home/vithursh/Coding/EazApply/backend/File Data/website_content.txt', 'w') as file:
                    file.write(str(clean_text))

                # Log text
                self.website_text_logs(URL, clean_text)

                # Convert the string to bytes
                URL_bytes = URL.encode('utf-8')
                title_bytes = title.encode('utf-8')

                # Call the function
                result = shared_library.indexDocument(URL_bytes, title_bytes)
                os.remove(URLFilePathName)

            # Delete an web page
            else:
                print("No, it is not a job application webpage!!!")
                print("The URL is: ", URL)
                time.sleep(20)
                # Delete the HTML page
                # print("The file path that will be deleted is:", URLFilePathName)
                df = pd.DataFrame({"Title": [URL]})
                df.to_csv('/home/vithursh/Coding/EazApply/backend/File Data/NotJobApplicationWebpages.csv', mode='a', header=False, index=False)
                os.remove(URLFilePathName)

        yield from self.crawl_loop(response, URL)
        print("The crawl_loop function has been called!!!")


    # Starts the crawling process
    def parse(self, response):

        # Creates the bucket of tokens
        self.createBucket('server')

        # Scrapes seed urls
        for url in self.start_urls:
            yield from self.crawl_start_urls(response, url)
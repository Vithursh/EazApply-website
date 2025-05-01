import scrapy
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import urljoin
from functools import partial
from collections import deque
from threading import Lock
import pandas as pd
import nltk
import spacy
import wordninja
from nltk.corpus import words as nltk_words
from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
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

from scrapy.crawler import Crawler

class EazApplySpider(scrapy.Spider):
    name = 'EazApplybot'
    start_urls = ['https://fa-evmr-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/?src=SNS-102']
    sub_urls = deque(start_urls)
    crawled_urls = set()

    raw_pages_path = "Raw HTML Pages"
    indexed_pages = "Indexed HTML Pages"

    csv_urls = []

    new_links = []

    # Word splitting function
    nltk.download('punkt_tab')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('omw-1.4')  # Optional for enhanced WordNet support

    # Load the spaCy model
    nlp = spacy.load("en_core_web_sm")

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
        # Configure logging
        # logging.basicConfig(
        #     level=logging.INFO,
        #     filename='/home/vithursh/Coding/EazApply/backend/File Data/scraper.log',
        #     filemode="w",
        #     format="%(asctime)s - %(levelname)s - %(message)s"
        # )


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
        
        # Split the URL at ".com" or ".ca"
        if ".com" in response.url:
            website_name = response.url.split("//")[-1].split(".com")[0]
        elif ".ca" in response.url:
            website_name = response.url.split("//")[-1].split(".ca")[0]

        # print("The website_name variable contains:",website_name)  # Outputs: "https://jobs.bell.ca"

        # print("The filename variable contains:",filename)

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        # print("\nAll of the urls in the 'new_links' array:")
        # for i in self.new_links:
        #     print("All the links in the new_links are:",i)
        
        yield from self.analyzer(response, url, filename, website_name)


    # Checks how weather to index its text by giving it to gemini to check to see if it's a job application or not
    def is_job_application_page(self, url: str) -> bool:
        # api_key = os.getenv("GEMINI_API_KEY")
        # instruction = (
        #     "You are a page classifier for job sites.  Decide if the given page text "
        #     "contains a **detailed job posting** (one individual job) with sections like:\n"
        #     "  • Job title AND at least one of: “Responsibilities”, “Qualifications”, “Job Description”, or “How to Apply”\n"
        #     "  • A paragraph (not just a list) describing the role’s duties\n"
        #     "  • Application instructions or an application form\n"
        #     "If you see only a list of positions or links (e.g. a homepage or careers listing), "
        #     "that is **not** a detailed job posting.\n\n"
        #     "If it **is** a detailed job posting page, respond with exactly:\n"
        #     "  Yes\n"
        #     "Otherwise respond with exactly:\n"
        #     "  No\n"
        #     "Do not output anything else—no punctuation, no extra words, no JSON."
        # )

        # payload = {
        #     "contents": [
        #         {"parts": [{"text": instruction}, {"text": text}]}
        #     ],
        #     "generationConfig": {
        #         "maxOutputTokens": 5,
        #         "temperature": 0.0
        #     }
        # }

        # resp = requests.post(
        #     "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key,
        #     json=payload,
        #     headers={"Content-Type": "application/json"}
        # )
        # resp.raise_for_status()
        # raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        # print("The LLM says:", raw)
        # time.sleep(20)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        driver.get(url)

         # wait up to 10s for any JSON-LD scripts to appear
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'script[type="application/ld+json"]'))
            )
        except:
            # no JSON-LD appeared in time; still proceed to parse whatever is here
            pass

        html_content = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html_content, 'html.parser')
        for tag in soup.select('script[type="application/ld+json"]'):
            raw = tag.string or tag.text
            try:
                data = json.loads(raw)
                print("The JSON data is:", data)
                time.sleep(20)
            except JSONDecodeError:
                continue
            entries = data if isinstance(data, list) else [data]
            for entry in entries:
                if entry.get("@type") == "JobPosting":
                    return True
        return False


    def clean_and_chunk(self, text: str) -> list[str]:
        api_key = os.getenv("GEMINI_API_KEY")
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-1.5-flash:generateContent"
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
                {"parts": [{"text": instruction}, {"text": text}]}
            ],
            "generationConfig": {
                "maxOutputTokens": 2048,
                "temperature": 0.0
            }
        }

        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()

        # Extract the raw text response
        body = resp.json()
        raw = body["candidates"][0]["content"]["parts"][0]["text"]
        
        # Split on double newlines into paragraphs
        paragraphs = [p.strip() for p in raw.split("\n\n") if p.strip()]
        return paragraphs


    def remove_short_words(self, input_str):
        input_words = input_str.split()
        final_word = []
        for word in input_words:
            if len(word) != 1:
                final_word.append(word)
        return ' '.join(final_word)


    # Word splitting function
    def split_compound_word(self, input_str):
        tokens = word_tokenize(input_str)

        # Split each compound word
        not_compound_words = []
        for token in tokens:
            # Ignore non-alphabetical tokens
            if token.isalpha():
                split_words = wordninja.split(token)
                # If the word is a compound word, split the words
                if len(split_words) != 1:
                    for word in split_words:
                        not_compound_words.append(word)
                # If the word is not a compound word, keep it as is
                else:
                    not_compound_words.append(token)

        # Join lemmatized words into a sentence
        return ' '.join(not_compound_words)


    # Function to convert the input string to lemmatized form
    def get_lemmatize(self, input_str):
        # Process the input string with spaCy NLP pipeline
        doc = self.nlp(input_str.lower())

        # Lemmatize each token and filter out punctuation
        lemmatized = []
        for token in doc:
            if token.is_alpha:  # Ignore non-alphabetical tokens
                lemma = token.lemma_  # Get the lemmatized word
                lemmatized.append(lemma)

        # Join lemmatized words into a sentence and return
        return self.split_compound_word(self.remove_short_words(' '.join(lemmatized)))


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
    def analyzer(self, response, URL, URLFilePathName, website_name):
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

                clean_text = self.clean_and_chunk(text)

                print("The URL is: ", URL)
                print("The chunk after cleaning is:", clean_text)
                time.sleep(100)

                # Define the path to the shared library
                # lib_path = os.path.join(os.path.dirname(__file__), '/home/vithursh/Coding/EazApply/backend/Search Engine/Indexer/libIndex.so')

                # Load the shared library
                # shared_library = ctypes.CDLL(lib_path)

                # Define the argument and return types
                # shared_library.indexDocument.argtypes = [ctypes.c_char_p]
                # shared_library.indexDocument.restype = ctypes.c_void_p

                # Using 'with' to open and write to the file
                # with open('/home/vithursh/Coding/EazApply/backend/File Data/website_content.txt', 'w') as file:
                    # file.write(str(clean_text))

                # Log text
                # self.website_text_logs(URL, clean_text)

                # Convert the string to bytes
                # URL_bytes = URL.encode('utf-8')

                # Call the function
                # result = shared_library.indexDocument(URL_bytes)
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
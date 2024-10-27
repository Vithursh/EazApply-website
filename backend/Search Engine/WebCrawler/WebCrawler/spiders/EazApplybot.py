import scrapy
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import urljoin
from functools import partial
from collections import deque
from threading import Lock
import pandas as pd
import time
import os
import shutil
import re
import ctypes
import requests

from scrapy.crawler import Crawler

class EazApplySpider(scrapy.Spider):
    name = 'EazApplybot'
    start_urls = ['http://books.toscrape.com/']
    sub_urls = deque(start_urls)
    crawled_urls = set()

    raw_pages_path = "Raw HTML Pages"
    indexed_pages = "Indexed HTML Pages"

    csv_urls = []

    new_links = []

    # Words to match to
    job_terms = {
            "Annual leave": 0,
            "Applicant tracking system (ATS)": 0,
            "Apprenticeship": 0,
            "Background check": 0,
            "Benefit-in-kind": 0,
            "Benefits": 0,
            "Branding statement": 0,
            "Breaks": 0,
            "Code of practice": 0,
            "Collective agreements": 0,
            "Compensation package": 0,
            "Constructive dismissal": 0,
            "Continuity of employment": 0,
            "Contract of employment": 0,
            "Contract employee": 0,
            "Cover letter": 0,
            "Deductions": 0,
            "Disciplinary procedure": 0,
            "Dismissal": 0,
            "Employee": 0,
            "Employment contract": 0,
            "Employment gap": 0,
            "Employment permit": 0,
            "Experience": 0,
            "Fixed-term contract": 0,
            "Follow-up": 0,
            "Freelancer": 0,
            "Hiring manager": 0,
            "Informational interview": 0,
            "Internship": 0,
            "Job sharing": 0,
            "Leave": 0,
            "Maternity leave": 0,
            "Minimum wage": 0,
            "Notice": 0,
            "Offer letter": 0,
            "Onboarding": 0,
            "Open-ended contract": 0,
            "Outsourcing": 0,
            "Overtime": 0,
            "Pension": 0,
            "References": 0,
            "Soft skills": 0,
            "STAR method": 0,
            "Temp": 0,
            "Temp-to-hire": 0,
            "Trade union": 0,
            "Transferable skills": 0,
            "White-collar": 0,
            "Zero-hours contract": 0
    }


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
        yield from self.crawl_loop(response)


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
    def crawl_loop(self, response):
        # Get all hyperlinks
        self.get_hyperlinks(response)

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
            print(df)
            df.to_csv('/home/vithursh/Coding/EazApply/backend/File Data/LinkInBooksToScrapeWebsite.csv', index=False)


    # Gets all sub URLS in a webpage
    def get_hyperlinks(self, response):
        # Anchor Tags
        anchor_tags = response.css('a::attr(href)').getall()

        # Adds the sub links to the sub_urls array
        for anchor_tag in anchor_tags:
            # total_score[3] += self.checkUseful(anchor_tag[0])  # Pass the text of the anchor tag to checkUseful
            official_Link = response.urljoin(anchor_tag)
            # if official_Link not in self.crawled_urls:
            if official_Link not in self.crawled_urls and official_Link not in self.sub_urls:
                self.sub_urls.append(official_Link)
                # print("The link:", official_Link,"is added")
                # print(f"Added URL: {official_Link}")  # Debugging statement

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


    # Checks how usefull each tag is by giving it a score based on how much matched words it contains from the list
    def checkUseful(self, tag):
        count = 0
        
        # print("\nThe text should be here:")

        # print("The tag is:",tag)
        
        if tag:  # Check if title exists
            # Checks if it is a BeautifulSoup object
            if isinstance(tag, Tag):
                tag_text = tag.get_text().strip()
            else:
                tag_text = tag.strip()  # Get the text from the tag
                
            tag_words = set(tag_text.split())  # Tokenize the tag text into words
            for useful_words in self.job_terms:
                job_terms_list = set(useful_words.split())
                common_words = tag_words & job_terms_list
                if common_words:
                    print(common_words)
                for words in common_words:
                    self.job_terms[useful_words] += 1
            
            # Adds up all of the scores for the words
            for total_word_score in self.job_terms:
                count += self.job_terms[total_word_score]
                self.job_terms[total_word_score] = 0

            # print(self.job_terms[useful_words])
            # print("The total score is",count)
        else:
            # print("No tag found.")
            count = 0
        
        return count


    # Extracts HTML tags from each webpage
    def analyzer(self, response, URL, URLFilePathName, website_name):
        print("The analyzer function has been called!!!")
        with open(URLFilePathName, 'r') as f:
            contents = f.read()
            total_score = [0] * 7

            # Fetch the HTML content
            page = requests.get(URL)

            # Parse the HTML
            soup = BeautifulSoup(page.content, 'html.parser')

            # Extract all text
            text = soup.get_text()

            # get score
            total_score[0] = self.checkUseful(text)         

            count = 0
            for i in total_score:
                count += i
            # print("The total score for this webpage is:", count)

            # If the score is greater than or equal to 10
            if count != 9:
                # If it's not at the end of the 'sub_urls' array
                if self.sub_urls:
                    
                    # Remove new lines and replace with commas
                    cleaned_text = re.sub(r"[()*&@^%|!.,;:?<>{}\[\]'-]", '', text)
                    cleaned_text = re.sub(r'\b(\w+)\b', r'\1,', cleaned_text)
                    cleaned_text = re.sub(r'([a-zA-Z0-9])\s+([a-zA-Z0-9])', r'\1,\2', cleaned_text)
                    trimmed_text = re.sub(r',\s+', ',', cleaned_text)

                    # Define the path to the shared library
                    lib_path = os.path.join(os.path.dirname(__file__), '/home/vithursh/Coding/EazApply/backend/Search Engine/Indexer/libIndex.so')

                    # Load the shared library
                    shared_library = ctypes.CDLL(lib_path)

                    # Define the argument and return types
                    shared_library.indexDocument.argtypes = [ctypes.c_char_p]
                    shared_library.indexDocument.restype = ctypes.c_void_p

                    # Using 'with' to open and write to the file
                    with open('/home/vithursh/Coding/EazApply/backend/File Data/website_content.txt', 'w') as file:
                        file.write(trimmed_text)

                    # Convert the string to bytes
                    URL_bytes = URL.encode('utf-8')

                    # Call the function
                    result = shared_library.indexDocument(URL_bytes)
                    os.remove(URLFilePathName)

            # Delete an web page
            else:
                # Delete the HTML page
                # print("The file path that will be deleted is:", URLFilePathName)
                os.remove(URLFilePathName)

        yield from self.crawl_loop(response)
        print("The crawl_loop function has been called!!!")


    # Starts the crawling process
    def parse(self, response):

        # Creates the bucket of tokens
        self.createBucket('server')

        # Scrapes seed urls
        for url in self.start_urls:
            yield from self.crawl_start_urls(response, url)
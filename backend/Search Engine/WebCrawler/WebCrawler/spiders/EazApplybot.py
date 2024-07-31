import scrapy
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import urljoin
from functools import partial
import os
import shutil
import re

from scrapy.crawler import Crawler

class EazApplySpider(scrapy.Spider):
    name = 'EazApplybot'
    start_urls = ['http://books.toscrape.com/']
    sub_urls = []
    crawled_urls = []

    raw_pages_path = "Raw HTML Pages"
    indexed_pages = "Indexed HTML Pages"

    switch_to_sub_urls = False

    global total_score

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

    def crawl_start_urls(self, response, new_start_urls):
        # Visit the links in the start url array
        # print("Went with:", self.switch_to_sub_urls)

        # Get the urls in the "start_urls" array and analyze it
        
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
        # self.analyzer(response, page, filename, website_name)

        # Anchor Tags
        anchor_tags = response.css('a::attr(href)').getall()
        # for seed_URLS in self.start_urls:
        for anchor_tag in anchor_tags:
            # total_score[3] += self.checkUseful(anchor_tag[0])  # Pass the text of the anchor tag to checkUseful
            official_Link = response.urljoin(anchor_tag)
            # print("The length is", len(self.sub_urls))
            if official_Link not in self.sub_urls:
                # print("The link:", official_Link)
                self.sub_urls.append(official_Link)
            # Removes repetitive sub-links
            if ".com/index.html" in official_Link:
                print("Contains '.com/index.html'")
                if official_Link in self.sub_urls:
                    self.sub_urls.remove(official_Link)
            # else:
            #     print(official_Link, "will not be put into the seed URL array")
        # print("\n\n\n The urls that are being pushed out:")

        # print("\nAll of the urls in the 'sub_urls' array:")
        # for i in self.sub_urls:
        #     print(i)

        for url in self.sub_urls:
            # If there are URLs to scrape, get the next URL and make a request
            if self.sub_urls:
                next_url = self.sub_urls.pop(0)
                self.crawled_urls.append(next_url)
                # print("The next url at index 0 is:", next_url)
                yield scrapy.Request(next_url, callback=partial(self.crawl_sub_urls, url=next_url))
                # yield scrapy.Request(next_url, callback=self.crawl_sub_urls())
            else:
                # If no URLs left to scrape, close the spider
                self.log('All URLs have been processed.')


    def crawl_sub_urls(self, response, url):
        print("The 'url' variable contains:", url)

        # Get the urls in the "sub_urls" array and analyze it
        page = response.url.split("//")[-1]
        print("The page contains:", page)

        # books.toscrape.com/catalogue/category/books_1/index.html.html
        url_without_link = " "
        for i in page:
            if i == "/":
                url_without_link = url_without_link + i.replace("/", "_")
            else:
                url_without_link = url_without_link + i

        print("The new string is:", url_without_link)

        # print("The page variable contains:",page)
        filename = f'/home/vithursh/Coding/EazApply/backend/File Data/{self.raw_pages_path}/{url_without_link}'
        
        # Split the URL at ".com" or ".ca"
        if ".com" in response.url:
            website_name = response.url.split("//")[-1].split(".com")[0]
        elif ".ca" in response.url:
            website_name = response.url.split("//")[-1].split(".ca")[0]

        # print("The website_name variable contains:",website_name)  # Outputs: "https://jobs.bell.ca"

        print("The filename variablecontains:",filename)

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        self.analyzer(response, page, filename, website_name)

    # Checks how usefull each tag is by giving it a score based on how much matched words it contains from the list
    def checkUseful(self, tag):
        count = 0
        
        print("\nThe text should be here:")

        print("The tag is:",tag)
        
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

            print(self.job_terms[useful_words])
            print("The total score is",count)
        else:
            print("No tag found.")
            count = 0
        
        return count


    def analyzer(self, response, URLName, URLFilePathName, website_name):
        with open(URLFilePathName, 'r') as f:
            contents = f.read()
            total_score = [0] * 7
            
            soup = BeautifulSoup(contents, 'html.parser')
            total_score[0] = self.checkUseful(soup.title)

            # Heading Tags
            soup2 = BeautifulSoup(contents, 'html.parser')
            headings = [tag.text for tag in soup2.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            for heading in headings:
                total_score[2] += self.checkUseful(heading)

            # Canonical Tag
            soup4 = BeautifulSoup(contents, 'html.parser')
            canonical_tag = soup4.find('link', attrs={'rel': 'canonical'})
            total_score[4] = self.checkUseful(canonical_tag)

            # Meta Robots Tag
            soup5 = BeautifulSoup(contents, 'html.parser')
            meta_robots = soup5.find('meta', attrs={'name': 'robots'})
            total_score[5] = self.checkUseful(meta_robots)

            # Structured Data
            soup6 = BeautifulSoup(contents, 'html.parser')
            structured_data = soup6.find('script', attrs={'type': 'application/ld+json'})
            total_score[6] = self.checkUseful(structured_data)

            # Meta Description Tag
            soup7 = BeautifulSoup(contents, 'html.parser')
            meta_description = soup7.find_all('meta', attrs={'name': 'description'})
            for meta in meta_description:
                content = meta.get('content')
                total_score[1] = self.checkUseful(content)

            count = 0
            for i in total_score:
                count += i
            print("The total score for this webpage is:", count)

            # If the score is greater than or equal to 10
            if count > 9:
                # If it's not at the end of the 'sub_urls' array
                if self.sub_urls:

                    # Sanitize the URL to use as a filename
                    sanitized_url = re.sub(r'[^\w\-_\. ]', '_', URLName)

                    # Remove leading and trailing whitespace
                    sanitized_url = sanitized_url.strip()

                    print("the sanitized_url is:", sanitized_url)

                    # Move the HTML file to the indexer folder
                    indexedURL = f'/home/vithursh/Coding/EazApply/backend/File Data/{self.indexed_pages}/{website_name}/{sanitized_url}'
                    
                    print("The indexedURL variable contains:", indexedURL)
                    
                    # Create the directory if it doesn't exist, but don't include the filename
                    os.makedirs(os.path.dirname(indexedURL), exist_ok=True)
                    
                    # Check if the source file exists
                    if not os.path.exists(URLFilePathName):
                        print(f"Source file {URLFilePathName} does not exist.")
                    else:
                        print(f"Source file {URLFilePathName} exists.")

                    # Check if the destination is a directory
                    if os.path.isdir(indexedURL):
                        print(f"Destination {indexedURL} is a directory.")
                    else:
                        print(f"Destination {indexedURL} is not a directory.")

                    # Check if the file exists before moving
                    if not os.path.exists(indexedURL):
                        shutil.move(URLFilePathName, indexedURL)
                    else:
                        print(f"File {indexedURL} already exists, skipping move operation.")
                    
                # If it's at the end of the 'sub_urls' array
                else:
                    # Create a new folder based on the main URL it's crawling in the 'Raw HTML Pages' folder
                    # indexedURL = f'/home/vithursh/Coding/EazApply/backend/File Data/{self.indexed_pages}/{URLName}'
                    # os.makedirs(indexedURL, exist_ok=True)
                    self.switch_to_sub_urls = False

            # Delete an web page
            else:
                # if not self.sub_urls:
                #     self.switch_to_sub_urls = False
                # Delete the HTML page
                print("The file path that will be deleted is:", URLFilePathName)
                os.remove(URLFilePathName)
            print("At the end of the link cycle, it is now:", self.switch_to_sub_urls)


    def parse(self, response):
        for url in self.start_urls:
            yield from self.crawl_start_urls(response, url)
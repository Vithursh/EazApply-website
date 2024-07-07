import scrapy
from bs4 import BeautifulSoup
from bs4.element import Tag

class EazApplySpider(scrapy.Spider):
    name = 'EazApplybot'
    start_urls = ['http://books.toscrape.com/']

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


    def analyzer(self, response, URLName, URLFilePathName):
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
            # print(headings_score)

            # Anchor Tags
            soup3 = BeautifulSoup(contents, 'html.parser')
            anchor_tags = [(tag.text, tag.get('href')) for tag in soup3.find_all('a')]
            for anchor_tag in anchor_tags:
                total_score[3] += self.checkUseful(anchor_tag[0])  # Pass the text of the anchor tag to checkUseful
                # offcial_Link = self.start_urls[0] + anchor_tag[1]
                print("The link:",anchor_tag[1])
                # self.start_urls.append(offcial_Link)
            # print(anchor_tags_score)


            # Canonical Tag
            soup4 = BeautifulSoup(contents, 'html.parser')
            canonical_tag_score = 0
            canonical_tag = soup4.find('link', attrs={'rel': 'canonical'})
            total_score[4] = self.checkUseful(canonical_tag)
            print(canonical_tag_score)

            # Meta Robots Tag
            soup5 = BeautifulSoup(contents, 'html.parser')
            meta_robots = soup5.find('meta', attrs={'name': 'robots'})
            total_score[5] = self.checkUseful(meta_robots)
            print(total_score[5])

            # Structured Data
            soup6 = BeautifulSoup(contents, 'html.parser')
            structured_data = soup6.find('script', attrs={'type': 'application/ld+json'})
            total_score[6] = self.checkUseful(structured_data)
            # print(structured_data_score)

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

            if count >= 10:
                # Save the html file for the indexer
                print()
            else:
                # Delete the html page
                print()


    def parse(self, response):
        page = response.url.split("//")[-1].split("/")[0]
        filename = f'/home/vithursh/Coding/EazApply/backend/File Data/Raw HTML Pages/{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
        # print(page)
        self.analyzer(response, page, filename)
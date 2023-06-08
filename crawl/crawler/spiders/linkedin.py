from ..items import JobsItem
from scrapy import signals, Spider, Request
from scrapy.selector import Selector
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

bad_words = ['java', '.net', 'node', 'springboot', 'c#']

URL_LOGIN = 'https://www.linkedin.com/'
URL_JOBS = 'https://www.linkedin.com/jobs/search?keywords=Cloud%20Engineer%20AWS&location=remote&position=1&pageNum=0'

class LinkedinSpider(Spider):
    name = "linkedin"
    
    # This url doesn't matter, I just need the parse callback to be invoked
    allowed_domains = ['linkedin.com']
    start_urls = ['https://www.linkedin.com']

    def parse(self, response):
        """
        First run the browser automation to load the page. Once the data is 
        loaded, Scrapy can take over to grab all the links I need
        """

        # Setup the web driver
        driver = webdriver.Chrome(
                    ChromeDriverManager().install(),
                )

        # Load the page
        driver.get(URL_LOGIN)
        driver.implicitly_wait(10)

        email_box = driver.find_element(By.XPATH, '''//*[@id="session_key"]''')
        pass_box = driver.find_element(By.XPATH, '''//*[@id="session_password"]''')
        email_box.send_keys({'EMAIL'})
        pass_box.send_keys({'PASS'})

        button = driver.find_element(By.XPATH, '''//*[@id="main-content"]/section[1]/div/div/form[1]/div[2]/button''')
        button.click()


        driver.get(URL_JOBS)
        driver.implicitly_wait(10)

        # LinkedIn only loads a handful of jobs initially, so need to scroll down 
        # to load more. Eventually a "See more jobs" button should appear, but
        # either way after n scrolls there are a ton of jobs to grab.
        # for _ in range(2):  
        #     try:
        #         driver.find_element(By.XPATH,
        #             '''//*[@id="main-content"]/section[2]/button'''
        #         ).click()
        #         break
        #     except:
        #         driver.execute_script(
        #             'window.scrollTo(0, document.body.scrollHeight);'
        #         )
        #         time.sleep(1)

        # Now click each of those links
        links = driver.find_elements(By.TAG_NAME, "a")
        cleaned_links = [link.get_attribute('href') for link in links if 'linkedin.com/jobs/view' in link.get_attribute('href') ]

        for link in cleaned_links[:5]:
            driver.get(link)
            driver.implicitly_wait(10)
            try:
                driver.find_element(By.XPATH, '''//*[@id="ember31"]''').click()
                time.sleep(2)
                driver.find_element(By.XPATH, '''//*[@id="ember32"]''').click()
                time.sleep(2)
            except:
                pass

            sel = Selector(text=driver.page_source)
            content = sel.xpath('''//*[@id="job-details"]/span/text()''').getall()
            # Check for bad words                    
            if not any(bw in string.lower() for bw in bad_words for string in content):
                    
                # Create scrapy items from the objects in those lists
                job = JobsItem()
                job['title'] = sel.xpath('''/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/h1/text()''').getall()
                job['url'] = link
                job['content'] = content

                yield job
            
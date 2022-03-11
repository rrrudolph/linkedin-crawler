from ..crawler.css_and_xpaths import xpath_paths
from ..crawler.items import JobsItem
from scrapy import signals
from scrapy import Spider
from scrapy.selector import Selector
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


URL = 'https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=remote&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

s3_client = boto3.client(service_name='s3')

class LinkedinSpider(Spider):
    name = "linkedinjobs"
    
    # This url doesn't matter, I just need the parse callback to be invoked
    allowed_domains = ["toscrape.com"]
    start_urls = ['https://quotes.toscrape.com/page/1/']

    # This receives event hooks - only tracking "spider_closed"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LinkedinSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        """
        When the spider finishes this callback will upload the saved
        file to s3.
        """

        try:
            response = s3_client.upload_file(
                'linkedin_jobs_raw.csv', # local file
                'rudy-scrapy-project', # bucket 
                'linkedin_jobs_raw.csv', # s3 file
            )
            self.log('~~~ Uploaded file to s3 ~~~')
            self.log(response)

        except ClientError as e:
            self.log(e)
        except NoCredentialsError as e:            
            self.log(e)

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
        driver.get(URL)

        # LinkedIn only loads a handful of jobs initially, so need to scroll down 
        # to load more. Eventually a "See more jobs" button should appear, but
        # either way after 10 scrolls there are a ton of jobs to grab.
        for _ in range(10):  
            try:
                driver.find_element_by_xpath(
                    '''/html/body/div[1]/div/main/section[2]/button'''
                ).click()
                break
            except:
                driver.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight);'
                )
                time.sleep(1)

        # Scrapy can take over now that the page is loaded
        sel = Selector(text=driver.page_source)

        titles = sel.xpath(xpath_paths['titles']).getall()
        links = sel.xpath(xpath_paths['links']).getall()

        # Create scrapy items from the objects in those lists
        for title, link in zip(titles, links):
            job = JobsItem()
            job['title'] = title
            job['url'] = link
            
            yield job


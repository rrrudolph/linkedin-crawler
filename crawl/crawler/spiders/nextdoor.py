from ..items import JobsItem
from scrapy import signals, Spider, Request
from scrapy.selector import Selector
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pyperclip as pc

EMAIL = 'rudysemail@gmail.com'
PASSWORD = 'nextdoor!1'

URL_LOGIN = 'https://nextdoor.com/login/?next=news_feed'
URL_POSTS= 'https://nextdoor.com/news_feed'
URL_SUBSCRIBE_NEIGHBORHOODS = 'https://nextdoor.com/neighborhood/?source=settings'

class LinkedinSpider(Spider):
    name = "nd"
    
    # This url doesn't matter, I just need the parse callback to be invoked
    allowed_domains = ['nextdoor.com']
    start_urls = ['https://www.nextdoor.com']

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
        # driver.get(URL_LOGIN)
        driver.get(URL_POSTS)
        driver.implicitly_wait(10)

        email_box = driver.find_element(By.XPATH, '''//*[@id="id_email"]''')
        pass_box = driver.find_element(By.XPATH, '''//*[@id="id_password"]''')
        email_box.send_keys(EMAIL)
        pass_box.send_keys(PASSWORD)

        button = driver.find_element(By.XPATH, '''//*[@id="signin_button"]''')
        button.click()
            
        driver.implicitly_wait(5)

        # See if it's asking for my phone number
        try:
            button = driver.find_element(By.XPATH, '''//*[@id="id-5"]/div/div[3]/button[2]/div''')
            button.click()
        except:
            pass

        # See if it's asking for contacts
        try:
            button = driver.find_element(By.XPATH, '''//*[@id="id-8"]/div/div[3]/div[2]/button/div''')
            button.click()
        except:
            pass
        
        # Load some posts onto the page
        # for _ in range(2):
        #     driver.execute_script(
        #         'window.scrollTo(0, document.body.scrollHeight);'
        #     )
        #     time.sleep(1)

        # Poster Name 
        # //*[@id="s_275806385"]/div/div/div[2]/div[1]/div/div[1]/span/span[1]/span/div/div[1]/a
        # a class='_3I7vNNNM E7NPJ3WK'

        # Post Body
        # //*[@id="s_275806385"]/div/div/div[2]/div[2]/div/p/div/span/span/span/div/span/span/text()
        # span class='Linkify'

        # posts = driver.find_elements(By.CLASS_NAME, 'Linkify')
        # pposts = [ p.text for p in posts ]
        
        links = []
        buttons = [ # share buttons
            "//*[@id='s_274578444']/div/div/div[3]/div/div/div/div[2]/div[3]/div/div",
            "//*[@id='s_274578444']/div/div/div[3]/div/div/div/div[2]/div[3]/div/div/svg",
            "//*[@id='s_274578444']/div/div/div[3]/div/div/div/div[2]/div[3]/div/div/span"]
        twitter = "//*[@id='id-9']/div/div/a[3]"
        share_button_possibles = [ #class buttons
            'css-q4c23q', 
            'css-13amqrt', 
            'css-1eqm8dr', #(worked once) 
            'css-qu9bfj', 
            'css-1tr6k6r', 
            'css-1vqa2q6' #(worked once)
            'css-8htnpl',
            'css-86f3ks'
        ]
        
        share_buttons = driver.find_elements(By.CLASS_NAME, share_button_possibles[0])
        share_buttons = driver.find_element(By.CLASS_NAME, share_button_possibles[-1]).click()

        # for num, b in enumerate(share_buttons):
        #     job = JobsItem()
        #     job['title'] = num
        #     yield job

        #     b.click()

        raw_links = driver.find_elements(By.CLASS_NAME, 'css-q4c23q')
        links = []
        for l in raw_links:
            try:
                links.append(l.get_attribute('href'))
            except:
                continue

        real = [l for l in links if l ]
        t = [l.split('url=')[1] for l in real if 'twitter' in l ]
            
        job = JobsItem()
        job['url'] = t
        # job['title'] = links
        yield job
            # time.sleep(1)

            # if it's an event there won't be an embed button
            # try:
                # embed_button = driver.find_elements(By.CLASS_NAME, 'css-q4c23q') # css-1eqm8dr css-4royqz
                # embed_button.click()
                # time.sleep(2)
                # embed_text = driver.find_elements(By.CLASS_NAME, 'css-1gzg1wd')
                # links.append(embed_text)

                # link_button = driver.find_element(By.XPATH, '''/html/body/div[1]/div/div/div[4]/div/div[2]/div[4]/div[1]/div/div/div/div/div[3]/div/div/div/div/div[3]/div[2]/div/div/div[3]/div/div[1]/svg''') #  class name:  q4c23q 13amqrt 1eqm8dr(worked once) qu9bfj 1tr6k6r 1vqa2q6(worked once)
                # /html/body/div[1]/div/div/div[4]/div/div[2]/div[4]/div[1]/div/div/div/div/div[3]/div/div/div/div/div[3]/div[2]/div/div/div[3]/div/div[2]/span
                # link_button.click()
                # links.append(pc.paste())
                
                # link = driver.find_elements(By.CLASS_NAME, 'css-q4c23q')
            # except:
                # pass
            

            # mailto:?subject=Hello%20all.%20%E2%80%94%20Nextdoor&body=From%20my%20neighborhood%3A%20https%3A%2F%2Fnextdoor.com%2Fp%2FLkqCzLgFL7fr%3Futm_source%3Dshare%26utm_content%3Dstatic_email_share%26extras%3DODMzMzI3NzA%253D
            # https%3A%2F%2Fnextdoor.com%2Fp%2FLkqCzLgFL7fr%3Futm_source%3Dshare%26utm_content%3Dstatic_email_share%26extras%3DODMzMzI3NzA%253D
            # https://nextdoor.com/p/LkqCzLgFL7fr?utm_source=share&extras=ODMzMzI3NzA%3D
            # https://twitter.com/intent/tweet/?text=From%20my%20neighborhood%3A%20&url=https%3A%2F%2Fnextdoor.com%2Fp%2FLkqCzLgFL7fr%3Futm_source%3Dshare%26extras%3DODMzMzI3NzA%253D

        # for p, l in zip(pposts, links):
        # for l in links:
        #     job = JobsItem()
            # job['title'] = sel.xpath('''/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/h1/text()''').getall()
            # job['url'] = l
            # job['content'] = p

            # yield job
        # Share button
        # span class='css-86f3ks'
        # If you click `share` then `embed`

        # Embed buttom  
        # svg class='css-qu9bfj'
        # //*[@id="id-136"]/div/div/div[4]/div/div[1]/svg
        # //*[@id="id-376"]/div/div/div[4]/div/div[1]/svg
        # //*[@id="id-406"]/div/div/div[4]/div/div[1]/svg
        # //*[@id="id-415"]/div/div/div[4]/div/div[1]/svg

        # Embed popup
        # textarea ckass='css-1gzg1wd'
        # //*[@id="id-188"]/div/div/div[3]/div/textarea
        # //*[@id="id-465"]/div/div/div[3]/div/textarea

        # Sub Neighborhoods
        # //*[@id="layout_container"]/div/div[3]/div/div[1]/div/div[2]/div/div/div/div[2]/div[1]

        # Neighborhood from search
        # //*[@id="layout_container"]/div/div/div[4]/div/div[2]/div[3]/div/div/div[2]/div/a/div/div[1]/div/div[2]/div/div[1]/div/div[1]/div/span


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
        # links = driver.find_elements(By.TAG_NAME, "a")
        # cleaned_links = [link.get_attribute('href') for link in links if 'linkedin.com/jobs/view' in link.get_attribute('href') ]

        # for link in cleaned_links[:5]:
        #     driver.get(link)
        #     driver.implicitly_wait(10)
        #     try:
        #         driver.find_element(By.XPATH, '''//*[@id="ember31"]''').click()
        #         time.sleep(2)
        #         driver.find_element(By.XPATH, '''//*[@id="ember32"]''').click()
        #         time.sleep(2)
        #     except:
        #         pass

        #     sel = Selector(text=driver.page_source)
        #     content = sel.xpath('''//*[@id="job-details"]/span/text()''').getall()
        #     # Check for bad words                    
        #     if not any(bw in string.lower() for bw in bad_words for string in content):
                    
        #         # Create scrapy items from the objects in those lists
        #         job = JobsItem()
        #         job['title'] = sel.xpath('''/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/h1/text()''').getall()
        #         job['url'] = link
        #         job['content'] = content

        #         yield job
            
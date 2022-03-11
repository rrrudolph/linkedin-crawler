# Linkedin Crawler
```bash
├── crawl
│   ├── crawler
│   │   ├── __init__.py
│   │   ├── css_and_xpaths.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── spiders
│   │       ├── __init__.py
│   │       └── linkedin_spider.py
│   ├── __init__.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── scrapy.cfg
│   └── tests
│       ├── __init__.py
│       └── test_linkedin_spider.py
└── process
    ├── clean_raw.py
    ├── Dockerfile
    └── requirements.txt
```
This repo utilizes Selenium and a simple Scrapy spider to grab Data Engineer job titles and links from LinkedIn.  Once the spider finishes, one of the built in Scrapy event hooks executes an upload to S3.

From there AWS Batch is used to read the data from S3, do some basic cleaning, and then save back into S3.

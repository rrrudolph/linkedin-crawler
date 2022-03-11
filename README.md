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
This repo utilizes Selenium and a simple Scrapy spider to grab Data Engineer job titles and links from LinkedIn.  Once the spider finishes, one of the standard Scrapy event hooks executes an upload to S3.

From there AWS Batch is used to read the data from S3, do some basic cleaning, and then save back into S3.

I used Poetry to manage dependencies in the `crawl` side of the project, but because the `process` side has very few dependencies I went with a simple `requirements.txt` for it.

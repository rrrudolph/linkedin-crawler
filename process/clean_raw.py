import boto3
import pandas as pd
from io import StringIO
from botocore.exceptions import NoCredentialsError, ClientError


# going to read in the raw json, cnvert to df and then save as csv to s3
bucket_name = 'rudy-scrapy-project'
# filename = 'linkedinjobs.csv'
filename = 'linkedin_jobs_raw.csv'

s3 = boto3.client(
    's3',
    region_name='us-east-1'
)

raw_jobs_file = s3.get_object(
    Bucket=bucket_name,
    Key=filename
    ) 

# s3 delivers a binary stream that has to be decoded
contents = raw_jobs_file['Body'].read().decode('utf-8')
df = pd.read_csv(StringIO(contents))

# print(df)
#                                                  title                                                url
# 0    \n            \n        \n        Data Enginee...  https://www.linkedin.com/jobs/view/data-engine...
# 1    \n            \n        \n        Data Enginee...  https://www.linkedin.com/jobs/view/data-engine...
# 2    \n            \n        \n        Data Enginee...  https://www.linkedin.com/jobs/view/data-engine...

df.title = df.title.replace('\n', '', regex=True)
df.title = df.title.str.lstrip()
df.title = df.title.str.rstrip()

# Save to local file
df.to_csv('linked_jobs_clean.csv')

try:
    response = s3.upload_file(
        'linked_jobs_clean.csv', # local file
        'rudy-scrapy-project', # bucket 
        'linked_jobs_clean.csv', # s3 file
    )

except ClientError as e:
    print(e)
except NoCredentialsError as e:            
    print(e)
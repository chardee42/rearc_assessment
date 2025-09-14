import requests
from bs4 import BeautifulSoup
import boto3
import os
import time


s3 = boto3.client("s3")      # access to S3 service
S3_BUCKET = os.environ.get("BUCKET_NAME", "rearc-chardee-project")

def get_file_list(url):
    """Get the list of files from BLS"""
    headers = {     # Added user agent info to get past 403 error
        "User-Agent": "Mozilla/5.0 (compatible; Chris Hardee; chardee42@gmail.com)"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  

    soup = BeautifulSoup(response.text, "html.parser")

    # Get file list
    files = [
        link.get("href")
        for link in soup.find_all("a")
        if link.get("href") not in (None, "../")  # skip parent dir
    ]

    return files

def copy_files(url, files):
    """ Copy the files to the Amazon S3 bucket """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Chris Hardee; chardee42@gmail.com)"}
    
    for file_name in files:
        try:
            file_name_only = file_name[20:]
            if file_name_only != "":
                response = requests.get(url + file_name_only, headers=headers)   # headers required to bypass 403
                time.sleep(1)
                if response.status_code == 200:
                    s3.put_object(Bucket=S3_BUCKET, Key=file_name, Body=response.content)
                    print(f'Upload {file_name}')
                else:
                   print('Upload failed')
                
                #
                
        except Exception as e:
            print (f"Exception: {e}")
        
        

def lambda_handler(event, context):
    url="https://download.bls.gov/pub/time.series/pr/"
    files = get_file_list(url)
    copy_files(url, files)
    
    return {"statusCode": 200, "body": f"Copied files"}
    
import boto3
import json
import os
import requests

# Link for API: https://honolulu-api.datausa.io/tesseract/data.jsonrecords?cube=acs_yg_total_population_1&drilldowns=Year%2CNation&locale=en&measures=Population
# Event payload to trigger: {'address': 'https://api.example.com/data'}.

# Actual trigger (double quotes required):
## {"address": "https://honolulu-api.datausa.io/tesseract/data.jsonrecords?cube=acs_yg_total_population_1&drilldowns=Year%2CNation&locale=en&measures=Population"}


s3 = boto3.client("s3")      # access to S3 service
S3_BUCKET = os.environ.get("BUCKET_NAME", "rearc-chardee-project")

USER_AGENT = "Mozilla/5.0 (compatible; Chris Hardee; chardee42@gmail.com)"                                                                          

def upload_json_to_s3(data: dict, key: str = "api_out.json"):
    """
    Upload a Python dict as JSON to S3 with proper content-type.
    """
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json; charset=utf-8",
    )
    print(f"Uploaded {key} to s3://{S3_BUCKET}/{key}")
    



def lambda_handler(event, context):
    # input an event address
    address = event.get("address")

    if not address:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No address parameter provided'})
        }

    try:
        resp = requests.get(address, headers={"User-Agent": USER_AGENT}, timeout=30)
        resp.raise_for_status()

        try:
            payload = resp.json()
        except ValueError:
            payload = {"raw": resp.text}

        upload_json_to_s3(payload, key="api_out.json")
         

        return {"statusCode": 200, "body": json.dumps({"message": "OK", "s3_bucket": S3_BUCKET, "s3_key": "api_out.json"})}

    except requests.exceptions.RequestException as rexc:
        return {"statusCode": 502, "body": json.dumps({"error": f"Upstream request failed: {str(rexc)}"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}




# This code was written by ChatGPT

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_reports(event, context):
    """
    Processes messages from SQS (triggered by S3 JSON uploads).
    For the assessment: just log details to CloudWatch.
    """
    for record in event["Records"]:
        body = json.loads(record["body"])
        logger.info(f"Processing report for S3 event: {json.dumps(body)}")

    return {"status": "reports generated"}

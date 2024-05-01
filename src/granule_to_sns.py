import os

import boto3
from mandible.log import init_root_logger, log_errors
from run_cumulus_task import run_cumulus_task

import json


def generate_message(granule) -> dict:
    return {
        "identifier": granule["granuleId"],
        "collection": granule["dataType"],
        "product": {
            "name": granule["granuleId"],
            "files": [
                {
                    "name": file["fileName"],
                    "uri": f"s3://{file['bucket']}/{file['key']}",
                }
                for file in granule["files"]
            ]
        }
    }


def granule_to_sns(event: dict, _):
    client = boto3.client("sns")
    granules = event["input"]["granules"]

    for granule in granules:
        print(granule)
        client.publish(
            TopicArn=os.getenv("SNS_TOPIC_ARN"),
            Message=json.dumps(generate_message(granule)),
        )


def lambda_handler(event, context):
    init_root_logger()
    with log_errors():
        run_cumulus_task(granule_to_sns, event, context)

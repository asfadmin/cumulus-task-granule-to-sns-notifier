import json
import logging
import os

import boto3
from mandible.log import init_root_logger, log_errors
from run_cumulus_task import run_cumulus_task

log = logging.getLogger(__name__)


def generate_message(granule: dict) -> dict:
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
            ],
        },
    }


def granule_to_sns(event: dict, _) -> dict:
    client = boto3.client("sns")
    granules = event["input"]["granules"]

    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")

    for granule in granules:
        message = json.dumps(generate_message(granule))
        log.info("Sending message:\n %s\n to SNS topic %s", message, sns_topic_arn)
        client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            MessageAttributes={
                "collection": {
                    'DataType': 'String',
                    'StringValue': granule["dataType"],
                },
            },
        )

    return event


def lambda_handler(event, context):
    init_root_logger()
    with log_errors():
        return run_cumulus_task(granule_to_sns, event, context)

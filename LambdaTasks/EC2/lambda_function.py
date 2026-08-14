import json
import boto3
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    ec2 = boto3.client("ec2")
    current_date = datetime.now().strftime("%Y-%M-%D")

    try:
        response = ec2.create_snapshot(
            VolumeId="vol-0a9f470c3bba98d57",
            Description="My EC2 Snapshot",
            TagSpecification=[
                {
                    "ResourceType": "snapshot",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": f"My EC2 Snapshot {current_date}"
                        }
                    ]

                }
            ]
        )
        logger.info(
            f"Successfully created a snapshot: {json.dumps(response, default=str)}")

    except Exception as e:
        logger.error(f"Error creating the snapshot {str(e)}")

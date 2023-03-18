import json
from typing import Optional

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import Response, content_types
from models.region_azs import Region

logger = Logger()

available_regions = [
    "us-east-2",
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "ap-east-1",
    "ap-south-1",
    "ap-northeast-3",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "cn-north-1",
    "cn-northwest-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-north-1",
    "me-south-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
]


def get_region_azs(region: str, state: Optional[str] = None) -> dict:
    """
    Get the availability zones for a region.

    Args:
        region (str): AWS Region

    URLs:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_availability_zones.html

    Returns:
        dict: Availability zones for the region
    """

    if region not in available_regions:
        body = {"message": f"region must be one of {available_regions}"}
        return Response(
            status_code=404,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps(body),
        )

    states = ["available", "information", "impaired", "unavailable"]
    if state is None:
        state = "available"
    elif state.lower() not in states:
        body = {"message": f"state must be one of {states}"}
        return Response(
            status_code=404,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps(body),
        )

    ec2 = boto3.client("ec2", region_name=region)
    azs = ec2.describe_availability_zones(
        Filters=[
            {
                "Name": "region-name",
                "Values": [
                    region,
                ],
            },
            {
                "Name": "state",
                "Values": [
                    state,
                ],
            },
        ]
    )

    region_details = Region.parse_obj(azs).dict()
    logger.debug(region_details)
    return region_details.get("availability_zones")

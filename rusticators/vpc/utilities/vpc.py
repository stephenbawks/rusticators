import json
from ipaddress import ip_address, ip_network

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import Response, content_types
from cachetools import LRUCache, cached
from utilities.vpc_layouts import get_vpc_layout
from http import HTTPStatus

logger = Logger()


@cached(cache=LRUCache(maxsize=128))
def generate_vpc(
    vpc_type: str, cidr_block: str, subnet_mask: int, ephemeral: bool
) -> dict:
    """
    Get the layout of a VPC.

    Args:
        vpc_type (str): VPC Type
        cidr_block (str): CIDR Block for the VPC
        subnet_mask (int): Subnet Mask for the VPC

    Returns:
        dict: VPC Layout
    """

    supported_vpc_types = ["a", "b", "s"]

    if vpc_type in {"a", "b"}:
        supported_subnet_masks = [16, 17, 18, 19, 20, 21, 22, 23, 24]
    elif vpc_type in {"s"}:
        supported_subnet_masks = [56]

    if vpc_type not in supported_vpc_types:
        body = {"message": f"vpc_type must a string value of {supported_vpc_types}"}
        print(body)
        return Response(
            status_code=HTTPStatus.BAD_REQUEST.value,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps(body),
        )

    if subnet_mask not in supported_subnet_masks:
        body = {
            "message": f"subnet_mask must be an integer value of {supported_subnet_masks}"
        }
        print(body)
        return Response(
            status_code=HTTPStatus.BAD_REQUEST.value,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps(body),
        )

    try:
        ip_address(cidr_block)
    except ValueError:
        body = {"message": 'cidr_block must be a string formatted like "10.150.0.0/22"'}
        return Response(
            status_code=HTTPStatus.BAD_REQUEST.value,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps(body),
        )

    if not isinstance(ephemeral, bool):
        body = {"message": "ephemeral must be a boolean value"}
        return Response(
            status_code=HTTPStatus.BAD_REQUEST.value,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps(body),
        )

    vpc_details = get_vpc_layout(vpc_type=vpc_type)

    public_subnet_size = vpc_details.get("public").get("block_size")
    number_of_public = vpc_details.get("public").get("number")
    private_subnet_size = vpc_details.get("private").get("block_size")
    number_of_private = vpc_details.get("private").get("number")
    ephemeral_subnet_size = vpc_details.get("ephemeral").get("block_size")
    number_of_ephemeral = vpc_details.get("ephemeral").get("number")

    try:
        available_public_subnets = list(
            ip_network(f"{cidr_block}/{subnet_mask}").subnets(
                prefixlen_diff=public_subnet_size
            )
        )
        available_private_subnets = list(
            ip_network(f"{cidr_block}/{subnet_mask}").subnets(
                prefixlen_diff=private_subnet_size
            )
        )
        available_ephemeral_subnets = list(
            ip_network(f"{cidr_block}/{subnet_mask}").subnets(
                prefixlen_diff=ephemeral_subnet_size
            )
        )
    except ValueError as error:
        return Response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps(error),
        )

    public_subnets = [str(available_public_subnets[item]) for item in number_of_public]
    private_subnets = [
        str(available_private_subnets[item]) for item in number_of_private
    ]
    return_object = {
        "public": public_subnets,
        "private": private_subnets,
    }

    if ephemeral:
        ephemeral_subnets = [
            str(available_ephemeral_subnets[item]) for item in number_of_ephemeral
        ]
        return_object["ephemeral"] = ephemeral_subnets

    logger.debug(return_object)
    return return_object

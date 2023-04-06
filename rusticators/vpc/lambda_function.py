import json

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver,
    Response,
    content_types,
)
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from utilities.region import get_region_azs
from utilities.vpc import generate_vpc

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver(strip_prefixes=["/v1"])


@app.not_found
@tracer.capture_method
def handle_not_found_errors(exc: NotFoundError) -> Response:
    """
    Handle not found paths.

    Args:
        exc (NotFoundError): Not found error

    Returns:
        Response: dict
    """
    logger.info(f"Not found route: {app.current_event.path}")
    return Response(
        status_code=418,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps({"error": "Not found"}),
    )


@app.post("/vpc", compress=True)
def calculate_vpc() -> dict:
    """
    Calculate a VPC.
    """
    try:
        request_data: dict = app.current_event.json_body
    except json.JSONDecodeError as e:
        logger.debug(e)
        return Response(
            status_code=400,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps({"error": "Invalid JSON"}),
        )

    vpc_type = request_data.get("vpc_type")
    cidr_block = request_data.get("cidr_block")
    subnet_mask = request_data.get("subnet_mask")
    ephemeral = request_data.get("ephemeral")
    if ephemeral is None:
        ephemeral = False

    return generate_vpc(
        vpc_type=vpc_type,
        cidr_block=cidr_block,
        subnet_mask=subnet_mask,
        ephemeral=ephemeral,
    )


@app.get("/region/<path_region>", compress=True)
def lookup_region_azs(path_region: str) -> dict:
    """
    Lookup the AZs for a region.

    Args:
        path_region (str): Region - Query String Parameter

    Returns:
        dict: AZs response
    """

    az_state: str = app.current_event.get_query_string_value(
        name="state", default_value="available"
    )

    return get_region_azs(region=path_region, state=az_state)


@tracer.capture_lambda_handler
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    # when setting POWERTOOLS_LOGGER_SAMPLE_RATE env var
    # logger will only log what's defined in the sample rate
    # and turn on debug logging
    logger.debug(event)
    return app.resolve(event, context)

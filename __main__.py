"""Rusticators Pulumi Infrastructure as Code (IaC)"""

import json

import pulumi
import pulumi_aws as aws
import pulumi_aws_native as aws_native
# import pulumi_docker as docker


# ----------------------------------------------------------------
# Pull Stack Variables from Config File
# ----------------------------------------------------------------

config = pulumi.Config()
account_id = (aws.get_caller_identity()).account_id
region = (aws.get_region()).name

environment = pulumi.get_stack()
app_name = pulumi.get_project()
stack_name = f"{environment}-{app_name}"

powertools_layer = config.get("powertools_layer")
lambda_memory = config.get_int("lambda_vpc_memory")

api_domain_name = config.require("api_domain_name")
certificate_arn = config.require("certificate_arn")
route_53_zone_id = config.require("route_53_zone")

# ------------------------------------------------------------------------------------
# Lambda Function
# https://www.pulumi.com/registry/packages/aws/api-docs/lambda/function/
# ------------------------------------------------------------------------------------

lambda_assume_role_trust = aws.iam.get_policy_document(
    statements=[
        aws.iam.GetPolicyDocumentStatementArgs(
            actions = ["sts:AssumeRole"],
            principals = [aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type = "Service",
                    identifiers = ["lambda.amazonaws.com"]
                )
            ],
        ),
    ]
)

lambda_vpc_policy = aws.iam.get_policy_document(
    statements=[
        aws.iam.GetPolicyDocumentStatementArgs(
            actions = ["ec2:DescribeAvailabilityZones"],
            resources = ["*"],
        ),
    ]
)

vpc_lambda_role = aws.iam.Role(
    f"{stack_name}-vpc-lambda-role",
    assume_role_policy = lambda_assume_role_trust.json,
    managed_policy_arns = [
        "arn:aws:iam::aws:policy/CloudWatchLambdaInsightsExecutionRolePolicy",
        "arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
)

aws.iam.RolePolicy(
    f"{stack_name}-lambda-vpc-policy",
    role = vpc_lambda_role.id,
    policy = lambda_vpc_policy.json,
    opts=pulumi.ResourceOptions(parent=vpc_lambda_role)
)

vpc_function = aws.lambda_.Function(
    "vpc-function",
    architectures = ["arm64"],
    memory_size = lambda_memory,
    role = vpc_lambda_role.arn,
    timeout = 10,
    runtime="python3.9",
    code = pulumi.FileArchive("./src/vpc"),
    layers = [
        powertools_layer
    ],
    handler="lambda_function.lambda_handler",
    tracing_config = aws.lambda_.FunctionTracingConfigArgs(mode="Active"),
    environment = aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "ENVIRONMENT": environment,
        }
    )
)


# ------------------------------------------------------------------------------------
# HTTP API Gateway
# ------------------------------------------------------------------------------------

httpApi = aws.apigatewayv2.Api(
    f"{stack_name}-api",
    protocol_type="HTTP"
)

httpApiLogs = aws.cloudwatch.LogGroup(
    f"{stack_name}-api-logs",
    name=f"{stack_name}-api-logs",
    retention_in_days=config.get_int("logs_retention_days") or 14,
    opts=pulumi.ResourceOptions(parent=httpApi)
)

httpApiStage = aws.apigatewayv2.Stage(
    f"{stack_name}-api-stage",
    api_id = httpApi,
    access_log_settings = aws.apigatewayv2.StageAccessLogSettingsArgs(
        destination_arn=httpApiLogs.arn,
        format='{"requestId":"$context.requestId", "ip": "$context.identity.sourceIp", "requestTime":"$context.requestTime", "httpMethod":"$context.httpMethod","routeKey":"$context.routeKey", "status":"$context.status","protocol":"$context.protocol", "responseLength":"$context.responseLength","integrationRequestId":"$context.integration.requestId","integrationStatus":"$context.integration.integrationStatus","integrationLatency":"$context.integrationLatency","integrationErrorMessage":"$context.integrationErrorMessage","errorMessageString":"$context.error.message","authorizerError":"$context.authorizer.error"}'
    ),
    auto_deploy = True,
    opts = pulumi.ResourceOptions(parent=httpApi)
)

# ------------------------------------------------------------------------------------
# Lambda API Query - HTTP API Gateway Settings
# ------------------------------------------------------------------------------------

vpc_lambda_api_integration = aws.apigatewayv2.Integration(
    f"{stack_name}-integration",
    api_id = httpApi.id,
    integration_type = "AWS_PROXY",
    connection_type = "INTERNET",
    description = "Lambda API Integration",
    integration_method = "POST",
    payload_format_version = "2.0",
    integration_uri = vpc_function.invoke_arn,
    passthrough_behavior = "WHEN_NO_MATCH",
    opts = pulumi.ResourceOptions(parent=httpApi)
)

aws.lambda_.Permission(
    "api-invoke-vpc-lambda-permission",
    action = "lambda:InvokeFunction",
    function = vpc_function.name,
    principal = "apigateway.amazonaws.com",
    source_arn = httpApi.execution_arn.apply(lambda execution_arn: f"{execution_arn}/*/*/*"),
    opts = pulumi.ResourceOptions(parent=vpc_lambda_api_integration, depends_on=[vpc_lambda_api_integration, httpApiStage])
)

aws.apigatewayv2.Route(
    f"{stack_name}-post-route",
    api_id = httpApi.id,
    route_key = "POST /{proxy+}",
    authorization_type = "NONE",
    target = vpc_lambda_api_integration.id.apply(lambda id: f"integrations/{id}"),
    opts = pulumi.ResourceOptions(parent=httpApi, delete_before_replace=True)
)

aws.apigatewayv2.Route(
    f"{stack_name}-get-route",
    api_id = httpApi.id,
    route_key = "GET /{proxy+}",
    authorization_type = "NONE",
    target = vpc_lambda_api_integration.id.apply(lambda id: f"integrations/{id}"),
    opts = pulumi.ResourceOptions(parent=httpApi, delete_before_replace=True)
)


# ------------------------------------------------------------------------------------
# API GAteway Domain Name and Route53 Record
# https://www.pulumi.com/registry/packages/aws/api-docs/cognito
# ------------------------------------------------------------------------------------

httpDomainName = aws.apigatewayv2.DomainName(
    f"{stack_name}-domain",
    domain_name = api_domain_name,
    domain_name_configuration = aws.apigatewayv2.DomainNameDomainNameConfigurationArgs(
        certificate_arn = certificate_arn,
        endpoint_type = "REGIONAL",
        security_policy = "TLS_1_2",
    )
)

domain_name_mapping_v1 = aws.apigatewayv2.ApiMapping(
    f"{stack_name}-v1-mapping",
    api_id = httpApi.id,
    domain_name = httpDomainName,
    api_mapping_key="v1",
    stage = httpApiStage.id
)

# https://www.pulumi.com/registry/packages/aws/api-docs/route53/record/
aws.route53.Record(
    f"{stack_name}-route-record",
    name = httpDomainName,
    type = "A",
    zone_id = route_53_zone_id,
    aliases = [aws.route53.RecordAliasArgs(
        name = httpDomainName.domain_name_configuration.target_domain_name,
        zone_id = httpDomainName.domain_name_configuration.hosted_zone_id,
        evaluate_target_health = False,
    )],
    opts=pulumi.ResourceOptions(
        depends_on=[domain_name_mapping_v1],
        parent=domain_name_mapping_v1
    )
)

# ------------------------------------------------------------------------------------
# Exports
# ------------------------------------------------------------------------------------

pulumi.export("httpApi", httpApi.execution_arn)
pulumi.export("httpApiStage", httpApiStage.name)
pulumi.export("httpApiMappingV1", domain_name_mapping_v1.api_mapping_key)
pulumi.export("httpDomainName", httpDomainName.domain_name)
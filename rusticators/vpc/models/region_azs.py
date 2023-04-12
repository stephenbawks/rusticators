from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AvailabilityZone(BaseModel):
    state: str = Field(..., alias="State")
    opt_in_status: str = Field(..., alias="OptInStatus")
    messages: List = Field(..., alias="Messages")
    region_name: str = Field(..., alias="RegionName")
    zone_name: str = Field(..., alias="ZoneName")
    zone_id: str = Field(..., alias="ZoneId")
    group_name: str = Field(..., alias="GroupName")
    network_border_group: str = Field(..., alias="NetworkBorderGroup")
    zone_type: str = Field(..., alias="ZoneType")


class HttpHeaders(BaseModel):
    x_amzn_requestid: str = Field(..., alias="x-amzn-requestid")
    cache_control: str = Field(..., alias="cache-control")
    strict_transport_security: str = Field(..., alias="strict-transport-security")
    content_type: str = Field(..., alias="content-type")
    content_length: str = Field(..., alias="content-length")
    date: str
    server: str


class ResponseMetadata(BaseModel):
    request_id: str = Field(..., alias="RequestId")
    http_status_code: int = Field(..., alias="HTTPStatusCode")
    http_headers: HttpHeaders = Field(..., alias="HTTPHeaders")
    retry_attempts: int = Field(..., alias="RetryAttempts")


class Region(BaseModel):
    availability_zones: Optional[List[AvailabilityZone]] = Field(
        None, alias="AvailabilityZones"
    )
    response_metadata: Optional[ResponseMetadata] = Field(
        None, alias="ResponseMetadata"
    )

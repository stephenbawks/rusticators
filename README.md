# Rusticators
- [Rusticators](#rusticators)
- [API](#api)
  - [Base API URL](#base-api-url)
- [VPC's](#vpcs)
  - [Generating VPC Layout](#generating-vpc-layout)
    - [Example Request](#example-request)
    - [Example Response](#example-response)
  - [VPC Types](#vpc-types)
  - [Using VPC Layout in IAC](#using-vpc-layout-in-iac)


Rusticators API is capable of doing a few things with the intention of adding more in the future.

# API

Cutting  to the chase, here are the instructions for communicating with the API. As well as the endpoints and what each one is doing.

## Base API URL
https://api.rusticators.dev


# VPC's

VPC layouts and subnetting can be difficult.  Created this years ago and wanted to finally get around to making this available to others with the hope that it could help other people with their VPC design and layouts. The way this works is that you can use any 10.x range to create a VPC and it will calculate the appropiate subnet layout depending on what VPC Type you select.

There are a few different layouts that I have found to work well.  The catch with subnet math is that most of the time it does not play well with being able to use the full amount of IP space.  Add in the fact that each subnet in AWS has an overhead of 5 IPs that are unuseable as they are reservered for AWS networking reasons. There is a little trade-off or balance between trying to achieve the most amount of unsable space while also providing a VPC layout that offers up some protection for "blast radius" and general high availability best practices.

Typically I generally reccomend a VPC with three availability zones, however there are a few locations where three is not possible.  I have also included a VPC layout that is built around 2 availability zones.

## Generating VPC Layout

When requesting a VPC layout you just need to make sure that you are sending a `POST` request to the VPC endpoint. You also just need to pass in the required variables to have it generate you a layout. You can use the example below and amend it as needed.

- POST: `https://api.rusticators.dev/v1/vpc`

| Variables     | Required |
|---------------|----------|
| `vpc_type`    | Yes      |
| `cidr_block`  | Yes      |
| `subnet_mask` | Yes      |
| `ephemeral`   | No       |

### Example Request
```json
{
    "vpc_type": "b",
    "cidr_block": "10.144.0.0",
    "subnet_mask": 17,
    "ephemeral": true
}
```

### Example Response
```json
{
    "public": [
        "10.144.0.0/21",
        "10.144.8.0/21",
        "10.144.16.0/21"
    ],
    "private": [
        "10.144.32.0/19",
        "10.144.64.0/19",
        "10.144.96.0/19"
    ],
    "ephemeral": [
        "10.144.24.0/21"
    ]
}
```

## VPC Types

You can generate VPC Types of `A` and `B` at the moment but more can be added easily if need be.

Check out the [VPC Types page](/docs/vpc_layouts.md) for more details on each of the VPC types.

## Using VPC Layout in IAC

Couple of examples of how you can use the VPC layout in your IAC.  I have included examples for both Terraform and Pulumi.

Check out some examples [here](/docs/vpc_layouts.md#using-vpc-layout-in-iac)

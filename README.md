# Rusticators
- [Rusticators](#rusticators)
- [API](#api)
  - [Base API URL](#base-api-url)
- [VPC's](#vpcs)
  - [Body](#body)
  - [VPC Types](#vpc-types)
    - [Type A](#type-a)
      - [Subnet Mask](#subnet-mask)
    - [Type B](#type-b)
      - [Subnet Mask](#subnet-mask-1)


Rusticators API is capable of doing a few things with the intention of adding more in the future.

# API

Cutting the chase, here are the instructions for communicating with the API. As well as the endpoints and what each one is doing.

## Base API URL
https://api.rusticators.dev


# VPC's

VPC layouts and subnetting can be difficult.  Created this years ago and wanted to finally get around to making this available to others with the hope that it could help other people with their VPC design and layouts. The way this works is that you can use any 10.x range to create a VPC and it will calculate the appropiate subnet layout depending on what VPC Type you select.

There are a few different layouts that I have found to work well.  The catch with subnet math is that most of the time it does not play well with being able to use the full amount of IP space.  Add in the fact that each subnet in AWS has an overhead of 5 IPs that are unuseable as they are reservered for AWS networking reasons. There is a little trade-off or balance between trying to achieve the most amount of unsable space while also providing a VPC layout that offers up some protection for "blast radius" and general high availability best practices.

Typically I generally reccomend a VPC with three availability zones, however there are a few locations where three is not possible.  I have also included a VPC layout that is built around 2 availability zones.

## Body

When requesting a VPC layout you just need to make sure that you are sending a `POST` request to the VPC endpoint. You also just need to pass in the required variables to have it generate you a layout. You can use the example below and amend it as needed.

- URL: `https://api.rusticators.dev/v1/vpc`

```json
{
    "vpc_type": "b",
    "cidr_block": "10.144.0.0",
    "subnet_mask": 17,
    "ephemeral": true
}
```

## VPC Types

You can generate VPC Types of `A` and `B` at the moment but more can be added easily if need be.

### Type A
This VPC is my most generally prescribed layout.  It is laid out over three availability zones and offers what I feel is the most protection in case of outages.


#### Subnet Mask
You can create an `A` type with any of the following VPC Subnet masks.

* 16, 17, 18, 19, 20, 21, 22, 23, 24

| /16        | AZ 1           | AZ 2             | AZ 3            |
|------------|----------------|------------------|-----------------|
| Public     | 10.144.0.0/20  | 10.144.16.0/20   | 10.144.32.0/20  |
| Private    | 10.144.64.0/18 | 10.144.128.0/18  | 10.144.192.0/18 |
| Ephemeral  | 10.144.48.0/20 |                  |                 |


| /17        | AZ 1           | AZ 2             | AZ 3            |
|------------|----------------|------------------|-----------------|
| Public     | 10.144.0.0/21  | 10.144.8.0/21    | 10.144.16.0/21  |
| Private    | 10.144.32.0/19 | 10.144.64.0/19   | 10.144.96.0/19  |
| Ephemeral  | 10.144.24.0/21 |                  |                 |

| /18        | AZ 1           | AZ 2             | AZ 3            |
|------------|----------------|------------------|-----------------|
| Public     | 10.144.0.0/22  | 10.144.4.0/22    | 10.144.8.0/22   |
| Private    | 10.144.16.0/20 | 10.144.32.0/20   | 10.144.48.0/20  |
| Ephemeral  | 10.144.12.0/22 |                  |                 |

### Type B

The `B` type is laid out over 2 availbility zones.

There are reasons you may only want two availability zones.  The most obvious reason is that there are that some regions only have two availability zones.  Another reason may be focused around costs.  While you are not being billed for extra subnets, if your VPC has NAT gateways in each availability zone you will certainly be paying for those.

#### Subnet Mask

You can create an `B` type with any of the following VPC Subnet masks.

- 16, 17, 18, 19, 20, 21, 22, 23, 24



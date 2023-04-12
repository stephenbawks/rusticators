# VPC Layouts
- [VPC Layouts](#vpc-layouts)
  - [VPC Types](#vpc-types)
    - [Ephemeral Subnet](#ephemeral-subnet)
    - [Type A](#type-a)
      - [Subnet Mask](#subnet-mask)
    - [Type B](#type-b)
      - [Subnet Mask](#subnet-mask-1)
  - [Using VPC Layout in IAC](#using-vpc-layout-in-iac)
    - [Terraform](#terraform)


## VPC Types

You can generate VPC Types of `A` and `B` at the moment but more can be added easily if need be.

> **Note**
>
> All the VPC layouts are based on the CIDR block of `10.144.0.0` however you can change this to any CIDR block you want. As long as you are using anything in the 10.x.x.x range you should be fine.

### Ephemeral Subnet
First off, the ephemeral subnet is completely optional. You do not need to use it.

Both `A` and `B` types have an ephemeral subnet option.  This subnet is used for instances that are short lived and don't need to be persistent. This subnet was added because there is "extra" subnet space that is available in the VPC as CIDR math does not always perfectly divide the VPC into equal parts.  Being that there is only one ephermal subnet this subnet is not used for anything other than short lived instances.  A classic example has always been for a jumpbox or bastion host.

### Type A

This VPC is my most generally prescribed layout.  It is laid out over three availability zones and offers what I feel is the most protection in case of outages.

#### Subnet Mask

You can create an `A` type with any of the following VPC Subnet masks.

- 16, 17, 18, 19, 20, 21, 22, 23, 24

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

| /19        | AZ 1           | AZ 2             | AZ 3            |
|------------|----------------|------------------|-----------------|
| Public     | 10.144.0.0/23  | 10.144.2.0/23    | 10.144.4.0/23   |
| Private    | 10.144.8.0/21  | 10.144.16.0/21   | 10.144.24.0/21  |
| Ephemeral  | 10.144.6.0/23  |                  |                 |

| /20        | AZ 1           | AZ 2             | AZ 3            |
|------------|----------------|------------------|-----------------|
| Public     | 10.144.0.0/24  | 10.144.1.0/24    | 10.144.2.0/24   |
| Private    | 10.144.4.0/22  | 10.144.8.0/22    | 10.144.12.0/22  |
| Ephemeral  | 10.144.3.0/24  |                  |                 |

| /21        | AZ 1           | AZ 2             | AZ 3            |
|------------|----------------|------------------|-----------------|
| Public     | 10.144.0.0/25  | 10.144.0.128/25  | 10.144.1.0/25   |
| Private    | 10.144.2.0/23  | 10.144.4.0/23    | 10.144.6.0/23   |
| Ephemeral  | 10.144.1.128/25|                  |                 |

| /22        | AZ 1           | AZ 2             | AZ 3            |
|------------|----------------|------------------|-----------------|
| Public     | 10.144.0.0/26  | 10.144.0.64/26   | 10.144.0.128/26 |
| Private    | 10.144.1.0/24  | 10.144.2.0/24    | 10.144.3.0/24   |
| Ephemeral  | 10.144.0.192/26|                  |                 |

| /23        | AZ 1           | AZ 2             | AZ 3            |
|------------|----------------|------------------|-----------------|
| Public     | 10.144.0.0/27  | 10.144.0.32/27   | 10.144.0.64/27  |
| Private    | 10.144.0.128/25| 10.144.1.0/25    | 10.144.1.128/25 |
| Ephemeral  | 10.144.0.96/27 |                  |                 |

| /24        | AZ 1           | AZ 2             | AZ 3            |
|------------|----------------|------------------|-----------------|
| Public     | 10.144.0.0/28  | 10.144.0.16/28   | 10.144.0.32/28  |
| Private    | 10.144.0.64/26 | 10.144.0.128/26  | 10.144.0.196/26 |
| Ephemeral  | 10.144.0.48/28 |                  |                 |

### Type B

The `B` type is laid out over 2 availbility zones.

There are reasons you may only want two availability zones.  The most obvious reason is that there are that some regions only have two availability zones.  Another reason may be focused around costs.  While you are not being billed for extra subnets, if your VPC has NAT gateways in each availability zone you will certainly be paying for those.

#### Subnet Mask

You can create an `B` type with any of the following VPC Subnet masks.

- 16, 17, 18, 19, 20, 21, 22, 23, 24


| /16        | AZ 1           | AZ 2             |
|------------|----------------|------------------|
| Public     | 10.144.0.0/19  | 10.144.32.0/19   |
| Private    | 10.144.128.0/18| 10.144.192.0/18  |
| Ephemeral  | 10.144.64.0/19 |                  |

| /17        | AZ 1           | AZ 2             |
|------------|----------------|------------------|
| Public     | 10.144.0.0/20  | 10.144.16.0/20   |
| Private    | 10.144.64.0/19 | 10.144.96.0/19   |
| Ephemeral  | 10.144.32.0/20 |                  |

| /18        | AZ 1           | AZ 2             |
|------------|----------------|------------------|
| Public     | 10.144.0.0/21  | 10.144.8.0/21    |
| Private    | 10.144.32.0/20 | 10.144.48.0/20   |
| Ephemeral  | 10.144.16.0/21 |                  |

| /19        | AZ 1           | AZ 2             |
|------------|----------------|------------------|
| Public     | 10.144.0.0/22  | 10.144.4.0/22    |
| Private    | 10.144.16.0/21 | 10.144.24.0/21   |
| Ephemeral  | 10.144.8.0/22  |                  |

| /20        | AZ 1           | AZ 2             |
|------------|----------------|------------------|
| Public     | 10.144.0.0/23  | 10.144.2.0/23    |
| Private    | 10.144.8.0/22  | 10.144.12.0/22   |
| Ephemeral  | 10.144.4.0/23  |                  |

| /21        | AZ 1           | AZ 2             |
|------------|----------------|------------------|
| Public     | 10.144.0.0/24  | 10.144.1.0/24    |
| Private    | 10.144.4.0/23  | 10.144.6.0/23    |
| Ephemeral  | 10.144.2.0/24  |                  |

| /22        | AZ 1           | AZ 2             |
|------------|----------------|------------------|
| Public     | 10.144.0.0/25  | 10.144.0.128/25  |
| Private    | 10.144.2.0/24  | 10.144.3.0/24    |
| Ephemeral  | 10.144.2.0/25  |                  |

| /23        | AZ 1           | AZ 2             |
|------------|----------------|------------------|
| Public     | 10.144.0.0/26  | 10.144.0.64/26   |
| Private    | 10.144.1.0/25  | 10.144.1.128/25  |
| Ephemeral  | 10.144.0.128/26|                  |

| /24        | AZ 1           | AZ 2             |
|------------|----------------|------------------|
| Public     | 10.144.0.0/27  | 10.144.0.32/27   |
| Private    | 10.144.0.128/26| 10.144.0.192/26  |
| Ephemeral  | 10.144.0.64/27 |                  |

## Using VPC Layout in IAC

One thing I have run into many times before is trying to do a bunch of conditional logic in Terraform.   Not saying it cannot be done, but depending on what you are trying to do it sometimes feels like a square-peg-round-hole situation.

That being said, I sat down and wondered if there might not be a way I can just pull all the logic out of just make it much simplier and move the logic somewhere else.  Yes, I suppose I am just moving the problem somewhere else, but I think it is a better place.  Its also someplace where I can use a real programming language and handle changes and versions much nicer.

### Terraform

```hcl
data "http" "vpc_layout" {
  url    = "https://api.rusticators.dev/v1/vpc"
  method = "POST"

  request_body = jsonencode({
    "vpc_type"    = var.vpc_type,
    "cidr_block"  = var.cidr_block,
    "subnet_mask" = var.subnet_mask,
    "ephemeral"   = var.ephemeral_subnet
  })
}

resource "aws_vpc" "main" {
  cidr_block = "${var.cidr_block}/${var.subnet_mask}"
}


resource "aws_subnet" "public_subnets" {
  for_each   = toset(jsondecode(data.http.vpc_layout.response_body).public)
  vpc_id     = aws_vpc.main.id
  cidr_block = each.value
}

resource "aws_subnet" "private_subnets" {
  for_each   = toset(jsondecode(data.http.vpc_layout.response_body).private)
  vpc_id     = aws_vpc.main.id
  cidr_block = each.value
}

resource "aws_subnet" "private_subnets" {
  for_each   = toset(jsondecode(data.http.vpc_layout.response_body).private)
  vpc_id     = aws_vpc.main.id
  cidr_block = each.value
}

resource "aws_subnet" "ephemeral_subnet" {
  count      = var.ephemeral_subnet ? 1 : 0
  for_each   = toset(jsondecode(data.http.vpc_layout.response_body).ephemeral)
  vpc_id     = aws_vpc.main.id
  cidr_block = each.value
}


# output "name" {
#   value = jsondecode(data.http.vpc_layout.response_body).public
# }


```


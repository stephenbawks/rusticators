# Rusticators
- [Rusticators](#rusticators)
- [VPC's](#vpcs)
  - [VPC Types](#vpc-types)
    - [Type A](#type-a)
      - [Subnet Mask](#subnet-mask)
    - [Type B](#type-b)
      - [Subnet Mask](#subnet-mask-1)


Rusticators API is capable of doing a few things with the intention of adding more in the future.

# VPC's

VPC layouts and subnetting can be difficult.  Created this years ago and wanted to finally get around to making this available to others with the hope that it could help other people with their VPC design and layouts. The way this works is that you can use any 10.x range to create a VPC and it will calculate the appropiate subnet layout depending on what VPC Type you select.

There are a few different layouts that I have found to work well.  The catch with subnet math is that most of the time it does not play well with being able to use the full amount of IP space.  Add in the fact that each subnet in AWS has an overhead of 5 IPs that are unuseable as they are reservered for AWS networking reasons. There is a little trade-off or balance between trying to achieve the most amount of unsable space while also providing a VPC layout that offers up some protection for "blast radius" and general high availability best practices.

Typically I generally reccomend a VPC with three availability zones, however there are a few locations where three is not possible.  I have also included a VPC layout that is built around 2 availability zones.

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


#### Subnet Mask

You can create an `B` type with any of the following VPC Subnet masks.

- 16, 17, 18, 19, 20, 21, 22, 23, 24



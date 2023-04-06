# VPC Layouts
- [VPC Layouts](#vpc-layouts)
  - [VPC Types](#vpc-types)
    - [Type A](#type-a)
      - [Subnet Mask](#subnet-mask)
    - [Type B](#type-b)
      - [Subnet Mask](#subnet-mask-1)


## VPC Types

You can generate VPC Types of `A` and `B` at the moment but more can be added easily if need be.

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

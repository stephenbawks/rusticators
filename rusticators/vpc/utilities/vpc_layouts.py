def get_vpc_layout(vpc_type: str) -> dict:
    vpc_types = {
        "a": {
            "public": {
                "block_size": 4,
                "number": [0, 1, 2],
            },
            "private": {
                "block_size": 2,
                "number": [1, 2, 3],
            },
            "ephemeral": {
                "block_size": 4,
                "number": [3],
            },
            "ip_type": "ipv4",
        },
        "b": {
            "public": {
                "block_size": 3,
                "number": [0, 1],
            },
            "private": {
                "block_size": 2,
                "number": [2, 3],
            },
            "ephemeral": {
                "block_size": 3,
                "number": [2],
            },
            "ip_type": "ipv4",
        },
        "s": {
            "public": {
                "block_size": 8,
                "number": [0, 1, 2, 3],
            },
            "private": {
                "block_size": 8,
                "number": [4, 5, 6, 7],
            },
            "ephemeral": {
                "block_size": 8,
                "number": [8],
            },
            "ip_type": "ipv6",
        },
    }

    return vpc_types.get(vpc_type)

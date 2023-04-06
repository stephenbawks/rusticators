def get_vpc_layout(vpc_type: str) -> dict:
    vpc_types = {
        "a16": {
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
        },
        "a17": {
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
        },
        "a18": {
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
        },
        "a19": {
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
        },
        "a20": {
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
        },
        "a21": {
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
        },
        "a22": {
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
        },
        "a23": {
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
        },
        "a24": {
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
        },
        "b20": {
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
        },
        "b21": {
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
        },
        "b22": {
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
        },
    }

    return vpc_types.get(vpc_type)

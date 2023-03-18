ARG LAMBDA_TASK_ROOT="/var/task"
FROM --platform=arm64 python:3.11.2-slim-bullseye AS build-image
RUN apt-get update && \
    apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev

ARG LAMBDA_TASK_ROOT
RUN mkdir -p ${LAMBDA_TASK_ROOT}

COPY ./app ${LAMBDA_TASK_ROOT}
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt --target ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir --upgrade --target ${LAMBDA_TASK_ROOT} awslambdaric


FROM --platform=arm64 python:3.11.2-slim-bullseye

ARG LAMBDA_TASK_ROOT
WORKDIR ${LAMBDA_TASK_ROOT}

COPY --from=build-image ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}

ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]

CMD ["lambda_function.lambda_handler"]

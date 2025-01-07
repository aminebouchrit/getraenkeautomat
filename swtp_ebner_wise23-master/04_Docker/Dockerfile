FROM python:3.10-alpine

WORKDIR /app

COPY /docker_python_lib_requirements.txt .

RUN apk add --no-cache gcc && \
    apk add --no-cache libc-dev && \
    apk add --no-cache mariadb-connector-c-dev && \
    pip3 install --no-cache-dir -r docker_python_lib_requirements.txt

COPY . .

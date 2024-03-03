FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
LABEL authors="tiago98751"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./src /app
# syntax=docker/dockerfile:1
FROM python:3.13-rc-alpine

WORKDIR /api-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
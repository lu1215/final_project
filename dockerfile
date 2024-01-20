FROM python:3.10.12
LABEL maintainer="shangyi"
LABEL version="1.0"
LABEL description="Liver cancer screener web image"
ENV PYTHONUNBUFFERED 1
RUN mkdir /final_project
WORKDIR /final_project
COPY . /final_project/
RUN pip install -r requirements.txt
FROM techblog/fastapi:latest

LABEL maintainer="tomer.klein@gmail.com"


ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LOG_LEVEL "DEBUG"
ENV SEARCH_ENGINE_ID ""
ENV CSE_API_KEY ""
RUN apt update -yqq

RUN apt install -yqq python3-pip && \
    apt install -yqq libffi-dev && \
    apt install -yqq libssl-dev

RUN mkdir -p /app/{keys,config,db}

COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

EXPOSE 80

COPY app /app

WORKDIR /app

ENTRYPOINT ["/usr/bin/python3", "/app/app.py"]
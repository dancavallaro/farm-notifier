FROM ubuntu:22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip curl unzip

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY src/*.py /farm-notifier/
COPY sql/*.sql /farm-notifier/sql/
RUN chmod +x /farm-notifier/run.py

WORKDIR /farm-notifier


FROM base AS farm-notifier

RUN apt-get update && apt-get install -y \
    libglib2.0-dev libnss3-dev libatk-bridge2.0-dev libcups2 libdrm-dev libxkbcommon-dev \
    libxcomposite-dev libxdamage-dev libxrandr-dev libgbm-dev libgtk-3-dev libasound-dev

COPY bin/install-browser.sh /tmp
RUN /tmp/install-browser.sh

ENTRYPOINT [ "python3", "run.py" ]


FROM base AS debugger

RUN apt-get update && apt-get install -y sqlite3

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip \
    && unzip /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/awscliv2.zip /tmp/aws

ENTRYPOINT [ "sleep", "infinity" ]

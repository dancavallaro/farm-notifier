FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3 python3-pip curl unzip \
    libglib2.0-dev libnss3-dev libatk-bridge2.0-dev libcups2 libdrm-dev libxkbcommon-dev \
    libxcomposite-dev libxdamage-dev libxrandr-dev libgbm-dev libgtk-3-dev libasound-dev

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY bin/install-browser.sh /tmp
RUN /tmp/install-browser.sh

COPY src/ /website-parser/

WORKDIR /website-parser

ENTRYPOINT [ "python3" ]

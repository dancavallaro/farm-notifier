#!/usr/bin/env bash

CHROMEDRIVER_VERSION=89.0.4389.23
CHROMIUM_VERSION=843831

curl -Lo /tmp/chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip -q /tmp/chromedriver_linux64.zip -d /opt/chromedriver/

curl -Lo /tmp/chrome-linux.zip "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F${CHROMIUM_VERSION}%2Fchrome-linux.zip?alt=media"
unzip -q /tmp/chrome-linux.zip -d /opt/chrome/

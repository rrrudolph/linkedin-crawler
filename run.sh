#!/usr/bin/env bash

set -e

cd crawl
poetry shell
poetry install

set -o allexport && source ../.env && set +o allexport

sed -i "s~{'EMAIL'}~$LOGIN~" "$pwd/crawler/spiders/linkedin.py"
sed -i "s~{'PASS'}~$PASSWORD~" "$pwd/crawler/spiders/linkedin.py"

scrapy crawl linkedin -o data.json
#!/bin/bash


cp -r /statichtml /usr/share/nginx/html

find /usr/share/nginx/html -type f -exec sed -i "s/%%API_ENDPOINT_URL%%/$API_ENDPOINT_URL/g" {} \;


/docker-entrypoint.sh

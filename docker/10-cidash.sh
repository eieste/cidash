#!/bin/sh


cd /statichtml; cp -r ./* /usr/share/nginx/html

find /usr/share/nginx/html -type f -exec sed -i "s/%%API_ENDPOINT_URL%%/$API_ENDPOINT_URL/g" {} \;


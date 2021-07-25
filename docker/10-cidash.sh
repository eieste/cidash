#!/bin/sh


cd /statichtml; cp -r ./* /usr/share/nginx/html

find /usr/share/nginx/html/ -type f -print0 | xargs -0 -I {} sed -i "s|%%API_ENDPOINT_URL%%|${API_ENDPOINT_URL}|g" {}


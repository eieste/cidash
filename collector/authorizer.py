import json
import logging
from jsonschema import validate, Draft7Validator, validators
import boto3
from boto3.dynamodb.conditions import Key
import functools
import os
import hashlib
from exceptions import InvalidVersion, ValidationError, UnautorizedAccess
from datetime import datetime, timezone
import re


log = logging.getLogger(__name__)
s3 = boto3.client("s3")
MIN_EQ_VERSION = "19-07-2021"

@functools.lru_cache()
def get_config():
    response = s3.get_object(
            Bucket=os.environ.get("STORE_BUCKET"),
            Key="config.json")
    #config_data = json.load(response.get("Body"))

    with open("./config.json", "r") as fobj:
        config_data = json.load(fobj)

    if datetime.strptime(config_data.get("version"), '%d-%m-%Y') >= datetime.strptime(MIN_EQ_VERSION, '%d-%m-%Y'):
        with open("./config.schema.json", "r") as fobj:
            raw_schema = json.load(fobj)
            validate(instance=config_data, schema=raw_schema)
            DefaultValidatingDraft7Validator(raw_schema).validate(config_data)
        return config_data

    raise InvalidVersion("config.json has an invalid json")

def check_hook_auth(lambda_event):
    config = get_config()
    if lambda_event.get("queryStringParameters").get("key") == config.get("accessToken"):
        return True
    raise UnauthorizedAccess("Permission denied")


def check_user_auth(lambda_event):
    log.debug(lambda_event)
    auth_header = lambda_event.get("headers", {}).get("Authorization", ":")
    credentials = [item.strip() for item in auth_header[6:].split(":")]
    config = get_config()
    pwhash = hashlib.sha512(credentials[1]+config.get("privateToken"))
    for user in config.get("users"):
        if user.get("username") == credentials[0] and \
                user.get("password") == pwhash:
                    return True
    raise UnautorizedAccess("You are not allowed to access")


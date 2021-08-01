import functools
import os
import json
import boto3
from cidash.contrib.schema import DefaultValidatingDraft7Validator, validate
from datetime import datetime
from cidash.contrib.exceptions import InvalidVersion

s3 = boto3.client("s3")

MIN_EQ_VERSION = "19-07-2021"

@functools.lru_cache()
def get_config():
    response = s3.get_object(Bucket=os.environ.get("STORE_BUCKET"), Key="config.json")
    config_data = json.load(response.get("Body"))

    if datetime.strptime(config_data.get("version"), "%d-%m-%Y") >= datetime.strptime(
        MIN_EQ_VERSION, "%d-%m-%Y"
    ):
        with open(os.path.join(os.getcwd(), "cidash/schemas/config.schema.json"), "r") as fobj:
            raw_schema = json.load(fobj)
            validate(instance=config_data, schema=raw_schema)
            DefaultValidatingDraft7Validator(raw_schema).validate(config_data)
        return config_data

    raise InvalidVersion("config.json has an invalid json")

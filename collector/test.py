from cidash.contrib.schema import DefaultValidatingDraft7Validator, validate
import os
import json

config_data =""
with open(os.path.join(os.getcwd(), "config.json")) as fobj:
    config_data = json.load(fobj)

with open(os.path.join(os.getcwd(), "cidash/schemas/config.schema.json"), "r") as fobj:
    raw_schema = json.load(fobj)
    validate(instance=config_data, schema=raw_schema)
    DefaultValidatingDraft7Validator(raw_schema).validate(config_data)


for item in config_data.get("eventResource"):
    if "github" == item.get("eventSource"):
        print(item)

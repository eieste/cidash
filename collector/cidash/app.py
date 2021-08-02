import json
import logging
from cidash.contrib.schema import Draft7Validator, validate
import boto3
from boto3.dynamodb.conditions import Key
import os
from cidash.contrib.exceptions import (
    InvalidVersion,
    ValidationError,
    UnauthorizedAccess,
)
from cidash.contrib.settings import get_config
from cidash.contrib.miscellaneous import md5, find_event_config, save_event
from cidash.contrib.auth import check_hook_auth, check_user_auth

from cidash.hooks.github import hook_handle_github
from cidash.hooks.aws import hook_handle_sns_cfn, extract_cfn_msg

import urllib.request

log = logging.getLogger(__name__)
s3 = boto3.client("s3")
dd = boto3.resource("dynamodb")

def lambda_handler(lambda_event, lambda_context):
    try:
        return general_handler(lambda_event, lambda_context)
    except Exception as e:
        log.exception(e)
        return wrap_response(
            {
                "state": "error",
                "errors": [{"title": e.__class__.__name__, "message": str(e)}],
            },
            status_code=500,
        )

def general_handler(lambda_event, lambda_context):
    print(lambda_event)
    if lambda_event.get("httpMethod", "").lower() in ["options", "head"]:
        return wrap_response({})

    if lambda_event.get("Records", False):
        record = lambda_event.get("Records")[0]

        if record.get("EventSource") == "aws:sns":
            cfn_str = record.get("Sns", {}).get("Message", "").strip()
            cfn_msg = extract_cfn_msg(cfn_msg)
            message = record["Sns"]["Message"].strip()
            if cfn_msg.get("ResourceType") == "AWS::CloudFormation::Stack":
                log.info("Handle SNS CFN")
                return wrap_response(hook_handle_sns_cfn(cfn_msg))

    if lambda_event.get("resource") == "/event/{source}":
        check_hook_auth(lambda_event)
        source = lambda_event.get("pathParameters", {}).get("source", "")
        return event_post(lambda_event, lambda_context)

    if lambda_event.get("resource") == "/hook/{source}":
        source = lambda_event.get("pathParameters", {}).get("source", "")
        check_hook_auth(lambda_event)
        body = json.loads(lambda_event.get("body")) 
        if source.startswith("aws-sns"):
            if body.get("Type") == "SubscriptionConfirmation":
                try:
                    url = body.get("SubscribeURL")
                    urllib.request.urlopen(url)
                except Exception as e:
                    log.exception(e)

        if source == "aws-sns-cfn":
            print(body)
            return wrap_response(
                hook_handle_sns_cfn(extract_cfn_msg(body.get("Message")))
            )
        if source == "github":
            return wrap_response(
                hook_handle_github(body)
            )

    if lambda_event.get("resource") == "/data":
        check_user_auth(lambda_event)
        return wrap_response(get_event_data())
    print("NOTHING HAPPED")

def get_event_data():
    dd.Table(os.environ.get("TABLE"))
    config = get_config()

    response_dd = dd.batch_get_item(
        RequestItems={
            os.environ.get("TABLE"): {
                "Keys": [
                    {
                        "eventSourceIdentifierHash": md5(
                            event.get("eventSourceIdentifier")
                        )
                    }
                    for event in config.get("eventResource")
                ],
                "ConsistentRead": True,
            }
        }
    )

    response_data = {
        "version": config.get("version"),
        "eventSource": config.get("eventSource"),
        "eventResource": [],
    }
    for resource in response_dd.get("Responses").get(os.environ.get("TABLE")):
        event_config = find_event_config(
            resource.get("eventSourceIdentifier"), resource.get("eventSource")
        )
        data_config = event_config.copy()
        data_config.update(resource)
        response_data["eventResource"].append(data_config)
    return response_data

def event_post(lambda_event, lambda_context):

    try:
        event_source = lambda_event.get("pathParameters", {}).get("source", False)
        request_event = json.loads(lambda_event.get("body"))
        validate_event(request_event, event_source)
        save_event(request_event, event_source)

    except Exception as e:
        log.exception(e)
        return wrap_response(
            {
                "state": "error",
                "messages": [{"title": e.__class__.__name__, "message": str(e)}],
            },
            status_code=500,
        )

    return wrap_response({"state": "okay"})

def validate_event(event, event_source):
    config = get_config()
    if event_source in [item["slug"] for item in config.get("eventSource")]:
        with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "schemas/event.schema.json",
            ),
            "r",
        ) as fobj:
            schema = json.load(fobj)
        validate(instance=event, schema=schema)
        return True
    raise ValidationError("Cant find eventSource")

def wrap_response(data, status_code=200):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(data),
    }

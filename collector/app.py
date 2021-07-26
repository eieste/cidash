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
dd = boto3.resource('dynamodb')
MIN_EQ_VERSION = "19-07-2021"


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties" : set_defaults},
    )

DefaultValidatingDraft7Validator = extend_with_default(Draft7Validator)

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

def md5(data):
    return hashlib.md5(data.encode("utf-8")).hexdigest()

def lambda_handler(lambda_event, lambda_context):
    try:
        return general_handler(lambda_event, lambda_context)
    except Exception as e:
        log.exception(e)
        return wrap_response({
            "state": "error",
            "errors": [
                {"title": e.__class__.__name__, "message": str(e)}
            ]
        }, status_code=500)

def check_hook_auth(lambda_event):
    return True
    config = get_config()
    if lambda_event.get("queryStringParameters").get("key") == config.get("accessToken"):
        return True
    raise UnauthorizedAccess("Permission denied")


def check_user_auth(lambda_event):
    return True
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


def general_handler(lambda_event, lambda_context):
    if lambda_event("httpMethod", "").lower() in ["options", "head"]:
        return wrap_response({})

    if lambda_event.get("Records", False):
        record = lambda_event.get("Records")[0]

        if record.get("EventSource") == "aws:sns":
            message = record['Sns']['Message'].strip()
            cfn_msg = {k:v.strip('\'').strip("\"") for k,v in (x.split('=') for x in message.split('\n')) }

            if cfn_msg.get("ResourceType") == "AWS::CloudFormation::Stack":
                log.info("Handle SNS CFN")
                return wrap_response(hook_handle_sns_cfn(cfn_msg))

    if lambda_event.get("resource") == '/event/{source}':
        check_hook_auth(lambda_event)
        return event_post(lambda_event, lambda_context)

    if lambda_event.get("resource") == '/hook/{source}':
        check_hook_auth(lambda_event)
        if source == "aws-sns-cfn":
            return wrap_response(hook_handle_sns_cfn(json.loads(lambda_event.get("body"))))

    if lambda_event.get("resource") == "/data":
        check_user_auth(lambda_event)
        return wrap_response(get_event_data())

def get_event_data():
    table = dd.Table(os.environ.get("TABLE"))
    config = get_config()

    response_dd = dd.batch_get_item(
        RequestItems={
            os.environ.get("TABLE"): {
                'Keys': [ {"eventSourceIdentifierHash": md5(event.get("eventSourceIdentifier")) } for event in config.get("eventResource") ],
                'ConsistentRead': True
            }
        },
    )

    response_data = {
        "version": config.get("version"),
        "eventSource": config.get("eventSource"),
        "eventResource": []
    }
    for resource in response_dd.get("Responses").get(os.environ.get("TABLE")):
        event_config = find_event_config(resource, resource.get("eventSource"))
        data_config = event_config.copy()
        data_config.update(resource)
        response_data["eventResource"].append(
            data_config
        )
    return response_data


def resolve_sns_cfn_state(state):

    if state.lower() in [
            "create_complete",
            "delete_complete",
            "update_complete",
            "update_complete_cleanup_in_progress",
            "import_complete"]:
        return "okay"
    elif state.lower() in ["create_in_progress",
                           "delete_in_progress",
                           "update_in_progress"]:
        return "pending"
    elif state.lower() in ["rollback_complete",
                           "update_rollback_complete",
                           "update_rollback_complete_cleanup_in_progress",
                           "update_rollback_in_progress",
                           "import_in_progress",
                           "import_rollback_in_progress",
                           "import_rollback_complete"]:
        return "warning"
    elif state.lower() in ["create_failed",
                           "delete_failed",
                           "rollback_failed",
                           "rollback_in_progress",
                           "update_failed",
                           "update_rollback_failed",
                           "import_rollback_failed"]:
        return "error"
    elif state.lower() in ["review_in_progress"]:
        return "information"


def hook_handle_sns_cfn(cfn_msg):
    save_event({
        "eventSourceIdentifier": cfn_msg.get("StackId"),
        "simpleState": resolve_sns_cfn_state(cfn_msg.get("ResourceStatus")),
        "complexState": cfn_msg.get("ResourceStatus"),
        "complexMessage": cfn_msg.get("ResourceStatusReason"),
    }, "aws-sns-cfn")


def event_post(lambda_event, lambda_context):

    try:
        event_source = lambda_event.get("pathParameters", {}).get("source", False)
        request_event = json.loads(lambda_event.get("body"))
        validate_event(request_event, event_source)
        save_event(request_event, event_source)

    except Exception as e:
        log.exception(e)
        return wrap_response({
                "state": "error",
                "errors": [
                    {"title": e.__class__.__name__, "message": str(e)}
                ]
        }, status_code=500)

    return wrap_response({
            "state": "ok"
        })

def validate_event(event, event_source):
    config = get_config()
    if event_source in [item["slug"] for item in config.get("eventSource")]:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "event.schema.json"), "r") as fobj:
            schema = json.load(fobj)
        validate(instance=event, schema=schema)
        return True
    raise ValidationError("Cant find eventSource")

def find_event_config(event, event_source):
    config = get_config()

    for event_config in config.get("eventResource"):
        if event_config.get("eventSource") == event_source:
            reg = re.compile(event_config.get("eventSourceIdentifier"))
            if bool(reg.search(event.get("eventSourceIdentifier"))):
                return event_config
    return False

def save_event(origin_event, event_source):
    table = dd.Table(os.environ.get("TABLE"))
    current_time = datetime.now(timezone.utc)
    iso_now = current_time.isoformat(timespec="seconds")
    event_config = find_event_config(origin_event, event_source)

    if not event_config:
       raise ValidationError("Unknown Event Source")

    event_source_identifier_hash = md5(event_config.get("eventSourceIdentifier"))
    response = table.query(
        KeyConditionExpression= Key("eventSourceIdentifierHash").eq(event_source_identifier_hash)
    )

    event = {
        "timestamp": iso_now,
        "simpleState": origin_event.get("simpleState"),
        "complexState": origin_event.get("complexState"),
        "complexMessage": origin_event.get("complexMessage"),
        "eventSourceUrl": origin_event.get("eventSourceUrl")
    }

    if len(response.get("Items")) <= 0:
        response = table.put_item(
            Item={
                "version": MIN_EQ_VERSION,
                "eventSource": event_source,
                "eventSourceIdentifier": origin_event.get("eventSourceIdentifier"),
                "eventSourceIdentifierHash": event_source_identifier_hash,
                "eventHistory": [
                    event
                ]
            }
        )
    else:
        history = response.get("Items")[0].get("eventHistory")
        sorted_history = sorted(history, key=lambda event: datetime.fromisoformat(event['timestamp']))
        last_history = sorted_history[(event_config.get("config", {}).get("maxHistory")-1)*-1:]
        last_history.append(event)
        response = table.update_item(
            Key={
                "eventSourceIdentifierHash": event_source_identifier_hash
            },
            UpdateExpression="set eventHistory=:history",
            ExpressionAttributeValues={
                ':history': last_history
            },
            ReturnValues="UPDATED_NEW"
        )
        return response


def wrap_response(data, status_code=200):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(data)
    }




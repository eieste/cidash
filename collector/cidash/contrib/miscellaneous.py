import hashlib
from cidash.contrib.exceptions import ValidationError
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key
import os
import re
import boto3
import logging
from cidash.contrib.settings import get_config, MIN_EQ_VERSION

dd = boto3.resource("dynamodb")
log = logging.getLogger(__name__)

def md5(data):
    return hashlib.md5(data.encode("utf-8")).hexdigest()

def find_event_config(eventSourceIdentifier, event_source):
    config = get_config()

    for event_config in config.get("eventResource"):
        if event_config.get("eventSource") == event_source:
            reg = re.compile(event_config.get("eventSourceIdentifier"))
            if bool(reg.search(eventSourceIdentifier)):
                return event_config
    return False

def save_version(eventSourceIdentifier, version):
    table = dd.Table(os.environ.get("TABLE"))
    current_time = datetime.now(timezone.utc)
    iso_now = current_time.isoformat(timespec="seconds")
    event_config = find_event_config(eventSourceIdentifier, "github")

    if not event_config:
        raise ValidationError("Unknown Event Source")

    event_source_identifier_hash = md5(event_config.get("eventSourceIdentifier"))

    response = table.query(
        KeyConditionExpression=Key("eventSourceIdentifierHash").eq(
            event_source_identifier_hash
        )
    )

    if len(response.get("Items")) <= 0:
        response = table.put_item(
            Item={
                "version": MIN_EQ_VERSION,
                "eventSource": "github",
                "eventSourceIdentifier": eventSourceIdentifier,
                "eventSourceIdentifierHash": event_source_identifier_hash,
                "resourceVersion": version,
                "eventHistory": []
            }
        )
    else:
        response = table.update_item(
            Key={"eventSourceIdentifierHash": event_source_identifier_hash},
            UpdateExpression="set resourceVersion=:version",
            ExpressionAttributeValues={":version": version},
            ReturnValues="UPDATED_NEW",
        )


def save_event(origin_event, event_source):
    table = dd.Table(os.environ.get("TABLE"))
    current_time = datetime.now(timezone.utc)
    iso_now = current_time.isoformat(timespec="seconds")
    event_config = find_event_config(
        origin_event.get("eventSourceIdentifier"), event_source
    )

    if not event_config:
        log.debug(origin_event)
        raise ValidationError("Unknown Event Source {} -- {}".format(event_source, origin_event.get("eventSourceIdentifier")))

    event_source_identifier_hash = md5(event_config.get("eventSourceIdentifier"))
    response = table.query(
        KeyConditionExpression=Key("eventSourceIdentifierHash").eq(
            event_source_identifier_hash
        )
    )

    event = {
        "timestamp": iso_now,
        "simpleState": origin_event.get("simpleState"),
        "complexState": origin_event.get("complexState"),
        "complexMessage": origin_event.get("complexMessage"),
        "eventSourceUrl": origin_event.get("eventSourceUrl"),
    }

    if len(response.get("Items")) <= 0:
        response = table.put_item(
            Item={
                "version": MIN_EQ_VERSION,
                "eventSource": event_source,
                "eventSourceIdentifier": origin_event.get("eventSourceIdentifier"),
                "eventSourceIdentifierHash": event_source_identifier_hash,
                "eventHistory": [event],
            }
        )
    else:
        history = response.get("Items")[0].get("eventHistory")
        sorted_history = sorted(
            history, key=lambda event: datetime.fromisoformat(event["timestamp"])
        )
        last_history = sorted_history[
            (event_config.get("config", {}).get("maxHistory") - 1) * -1 :
        ]
        last_history.append(event)
        response = table.update_item(
            Key={"eventSourceIdentifierHash": event_source_identifier_hash},
            UpdateExpression="set eventHistory=:history",
            ExpressionAttributeValues={":history": last_history},
            ReturnValues="UPDATED_NEW",
        )
        return response

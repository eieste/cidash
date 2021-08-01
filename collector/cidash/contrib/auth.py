from cidash.contrib.settings import get_config
from cidash.contrib.exceptions import UnauthorizedAccess
import logging
import hashlib
import base64

log = logging.getLogger(__name__)

def check_hook_auth(lambda_event):
    config = get_config()
    if lambda_event.get("queryStringParameters").get("key") == config.get(
        "accessToken"
    ):
        return True
    raise UnauthorizedAccess("Permission denied")

def check_user_auth(lambda_event):
    log.debug(lambda_event)
    auth_header = lambda_event.get("headers", {}).get("Authorization", ":")[6:]
    credentials = [
        item.strip()
        for item in base64.b64decode(auth_header).decode("utf-8").split(":")
    ]
    config = get_config()
    pwhash = hashlib.sha512(
        str(credentials[1] + config.get("privateToken")).encode("utf-8")
    ).hexdigest()
    for user in config.get("userList", []):
        if user.get("username") == credentials[0] and user.get("password") == pwhash:
            return True
    raise UnauthorizedAccess("You are not allowed to access")

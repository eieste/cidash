from cidash.contrib.miscellaneous import save_event
import logging
import urllib.parse

log = logging.getLogger(__name__)


def extract_cfn_msg(msg_str):
    return {
        k: v.strip("'").strip('"')
        for k, v in (x.split("=") for x in msg_str.strip('\n').split('\n'))
    }

def resolve_sns_cfn_state(state):

    if state.lower() in [
        "create_complete",
        "delete_complete",
        "update_complete",
        "update_complete_cleanup_in_progress",
        "import_complete",
    ]:
        return "okay"
    elif state.lower() in [
        "create_in_progress",
        "delete_in_progress",
        "update_in_progress",
    ]:
        return "pending"
    elif state.lower() in [
        "rollback_complete",
        "update_rollback_complete",
        "update_rollback_complete_cleanup_in_progress",
        "update_rollback_in_progress",
        "import_in_progress",
        "import_rollback_in_progress",
        "import_rollback_complete",
    ]:
        return "warning"
    elif state.lower() in [
        "create_failed",
        "delete_failed",
        "rollback_failed",
        "rollback_in_progress",
        "update_failed",
        "update_rollback_failed",
        "import_rollback_failed",
    ]:
        return "error"
    elif state.lower() in ["review_in_progress"]:
        return "information"

def hook_handle_sns_cfn(cfn_msg):

    save_event(
        {
            "eventSourceIdentifier": cfn_msg.get("StackId"),
            "simpleState": resolve_sns_cfn_state(cfn_msg.get("ResourceStatus")),
            "complexState": cfn_msg.get("ResourceStatus"),
            "complexMessage": cfn_msg.get("ResourceStatusReason"),
            "eventSourceUrl": "https://eu-central-1.console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/stackinfo?stackId={}".format(
                urllib.parse.quote(cfn_msg.get("StackId"))
            ),
        },
        "aws-sns-cfn",
    )

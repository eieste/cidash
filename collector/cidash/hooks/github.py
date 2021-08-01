from cidash.contrib.miscellaneous import save_version, save_event
import logging


log = logging.getLogger(__name__)


def hook_handle_github(body):
    state = "unknown"

    if body.get("ref", False) and body.get("ref_type", False):
        save_version(
            eventSourceIdentifier=body.get("repository", {}).get("full_name", ""),
            version=body.get("ref"),
        )
        return

    if "check_suite" in body:
        return {
            "state": "okay",
            "messages": [
                {"title": "nothing to do", "message": "useless github request"}
            ],
        }

    check_run = body.get("check_run", False)
    if check_run is False:
        log.warning("Unahndeld Github Event")
        return
    state = check_run.get("conclusion", "")
    url = check_run.get("details_url", "")

    save_event(
        {
            "eventSourceIdentifier": body.get("repository", {}).get("full_name", ""),
            "simpleState": resolve_github_state(state),
            "complexState": check_run.get("output", {}).get("title", ""),
            "complexMessage": check_run.get("output", {}).get("title", ""),
            "eventSourceUrl": url,
        },
        "github",
    )

def resolve_github_state(state):

    if state.lower() in ["success", "completed"]:
        return "okay"
    elif state.lower() in ["queue"]:
        return "pending"
    elif state.lower() in ["failure", "startup_failure"]:
        return "error"
    return "unknown"

import logging
from cidash.app import general_handler, wrap_response

log = logging.getLogger(__name__)

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

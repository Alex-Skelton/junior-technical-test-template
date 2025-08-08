from flask import Blueprint, current_app, request, jsonify
from pydantic import ValidationError

from services.user_service import handle_user_event_logic

api = Blueprint("api", __name__)


@api.post("/event")
def handle_user_event() -> tuple:
    current_app.logger.info("Handling user event: /event")

    api_body = request.get_json()
    if not api_body:
        current_app.logger.warning("No JSON data provided in the request body.")
        return jsonify({"message": "No input data provided"}), 400

    try:
        response_json = handle_user_event_logic(api_body)
        current_app.logger.info("/event payload executed")
        return response_json, 200

    except ValidationError as e:
        current_app.logger.warning(f"Validation failed on JSON request body: {e.errors()}")
        return jsonify({"Data validation error occurred": e.errors()}), 400

    except Exception as e:
        current_app.logger.exception(f"An unexpected error occurred in /event: {str(e)}")
        return jsonify({"message": f"An internal server error occurred: {str(e)}"}), 500


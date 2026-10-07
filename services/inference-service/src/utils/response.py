from typing import Any


def api_response(success: bool, message: str, data: Any = None, error: Any = None):
    return {"success": success, "message": message, "data": data, "error": error}

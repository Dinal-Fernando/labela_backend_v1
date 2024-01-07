def validate_payload(payload, data):

    missing_keys = [key for key in payload if key not in data or data[key] is None]

    if missing_keys:
        return False, f"Following fields are required: {', '.join(missing_keys)}"
    else:
        return True, ""

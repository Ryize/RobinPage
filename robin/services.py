import datetime

# Dictionary with request data for each client (determined by ip).
# By default, the dictionary contains a template that will be used to create other entries
_requests_per_day = {
    "127.0.0.1": {
        "count": 1,
        "date_last_requests": datetime.date.today(),
    }
}


def _check_counter_date(client: dict) -> dict:
    """If the day of the last request does not coincide with the current, then the request counter is reset to 0."""
    if client["date_last_requests"] != datetime.date.today():
        client["date_last_requests"] = datetime.date.today()
        client["count"] = 0
    return client


def get_client_ip(req) -> str:
    """
    This is used to get the user's IP from the request object.
    """
    x_forwarded_for = req.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = req.META.get("REMOTE_ADDR", "unknown")
    return ip


def check_requests_per_day(client_ip: str) -> int:
    """Here we get the number of user requests for the last day."""
    if not isinstance(client_ip, str):
        raise TypeError("The client_ip parameter must be str")
    client = _requests_per_day.get(client_ip)
    if not client:
        return 0
    client = _check_counter_date(client)
    return client["count"]


def add_request_from_client(client_ip: str) -> int:
    """This function is used to increment the client's request counter (_requests_per_day variable)."""
    if not isinstance(client_ip, str):
        raise TypeError("The client_ip parameter must be str")
    client = _requests_per_day.get(client_ip)
    if not client:
        _requests_per_day[client_ip] = {
            "count": 0,
            "date_last_requests": datetime.date.today(),
        }
        client = _requests_per_day.get(client_ip)
    client = _check_counter_date(client)
    client["count"] += 1
    return client["count"]


def clear_request_counter(client_ip: str) -> bool:
    """This function sets the number of requests from the passed client ip to 0 (_requests_per_day variable)."""
    if not isinstance(client_ip, str):
        raise TypeError("The client_ip parameter must be str")
    client = _requests_per_day.get(client_ip)
    if not client:
        return False
    client["count"] = 0
    return True

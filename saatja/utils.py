from datetime import datetime, timezone


def now_utc():
    """
    Get timezone aware "now" datetime
    :return datetime:
    """
    return datetime.utcnow().replace(tzinfo=timezone.utc)

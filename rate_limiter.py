from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = timedelta(seconds=window_seconds)
        self.user_requests = {}

    def is_allowed(self, user_id: int) -> bool:
        now = datetime.now()
        if user_id not in self.user_requests:
            self.user_requests[user_id] = [now]
            return True

        # Filter out old requests
        self.user_requests[user_id] = [
            t for t in self.user_requests[user_id] if now - t <= self.window
        ]

        if len(self.user_requests[user_id]) < self.limit:
            self.user_requests[user_id].append(now)
            return True

        return False

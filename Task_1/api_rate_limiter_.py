import time
import threading
from concurrent.futures import ThreadPoolExecutor


MAX_REQUESTS = 3
TIME_WINDOW = 5

request_data = {}
exceeded_requests = {}

lock = threading.Lock()


def check_rate_limit(user):
    current_time = time.time()

    with lock:
        # First request from this user
        if user not in request_data:
            request_data[user] = {
                "count": 1,
                "window_start": current_time
            }

            print(f"{user}: Request allowed (1/{MAX_REQUESTS})")
            return True

        user_data = request_data[user]

        # Check whether the current time window has expired
        elapsed_time = current_time - user_data["window_start"]

        if elapsed_time >= TIME_WINDOW:
            user_data["count"] = 1
            user_data["window_start"] = current_time

            print(f"{user}: New time window - Request allowed (1/{MAX_REQUESTS})")
            return True

        # User is still inside the current time window
        if user_data["count"] < MAX_REQUESTS:
            user_data["count"] += 1

            print(
                f"{user}: Request allowed "
                f"({user_data['count']}/{MAX_REQUESTS})"
            )
            return True

        # Rate limit exceeded
        exceeded_requests[user] = exceeded_requests.get(user, 0) + 1

        print(
            f"{user}: Rate limit exceeded "
            f"(rejected requests: {exceeded_requests[user]})"
        )

        return False


def make_api_call(user):
    allowed = check_rate_limit(user)

    if allowed:
        # Simulating API processing
        time.sleep(0.2)
        print(f"{user}: API call completed")


def main():
    users = [
        "user_1",
        "user_1",
        "user_2",
        "user_1",
        "user_2",
        "user_1",
        "user_3",
        "user_1",
        "user_2",
        "user_2",
        "user_3",
        "user_3",
        "user_3"
    ]

    print("Starting concurrent API requests...\n")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(make_api_call, users)

    print("\n--- Final Report ---")

    for user in request_data:
        rejected = exceeded_requests.get(user, 0)

        print(
            f"{user}: "
            f"Allowed in current window = {request_data[user]['count']}, "
            f"Rejected = {rejected}"
        )


if __name__ == "__main__":
    main()
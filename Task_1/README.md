# Parallel API Rate Limiter

## Overview

This mini project implements a concurrent API rate limiter using Python. It simulates multiple API requests from different users, limits the number of requests each user can make within a fixed time window, and tracks requests that exceed the allowed threshold.

The project uses Python multithreading to simulate concurrent API calls and a lock to safely manage shared request data.

## Problem Statement

Create a parallel API rate limiter that simulates multiple concurrent API calls. Enforce rate limits per user or token and track requests that exceed allowed thresholds.

## Features

* Simulates multiple concurrent API requests.
* Applies rate limits separately for each user.
* Allows a maximum of 3 requests per user within 5 seconds.
* Rejects requests that exceed the allowed threshold.
* Tracks the number of rejected requests for each user.
* Uses a thread lock to prevent race conditions.
* Displays a final report of allowed and rejected requests.

## Technologies Used

* Python 3
* `threading`
* `time`
* `concurrent.futures.ThreadPoolExecutor`

No external libraries are required.

## Rate Limit Configuration

The rate limit is defined using:

```python
MAX_REQUESTS = 3
TIME_WINDOW = 5
```

This means that each user can make a maximum of **3 requests within 5 seconds**.

Example:

```text
Request 1 → Allowed
Request 2 → Allowed
Request 3 → Allowed
Request 4 → Rate Limit Exceeded
```

After the time window expires, a new window starts and the user can make requests again.

## How It Works

1. A list of users represents incoming API requests.
2. `ThreadPoolExecutor` processes multiple requests concurrently.
3. Each request is passed to the rate limiter.
4. The program checks the user's current request count.
5. If the user is within the allowed limit, the request is processed.
6. If the user exceeds the limit, the request is rejected and tracked.
7. A `threading.Lock` protects shared data from race conditions.
8. After all requests are processed, a final report is displayed.

## Project Flow

```text
Multiple User Requests
        |
        v
ThreadPoolExecutor
        |
        v
 check_rate_limit()
        |
        v
 Check User's Request Count
      /           \
 Within Limit    Limit Exceeded
      |                |
   Allowed           Rejected
      |                |
 Process API      Track Rejection
        \              /
         Final Report
```

## Project Structure

```text
project-folder/
|
|-- parallel_api_rate_limiter.py
|-- README.md
```

## How to Run

1. Make sure Python 3 is installed.

2. Open a terminal in the project folder.

3. Run the program:

```bash
python parallel_api_rate_limiter.py
```

## Sample Output

```text
Starting concurrent API requests...

user_1: Request allowed (1/3)
user_1: Request allowed (2/3)
user_2: Request allowed (1/3)
user_1: Request allowed (3/3)
user_1: Rate limit exceeded (rejected requests: 1)

--- Final Report ---

user_1: Allowed in current window = 3, Rejected = 2
user_2: Allowed in current window = 3, Rejected = 1
user_3: Allowed in current window = 3, Rejected = 1
```

The exact order of the output may vary because the requests are processed concurrently.

## Main Concepts Used

### Rate Limiting

Rate limiting controls how many requests a user can make within a specific period of time.

### Threshold

The threshold is the maximum allowed number of requests.

In this project:

```text
Threshold = 3 requests per user per 5 seconds
```

### Concurrency

Multiple API requests are simulated concurrently using:

```python
ThreadPoolExecutor
```

### Thread Safety

Multiple threads may access shared request data at the same time. A lock is used to ensure that only one thread updates the shared data at a time:

```python
lock = threading.Lock()
```

### Fixed Window Rate Limiting

This project uses a fixed-window rate-limiting approach. Each user has a request count and a window start time. When the time window expires, the request count is reset and a new window begins.

## Future Improvements

* Integrate the rate limiter with Flask or FastAPI.
* Use API tokens instead of simple user names.
* Return HTTP status code `429 Too Many Requests` for rejected requests.
* Store request data in Redis or a database.
* Implement other algorithms such as Sliding Window or Token Bucket.
* Add different rate limits for different users.

## Conclusion

This project demonstrates how API rate limiting can be implemented in Python while handling concurrent requests. It uses `ThreadPoolExecutor` to simulate multiple API calls, a fixed-window algorithm to enforce per-user limits, and `threading.Lock` to safely manage shared data.

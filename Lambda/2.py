import json
import time

# ---------- GLOBAL SCOPE (Cold start happens here) ----------
start_time = time.time()
cold_start = True

# Simulate heavy initialization
time.sleep(2)  # 2 seconds delay

init_time = time.time() - start_time
print(f"INIT time (cold start only): {init_time:.2f} seconds")

# ---------- HANDLER ----------
def lambda_handler(event, context):
    global cold_start

    handler_start = time.time()

    if cold_start:
        start_type = "COLD START"
        cold_start = False
    else:
        start_type = "HOT START"

    handler_time = time.time() - handler_start

    return {
        "statusCode": 200,
        "body": json.dumps({
            "start_type": start_type,
            "init_time_seconds": round(init_time, 2),
            "handler_time_ms": round(handler_time * 1000, 2),
            "request_id": context.aws_request_id
        })
    }

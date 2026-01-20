import json
import os

# ---------- GLOBAL SCOPE (Cold start happens here) ----------

print(os.environ)

name = os.environ.get("name", "unknown")
age = os.environ.get("age", "0")


# ---------- HANDLER ----------
def lambda_handler(event, context):

    debug = os.environ.get("debugging", "false").lower() == "true"

    if debug:
        print(event)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "name": name,
            "age": age
        })
    }

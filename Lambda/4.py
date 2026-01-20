import json
import os
import subprocess

# ---------- GLOBAL SCOPE (Cold start happens here) ----------

try:
    # Command as a list of arguments (recommended for security)
    result = subprocess.run(
        ["ls", "-l", "/tmp"],
        capture_output=True,  # Capture stdout and stderr
        text=True,            # Return output as strings (instead of bytes)
        check=True            # Raise CalledProcessError if the command fails
    )
    print("Command output:", result.stdout)
except subprocess.CalledProcessError as e:
    print("Command failed with error:", e.stderr)
except FileNotFoundError as e:
    print(f"Error: The command was not found: {e}")

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

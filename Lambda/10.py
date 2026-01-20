import json
import requests

def lambda_handler(event, context):
    try:
        r = requests.get("https://www.example.com", timeout=5)

        if r.status_code == 200:
            message = "Website reachable"
        else:
            message = f"Website returned status {r.status_code}"

        return {
            "statusCode": 200,
            "body": json.dumps(message)
        }

    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Website not reachable: {str(e)}")
        }

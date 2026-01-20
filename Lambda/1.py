import json

def lambda_handler(event, context):

    # Allow only POST
    if event["requestContext"]["http"]["method"] != "POST":
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Only POST method is allowed"
            })
        }

    print("*" * 10)
    print(json.dumps(event, indent=2))
    print(event)
    print("*" * 10)

    body = json.loads(event["body"])

    # Convert to numbers (important)
    number1 = float(body["number1"])
    number2 = float(body["number2"])

    add = number1 + number2
    sub = number1 - number2
    mul = number1 * number2

    # Safe division
    div = None
    if number2 != 0:
        div = number1 / number2

    return {
        "statusCode": 200,
        "body": json.dumps({
            "add": add,
            "sub": sub,
            "mul": mul,
            "div": div
        })
    }

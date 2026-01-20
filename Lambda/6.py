import boto3
import time
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("IdempotencyTable")

def lambda_handler(event, context):
    key = event["order_id"]
    ttl = int(time.time()) + 3600

    try:
        table.put_item(
            Item={
                "idempotency_key": key,
                "expiry_time": ttl
            },
            ConditionExpression="attribute_not_exists(idempotency_key)"
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print("Duplicate event detected. Skipping.")
            return "Duplicate ignored"
        else:
            raise

    print("Processing order:", key)
    time.sleep(2)
    print("Order created:", key)

    return "Order processed"
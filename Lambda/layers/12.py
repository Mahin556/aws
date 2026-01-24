import json
from my_module.my_function import function_from_lambda_layer

def lambda_handler(event, context):
    result = function_from_lambda_layer()
    return {
        "statusCode": 200,
        "body": json.dumps({
            result: result
        })
    }

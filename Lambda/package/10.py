import json
import requests

def lambda_handler(event, context):
    
    r = requests.get('https://www.example.com')
    try: 
        if r.status_code == 200:
            return {
                'statusCode': 200,
                'body': json.dumps('Website reachable')
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps('Website not reachable')
            }
    except Exception as e:
        raise e

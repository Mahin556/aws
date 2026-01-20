```bash
$ curl demo-296794782.ap-south-1.elb.amazonaws.com
"Hello from Lambda!"
```
```bash
{'requestContext': {'elb': {'targetGroupArn': 'arn:aws:elasticloadbalancing:ap-south-1:361769558190:targetgroup/demo/afe00575f54749b5'}}, 'httpMethod': 'GET', 'path': '/', 'queryStringParameters': {}, 'headers': {'accept': '*/*', 'host': 'demo-296794782.ap-south-1.elb.amazonaws.com', 'user-agent': 'curl/8.12.1', 'x-amzn-trace-id': 'Root=1-696e6f65-5fabb3600460c16149a3b0a5', 'x-forwarded-for': '49.36.235.154', 'x-forwarded-port': '80', 'x-forwarded-proto': 'http'}, 'body': '', 'isBase64Encoded': False}
```

### https://docs.aws.amazon.com/lambda/latest/dg/services-alb.html


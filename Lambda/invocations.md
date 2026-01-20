* 2 type of invocation `SYNCHRONOUS`,`ASYNCHRONOUS`

#### `SYNCHRONOUS`
* Caller waits for Lambda to finish.
* Lambda returns a response immediately.
* Errors are returned directly to the caller.

**COMMON TRIGGERS**
- API Gateway
- Lambda Function URL
- ALB
- SDK invoke with InvocationType=RequestResponse


```python
import json
import time

def lambda_handler(event, context):
    print("Processing started")
    time.sleep(3)   # simulate work
    print("Processing finished")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Synchronous execution completed"
        })
    }
```
```bash
aws lambda invoke \
  --function-name my-function \
  --invocation-type RequestResponse \
  response.json
```

**API Gateway / Lambda URL:**
* Client sends HTTP request
* Client waits for response

**WHAT YOU OBSERVE (SYNC)**
* Client waits ~3 seconds
* Client receives response
* If Lambda errors → client gets error
* Timeout affects client directly


#### `ASYNCHRONOUS INVOCATION (FIRE AND FORGET)`
* Caller does NOT wait
* Lambda is queued internally
* Response is sent immediately (202 Accepted)
* Lambda runs later

**COMMON TRIGGERS**
* S3
* EventBridge
* SNS
* SDK invoke with InvocationType=Event

```bash
import json
import time

def lambda_handler(event, context):
    print("Async processing started")
    time.sleep(5)
    print("Async processing finished")
```
```bash
aws lambda invoke \
  --function-name my-function \
  --invocation-type Event \
  response.json
```
**CLI output:**
* StatusCode: 202
* `response.json` is empty

**WHAT YOU OBSERVE (ASYNC)**
* Client returns immediately
* Lambda runs in background
* Logs appear later in CloudWatch
* Client NEVER sees Lambda result

**ERROR HANDLING DIFFERENCE (VERY IMPORTANT)**

**SYNCHRONOUS**
* Error returned to caller immediately
* Caller responsible for retry

**ASYNCHRONOUS**
* AWS retries automatically:
    * 2 retries
    * Up to ~6 hours
    * If still failing:
        * Event sent to DLQ or Destination

**ASYNC RETRY DEMO**
```python
def lambda_handler(event, context):
    raise Exception("Simulated failure")
```

**Behavior:**
* AWS retries automatically
* You will see multiple log entries
* Eventually sent to DLQ if configured

**TIMEOUT BEHAVIOR**

**SYNCHRONOUS**
* Client waits until timeout
* Bad UX if slow

**ASYNCHRONOUS**
* Client unaffected by timeout
* Lambda may still retry

**WHEN TO USE SYNCHRONOUS**
✔ APIs
✔ User-facing requests
✔ Real-time responses
✔ Validation / queries

**WHEN TO USE ASYNCHRONOUS**
✔ Background processing
✔ File processing
✔ Notifications
✔ ETL jobs
✔ Event-driven workflows

```bash
ASYNCHRONOUS LAMBDA INVOCATION – QUICK SUMMARY (IMPORTANT POINTS)

- Asynchronous invocation means “fire and forget”
- Caller does NOT wait for Lambda to finish
- Common async sources: S3, EventBridge, SNS

- When a Lambda function FAILS in async mode:
  raise Exception("Simulated failure")

- Raising an exception means:
  - Invocation is marked as FAILED
  - AWS automatically retries the event

- Default retry behavior:
  - AWS retries up to 2 additional times
  - Retries use exponential backoff
  - Retries continue until success or event age limit is reached

- Maximum Event Age:
  - Default: 6 hours (21600 seconds)
  - Configurable: 60 seconds to 6 hours
  - Defines TOTAL time AWS will keep retrying

- Important distinction:
  - Lambda timeout (max 15 minutes) applies per invocation
  - Maximum Event Age applies across ALL retries

- What happens after retries are exhausted:
  - Event is sent to DLQ or OnFailure destination (if configured)
  - Otherwise, event is dropped

- Synchronous vs Asynchronous failure:
  - Synchronous: error returned immediately to caller
  - Asynchronous: caller never sees error; AWS handles retries

- Best practices:
  - Use raise Exception() to signal failure explicitly
  - Configure DLQ or Lambda Destinations for visibility
  - Tune Maximum Event Age based on business need
```
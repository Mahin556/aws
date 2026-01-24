* Serverless
* Cost optimization
    * Start and stop EC2 instance at specific time
    * Convert uploaded video into multiple formats --> 360p 480p 720p etc..
    * Find, list or remove unattached EBS Volumes.
    * Find, list or remove unused/aged snapshots.
    * Find, list or remove EC2 Instance that have very less CPU utilization.
    * 

* `event` object is used to give input to lambda function through --> http request, test, s3 etc
* `memory` --> 128MB to 10240MB(12GB), VCPU/CPU selectes BTS with respect to memory(more memory more CPU enable multi threading)
* `Ephemeral Storate` --> Storage of `/tmp` in lambda, 512MB to 10240MB, used when downloading a data from internet
* `timeout` --> max 15min, programm must exit within 15min
* `snapstart` -->
* can delete the stale resource --> ebs, snapshotsm s3buckets, eks
* lambda function are event driven so we can trigger them thourh any of cloudwatch, s3, function url, api gatewat, loadbalancer.

```bash
Cold Start vs Hot Start in AWS Lambda (Practical, Production-Focused)

What a Lambda execution environment is
- AWS creates an isolated runtime environment to run your Lambda function
- This environment includes:
  - OS + container
  - Language runtime (Python, Node.js, etc.)
  - Your function code
  - Initialized global variables
- The environment may be reused for multiple invocations

Cold Start – what it means
- Happens when AWS must create a new execution environment
- Common scenarios:
  - First-ever invocation of the function
  - Function hasn’t been used for some time
  - Sudden traffic spike requiring new containers
  - Function was updated (new code/version)
  - Change in memory, architecture, or runtime
- Cold start includes:
  - Creating container
  - Starting runtime
  - Downloading code
  - Running global scope code
  - Initializing libraries and dependencies

Cold Start – what happens step by step
- AWS receives request
- No warm container available
- New container is created
- Runtime is started
- Code package is loaded
- Global code executes
  import boto3
  client = boto3.client("s3")
- Handler function is called
- Response is returned

Cold Start latency (real numbers)
- Python / Node.js: ~100 ms – 600 ms
- Java: 500 ms – several seconds
- .NET: 300 ms – 1.5 s
- VPC-enabled functions: higher latency
- Heavy dependencies increase cold start time

Hot Start – what it means
- Happens when AWS reuses an existing execution environment
- No container creation
- No runtime startup
- No global initialization
- Only the handler function runs

Hot Start – what happens
- Request arrives
- Warm container already exists
- Handler executes immediately
- Response is returned
- Much lower latency

Hot Start latency
- Usually single-digit milliseconds
- Often 5–20 ms depending on logic

How AWS decides Cold vs Hot
- Completely managed by AWS
- Reuse is best effort, not guaranteed
- Same container can handle:
  - Multiple sequential invocations
  - Not concurrent invocations
- Concurrency > 1 → multiple containers → cold starts possible

Global scope vs handler scope
- Code outside lambda_handler():
  - Runs during cold start
  - Reused during hot starts
- Code inside lambda_handler():
  - Runs every time

Example
import boto3
s3 = boto3.client("s3")

def lambda_handler(event, context):
    return "Hello"

Why cold starts hurt
- User-facing latency
- Timeout risks
- Poor UX for synchronous workloads
- Spikes during traffic bursts

Cold start impact by trigger
- API Gateway / Lambda URL: user-visible delay
- SQS / EventBridge: acceptable
- Step Functions: acceptable
- Cron jobs: acceptable

How to reduce cold starts
- Move heavy initialization outside handler
- Reduce package size
- Avoid unnecessary SDK clients
- Increase memory (CPU scales with memory)
- Prefer Python / Node.js for latency-sensitive APIs
- Avoid unnecessary VPC attachment

Provisioned Concurrency
- Keeps Lambda pre-warmed
- Eliminates cold starts
- You pay for idle capacity
- Ideal for APIs and latency-sensitive workloads

Reserved vs Provisioned Concurrency
- Reserved: limits concurrency, does not prevent cold start
- Provisioned: pre-initialized containers, prevents cold start

Cold start myths
- Cold start happens on every request: false
- Globals reset every invocation: false
- You can fully control reuse: false
- Globals persist across hot starts: true

How to detect cold starts
cold_start = True

def lambda_handler(event, context):
    global cold_start
    if cold_start:
        print("Cold start")
        cold_start = False
    else:
        print("Hot start")

When cold starts do not matter
- Async processing
- Batch jobs
- Nightly jobs
- Non-user-facing workflows

Final takeaway
- Cold start = container + runtime + initialization
- Hot start = reuse + fast execution
- You can design for it even if you cannot control it
- Correct placement of code makes a big difference
```

```bash
AWS LAMBDA – COLD START vs HOT START

QUESTION
Does code in the GLOBAL SCOPE run only during cold start?

ANSWER
Yes.
Code in the GLOBAL SCOPE runs ONLY during a COLD START.
It runs once per execution environment (container).
It does NOT run again during HOT STARTS.

WHAT IS GLOBAL SCOPE?
Code written OUTSIDE the lambda_handler() function.

Example:
import boto3
client = boto3.client("s3")

This code runs when:
- Lambda container is created
- Runtime starts
- Code is loaded

This phase is called a COLD START.

WHAT IS HANDLER SCOPE?
Code written INSIDE lambda_handler().

This code runs:
- On every invocation
- During both cold and hot starts

EXECUTION FLOW

Cold Start:
- New container is created
- Global scope code runs
- Handler function runs

Hot Start:
- Existing container is reused
- Global scope code is skipped
- Handler function runs immediately

YOUR CODE BEHAVIOR

time.sleep(2)
- Runs only once during cold start

lambda_handler()
- Runs on every request

IMPORTANT NUANCE (INTERVIEW-LEVEL)

Global scope runs once per CONTAINER.
Not once per function.
Not once per region.
Not once per account.

If concurrency increases:
- AWS creates new containers
- Global scope runs again
- Cold start occurs again

BEST PRACTICES

Put in GLOBAL scope:
- SDK clients (boto3, etc.)
- Database connections
- Heavy imports
- Configuration loading

Avoid in GLOBAL scope:
- Long sleeps (except demos)
- Network calls that may fail
- Large unused libraries

ONE-LINE TAKEAWAY

Global scope code runs only during cold start.
Handler code runs on every invocation.
```

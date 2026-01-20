```bash
#Windows
winzip

#Linux
zip -r app.zip <dir>
zip -r app.zip .
```
* If zip file size is greater then 10mb then user s3 instead of direct upload.

```bash
#Install a third party library that are not presetn in lambda and need to be uploaded with the function code
pip install -t . request
```

---
---

• **What is a Lambda Layer?**
* A layer is a **separate file system** that sits on top of the Lambda execution environment
* It is used to store:
  * Third-party libraries
  * Shared code
  * Custom utilities
* Lambda automatically loads layers at runtime

---

• A **new Lambda function** was created just for demonstration
• Runtime selected: **Python 3.12**
* Because the system supports Python 3.12
* Libraries installed in the layer must match the runtime version

---

• When `import requests` was tested:
* Lambda failed with `ModuleNotFoundError`
* This confirmed that the library is not available by default

---

• Instead of installing libraries in every Lambda function:
* The goal is to **install them once**
* And reuse them using a **Lambda Layer**

---

• **Important folder structure for Python Lambda Layers**
* The ZIP file must contain a folder named exactly:
  ```
  python/
  ```
* Inside `python/`, all libraries must be installed
* Example:
  ```
  python/
    └── requests/
    └── urllib3/
    └── certifi/
  ```

---

• Libraries should **NOT** be placed directly at the root of the ZIP
• If the folder structure is wrong:
* Lambda will NOT find the modules
* Import will fail

---

• Steps followed to create the layer:
* Create a folder (e.g., `layer-one`)
* Inside it, create a `python/` directory
* Install the library using `pip` into `python/`
* Zip the folder
* Upload it as a **Lambda Layer**
* Select the correct runtime (Python 3.12)

---

• After creating the layer:
* Go back to the Lambda function
* Add the layer under **Configuration → Layers**
* Select the layer and its version

---

• After attaching the layer:
* The same Lambda code was tested again
* No code changes were made
* `import requests` worked successfully

---

• **Key benefits of using Lambda Layers**
* Keeps Lambda code **clean and readable**
* Avoids repeating the same libraries in multiple functions
* Saves storage and deployment effort
* Makes maintenance easier

---

• **Real-world use case**
* If you have 5–100 Lambda functions
* And all of them use the same libraries
* You create **one layer**
* And attach it to all Lambda functions

---

• **Very important rule**
* Folder structure and naming inside the ZIP file is **critical**
* Wrong folder name = Lambda won’t find the library
* This rule applies to:
  * Python
  * Java
  * Node.js
  * Ruby
  * All runtimes

---

• Lambda Layers can also contain:
* Organization’s **custom internal libraries**
* Shared helper functions
* Common business logic

---

• **Final takeaway**
* Lambda Layers help you:
  * Manage dependencies cleanly
  * Reuse libraries across functions
  * Keep application code lightweight
* Always follow the correct folder structure
* Match the layer runtime with the Lambda runtime

---
---

• In this video, the focus is on a **real organizational use case**
• The organization has a **common internal library** containing reusable functions
• Example use cases of such functions:
    * Get user details by user ID
    * Get user details by username
    * Common utility logic shared across many Lambda functions

---

• The problem:
* There are **50+ Lambda functions**
* All of them use the **same common logic**
* Rewriting or copying the same code in every Lambda is:
  * Error-prone
  * Hard to maintain
  * Not scalable

---

• The solution:
* Create a **custom Lambda Layer** containing the organization’s internal utility functions
* Write the common logic **once**
* Reuse it across all Lambda functions

---

• A new layer (`layer-two`) is created
• Inside the layer:
* A `python/` directory is created (mandatory for Python)
* A Python file (example: `gsa_utils.py`) is added
* Functions like:
  * `greet()`
  * `get_user_by_name()`
    are defined

---

• These functions simulate:
* Database calls
* API calls
* S3 or other AWS service interactions

---

• The layer is packaged as a ZIP file with **correct folder structure**
• The layer is uploaded in AWS Lambda → Layers
• Runtime is selected (Python 3.12)

---

• A new Lambda function is created
• The custom layer is attached to the Lambda function
• Initially, calling `greet()` directly fails because:
* The function is not defined in the Lambda code

---

• The correct way to use the function:
* Import it explicitly from the layer module
* Example:
  ```
  from gsa_utils import greet
  ```
• After importing, the function works successfully

---

• Another function (`get_user_by_name`) is also tested
• It returns sample data (dictionary)
• The Lambda function can now reuse all shared logic from the layer

---

• Key real-world benefit:
* Lambda functions stay **clean and lightweight**
* All common logic lives in **one place**
* Changes in one layer affect all dependent Lambdas

---

• Important trade-off (VERY IMPORTANT):
* If you change a function inside the layer:
  * It affects **all Lambda functions using that layer**
* This can be:
  * A big advantage (centralized change)
  * Or a big risk (breaking many Lambdas at once)

---

• Example risk scenario:
* A function originally returns a dictionary
* Later it is changed to return a list
* All dependent Lambda functions may break

---

• Example benefit scenario:
* A welcome message format needs to change
* Change it once in the layer
* All Lambdas automatically reflect the new standard

---

• Decision guidance:
* Use layers for:
  * Stable
  * Well-tested
  * Common logic
* Be cautious with frequent or breaking changes

---

• Another important concept shown:
* A Lambda function can use **multiple layers**
* Example:
  * One layer for `requests` library
  * One layer for internal utility functions

---

• If a library is not present in a layer:
* Import will fail
* You must attach the correct layer

---

• Final question raised in the video:
* What is the **maximum number of layers** allowed per Lambda function?
* (Answer: AWS allows **up to 5 layers per Lambda function**)

---

# A4

## Question 1

### (a) EC2 instance running screenshot

![Running_1](https://github.com/macs30113-s23/a4-magabrielaa/blob/main/images/instance_running_1.png)

![Running_2](https://github.com/macs30113-s23/a4-magabrielaa/blob/main/images/instance_running_2.png)

### (b) SSH into EC2 instance screenshot

![SSH](https://github.com/macs30113-s23/a4-magabrielaa/blob/main/images/instance_ssh.png)

### (c) Python version

As can be seen from the screenshot below, the Python version installed by default is **Python 3.7.16**. The Python packages that are installed are:
- bootstrap
- docutils
- lockfile
- pip
- pystache
- daemon
- setuptools
- simplejson

![Python_version](https://github.com/macs30113-s23/a4-magabrielaa/blob/main/images/python_version.png)

### (d) EC2 instance termination screenshot

![Terminated](https://github.com/macs30113-s23/a4-magabrielaa/blob/main/images/instance_terminated.png)

## Question 2
For Question 2, I created an AWS Lambda function called `lambda_handler`. I tested it on the AWS console before running it programatically. It gives status code 400 if the survey entry is invalid and specifies the type of error (_ie. not enough time elapsed vs. no text response_) in the body of the response. The function is located inside [q2.zip](https://github.com/macs30113-s23/a4-magabrielaa/blob/main/q2.zip), within a module called `lambda_function.py`. I also stored a copy for easier reference: [lambda_function.py](https://github.com/macs30113-s23/a4-magabrielaa/blob/main/lambda_function.py)

```python
def lambda_handler(event, context):

    if event["time_elapsed"] <= 3:
        return {
        'statusCode': 400,
        'body': 'Invalid entry. Not enough time elapsed.'
        }
    elif event["freetext"] == "":
        return {
        'statusCode': 400,
        'body':'Invalid entry. No text response'
        }
    else:
        return {
        'statusCode': 200,
        'body': 'OK'
        }
```

## Question 3
I created a Jupyter Notebook for this question, where I create the programmatic version of the Lambda function above and test it against the three provided survey data examples: [q3.ipynb](https://github.com/macs30113-s23/a4-magabrielaa/blob/main/q3.ipynb).
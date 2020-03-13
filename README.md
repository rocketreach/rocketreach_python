# Getting Started
This is a simple Python binding for the RocketReach API (https://rocketreach.co/api).

## Requirements
Python 3.4+.

## Installation
You can install this package using pip:

```
$ pip install rocketreach
```

## Testing
Includes a simple driver file, `main.py` which accepts 3 required arguments:
 1. `-i <input csv>`
 1. `-o <output csv>`
 1. `-k <api key>`
 
 The input csv is a 2 column csv with name (column 1) and company (column 2).
 The script loads the csv and does a lookup on each row, writing the results to
 output csv. 
 
 **Note that this will overwrite the output file if it exists**
 
 **Note this may charge the account associated with the API Key for any lookups incurred.**

A sample csv is included in the sample directory. You can run it by
```bash
$ ./main.py -i sample/sample01.csv -o sample01_lookup_output.csv -k <YOUR API KEY HERE>
```


## Setup
Sign up for RocketReach at https://rocketreach.co/signup.

Documentation for the API and python bindings available at the official API documentation page: https://rocketreach.co/api.

# Usage

## Configuration

Provide your api key and environment to get started. The default environment, production is usually sufficient to get started.
If you want to use the test key, leave the API key parameter blank or `None` and set the environment to Sandbox.

```
import rocketreach

config = rocketreach.GatewayConfig(None, rocketreach.GatewayEnvironment.sandbox)
rr = rocketreach.Gateway(config)
result = rr.account.get()
if result.is_success:
    print(result.account)
```

Or use the short-hand arguments and use the default `GatewayConfig`:

```
import rocketreach
rr = rocketreach.Gateway(api_key='my-api-key')
```

## Searches

After configuring your gateway perform RocketReach searches:

```
import rocketreach

rr = rocketreach.Gateway(rocketreach.GatewayConfig('api-key'))
s = rr.person.search().filter(current_employer='Acme', current_title='CEO')
result = s.execute()
for person in result.people:
    print(person)
```

To paginate search queries, call the `params()` method and provide a `start` and/or `size`:
```
import rocketreach

rr = rocketreach.Gateway(rocketreach.GatewayConfig('api-key'))
s = rr.person.search().filter(current_employer='Acme', current_title='CEO')
s = s.params(start=11, size=25)
result = s.execute()
for person in result.people:
    print(person)
```

## Lookups

To lookup a person, provide an `id` or `linkedin_url`. Note that not all people will have an `id`, so be sure
to allow the flexibility to use either attribute. At least one is garuanteed to exist. After a succesful lookup,
a person is gauranteed to have an `id` which can be used to check the lookup progress via the `checkStatus()` method.

By default, the `lookup` method is blocking and will add the person to your account's lookups as well
as poll `checkStatus` until the lookup has completed.
```
import rocketreach

rr = rocketreach.Gateway(rocketreach.GatewayConfig('api-key'))
result = rr.person.lookup(person_id=123)
print(result.person)
result = rr.person.lookup(linkedin_url='https://www.linkedin.com/in/john-doe-example')
print(result.person)
```

## Check Status

If you prefer not to block on lookups, pass `block=False` and use the `checkStatus` method manually.
Note that RocketReach does not block the lookup API endpoint, instead the system will mark the lookup as
added to your account and will begin searching for contact information in the background. The system may
finish the lookup inline in some instances, but in the majority of cases the person status will be incomplete.
Using `checkStatus` is the easiest way to find when the person's contact information has been found.

When calling `checkStatus` keep in mind that tight loops are best avoided, and may result in a rate limiting
error, indicated by a 429 status code. If a request fails with that status code, you can check the error
message to see how long to wait for your next request -- usually just a few seconds.

```
import rocketreach

rr = rocketreach.Gateway(rocketreach.GatewayConfig('api-key'))
result = rr.person.lookup(person_id=123, block=False)
while result.status != PersonLookupStatus.complete:
    result = rr.person.check_status([result.person.id])
    if not result.is_success and result.response.status_code == 429:
        time.sleep(1)
```

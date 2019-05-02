# Getting Started
This is a simple RocketReach client implemented in Python for doing lookups.

## Dependencies
Use pipenv to manage dependencies.

Example:
```
$ cd rocketreach_python
$ pipenv install
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
# vaccinecheck
Washington State Covid Vaccine Check

## Requirements
- Chrome
- Chrome Webdriver
- Python 3+
- A Programmatic AWS user with SNS permissions

## Setup
Install required python libraries
```
pip install -r requirements.txt
```    

Set the recipient phone numbers in the PHONE_NUMBERS list
```
PHONE_NUMBERS = ['+12223331234', '+12223331235']
```   

Set the admin phone number in the ADMIN_NUMBER list for script failures
```
ADMIN_NUMBER = ['+12223331234']
``` 

Set the INTERVAL (how often to check for vaccine openings) in seconds
```
INTERVAL = ['+12223331234']
```

Set the COUNTY in the format of **COUNTYNAME**+COUNTY
```
COUNTY = "CLARK+COUNTY"
```

Set the AWS Access and Secret key for your programmatic user.
``` 
GATEWAY.add_provider('amazon', AmazonSNSProvider,
    access_key='AWS_ACCESS_KEY',
    secret_access_key='AWS_SECRET_KEY',
    region_name='us-west-2',
)
```



## Usage
```
python covid_vaccines.py
```

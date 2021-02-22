'''Script to notify via SMS when COVID Vaccines Scheduling is available.'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from smsframework import Gateway
from smsframework_amazon_sns import AmazonSNSProvider
from smsframework import OutgoingMessage
import time
import json

INTERVAL = 60
SLEEP = 1
COUNTY = 'Clark+County'
PHONE_NUMBERS = ['+12223331234','+12223331235']
ADMIN_NUMBER = ['+12223331234']
DATA = {
  "Available": {
    "Links": [],
    "LastLinks": []
    },
  
  "Possible": {
    "Links": [],
    "LastLinks": []
  }
}

GATEWAY = Gateway()
GATEWAY.add_provider('amazon', AmazonSNSProvider,
    access_key='AWS_ACCESS_KEY',
    secret_access_key='AWS_SECRET_KEY',
    region_name='us-west-2',
)

def send_sms(recipients, message):
  '''Send SMS to recipients with message'''
  for pnumber in recipients:
    GATEWAY.send(OutgoingMessage(pnumber, message))

i = 1

while i > 0:
  try:
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.covidwa.com/?status=Available&county=%s" % (COUNTY))
    time.sleep(SLEEP)
    available = driver.find_elements_by_css_selector("button[class*='ms-Button']")
    for ele in available:
      url = ele.get_attribute("title")
      if "http" in url:
        DATA['Available']['Links'].append(url) 

    driver.get("https://www.covidwa.com/?status=Possible&county=%s" % (COUNTY))
    time.sleep(SLEEP)
    possible = driver.find_elements_by_css_selector("button[class*='ms-Button']")
    for ele in possible:
      url = ele.get_attribute("title")
      if "http" in url:
        DATA['Possible']['Links'].append(url)

    driver.close()
    #print(json.dumps(DATA, indent=4))
    if len(DATA['Available']['Links']) > 0:
      message = "Available Openings for Vaccines:\n\n"
      message = message + '\n\n'.join(DATA['Available']['Links'])
      if set(DATA['Available']['Links']) != set(DATA['Available']['LastLinks']):
        print("Sending SMS: %s" % (message))
        send_sms(PHONE_NUMBERS, message)
    DATA['Available']['LastLinks'] = DATA['Available']['Links']
    DATA['Available']['Links'] = []


    if len(DATA['Possible']['Links']) > 0:
      message = "\n\nPossible Openings for Vaccines:\n\n"
      message = message + '\n\n'.join(DATA['Possible']['Links'])
      if set(DATA['Possible']['Links']) != set(DATA['Possible']['LastLinks']):
        print("Sending SMS: %s" % (message))
        send_sms(PHONE_NUMBERS, message)
    DATA['Possible']['LastLinks'] = DATA['Possible']['Links']
    DATA['Possible']['Links'] = []

  except:
    send_sms(ADMIN_NUMBER, 'COVID Vaccine Script Failing')
  time.sleep(INTERVAL)
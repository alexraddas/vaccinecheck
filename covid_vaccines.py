'''Script to notify via SMS when COVID Vaccines Scheduling is available.'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from smsframework import Gateway
from smsframework_amazon_sns import AmazonSNSProvider
from smsframework import OutgoingMessage
import time

COUNTY = 'Clark+County'
PHONE_NUMBERS = ['+12223331234', '+12223331235']
ADMIN_NUMBER = ['+12223331234']
DATA = {
  "Available": [],
  "Possible": []
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
    driver = webdriver.Chrome()
    driver.get("https://www.covidwa.com/?status=Available&county=%s" % (COUNTY))
    time.sleep(2)
    available = driver.find_elements_by_css_selector("button[class*='ms-Button']")
    for ele in available:
      url = ele.get_attribute("title")
      if "http" in url:
        DATA['Available'].append(url) 

    driver.get("https://www.covidwa.com/?status=Possible&county=%s" % (COUNTY))
    time.sleep(2)
    possible = driver.find_elements_by_css_selector("button[class*='ms-Button']")
    for ele in possible:
      url = ele.get_attribute("title")
      if "http" in url:
        DATA['Possible'].append(url)

    driver.close()

    if len(DATA['Available']) > 0:
      message = "Available Openings for Vaccines:\n\n"
      message = message + '\n\n'.join(DATA['Available'])
      send_sms(PHONE_NUMBERS, message)

    if len(DATA['Possible']) > 0:
      message = "\n\nPossible Openings for Vaccines:\n\n"
      message = message + '\n\n'.join(DATA['Possible'])
      send_sms(PHONE_NUMBERS, message)

  except:
    send_sms(ADMIN_NUMBER, 'COVID Vaccine Script Failing')
  time.sleep(60)
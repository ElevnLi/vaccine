from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# Download Chrome webdriver from: https://chromedriver.chromium.org/downloads and put it under the same directory

username = "<Your email>"
password = "<Your password>"
# How many days in advance of your current booking you are willing to switch
day_buffer = 1
# Which month do you want to look at
month_of_interest = ("July", "August", "September")
month_step = {"Jul": 0, "Aug": 31, "Sep": 62, "Oct": 92}


def get_number_of_date(date):
    month, day = date.split()
    return month_step[month] + int(day)


driver = webdriver.Chrome('./chromedriver')
driver.get("https://nswhvam.health.nsw.gov.au/vam?id=reschedule_vaccination")
elem = driver.find_element_by_id("username")
elem.send_keys(username)
elem = driver.find_element_by_id("password")
elem.send_keys(password)
elem.send_keys(Keys.RETURN)

import pdb; pdb.set_trace()
# For you to type in multi-factor code
# press 'c' to continue

while True:
    time.sleep(3)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/section/header/div/header/div[1]/div/div[1]/a'))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="vaccine-booking-list"]/ul/li[1]/article/a'))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="reschedule-apt"]/div/a'))).click()
        
        current_booking = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="appointmentBookingAvailabilityModal"]/div/div[2]/section/p/b[2]'))).text.split(', ')[1]
        print(f"### Current booking at: {current_booking} ###")
        _ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'appointmentInfo')))
        month = driver.find_element_by_xpath('//*[@id="appointmentBookingAvailabilityModal"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div/span').text.split()[0]
        if month not in month_of_interest:
            print(f"### Ignore month: {month} ###")
            continue
        driver.find_elements_by_class_name('content')[0].find_elements_by_tag_name('div')[0].click()

        date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="appointmentBookingAvailabilityModal"]/div/div[2]/div/div/div[2]/b[1]'))).text.split(', ')[1]
        print(f"### Available date: {date} ###")
        if get_number_of_date(date) + day_buffer > get_number_of_date(current_booking):
            print(f"### Ignore date: {date} ###")
            continue
        _ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'appointmentInfo')))
        time.sleep(0.3)
        driver.find_elements_by_class_name('content')[-1].find_elements_by_tag_name('div')[-1].click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'submitBtn'))).click()
    except Exception:
        print("### Current search/booking failed ###")
        driver.get("https://nswhvam.health.nsw.gov.au/vam")
        continue
    else:
        print(f"### Trying to book date: {date} ###")
        time.sleep(10)

import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from flask import Flask, request, jsonify
from email.message import EmailMessage
from datetime import datetime
# from prettytable import PrettyTable

import pandas as pd

app = Flask(__name__)
# Configure logging
logging.basicConfig(level=logging.INFO)



while True:
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    # Navigate to the webpage
    driver.get('https://taostats.io/validators/neural-internet/')

    # Adding a delay after the page loads
    time.sleep(2)

    # Wait for the elements to be present on the page
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'staking_data_block')))
    except Exception as e:
        logging.error(f"Error waiting for elements: {e}")
        driver.quit()
    # continue  # Continue to the next iteration of the loop

    # locate the data_block
    data_block = driver.find_elements(By.CLASS_NAME, 'staking_data_block')

    # Lists
    SN = []
    Updated = []
    Vtrust = []
    vtrust_below_threshold = []  
    Updated_below_threshold = []  

# Process the found elements as needed

    for block in data_block:
        try:
            #SN.append(block.find_element(By.XPATH, './/div[1]/div/small').text)
            SN.append(block.find_element(By.XPATH, './/div[1]/div[@class="stake_val"]/small').text)
            updated_value = block.find_element(By.XPATH, './/div[6]/div/small').text
            Updated.append(updated_value)
            vtrust_value = float(block.find_element(By.XPATH, './/div[7]/div/small').text)
            Vtrust.append(vtrust_value)

            logging.info(f"Data extracted for SN: {SN[-1]}, Updated: {updated_value}, VTrust: {vtrust_value}")

            # Check if Vtrust is below 0.90 and store the information
            print("updated_value : "+updated_value+" Type : "+str(type(updated_value)))
            # if vtrust_value < 0.90 :
            vtrust_below_threshold.append((SN[-1], updated_value, vtrust_value))


        except NoSuchElementException as e:
            logging.error(f"Error extracting data: {e}. Skipping this validator.")
            continue  # Skip to the next iteration if an element is not found
        except ValueError as e:
            logging.error(f"Error converting Vtrust value to float: {e}. Skipping this validator.")
            continue  # Skip to the next iteration if the Vtrust value cannot be converted to float
    print(vtrust_below_threshold)
    # Close the WebDriver
    driver.quit()
    now = datetime.now()
    current_time = now.time()
    current_date = now.date()
    df = pd.DataFrame({
        'SN': SN,
        'Updated': Updated,
        'Vtrust': Vtrust,
        'Date':current_date,
        'Time':current_time,
        'datetime':now


    })


    print(df)
    df.to_csv('vtrust_log.csv', mode='a', header=False, index=False)
    time.sleep(14400)
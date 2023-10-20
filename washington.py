from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime, timedelta


# import fitz 
# doc = fitz.open('a.pdf') 
# text = "" 
# for page in doc: 
#    text+=page.get_text() 
# print(text) 



# from PyPDF2 import PdfReader
# import glob
# import os

# list_of_files = glob.glob('C:/Users/Administrator/Downloads/*') # * means all if need specific format then *.csv
# latest_file = max(list_of_files, key=os.path.getctime)
# # print(len(list_of_files))
# print(latest_file)

 
  
# # creating a pdf reader object 
# reader = PdfReader(latest_file) 
  
# # printing number of pages in pdf file 
# print(len(reader.pages)) 
  
# # getting a specific page from the pdf file 
# page = reader.pages[0] 
  
# # extracting text from page 
# text = page.extract_text() 
# print(text) 


def convert_to_standard_date_format():
    current_date = datetime.now().date()
    one_day_before = current_date - timedelta(days=1)
    formatted_date = one_day_before.strftime("%m/%d/%Y")
    return formatted_date

# configure webdriver
options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen
# configure chrome browser to not load images and javascript
chrome_options = webdriver.ChromeOptions()

# Inicializa o ChromeDriver 
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.sos.wa.gov/corporations-charities")
# wait for page to load
element = WebDriverWait(driver=driver, timeout=5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
)
time.sleep(5)

filter_button = driver.find_element(By.CLASS_NAME, 'btn-green')
filter_button.click()
time.sleep(5)

advanced_search_buttons = driver.find_elements(By.CLASS_NAME, 'btn-advdSearch')
advanced_search_buttons[0].click()
time.sleep(5)

start_date_input = driver.find_element(By.ID, 'txtStartDateOfIncorporation')
end_date_input = driver.find_element(By.ID, 'txtEndDateOfIncorporation')
standard_date = convert_to_standard_date_format()

start_date_input.send_keys(standard_date)
time.sleep(1)
end_date_input.send_keys(standard_date)
time.sleep(1)

search_button = driver.find_element(By.XPATH, '//*[@id="btnSearch"]')
search_button.click()
time.sleep(5)

page_span = driver.find_element(By.XPATH, '//span[contains(@class, "ng-binding") and contains(@style, "1%")]')
# print(page_span.text)

# Find the <ul> element with class attribute "pagination"
pagination_ul = driver.find_element(By.CLASS_NAME, 'pagination') # the same as (By.CSS_SELECTORS, 'ul.pagination')

# Find all the <li> elements inside the <ul> element
pagination_lis = pagination_ul.find_elements(By.TAG_NAME, 'li')

a = driver.find_element(By.CSS_SELECTOR, 'ul.pagination li:nth-child('+f"{len(pagination_lis) - 1}" + ') a')
a.click()
time.sleep(4)
a.click()
time.sleep(4)

# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='newsletter_popup_close-cta']"))).click()
# print([my_elem.get_attribute("href") for my_elem in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.core[data-brand='Always'][href]")))])

table_element = driver.find_element(By.CLASS_NAME, 'table-responsive')
table_trs = driver.find_elements(By.CSS_SELECTOR, 'table.table-responsive tbody tr')
for j in range(1, len(table_trs)-1):
    # wait = WebDriverWait(driver,60)
    # succeed = False
    # while not succeed:
    #     try:
    #         wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'table.table-responsive tbody tr:nth-child(' + f"{j}" + ') td a'))).click()
    #         succeed = True
    #     except:
    #         pass

    table_td = driver.find_elements(By.CSS_SELECTOR, 'table.table-responsive tbody tr:nth-child(' + f"{j}" + ') td')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'table.table-responsive tbody tr:nth-child(' + f"{j}" + ') td')))
    table_a = table_td.find_element(By.TAG_NAME, 'a')
    
    # table_a.click()
    driver.execute_script("arguments[0].ng-click();", table_a)

    print(table_a.text)
    time.sleep(5)
    # history_btn = driver.find_element(By.ID, 'btnFilingHistory')
    # history_btn.click()

    # pdf_table = driver.find_element(By.CLASS_NAME, 'table-striped')
    # pdf_table_tbody = driver.find_elements(By.CSS_SELECTOR, 'table.table-striped tbody')[0]
    # pdf_table_trs = pdf_table_tbody.find_elements(By.CSS_SELECTOR, 'tr')
    # print(len(pdf_table_trs))
    # driver.back()

# for i in range(4):
#     time.sleep(3)
#     pagination_lis[len(pagination_lis) - 2].click()

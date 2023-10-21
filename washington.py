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
import re

# import fitz 
# doc = fitz.open('a.pdf') 
# text = "" 
# for page in doc: 
#    text+=page.get_text() 
# print(text) 



from PyPDF2 import PdfReader
import glob
import os




def convert_to_standard_date_format():
    current_date = datetime.now().date()
    one_day_before = current_date - timedelta(days=1)
    formatted_date = one_day_before.strftime("%m/%d/%Y")
    return formatted_date

def is_contains_number(string):
    pattern = r'\d'  # regular expression pattern for any digit

    if re.search(pattern, string):
        return True
    else:
        return False
    
def is_email_format(string):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # regular expression pattern for email format

    if re.match(pattern, string):
        return True
    else:
        return False


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

# a = driver.find_element(By.CSS_SELECTOR, 'ul.pagination li:nth-child('+f"{len(pagination_lis) - 1}" + ') a')
# a.click()
# time.sleep(4)
# a.click()
# time.sleep(4)


table_element = driver.find_element(By.CSS_SELECTOR, 'table.table')
table_trs = table_element.find_elements(By.CSS_SELECTOR, 'tbody tr')

# for j in range(0, len(table_trs)-1):
table_element = driver.find_element(By.CSS_SELECTOR, 'table.table')
table_trs = table_element.find_elements(By.CSS_SELECTOR, 'tbody tr')
# print(len(table_trs))
time.sleep(1)
table_tds = table_trs[0].find_element(By.CSS_SELECTOR, 'td a')
try:
    table_tds.click()
    time.sleep(2)
    history_btn = driver.find_element(By.ID, 'btnFilingHistory')
    history_btn.click()
    time.sleep(2)
    pdf_table = driver.find_elements(By.CSS_SELECTOR, 'table.table')
    pdf_table_tbody = pdf_table[0].find_element(By.CSS_SELECTOR, 'tbody')
    pdf_table_trs = pdf_table_tbody.find_elements(By.CSS_SELECTOR, 'tr')
    pdf_table_tds = pdf_table_trs[len(pdf_table_trs) - 1].find_elements(By.CSS_SELECTOR, 'td')
    view_pdf_a = pdf_table_tds[len(pdf_table_tds) - 1].find_element(By.TAG_NAME, 'a')
    time.sleep(1)
    view_pdf_a.click()
    time.sleep(4)
    
    final_pdf_table_tbodies = pdf_table[1].find_elements(By.CSS_SELECTOR, 'tbody')
    final_pdf_table_trs = final_pdf_table_tbodies[len(final_pdf_table_tbodies) - 2].find_elements(By.CSS_SELECTOR, 'tr')
    final_pdf_table_tds = final_pdf_table_trs[len(final_pdf_table_trs) - 1].find_elements(By.CSS_SELECTOR, 'td')
    final_pdf_table_i = final_pdf_table_tds[len(final_pdf_table_tds) - 1].find_element(By.TAG_NAME, 'i')
    time.sleep(2)
    final_pdf_table_i.click()
    time.sleep(4)
    
    
    list_of_files = glob.glob('C:/Users/Christian/Downloads/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    # print(len(list_of_files))

    
    
    # creating a pdf reader object 
    reader = PdfReader(latest_file) 
    
    # printing number of pages in pdf file 
    
    
    # getting a specific page from the pdf file 
    text = ''
    for i in range(0, len(reader.pages)):
        page = reader.pages[i]
        page_text = page.extract_text()
        # extracting text from page 
        text = text + page_text

    try:
        lines = text.splitlines()
        ubi_number = ''
        business_name = ''
        phone_number = ''
        email = ''
        address = ''
        first_name = ''
        last_name = ''
        for i in range(len(lines)):
            if 'UBI Number:' in lines[i]:  # Case-sensitive match
                if i + 1 < len(lines):
                    if is_contains_number(lines[i + 1]):
                        ubi_number = lines[i + 1]
            if 'Business Name' in lines[i]: 
                if i + 1 < len(lines):
                    business_name = lines[i + 1]
            if 'Phone:' in lines[i]:
                if i + 1 < len(lines):
                    if is_contains_number(lines[i + 1]):
                        phone_number = lines[i + 1]
            if 'Email:' in lines[i] and email == '':
                if i + 1 < len(lines):
                    if is_email_format(lines[i + 1]):
                        email = lines[i + 1]
            if 'Street Address:' in lines[i]:
                if i + 1 < len(lines):
                    address = lines[i + 1]
            if 'First Name:' in lines[i]:
                if i + 1 < len(lines):
                    first_name = lines[i + 1]
            if 'Last Name:' in lines[i]:
                if i + 1 < len(lines):
                    last_name = lines[i + 1]
        print(ubi_number + '  =======  ' + business_name + '  ==========  ' + phone_number + '  ==========  ' + email + '  =======  ' + address + '  ==========  ' + first_name + '  ==========  ' + last_name)
    except Exception as e:
        print(f"{e}")
    driver.back()
    time.sleep(3)
    driver.back()
    time.sleep(3)
except Exception as e:
    print(f"{e}")
    # table_a = table_tds[0].find_element(By.CSS_SELECTOR, 'a')
    # table_a.click()

    # driver.execute_script("arguments[0].ng-click();", table_a)
    # time.sleep(5)
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

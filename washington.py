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


import tkinter as tk
from multiprocessing import freeze_support, Lock
from multiprocessing.pool import ThreadPool
from tkinter import filedialog as fd
from tkinter import ttk

import sv_ttk

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

def get_substring(string):
    start_index = string.find('of') + 3
    end_index = string.rfind(',')

    if start_index >= 0 and end_index >= 0 and end_index > start_index:
        substring = string[start_index:end_index]
        return substring
    else:
        return None

total_results = []
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

table_element = driver.find_element(By.CSS_SELECTOR, 'table.table')
table_trs = table_element.find_elements(By.CSS_SELECTOR, 'tbody tr')
page_num_str = get_substring(page_span.text)

# print(len(pagination_lis))
if page_num_str is not None:
    page_num = int(page_num_str)
    # print(page_num)
    time.sleep(2)
    for k in range(2, page_num - 1):
        try:
            if k > 0:
                for p in range(k):
                    nav = pagination_lis[-2].find_element(By.TAG_NAME, 'a')
                    time.sleep(2)
                    nav.click()
                    time.sleep(2)
            
            for j in range(0, len(table_trs)-1):
                table_element = driver.find_element(By.CSS_SELECTOR, 'table.table')
                table_trs = table_element.find_elements(By.CSS_SELECTOR, 'tbody tr')
                
                table_tds = table_trs[j].find_element(By.CSS_SELECTOR, 'td a')
                try:
                    time.sleep(3)
                    table_tds.click()
                    time.sleep(4)
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

                    driver.refresh()                    
                    list_of_files = glob.glob('C:/Users/Christian/Downloads/*') # * means all if need specific format then *.csv
                    latest_file = max(list_of_files, key=os.path.getctime)

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
                        one_item = {}
                        one_item["ubi_number"] = ubi_number
                        one_item["business_name"] = business_name
                        one_item["phone_number"] = phone_number
                        one_item["email"] = email
                        one_item["address"] = address
                        one_item["first_name"] = first_name
                        one_item["last_name"] = last_name

                        total_results.append(one_item)
                        if len(total_results) > 24:
                            current_datetime = datetime.datetime.now()
                            csv_file = f"washington-{current_datetime.strftime('%d-%m-%Y %H_%M_%S')}.csv"

                            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                                fieldnames = ["business_name", "ubi_number", "phone_number", "email", "address", "first_name", "last_name"]
                                writer = csv.DictWriter(file, fieldnames=fieldnames)

                                writer.writeheader()
                                for item in total_results:
                                    writer.writerow(item)
                            total_results = []
                    except Exception as e:
                        print(f"{e}")
                    driver.back()
                    time.sleep(3)
                    driver.back()
                    time.sleep(3)
                    # Find the <ul> element with class attribute "pagination"
                    pagination_ul = driver.find_element(By.CLASS_NAME, 'pagination') # the same as (By.CSS_SELECTORS, 'ul.pagination')

                    # Find all the <li> elements inside the <ul> element
                    pagination_lis = pagination_ul.find_elements(By.TAG_NAME, 'li')
                    if k > 0:
                        for p in range(k):
                            nav = pagination_lis[-2].find_element(By.TAG_NAME, 'a')
                            time.sleep(2)
                            nav.click()
                            time.sleep(2)
                except Exception as e:
                    print(f"{e}")
                    
        except Exception as e:
            print(f"{e}")
        

    # rest item less than 25
    if len(total_results) > 0:
        current_datetime = datetime.datetime.now()
        csv_file = f"washington-{current_datetime.strftime('%d-%m-%Y %H_%M_%S')}.csv"

        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["business_name", "ubi_number", "phone_number", "email", "address", "first_name", "last_name"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for item in total_results:
                writer.writerow(item)


# if __name__ == '__main__':
#     freeze_support()

#     app = tk.Tk()
#     app.title(f'Washington Website Scraper')
#     app.geometry('400x400')
#     app.minsize(400, 400)
#     app.maxsize(400, 400)

#     ttk.Frame(app, height=30).pack()
#     title = tk.Label(app, text='Washington Website Scraper', font=("Calibri", 24, "bold"))
#     title.pack(pady=20)

#     startbot = ttk.Button(app, text='Start Bot', style='Accent.TButton', width=15,
#                           command=lambda: main())
#     startbot.pack(pady=10)

#     info_text = ttk.Label(app, text='', justify=tk.CENTER)
#     info_text.pack(pady=5)

#     sv_ttk.set_theme('dark')
#     app.mainloop()

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


WEBSITE = 'https://hk.jobsdb.com/hk/job-list/information-technology/data-scientist/'
LOAD_SEC_PER_JOB = 3       # increase if internet is slow

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(WEBSITE+'1')
# the landing page of Browse by job type/Information Technology(IT)/Data scientist
time.sleep(3)

last_page = (driver.find_elements(By.XPATH, '//*[@id="pagination"]/option')[-1].text)
print('last page is ', last_page)
for i in range(1, int(last_page)+1):
    next_page = WEBSITE+str(i)
    print(next_page)
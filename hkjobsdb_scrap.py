from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


WEBSITE = 'https://hk.jobsdb.com/hk/job-list/information-technology/data-scientist/1'
LOAD_SEC_PER_JOB = 5        # increase if internet is slow


def get_job_ad_data ():
    """
    :param: element containing a single complete job ad at the right panel
    :return: a list of elements containing job ad data by category: title, company, salary, posted_date, district, job description
    """
    # title, company
    single_job_ad_data = []
    time.sleep(LOAD_SEC_PER_JOB)
    try:
        title = driver.find_element(By.XPATH, '//h1[@class ="sx2jih0 _18qlyvc0 _18qlyvch _1d0g9qk4 _18qlyvcp _18qlyvc1x"]').text
    except NoSuchElementException:
        title = 'title'     # scrape fail/missing value placeholder
    single_job_ad_data.append(title)

    try:
        company = driver.find_element(By.XPATH, '//span[@class="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc2 _1d0g9qk4 _18qlyvcb"]').text
    except NoSuchElementException:
        company = 'company'
    single_job_ad_data.append(company)

    posted_date = 'posted_date'
    blob = driver.find_elements(By.XPATH, '//span[@class ="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca"]')
    #
    bblob_1 = [blob[5].text, blob[6].text, blob[7].text]
    posted_date = 'posted_date'
    salary = 'salary'
    district = 'district'
    try:
        for i in bblob_1:
            if 'posted' in i.lower() and len(i)<30:
                posted_date = i
            elif 'hk' in i.lower() and len(i)<30:
                salary = i
            elif len(i)<30:
                district = i
    except NoSuchElementException:
        pass
    single_job_ad_data.append(salary)
    single_job_ad_data.append(posted_date)
    single_job_ad_data.append(district)

    # job description
    job_description = driver.find_element(By.XPATH, '//div[@data-automation="jobDescription"]').text
    single_job_ad_data.append(job_description)

    '''
    # test code do not delete
    temp = driver.find_elements(By.XPATH, '//span[@class ="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca"]')
    k = 0
    for i in temp:
        s = i.text
        single_job_ad_data.append(f'*{k}*\n'+s)
        k += 1
    '''

    return single_job_ad_data


options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(WEBSITE)
# the landing page of Browse by job type/Information Technology(IT)/Data scientist
time.sleep(3)

# left_panel_job_list = driver.find_elements(By.XPATH, '//*[@id="jobList"]')
# for job in left_panel_job_list:
#    print(job.text)

left_panel_job_link_list = driver.find_elements(By.XPATH, '//div[@class="sx2jih0 zcydq8n lmSnC_0"]')
max_job_per_page = 30
current_reading_job_item = 0        # counter
scrolling = True

while scrolling:

    for job_link in left_panel_job_link_list:

        job_link.location_once_scrolled_into_view
        job_link.click()

        # visit the right panel
        job_ad_data = get_job_ad_data()
        for item in job_ad_data:
            print('~'+item)
        print('***')
        current_reading_job_item += 1
        if current_reading_job_item > max_job_per_page:
            scrolling = False
            break
driver.quit()

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
from datetime import date


WEBSITE = 'https://hk.jobsdb.com/hk/job-list/information-technology/data-scientist/'
LOAD_SEC_PER_JOB = 5       # increase if internet is slow


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
    except exceptions.NoSuchElementException:
        title = 'title'     # scrape fail/missing value placeholder

    try:
        company = driver.find_element(By.XPATH, '//span[@class="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc2 _1d0g9qk4 _18qlyvcb"]').text
    except exceptions.NoSuchElementException:
        company = 'company'

    posted_date = 'posted_date'
    salary = 'salary'
    district = 'district'
    try:
        blob = driver.find_elements(By.XPATH, '//span[@class ="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca"]')
        bblob_1 = [blob[5].text, blob[6].text, blob[7].text]
        for i in bblob_1:
            if 'posted' in i.lower() and len(i)<30:
                posted_date = i
            elif 'hk' in i.lower() and len(i)<30:
                salary = i
            elif len(i)<30:
                district = i
    except exceptions.NoSuchElementException:
        pass

    # job description
    try:
        job_description = driver.find_element(By.XPATH, '//div[@data-automation="jobDescription"]').text
    except:
        job_description = 'job_description'

    single_job_ad_data.append(title)
    single_job_ad_data.append(company)
    single_job_ad_data.append(salary)
    single_job_ad_data.append(posted_date)
    single_job_ad_data.append(district)
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


def page_list (driver):
    # generate page list
    time.sleep(LOAD_SEC_PER_JOB)
    last_page = driver.find_elements(By.XPATH, '//*[@id="pagination"]/option')[-1].text
    page_list = []
    print('last page is ', last_page)
    for i in range(1, int(last_page)+1):
        next_page = WEBSITE+str(i)
        # print(next_page)
        page_list.append(next_page)
    return page_list


# setup driver
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(WEBSITE+'1')
# the landing page of Browse by job type/Information Technology(IT)/Data scientist


search_results = page_list(driver)

i = 1
jobs_title = []
jobs_company = []
jobs_salary = []
jobs_posted_date = []
jobs_district = []
jobs_job_description = []

for page in search_results:

    print('trying: ', page)
    driver.get(page)
    time.sleep(LOAD_SEC_PER_JOB)
    current_reading_job_item = 1
    max_job_per_page = len(driver.find_elements(By.XPATH, '//div[@data-search-sol-meta]'))
    scrolling = True

    # single page
    while scrolling:

        try:

            left_panel_job_link_list = driver.find_elements(By.XPATH, '//div[@class="sx2jih0 zcydq8n lmSnC_0"]')

            for job_link in left_panel_job_link_list:

                job_link.location_once_scrolled_into_view
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(job_link)).click()
                except exceptions.ElementClickInterceptedException:
                    print('job not clickable')
                    pass

                # visit the right panel to access data of this job
                single_job_ad_data = get_job_ad_data()

                jobs_title.append(single_job_ad_data[0])
                jobs_company.append(single_job_ad_data[1])
                jobs_salary.append(single_job_ad_data[2])
                jobs_posted_date.append(single_job_ad_data[3])
                jobs_district.append(single_job_ad_data[4])
                jobs_job_description.append(single_job_ad_data[5])

                i += 1
                # for item in single_job_ad_data:
                #    print('~'+item)
                print('job ad number: ',i)
                current_reading_job_item += 1
                if current_reading_job_item > max_job_per_page:
                    scrolling = False
                    break
        except exceptions.StaleElementReferenceException:
            print('stale')
            # prevent the program from breaking when there is not more job ad to scrap on this single page
            break
    print('loading next page')
print('end of scrapping')

# export result to pandas
df = pd.DataFrame({'title': jobs_title,
                   'company': jobs_company,
                   'salary': jobs_salary,
                   'posted_date': jobs_posted_date,
                   'district': jobs_district,
                   'description': jobs_job_description})

today = str(date.today())
df.to_csv(f'{today}.csv', index=False)

driver.quit()

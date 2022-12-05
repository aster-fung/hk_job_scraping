import time
from csv import DictWriter
from datetime import date

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import hkjobsdb_date_reformat

TARGET_JOB = 'data-scientist'
WEBSITE = f'https://hk.jobsdb.com/hk/job-list/information-technology/{TARGET_JOB}/'
LOAD_SEC_PER_JOB = 5       # increase if internet is slow

TODAY_STR = str(date.today())


def generate_list_of_job_pages(element_driver):
    # generate page list
    time.sleep(LOAD_SEC_PER_JOB)
    last_page = element_driver.find_elements(By.XPATH, '//*[@id="pagination"]/option')[-1].text
    job_page_list = []
    print('last page is ', last_page)
    for i in range(1, int(last_page)+1):
        next_page = WEBSITE+str(i)
        # print(next_page)
        job_page_list.append(next_page)
    return job_page_list


def initialize_field_names():
    field_names_fscope = ['title',
                          'salary',
                          'company',
                          'posted',
                          'district',
                          'job_description',
                          'Career Level',
                          'Years of Experience',
                          'Company Website',
                          'Qualification',
                          'Job Type',
                          'Job Functions'
                          ]
    return field_names_fscope


def get_job_ad_data():
    """
    :param: element containing a single complete job ad at the right panel
    :return: a list of elements containing job ad data by category: title, company, salary, posted_date, district, job description
    """
    # title, company
    single_job_ad_data_fscope = []
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
            if 'posted' in i.lower() and len(i) < 30:
                posted_date = hkjobsdb_date_reformat.date_reformat(i)
            elif 'hk' in i.lower() and len(i) < 30:
                salary = i
            elif len(i) < 30:
                district = i
    except exceptions.NoSuchElementException:
        pass

    # job description
    try:
        job_description = driver.find_element(By.XPATH, '//div[@data-automation="jobDescription"]').text
    except:
        job_description = 'job_description'

    # get additional info about the job add
    # separate function because of the html structure

    single_job_ad_data_fscope.append(title)
    single_job_ad_data_fscope.append(salary)
    single_job_ad_data_fscope.append(company)
    single_job_ad_data_fscope.append(posted_date)
    single_job_ad_data_fscope.append(district)
    single_job_ad_data_fscope.append(job_description)

    return single_job_ad_data_fscope


def scrap_additional_info_as_dict():
    """
    :return: a dictionary of scrapped text. keys are Career Level, Years of Experience, Company Website, Qualification, Job Type, Job Functions
    """
    time.sleep(5)
    # assume all data are missing
    additional_columns_default = ['Career Level', 'Years of Experience', 'Company Website', 'Qualification', 'Job Type', 'Job Functions']
    additional_values_default = ['career', 'yearsofexperience', 'companywebsite', 'qualification', 'jobtype', ]
    additional_info_dict = dict(map(lambda i, j: (i, j), additional_columns_default, additional_values_default))
    try:
        additional_table = driver.find_element(By.XPATH, '//div[@class ="sx2jih0 zcydq856 zcydq8fe _17fduda27"]')
        # a table containing 6 pieces of info
        additional_info_raw = additional_table.text
        additional_info_list = additional_info_raw.split('\n')
        table_len = len(additional_info_list)
        additional_columns = []
        additional_values = []
        for i in range(table_len):
            if i % 2 == 0:
                additional_columns.append(additional_info_list[i])
            else:
                additional_values.append(additional_info_list[i])
                additional_info_dict = dict(map(lambda i, j: (i, j), additional_columns, additional_values))
    except exceptions.NoSuchElementException:
        print('failed to scrape additional info')
        # the additional data remains the default values
        # meaning they are missing
        pass
    return additional_info_dict
    # always has 6 key/value pairs


# setup driver
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(WEBSITE+'1')
# the landing page of Browse by job type/Information Technology(IT)/Data scientist


search_results = generate_list_of_job_pages(driver)

scrap_count = 1
field_names = initialize_field_names()
file_name = f'{TARGET_JOB}-{TODAY_STR}-1.csv'

with open(file_name, 'w', encoding="utf-8", newline='') as fh:
    odictwriter = DictWriter(fh, fieldnames=field_names)
    odictwriter.writeheader()

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

                current_entry_part_1 = {'title': single_job_ad_data[0],
                                        'salary': single_job_ad_data[1],
                                        'company': single_job_ad_data[2],
                                        'posted': single_job_ad_data[3],
                                        'district': single_job_ad_data[4],
                                        'job_description': single_job_ad_data[5]
                                        }
                # get dictionary
                current_entry_part_2 = scrap_additional_info_as_dict()
                print(current_entry_part_2)        # scaffold

                print('scrapping job ad number: ', scrap_count)
                scrap_count += 1

                # merge two scraped data
                current_entry_final = current_entry_part_1
                current_entry_final.update(current_entry_part_2)
                print('final')                       # scaffold
                print(current_entry_final)           # scaffold

                with open(file_name, 'a', encoding="utf-8", newline='') as fh:
                    odictwriter = DictWriter(fh, fieldnames=field_names)
                    odictwriter.writerow(current_entry_final)

                current_reading_job_item += 1
                if current_reading_job_item > max_job_per_page:
                    scrolling = False
                    break

        except exceptions.StaleElementReferenceException:
            print('end of page')
            # prevent the program from breaking when there is not more job ad to scrap on this single page
            break
    print('loading next page')
print('end of scrapping')
fh.close()

driver.quit()

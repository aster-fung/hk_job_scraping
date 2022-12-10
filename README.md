# Welcome to the dataset and the jupyter notebook for Hong Kong JobsDB job advertisement analysis

This dataset and notebook can be also found on Kaggle
[dataset](https://www.kaggle.com/datasets/asterfung/ds-obsdbhk)
[exploratory data anaylsis](https://www.kaggle.com/code/asterfung/data-science-jobs-in-hong-kong-eda)

Since we are here, we could agree that data science is a cool profession.

When "Data Science is the sexist job of the 21 century" by Harvard Business Review  took a storm on the internet on 2012, Hong Kong was still starting out on the big data trend. So, 10 years has past, what is the status quo of the data industry? To gain insights to answer this question, I have scrapped job postings from one of popular job posting platform in Hong Kong and perform some data analysis. 


## License

![CCBYNC4](https://img.shields.io/badge/License-Attribution--NonCommercial%204.0%20International%20(CC%20BY--NC%204.0)-blue)


## Dependency

Download and install ChromDriver
[ChromeDriver](https://chromedriver.chromium.org/downloads)

python libraries:

![selenium](https://img.shields.io/badge/selenium-4.7.0-orange)<br>
![pandas](https://img.shields.io/badge/pandas-1.5.2-yellow)
![matplotlib](https://img.shields.io/badge/matplotlib-3.6.2-yellow)
![scipy](https://img.shields.io/badge/scipy-1.9.3-yellow)
![seaborn](https://img.shields.io/badge/seaborn-0.12.1-yellow)<br>
![geopy](https://img.shields.io/badge/geopy-2.3.0-green)
![geopandas](https://img.shields.io/badge/geopandas-0.12.1-green)
![folium](https://img.shields.io/badge/folium-0.13.0-green)<br>



# the Dataset 

A python script was written [here](https://github.com/aster-fung/hk_job_scraping/blob/master/hkjobsdb_scrap.py) to scrape job postings under "Information Technology\Data Scientist" category. The script was implemented in a way that for each job posting was read, an observation ( row of data) is added to the csv file. Preliminary data cleaning was incoporated to the script to make the dataset easier for downstream processing. 


| column | null placeholder | non-null example |
|---|---|---|
| title | (not applicable) | Data Analyst - Top ranked Virtual Bank |
| salary | "salary" | HK$35,000 - HK$55,000 /month |
| company | "company" | CGP |
| posted | (not applicable) | 2022-11-18 |
| District | "district" | Shatin district |
| job description | (not applicable) | Job Description:  Research, collate, obtain and analyze data ... |
| Career level | empty | Entry Level |
| Years of Experience | empty | N/A |
| Company Website | empty | www.companyname.com |
| Qualification | empty | Degree |
| Job Type | empty | Full Time, Permanent |
| Job Functions | empty | Banking / Finance, Others, Information Technology (IT), Others, Data Scientist |
| url | empty | https://hk.jobsdb.com/hk/en/job/data-analyst-data-governance-... |

# Key Findings of the Analysis 
can be found inside the [\analysis\data-scientist-job-postings-in-hong-kong-eda.ipynb](https://github.com/aster-fung/hk_job_scraping/blob/master/analysis/data-scientist-job-postings-in-hong-kong-eda.ipynb)

![job position](https://github.com/aster-fung/hk_job_scraping/blob/master/analysis/data_viz/job_titles.png)

![Career level, yoe and education](https://github.com/aster-fung/hk_job_scraping/blob/master/analysis/data_viz/additional_info_breakdown.png)

![map](https://github.com/aster-fung/hk_job_scraping/blob/master/analysis/data_viz/map.png)





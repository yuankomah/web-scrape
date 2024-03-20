
from bs4 import BeautifulSoup
from helium import *
from selenium.common.exceptions import TimeoutException

def scrape(job_name, min_s, max_s, filter_employment):

    data = []
    web_urls = job_name.split()

    web = 'https://www.mycareersfuture.gov.sg/search?search='

    for index, word in enumerate(web_urls):
        if index == 0:
            web += word
        else: 
            web = web + '%20' + word

    web += '&sortBy=relevancy&page='

    for i in range(10000):
        url = web + str(i)

        # Start a headless Chrome browser
        browser = start_chrome(url, headless=True)

        try:
            wait_until(Text(job_name).exists, timeout_secs=10)
        except TimeoutException:
            browser.quit()  
            break 

        page_source = browser.page_source
        browser.quit()

        soup = BeautifulSoup(page_source, 'html.parser')

        for j in range(100):
            job = soup.find_all('div', {'id': f'job-card-{j}'})

            if job == []:
                break
            for item in job:
                company = item.find('p', {'data-testid': 'company-hire-info'}).text
                company = company.replace('"','').replace("|","/")

                job = item.find('span', {'data-testid': 'job-card__job-title'}).text
                job = job.replace('"','').replace("|","/")

                employment = item.find('p', {'data-cy': 'job-card__employment-type'}).text
                employment = employment.replace('"','').replace("|","/")

                salary = item.find('span', {'data-cy': 'salary-range'}).text
                min_salary, max_salary = salary.replace('to', ' ').replace('$','').replace(',','').split(' ')
                salary = salary.replace('to', ' to ')

                link = item.find('a')['href']

                # Filter salary
                if int(min_salary) < min_s or int(max_salary) > max_s:
                    continue

                if filter(filter_employment, employment) == False:
                    continue

                data.append({
                    'Company': f'{company}',
                    'Job':  f'{job}',
                    'Employment': f'{employment}',
                    'Salary': f'{salary}',
                    'Link': f'https://www.mycareersfuture.gov.sg{link}'
                })

    return data

def filter(filter_employment, employment):
    if filter_employment != ['']:
        for i in filter_employment:
            if i.lower() in employment.lower():
                return False
        
    return True

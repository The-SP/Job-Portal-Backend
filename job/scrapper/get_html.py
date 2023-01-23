from bs4 import BeautifulSoup
import requests

# Pass the url of job portal website to extract its html
# Save the html to a file
def get_source_code(url, filename):
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')

    # Write the content to a file
    with open(filename, "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))

HAMRO_DEV_JOBS = 'https://hamrodevjobs.com/'
MERO_JOB = 'https://merojob.com/search/?q=&job_category=111&page='

get_source_code(HAMRO_DEV_JOBS, 'scrapper/html_source/hamrodevjobs.html')
for page in range(1, 5):
    get_source_code(MERO_JOB+str(page), f'scrapper/html_source/merojob{page}.html')

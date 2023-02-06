from bs4 import BeautifulSoup
from dict_to_csv import dict_to_csv

# Read the HTML content from the file
with open("scrapper/html_source/hamrodevjobs.html", "r") as file:
    html = file.read()

# Parse the HTML content
soup = BeautifulSoup(html, 'lxml')

# Find all listed jobs
# Find all div elements with attribute _ngcontent-sc175 and class card-body py-2
divs = soup.find_all("a", {"_ngcontent-serverapp-c101":"", "class":"text-decoration-none"}, limit=20)

# Print the number of divs found
# print(f'Number of divs found: {len(divs)}')

# Create an empty list to store the dictionaries
job_list = []

# Iterate through each div
for div in divs:
    # Extract the information
    logo_url = div.find('img', class_="company-logo mr-lg-3").get('src')
    url = div.get('href')
    title = div.find("div", class_="job-title").get_text(strip=True)
    company = div.find("span", class_="mr-md-4 mr-2").get_text(strip=True)
    location = div.find("span", class_="d-none d-lg-inline-block").get_text(strip=True)
    tags = []
    for tag in div.find_all("span", class_="badge default mr-2 badge-primary badge-custom badge-pill mb-2 ng-star-inserted"):
        tags.append(tag.get_text(strip=True))
    salary_div = div.find("div", class_="job-salary-mobile")
    if salary_div:
        salary = salary_div.get_text(strip=True)
    else:
        salary = ''
        
    # Create a dictionary for each div
    job = {
        "logo_url": logo_url.strip(),
        "url": "https://hamrodevjobs.com"+url.strip(),
        "title": title,
        "company": company,
        "location": location,
        "tags": tags,
        "salary": salary.replace(',', ''),
        "deadline": ""
    }

    # Append the dictionary to the list
    job_list.append(job)

# Save the job_list to a csv file
dict_to_csv(job_list, 'scrapper/jobs_csv/jobs1.csv')
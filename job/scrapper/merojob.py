from bs4 import BeautifulSoup
from dict_to_csv import dict_to_csv


def get_jobs(html_filename):
    # Read the HTML content from the file
    with open("scrapper/html_source/" + html_filename, "r") as file:
        html = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html, "lxml")

    # Find all listed jobs
    # Find all div elements with class="row job-card text-center text-lg-left ml-2"
    divs = soup.find_all(
        "div", class_="row job-card text-center text-lg-left ml-2", limit=20
    )
    deadline_divs = soup.find_all("p", class_="text-primary mb-0")

    # Iterate through each div
    for index, div in enumerate(divs):
        # Extract the information
        logo_url = div.find("img").get("src")
        heading_div = div.find(
            "h1", class_="text-primary font-weight-bold media-heading h4"
        ).find("a")
        url = heading_div.get("href")
        title = heading_div.get("title")
        company = div.find("h3", class_="h6").get_text()
        location = div.find("span", {"itemprop": "addressLocality"}).get_text()
        deadline = (
            deadline_divs[index]
            .find("span", string=lambda text: "from now" in text)
            .text
        )

        tags = []
        for tag in div.find_all(
            "span", class_="badge badge-pill badge-light rounded text-muted"
        ):
            tags.append(tag.get_text().strip())

        # Create a dictionary for each div
        job = {
            "logo_url": "https://merojob.com" + logo_url.strip(),
            "url": "https://merojob.com" + url.strip(),
            "title": title.strip(),
            "company": company.strip(),
            "location": location.strip(),
            "tags": tags,
            "salary": "",
            "deadline": deadline.strip()[14:-9],
        }

        # Append the dictionary to the list
        job_list.append(job)


# Create an empty list to store the dictionaries
job_list = []
for page in range(1, 5):
    get_jobs(f"merojob{page}.html")

# Save the job_list to a csv file
dict_to_csv(job_list, 'scrapper/jobs_csv/jobs.csv')
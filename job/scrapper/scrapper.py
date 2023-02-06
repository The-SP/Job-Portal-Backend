import subprocess, sys

# Run all scraping related python files and generate csv with jobs list
def run_files():
    print("Scraping the html source...\n")
    subprocess.run([sys.executable, 'scrapper/get_html.py'])
    # sys.executable to get the path of the current running python script executable, this way, you don't have to hardcode the path.

    print("Extracting hamrodevjobs...")
    print("CSV Generated Successfully\n")
    subprocess.run([sys.executable, 'scrapper/hamrodevjobs.py'])

    print("Extracting merojob...")
    print("CSV Generated Successfully\n")
    subprocess.run([sys.executable, 'scrapper/merojob.py'])
    print("Scraping complete.")

if __name__ == "__main__":
    run_files() 
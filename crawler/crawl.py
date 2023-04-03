import os
import shutil

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Set the URL of the website you want to crawl
url = 'https://www.opzelura.com/'

# Set the headers to send with the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


# Make a request to the website and get its HTML content
response = requests.get(url, headers=headers)

# Check that the response is successful
if response.status_code != 200:
    print('Failed to retrieve content from', url)
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the links on the website
links = soup.find_all('a')

# Create a directory to store the page files
if os.path.exists('pages'):
    shutil.rmtree('pages')

   # Create fresh
    os.mkdir('pages')

# Loop through the links and crawl each page
for link in links:
    href = link.get('href')
    if href:
        # Join the href with the base URL to get the complete URL
        href = urljoin(url, href)

        # Make sure the href is from the same domain as the base URL
        if urlparse(href).netloc != urlparse(url).netloc:
            continue

        # Make a request to the page and get its HTML content
        response = requests.get(href, headers=headers)

        # Check that the response is successful
        if response.status_code != 200:
            print('Failed to retrieve content from', href)
            continue

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title and body of the page
        title_tag = soup.find('title')
        if not title_tag:
            print('Failed to find title tag on', href)
            continue
        title = title_tag.string
        body = soup.get_text()

        # Create a filename for the page based on its title
        filename = os.path.join('pages', title + '.txt')

        # Write the title and body to a file in the pages directory
        try:
            with open(filename, 'w') as f:
                f.write(title + '\n\n')
                f.write(body)
        except Exception as e:
            print('Failed to write file:', filename, e)
            continue
        print('Wrote file:', filename)

import re
import os
import requests
from bs4 import BeautifulSoup

# make directory "Math Problems" if it doesn't exist
directory = 'Math Problems'
parent_dir = os.getcwd()
path = os.path.join(parent_dir, directory)
if not os.path.exists(path):
    os.mkdir(path)

# connect to URL to scrape
url_to_scrape = 'https://cms.math.ca/competitions/cmo/'
response = requests.get(url_to_scrape)

# get the list of a tags containing pdf links
soup = BeautifulSoup(response.content, 'html5lib')
pdf_tags = soup.findAll('a', attrs={'href': re.compile(r'(.pdf)')})

# extract pdf links
base_url = 'https://cms.math.ca/'
pdf_links = []
for el in pdf_tags:
    if (el['href'].startswith('http')):
        pdf_links.append(el['href'])
    else:
        pdf_links.append((base_url + el['href']))

# Download files in the directory "Math Problems"
i = 0
print('Downloading...')
for link in pdf_links:
    filename = os.path.join(path, link.split('/')[-1])
    if not os.path.exists(filename):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                i += 1
                pdf = open(filename + ".pdf", 'wb')
                pdf.write(response.content)
                pdf.close()
                print(f'Downloaded {filename}')
        except:
            print(f'Something went wrong. Skipped downloading: {link}')

print(f'{i} files downloaded')
print(f'Skipped {len(pdf_links) - i} files')

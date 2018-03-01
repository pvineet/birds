import requests
import csv
from bs4 import BeautifulSoup

base_url = "http://orientalbirdimages.org"
bird_images_url = "http://orientalbirdimages.org/birdimages.php"
groups = []

def parse_images_page(response):
    page_content = BeautifulSoup(response.content, 'html.parser')
    with open('groups.csv', 'w') as csvfile:
        fieldnames = ['group_name', 'href']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link in page_content.find_all('a'):
            #print link.__dict__
            try:
                if(link.get('class')[0] == 'mlink'):
                    href = link.get('href')
                    writer.writerow({'group_name': link.next_element, 'href': base_url+href})
            except TypeError:
                print("Not the correct link")
    return 0

response = requests.get(bird_images_url)
#print type(response.status_code)
if(response.status_code == 200):
    print("Page available")
else:
    print("Error in reaching bird images page")

parse_images_page(response)


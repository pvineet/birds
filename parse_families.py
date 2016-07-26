import requests
import csv
from bs4 import BeautifulSoup

base_url = "http://orientalbirdimages.org"
read_file = "groups.csv"

def get_num_photos(string):
    name = string.split(' ')[0]
    num_photos = string.split(' ')[1].strip('(').strip(')')
    return name, num_photos
def write_family_csv(group_name, content):
    file_name = group_name.lower()+".csv"
    print file_name
    with open(file_name, 'wb') as csvfile:
        fieldnames = ['family_name', 'href', 'num_photos']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link in content:
            #print link.__dict__
            try:
                if(link.get('class')[0] == 'mlink'):
                    href = link.get('href')
                    name, num_photos = get_num_photos(link.next_element)
                    writer.writerow({'family_name': name, 'href': base_url+href, 'num_photos': num_photos})
            except TypeError:
                print "Not the correct link"

def get_family(row):
    response =  requests.get(row['href'])
    if(response.status_code == 200):
        print "Page available"
    else:
        print "Error in %s page" %row['group_name']
    page_content = BeautifulSoup(response.content, 'html.parser')
    write_family_csv(row['group_name'], page_content.find_all('a'))

with open(read_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        get_family(row)


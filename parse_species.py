import os
import csv
from bs4 import BeautifulSoup
import requests

current_dir = os.getcwd()
base_path = current_dir+"/image_db"
groups_csv = base_path+"/groups.csv"

def get_family_page(row):
    response =  requests.get(row['href'])
    if(response.status_code == 200):
    	page_content = BeautifulSoup(response.content, 'html.parser')
    	#write_group_csv(row['family_name'], page_content.find_all('a'))
        return "Page parsed"
    else:
        return "Error in %s page" %row['group_name']


def get_specie(group):
    os.chdir(base_path+"/"+group)
    print "In dir %s" % group
    file_name = group+".csv"
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
	for row in reader:
	    print row['family_name']
     	    print get_family_page(row)

with open(groups_csv) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
	get_specie(row['group_name'].lower())

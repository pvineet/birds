import urllib
import os
import csv
from bs4 import BeautifulSoup,UnicodeDammit
import requests

base_url = "http://orientalbirdimages.org"
current_dir = os.getcwd()
base_path = current_dir+"/image_db"
groups_csv = base_path+"/groups.csv"
dir_mode = 0775

def get_image_url(url):
    response = requests.get(url)
    if(response.status_code == 200):
	images = BeautifulSoup(response.content, 'html.parser').find_all('img')
	for image in images:
	    if(image.get('galleryimg') == 'no'):
		return image.get('src')
    else:
        return "Broken link %s" % url

def get_specie_page(specie):
    response = requests.get(specie['href'])
    print specie['latin_name']
    if(response.status_code == 200):
    	page_content = BeautifulSoup(response.content, 'html.parser')
        #print os.getcwd()
        file_name = get_specie_dir(specie)+"/"+specie['latin_name'].lower().replace(" ","_")+".csv"
        with open(file_name, 'wb') as csvfile:
            fieldnames = ['page_url', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            count = 0
            for option in page_content.find_all('option'):
                page_url = base_url +"/"+option.parent.get('onchange').split('+')[0].split('(')[1].strip("'")+option.get('value')
                if "Bird_Group_ID" not in page_url:
                    #print get_image_url(page_url)
                    urllib.urlretrieve(get_image_url(page_url), get_specie_dir(specie)+"/"+str(count)+".jpg")
                    count = count+1
                    writer.writerow({'page_url':page_url, 'image_url':get_image_url(page_url)})
        csvfile.close()
	return "Page parsed"
    else:
        return "Error in %s page" % specie['latin_name']
    

def get_specie_dir(specie_row):
    return os.getcwd()+"/"+specie_row['latin_name'].lower().replace(" ","_")

def write_image_csv(specie):
#we need specie name, page href, 
#We dump image_id, image path,
    current_path = os.getcwd()
    get_specie_page(specie)

def get_bird_id(href):
    return href.split('&')[1].split('=')[1]

def write_family_csv(file_name, content):
    with open(file_name, 'wb') as csvfile:
        fieldnames = ['bird_id', 'common_name', 'href', 'latin_name', 'num_photos']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	specie_row = {}
	count = 0
	for link in content:
            try:
                if(link.get('class')[0] == 'mlink'):
                    specie_row['href'] = base_url+link.get('href')
            	    #print link.__dict__
		    if(count%2 == 0):
                    	count = count+1
		    	specie_row['bird_id'] = get_bird_id(link.get('href'))
			specie_row['common_name'] = link.next_element
			specie_row['num_photos'] = link.next_sibling.strip('(').strip(')')
			continue
		    #odd count
		    else:
                    	count = count+1
			specie_row['latin_name'] = link.next_element
    			specie_dir = get_specie_dir(specie_row)
			#print specie_dir
		    	#mkdir for the specie with Latin name
			try:
			    #print count
                    	    os.mkdir(specie_dir, dir_mode)
			except OSError:
			    print "Directory already exists %s" % specie_dir
			#write row in csv
			#writer.writerow(specie_row)
			try:
			    writer.writerow(specie_row)
			except UnicodeEncodeError:
			    print "Skipping %s" % specie_row['latin_name']
		    #make the specie's image csv
		    write_image_csv(specie_row)	
            except TypeError:
                print "Not the correct link"
    csvfile.close()
 
def cd_family_dir(family_name, content):
    print family_name
    group_dir = os.getcwd()
    family_dir = group_dir+"/"+family_name
    # cd family dir
    os.chdir(family_dir)
    #file_name = family_dir+"/"+family_name+".csv"
    file_name = family_name+".csv"
    write_family_csv(file_name, content, )
    #return to group dir
    os.chdir(group_dir)
    

def get_family_page(row):
    response =  requests.get(row['href'])
    if(response.status_code == 200):
	content = UnicodeDammit(response.content, ["windows-1252"], smart_quotes_to="ascii").unicode_markup
    	page_content = BeautifulSoup(content, 'html.parser')
    	cd_family_dir(row['family_name'].lower(), page_content.find_all('a'))
        return "Page parsed"
    else:
        return "Error in %s page" %row['family_name']


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
csvfile.close()

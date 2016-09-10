import os
import requests
import flickrapi
import urllib

api_key = u'124e63e738f445e410f8b348f0a991e0'
api_secret = u'81159f26a126d791'
id_list = []

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')



#check for species list
species_list = []
f = open("species_list.txt", 'rb')
for specie in f.readlines():
    species_list.append(specie.lower().strip())
f.close()
#mkdir flick_db
os.chdir('flickr_db')

for specie_name in species_list:
    #Call flickr api
    response = flickr.photos.search(tags=specie_name, per_page='500')
    for photo in response['photos']['photo']:
        id_list.append(photo['id'])

    #add check for dir condition
    dir_name = specie_name.replace(" ","_")
    os.mkdir(dir_name)
    os.chdir(dir_name)
    current_path = os.getcwd()
    i=0
    for photo_id in id_list:
    	response = flickr.photos.getSizes(photo_id=photo_id)
    	for size in response['sizes']['size']:
    	    if size['label'] == 'Medium 640':
	     	image_url = size['source']
	    	image_file = current_path+"/flickr_"+dir_name+"_"+str(i)+".jpg"		
	    	urllib.urlretrieve(image_url,image_file)
	    	i=i+1
    os.chdir("../")

import os
import requests
import flickrapi

api_key = u'124e63e738f445e410f8b348f0a991e0'
api_secret = u'81159f26a126d791'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
photos = flickr.photos.search(user_id='73509078@N00', per_page='10')


#mkdir flick_db
#check for species list
species_list = []
f = open("species_list.txt", 'rb')
for specie in f.readlines():
    species_list.append(specie.lower().strip())

#print species_list

#Call flickr api
print photos

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import onedrivesdk
import requests
from onedrivesdk.helpers import GetAuthCodeServer

driver = webdriver.PhantomJS()
redirect_uri = 'http://localhost:8080/'
client_secret = 'BFNTFFXLfd6niqq8HVbZO8s'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

client = onedrivesdk.get_default_client(
    client_id='a4bb6731-f8a5-4137-9322-236390c49d7f', scopes=scopes)

auth_url = client.auth_provider.get_auth_url(redirect_uri)
driver.get(auth_url)
print auth_url
#this will block until we have the code
#code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
#print code
#client.auth_provider.authenticate(code, redirect_uri, client_secret)

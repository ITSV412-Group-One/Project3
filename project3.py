import requests 
import datetime 

# Download log file
url = 'https://s3.amazonaws.com/tcmg476/http_access_log'
response = requests.get(url)


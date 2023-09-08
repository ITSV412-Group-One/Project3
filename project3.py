import requests 
import datetime 

# Download log file
url = 'https://s3.amazonaws.com/tcmg476/http_access_log'
response = requests.get(url)

with open('logs.txt', 'w') as f:
  f.write(response.text)

# Parse logs
total_requests = 0
monthly_requests = {}


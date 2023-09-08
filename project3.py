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

with open('logs.txt') as f:
  for line in f:
    parts = line.split()
    if len(parts) >= 4:
        date_str = parts[3].strip('[')  # Remove the leading '['
        try:
            date = datetime.datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S')
            total_requests += 1

            month = date.month
            if month in monthly_requests:
                monthly_requests[month] += 1
            else:
                monthly_requests[month] = 1
        except ValueError:
            pass  # Ignore lines with incorrect date format
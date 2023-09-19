import requests 
import datetime

# Download log file
url = 'https://s3.amazonaws.com/tcmg476/http_access_log'
response = requests.get(url)

with open('logs.txt', 'w') as f:
  f.write(response.text)

# Variables
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
        
# Calculate the total requests for the first six months
total_first_six_months = sum(monthly_requests.get(month, 0) for month in range (1, 7))
# Print results 
print('Analytics Report')
print('-'*15)     

print()
print('Monthly Breakdown:')
for month, count in monthly_requests.items():
  print(f'- {datetime.date(1900, month, 1).strftime("%B")}: {count}')
  
print()
print('Total numbers of first six months: ', total_first_six_months)
print()
print(f'Total requests: {total_requests}')


# Calculates the percentage of requests that were not successful // Maya 
failed_requests = 0 

with open('logs.txt') as f:
  for line in f:
    parts = line.split()
    if len(parts) >= 9:
      status_code = parts[8]
      if status_code.startswith('4'):
        failed_requests += 1
        
percentage_failed = failed_requests / total_requests * 100

# Outputs percentage of requests that were not successful  
print()
print(f'Percentage of requests that failed: {percentage_failed:.2f}%')

# ///////////////////////////////////////////////////////////////////

# Handles week requests and least request file // Danny

# /////////////////////////////////////////////////////


# Handles day-level requests and most requested file // Mel

# /////////////////////////////////////////////////////


# Calculates the percentage of requests redirected somewhere else // Andres 

# Variables 
totalResponses = 0 
redirectedResponses = 0

with open('logs.txt', "r") as file:
   for line in file:
      sections = line.split() # Will just split everything at an empty space " "
      if len(sections) >= 2: # This checks if there are more than two sections in the line since the shortest lines were just "local     index.html"
         try:
            statusCode = int(sections[-2]) # Goes to the second to the last "section" since that is where the status code is located
            totalResponses += 1
            if 300 <= statusCode < 400:
               redirectedResponses += 1
         except:
            pass
         
print("Percentage of Redirected Repsonses: " + str(round((redirectedResponses/totalResponses)* 100, 2)) + "%")

# /////////////////////////////////////////////////////
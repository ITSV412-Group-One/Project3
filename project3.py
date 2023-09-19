import collections
from distutils import text_file
import re
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
weekly_requests = {}  
file_requests = {}  

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
            # Calculate the week number and update weekly_requests
            week_number = date.strftime('%U-%Y')
            if week_number in weekly_requests:
                weekly_requests[week_number] += 1
            else:
                weekly_requests[week_number] = 1
                  
        except ValueError:
            pass  # Ignore lines with incorrect date format
        
# Calculate the total requests for the first six months
total_first_six_months = sum(monthly_requests.get(month, 0) for month in range (1, 7))
# Find the least-requested file
least_requested_file = min(file_requests, key=file_requests.get)
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
#Added Weekly Breakdown 
print()
print('Weekly Breakdown:')
for week, count in weekly_requests.items():
    print(f'- Week {week}: {count}')
#Added Least Requested File and the number of requests
print()
print(f'Least Requested File: {least_requested_file}')
print(f'Request Count: {file_requests[least_requested_file]}')


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
# Question 1 : request for each day

with open('logs.txt') as f:
    first_line = text_file.readlines()[1]
    first_datetime = first_line.split()[3]
    clean_datetime = datetime.strptime(first_datetime, '[%d/%b/%Y:%H:%M:%S')
    first_date = clean_datetime.date()

# begins process 
file = open("logs.txt", "f")
count = 0
Q1_dates = 0

for line in file:
   count += 1 

   # remove lines without date
   if ("["in line) != True:
      continue 
   # searches for datetime and only extracts date
   date_str = re.search('\d{2}/\D{3}/\d{4}', line)
   clean_datetime = datetime.strptime(date_str.group(), '%d/%b/%Y')
   line_date = clean_datetime.date()

delta = datetime.timedelta(days=1)

if line_date == first_date:
      Q1_dates +=1
else :
   print("There were", Q1_dates, "request on", first_date)
   Q1_dates = 0 
   first_date += delta

file.close()
# doesn't print last date request

# Question 5: the most requested file 

file = open("logs.txt", "f" )

clean_log = []

for line in file: 
  try:
      clean_log.append(line[line.index("GET")+4:line.index("HTTP")])
  except:
      pass
  
counter = collections.Counter(clean_log)

for count in counter.most_common(1):
   print("The most requested file was", str(count[0])) + "and was requested", str(count[1], "times")
   file.close()
 
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

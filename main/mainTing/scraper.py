import mechanicalsoup
import requests
from bs4 import BeautifulSoup
import re

# Assuming `html_content` is the HTML extracted from the PDF
# This should be the actual HTML content you're parsing
url = "https://schema.mau.se/setup/jsp/Schema.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sprak=SV&sokMedAND=true&forklaringar=true&resurser=k.DA336A-20241-TS153-"
response = requests.get(url)
# Initialize BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the main table containing the schedule. Adjust the class name if necessary.
schedule_table = soup.find('table', class_='schemaTabell')

events = []
current_week = None

# Iterate over each row in the table
for row in schedule_table.find_all('tr'):
    # Check if this row represents a week header
    week_marker = row.find('td', class_='vecka')
    if week_marker:
        current_week = week_marker.get_text(strip=True)
        continue  # Skip to the next iteration

    # If it's an event row, extract the event details
    day_cell = row.find('td', class_='commonCell')
    if day_cell:
        day = day_cell.get_text(strip=True)
        date = day_cell.find_next_sibling('td', class_='commonCell').get_text(strip=True)
        time = day_cell.find_next_sibling('td', class_='commonCell').find_next_sibling('td', class_='commonCell').get_text(strip=True)
        description_cells = row.find_all('td', class_='commonCell')
        if description_cells:
            # The description might be in the last `td`. Adjust the index if needed.
            description = description_cells[-1].get_text(strip=True).replace('\n', ' ').replace('\r', '')
            # Clean up the description, remove unnecessary spaces around commas, etc.
            description = re.sub(r'\s*,\s*', ', ', description)
            events.append({
                'week': current_week,
                'day': day,
                'date': date,
                'time': time,
                'description': description
            })
for event in events:
    if event['day'] != '':
        dag = event['day']
    if event['day'] == '':
        event['day'] = dag
    if event['date'] != '':
        date = event['date']
    if event['date'] == '':
        event['date'] = date

# Example to print out the extracted events
for event in events:
    print(f"Week: {event['week']}, Day: {event['day']}, Date: {event['date']}, Time: {event['time']}, Description: {event['description']}")

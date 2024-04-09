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

# Initialize events as a dictionary
events = {}

# Iterate over each row in the table
for row in schedule_table.find_all('tr'):
    # Check if this row represents a week header
    week_marker = row.find('td', class_='vecka')
    if week_marker:
        current_week = week_marker.get_text(strip=True)
        # Initialize the list for the current week in the events dictionary
        events[current_week] = []
        continue  # Skip to the next iteration

    # If it's an event row, extract the event details
    cells = row.find_all('td', class_='commonCell')
    # Check if it's an event row based on the expected number of cells
    if len(cells) >= 4:  # Assuming there are at least 4 cells when it's an event row
        day = cells[0].get_text(strip=True)
        date = cells[1].get_text(strip=True)
        time = cells[2].get_text(strip=True)
        description = cells[8].get_text(strip=True).replace('\n', ' ').replace('\r', '')
        description = re.sub(r'\s*,\s*', ', ', description)
        # Append the event to the list of the current week in the events dictionary
        events[current_week].append({
            'day': day,
            'date': date,
            'time': time,
            'description': description
        })
for week_events in events.values():
    for event in week_events:
        if event['day'] != '':
            dag = event['day']
        if event['day'] == '':
            event['day'] = dag
        if event['date'] != '':
            date = event['date']
        if event['date'] == '':
            event['date'] = date

# Example to print out the extracted events
for week, week_events in events.items():
    for event in week_events:
        print(f"Week: {week}, Day: {event['day']}, Date: {event['date']}, Time: {event['time']}, Description: {event['description']}")


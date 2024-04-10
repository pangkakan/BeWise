import mechanicalsoup
import requests
from bs4 import BeautifulSoup
import re

def scraper(search_term, course_or_no):
    """
    Main function that controls the scraping process.

    Args:
        search_term (str): The term to search for in the course database.
        course_or_no (bool): A flag to determine the type of description to scrape.

    Returns:
        dict: A dictionary containing the scraped schedule data, or None if an error occurs.
    """
    try:
        contentPage = getCourse(search_term)
        if contentPage is None:
            return None

        good_link = findLink(contentPage)
        if good_link is None:
            return None

        events = get_schedule(good_link, course_or_no)
        return events
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def getCourse(search_term):
    """
    Fetches the course page for the given search term.

    Args:
        search_term (str): The term to search for in the course database.

    Returns:
        str: The HTML content of the course page, or None if the fetch fails or an error occurs.
    """
    try:
        url = f"https://schema.mau.se/ajax/ajax_sokResurser.jsp?sokord={search_term}&startDatum=idag&slutDatum=&intervallTyp=m&intervallAntal=6"

        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred in getCourse: {e}")
        return None

def findLink(content_page):
    """
    Finds the first link in the content page with a text length greater than 20.

    Args:
        content_page (str): The HTML content of the page.

    Returns:
        str: The href of the found link, or None if no suitable link is found or an error occurs.
    """
    try:
        soup = BeautifulSoup(content_page, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            text = link.text.strip()
            if text.__len__() > 20:
                print(f"Found link: {href}")
                return href
        return None
    except Exception as e:
        print(f"An error occurred in findLink: {e}")
        return None




def get_schedule(url, course_or_no):
    """
    Scrapes the schedule from the given URL.

    Args:
        url (str): The URL of the page to scrape.
        course_or_no (bool): A flag to determine the type of description to scrape.

    Returns:
        dict: A dictionary containing the scraped schedule data, or None if no schedule table is found or an error occurs.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        schedule_table = soup.find('table', class_='schemaTabell')
        if schedule_table is None:
            print("No schedule table found")
            return None

        events = {}
        for row in schedule_table.find_all('tr'):
            week_marker = row.find('td', class_='vecka')
            if week_marker:
                current_week = week_marker.get_text(strip=True)
                events[current_week] = []
                continue

            cells = row.find_all('td', class_='commonCell')
            if len(cells) >= 4:
                day = cells[0].get_text(strip=True)
                date = cells[1].get_text(strip=True)
                time = cells[2].get_text(strip=True)
                if course_or_no:
                    description = cells[8].get_text(strip=True).replace('\n', ' ').replace('\r', '')
                else:
                    description = cells[7].get_text(strip=True).replace('\n', ' ').replace('\r', '')

                description = re.sub(r'\s*,\s*', ', ', description)
                events[current_week].append({
                    'day': day,
                    'date': date,
                    'time': time,
                    'description': description
                })
        # Fill in missing day and date values if event is not the first in a day
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
        # Print the schedule
        for week, week_events in events.items():
            for event in week_events:
                print(
                    f"Week: {week}, Day: {event['day']}, Date: {event['date']}, Time: {event['time']}, Description: {event['description']}")

        return events
    except Exception as e:
        print(f"An error occurred in get_schedule: {e}")
        return None


scraper("mv244e", True)
print("\n")
print("\n")
print("\n")


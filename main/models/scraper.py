import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class Scraper:
    """
    A class used to scrape course schedule data from a website.

    ...

    Attributes
    ----------
    search_term : str
        a string representing the term to search for in the course database
    course_or_no : bool
        a flag to determine the type of description to scrape

    Methods
    -------
    scrape():
        Controls the scraping process.
    getCourse(search_term):
        Fetches the course page for the given search term.
    findLink(content_page):
        Finds the first link in the content page with a text length greater than 20.
    get_schedule(url, course_or_no):
        Scrapes the schedule from the given URL.
    """

    def __init__(self, search_term, course_or_no):
        """
        Constructs all the necessary attributes for the Scraper object.

        Parameters
        ----------
            search_term : str
                The term to search for in the course database.
            course_or_no : bool
                A flag to determine the type of description to scrape.
        """
        self.search_term = search_term
        self.course_or_no = course_or_no

    def scrape(self):
        """
        Main function that controls the scraping process.

        Returns
        -------
        dict
            A dictionary containing the scraped schedule data, or None if an error occurs.
        """
        try:
            contentPage = self.getCourse(self.search_term)
            if contentPage is None:
                return None

            good_link = self.findLink(contentPage)
            if good_link is None:
                return None

            events = self.get_schedule(good_link, self.course_or_no)
            return events
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def getCourse(self, search_term):
        """
        Fetches the course page for the given search term.

        Parameters
        ----------
        search_term : str
            The term to search for in the course database.

        Returns
        -------
        str
            The HTML content of the course page, or None if the fetch fails or an error occurs.
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

    def findLink(self, content_page):
        """
        Finds the first link in the content page with a text length greater than 20.

        Parameters
        ----------
        content_page : str
            The HTML content of the page.

        Returns
        -------
        str
            The href of the found link, or None if no suitable link is found or an error occurs.
        """
        try:
            soup = BeautifulSoup(content_page, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                text = link.text.strip()
                if text.__len__() > 20:
                    print(f"Found link: {href}")
                    return href
            return None
        except Exception as e:
            print(f"An error occurred in findLink: {e}")
            return None

    def get_schedule(self, url, course_or_no):
        """
        Scrapes the schedule from the given URL.

        Parameters
        ----------
        url : str
            The URL of the page to scrape.
        course_or_no : bool
            A flag to determine the type of description to scrape.

        Returns
        -------
        dict
            A dictionary containing the scraped schedule data, or None if no schedule table is found or an error occurs.
        """
        month_map = {
            "Jan": "January",
            "Feb": "February",
            "Mar": "March",
            "Apr": "April",
            "Maj": "May",
            "Jun": "June",
            "Jul": "July",
            "Aug": "August",
            "Sep": "September",
            "Okt": "October",
            "Nov": "November",
            "Dec": "December",
        }
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            schedule_table = soup.find("table", class_="schemaTabell")
            if schedule_table is None:
                print("No schedule table found")
                return None

            events = {}
            for row in schedule_table.find_all("tr"):
                week_marker = row.find("td", class_="vecka")
                if week_marker:
                    current_week = week_marker.get_text(strip=True)
                    events[current_week] = []
                    continue

                cells = row.find_all("td", class_="commonCell")
                if len(cells) >= 4:
                    day = cells[0].get_text(strip=True)
                    scraped_date = cells[1].get_text(strip=True)
                    if scraped_date != "":
                        # Replace the month name in the scraped date with the English month name
                        for non_english_month, english_month in month_map.items():
                            scraped_date = scraped_date.replace(
                                non_english_month, english_month
                            )
                        # Add the current year to the scraped date
                        current_year = datetime.now().year
                        scraped_date = f"{scraped_date} {current_year}"
                        # Parse the date string to a date object
                        date = datetime.strptime(scraped_date, "%d %B %Y").date()
                    time = cells[2].get_text(strip=True)
                    starting_time, ending_time = time.split("-")
                    start_time = datetime.strptime(starting_time, "%H:%M").time()
                    end_time = datetime.strptime(ending_time, "%H:%M").time()
                    if course_or_no:
                        description = (
                            cells[8]
                            .get_text(strip=True)
                            .replace("\n", " ")
                            .replace("\r", "")
                        )
                        location = cells[6].get_text(strip=True)
                    else:
                        description = (
                            cells[7]
                            .get_text(strip=True)
                            .replace("\n", " ")
                            .replace("\r", "")
                        )
                        location = cells[5].get_text(strip=True)

                    description = re.sub(r"\s*,\s*", ", ", description)
                    events[current_week].append(
                        {
                            "day": day,
                            "date": date,
                            "start_time": start_time,
                            "end_time": end_time,
                            "location": location,
                            "description": description,
                        }
                    )
            # Fill in missing day and date values if event is not the first in a day
            for week_events in events.values():
                for event in week_events:
                    if event["day"] != "":
                        dag = event["day"]
                    if event["day"] == "":
                        event["day"] = dag
                    if event["date"] != "":
                        date = event["date"]
                    if event["date"] == "":
                        event["date"] = date
            # Print the schedule
            for week, week_events in events.items():
                for event in week_events:
                    print(
                        f"Week: {week}, Day: {event['day']}, Date: {event['date']}, From: {event['start_time']}, To: {event['end_time']}, Locale: {event['location']} Description: {event['description']}"
                    )

            return events
        except Exception as e:
            print(f"An error occurred in get_schedule: {e}")
            return None


print("\n")
print("\n")
print("\n")

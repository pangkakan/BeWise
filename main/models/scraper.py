import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, search_term, course_or_no):
        self.search_term = search_term
        self.course_or_no = course_or_no
        self.month_map = {
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
        self.keywords = ["lecture", "workshop", "lab", "other", "tentamen"]

    def extract_course_name(self):
        try:
            content_page = self.get_course(self.search_term)
            if not content_page:
                print("No content page found.")
                return None

            good_link = self.find_link(content_page)
            if not good_link:
                print("No good link found.")
                return None

            response = requests.get(good_link)
            soup = BeautifulSoup(response.text, "html.parser")
            row = soup.find("tr")
            if not row:
                print("No table row found.")
                return None

            data_cells = row.find_all("td", class_="data")
            if not data_cells or len(data_cells) < 2:
                print(f"Not enough data cells found: {data_cells}")
                return None

            course_info = data_cells[1].get_text(strip=True)
            if "," in course_info:
                course_name = course_info.split(",")[1].strip()
            else:
                print(f"Unexpected course info format: {course_info}")
                return None

            print(f"Course name: {course_name}")
            return course_name
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def scrape(self):
        try:
            content_page = self.get_course(self.search_term)
            if not content_page:
                return None

            good_link = self.find_link(content_page)
            if not good_link:
                return None

            events = self.get_schedule(good_link, self.course_or_no)
            return events
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_course(self, search_term):
        try:
            url = f"https://schema.mau.se/ajax/ajax_sokResurser.jsp?sokord={search_term}&startDatum=2024-02-15&slutDatum=&intervallTyp=m&intervallAntal=6"
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch data: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred in get_course: {e}")
            return None

    def find_link(self, content_page):
        try:
            soup = BeautifulSoup(content_page, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                text = link.text.strip()
                if len(text) > 20 and "-20241-" in text:
                    #print(f"Found link: {href}")
                    return href
            return None
        except Exception as e:
            print(f"An error occurred in find_link: {e}")
            return None

    def get_schedule(self, url, course_or_no):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            schedule_table = soup.find("table", class_="schemaTabell")
            if not schedule_table:
                print("No schedule table found")
                return None

            events = {}
            for row in schedule_table.find_all("tr"):
                if self.is_week_marker(row):
                    current_week = self.get_week_marker(row)
                    events[current_week] = []
                    continue

                event_data = self.parse_event_data(row, course_or_no)
                if event_data:
                    week = self.find_week_for_event(events, row)
                    events[week].append(event_data)
            self.fill_missing_event_details(events)
            return events
        except Exception as e:
            print(f"An error occurred in get_schedule: {e}")
            return None

    def is_week_marker(self, row):
        return row.find("td", class_="vecka") is not None

    def get_week_marker(self, row):
        return row.find("td", class_="vecka").get_text(strip=True)

    def parse_event_data(self, row, course_or_no):
        cells = row.find_all("td", class_="commonCell")
        if len(cells) < 4:
            return None

        date, start_time, end_time, location, description = self.extract_event_details(cells, course_or_no)
        if not date or not start_time or not end_time:
            return None

        event_data = {
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
            "description": description,
            "type": self.categorize_event(description)
        }
        return event_data

    def extract_event_details(self, cells, course_or_no):
        date = self.parse_date(cells[1].get_text(strip=True))
        time = cells[2].get_text(strip=True)
        start_time, end_time = self.parse_time_range(time)
        if course_or_no:
            description = self.clean_text(cells[8].get_text(strip=True))
            location = cells[6].get_text(strip=True)
        else:
            description = self.clean_text(cells[7].get_text(strip=True))
            location = cells[5].get_text(strip=True)
        return date, start_time, end_time, location, description

    def parse_date(self, scraped_date):
        if not scraped_date:
            return None
        for non_english_month, english_month in self.month_map.items():
            scraped_date = scraped_date.replace(non_english_month, english_month)
        current_year = datetime.now().year
        return datetime.strptime(f"{scraped_date} {current_year}", "%d %B %Y").date()

    def parse_time_range(self, time_range):
        try:
            starting_time, ending_time = time_range.split("-")
            start_time = datetime.strptime(starting_time, "%H:%M").time()
            end_time = datetime.strptime(ending_time, "%H:%M").time()
            return start_time, end_time
        except ValueError:
            return None, None

    def clean_text(self, text):
        return re.sub(r"\s*,\s*", ", ", text.replace("\n", " ").replace("\r", ""))

    def categorize_event(self, description):
        for keyword in self.keywords:
            if keyword.lower() in description.lower():
                return keyword
            if re.match(r"F\d+", description):
                return "lecture"
        return "other"

    def find_week_for_event(self, events, row):
        for week in events.keys():
            if row.find_previous("td", class_="vecka").get_text(strip=True) == week:
                return week
        return list(events.keys())[-1]

    def fill_missing_event_details(self, events):
        for week_events in events.values():
            last_date = None
            for event in week_events:
                if event["date"]:
                    last_date = event["date"]
                else:
                    event["date"] = last_date

"""
for week, week_events in events.items():
    for event in week_events:
        print(
            f"Week: {week}, Day: {event['day']}, Date: {event['date']}, From: {event['start_time']}, To: {event['end_time']}, Locale: {event['location']} Description: {event['description']}"
        )
        """

print("\n")
print("\n")
print("\n")

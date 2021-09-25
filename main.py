from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from datetime import datetime
import pickle
import pause
import os

from src.fetch import fetch_conferences
from src.data.credentials import Credentials
from src.page.zoom_meeting_page import ZoomMeetingPage


def load_conference_data(save_file, credentials, time_range):
    if os.path.exists(save_file):
        with open(save_file, 'rb') as fb:
            return pickle.load(fb)

    email, password = credentials.email, credentials.password
    data = fetch_conferences(email, password, *time_range)
    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    
    with open(save_file, 'wb') as fb:
        pickle.dump(data, fb)
    
    return data


def join_conference(conference):
    with Chrome(ChromeDriverManager().install()) as driver:
        driver.get(conference.url)
        meeting_page = ZoomMeetingPage(driver)
        meeting_page.click_join()
        meeting_page.accept_popup()


def main():
    credentials = Credentials.from_file("secret/credentials.json")
    save_file = 'saved/conferences.pkl'
    time_range = ("2021-09-02", "2021-12-31")

    print("Checking schedule...")
        
    conferences = load_conference_data(save_file, credentials, time_range)
    current_date = datetime.now()

    for conference in filter(lambda x: x.start >= current_date, conferences):
        course = conference.course
        start, end = conference.start, conference.end
        meeting_url = conference.url
        print(f"\n{course}: {start!s} - {end!s}\nJoin: {meeting_url}\n")
        
        pause.until(conference.start)
        join_conference(conference)        
       
        
if __name__ == '__main__':
    main()

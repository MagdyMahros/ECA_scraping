"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 18-11-20
    * description:This script extracts the corresponding undergraduate courses details and tabulate it.
"""

import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import os
import copy
from CustomMethods import TemplateData
from CustomMethods import DurationConverter as dura

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/ECA_courses_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/ECA_courses.csv'

course_data = {'Level_Code': '', 'University': 'Eastern College Australia', 'City': '',
               'Country': 'Australia', 'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD',
               'Currency_Time': 'year', 'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
               'Prerequisite_1': '', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': '', 'Prerequisite_1_grade': '',
               'Prerequisite_2_grade': '6.5', 'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '',
               'Availability': '', 'Description': '', 'Career_Outcomes': '', 'Online': '', 'Offline': '',
               'Distance': 'no', 'Face_to_Face': '', 'Blended': '', 'Remarks': ''}

possible_cities = {'online': 'Online', 'albany': 'Western Australia', 'sydney': 'Sydney', 'melbourne': 'Melbourne',
                   'victoria': 'Victoria'}

possible_languages = {'Japanese': 'Japanese', 'French': 'French', 'Italian': 'Italian', 'Korean': 'Korean',
                      'Indonesian': 'Indonesian', 'Chinese': 'Chinese', 'Spanish': 'Spanish'}

course_data_all = []
level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels

# GET EACH COURSE LINK
for each_url in course_links_file:
    actual_cities = []
    remarks_list = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # SAVE COURSE URL
    course_data['Website'] = pure_url

    # COURSE TITLE
    title = soup.find('h1', class_='page-title')
    if title:
        course_data['Course'] = title.get_text()
        print('COURSE TITLE: ', course_data['Course'])

        # DECIDE THE LEVEL CODE
        for i in level_key:
            for j in level_key[i]:
                if j in course_data['Course']:
                    course_data['Level_Code'] = i
        print('COURSE LEVEL CODE: ', course_data['Level_Code'])

        # DECIDE THE FACULTY
        for i in faculty_key:
            for j in faculty_key[i]:
                if j.lower() in course_data['Course'].lower():
                    course_data['Faculty'] = i
        print('COURSE FACULTY: ', course_data['Faculty'])

        # COURSE LANGUAGE
        for language in possible_languages:
            if language in course_data['Course']:
                course_data['Course_Lang'] = language
            else:
                course_data['Course_Lang'] = 'English'
        print('COURSE LANGUAGE: ', course_data['Course_Lang'])

    # DESCRIPTION
    desc_title = soup.find('h3', text=re.compile('Description', re.IGNORECASE))
    if desc_title:
        description = desc_title.find_next_sibling('p')
        if description:
            course_data['Description'] = description.get_text().strip()
            print('DESCRIPTION: ', description.get_text().strip())

    # CITY
    loc_title = soup.find('h3', text=re.compile('Delivery locations', re.IGNORECASE))
    if loc_title:
        temp = []
        loc_ul = loc_title.find_next_sibling('ul')
        if loc_ul:
            loc_list = loc_ul.find_all('li')
            if loc_list:
                for li in loc_list:
                    temp.append(li.get_text().lower().strip())
                temp = ' '.join(temp)
                print('TEMP: ', temp)
                if 'online' in temp:
                    actual_cities.append('online')
                    course_data['Online'] = 'yes'
                else:
                    course_data['Online'] = 'no'
                if 'full' in temp:
                    course_data['Full_Time'] = 'yes'
                else:
                    course_data['Full_Time'] = 'no'
                if 'partial' in temp:
                    course_data['Part_Time'] = 'yes'
                else:
                    course_data['Part_Time'] = 'no'
                if 'albany' in temp:
                    actual_cities.append('albany')
                if 'wantirna' in temp or 'youth' in temp or 'donvale' in temp or 'heatherton' in temp or 'belgrave' \
                        in temp:
                    actual_cities.append('melbourne')
                if 'victory' in temp:
                    actual_cities.append('victoria')
    else:
        actual_cities.append('melbourne')
    print('LOCATION: ', actual_cities)



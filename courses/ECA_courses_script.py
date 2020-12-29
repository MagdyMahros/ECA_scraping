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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4 as bs4
import os
import copy
from CustomMethods import TemplateData
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, \
    StaleElementReferenceException, JavascriptException, ElementClickInterceptedException

def tag_text(_tag_):
    return _tag_.get_text().__str__().strip()

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options = option)

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
               'Availability': '', 'Description': '', 'Career_Outcomes': '', 'Online': '', 'Offline': 'yes',
               'Distance': 'no', 'Face_to_Face': 'yes', 'Blended': 'no', 'Remarks': '',
               'Subject_Description_1': '', 'Subject_or_Unit_2': '', 'Subject_Objective_2': '',
               'Subject_Description_2': '',
               'Subject_or_Unit_3': '', 'Subject_Objective_3': '', 'Subject_Description_3': '',
               'Subject_or_Unit_4': '', 'Subject_Objective_4': '', 'Subject_Description_4': '',
               'Subject_or_Unit_5': '', 'Subject_Objective_5': '', 'Subject_Description_5': '',
               'Subject_or_Unit_6': '', 'Subject_Objective_6': '', 'Subject_Description_6': '',
               'Subject_or_Unit_7': '', 'Subject_Objective_7': '', 'Subject_Description_7': '',
               'Subject_or_Unit_8': '', 'Subject_Objective_8': '', 'Subject_Description_8': '',
               'Subject_or_Unit_9': '', 'Subject_Objective_9': '', 'Subject_Description_9': '',
               'Subject_or_Unit_10': '', 'Subject_Objective_10': '', 'Subject_Description_10': '',
               'Subject_or_Unit_11': '', 'Subject_Objective_11': '', 'Subject_Description_11': '',
               'Subject_or_Unit_12': '', 'Subject_Objective_12': '', 'Subject_Description_12': '',
               'Subject_or_Unit_13': '', 'Subject_Objective_13': '', 'Subject_Description_13': '',
               'Subject_or_Unit_14': '', 'Subject_Objective_14': '', 'Subject_Description_14': '',
               'Subject_or_Unit_15': '', 'Subject_Objective_15': '', 'Subject_Description_15': '',
               'Subject_or_Unit_16': '', 'Subject_Objective_16': '', 'Subject_Description_16': '',
               'Subject_or_Unit_17': '', 'Subject_Objective_17': '', 'Subject_Description_17': '',
               'Subject_or_Unit_18': '', 'Subject_Objective_18': '', 'Subject_Description_18': '',
               'Subject_or_Unit_19': '', 'Subject_Objective_19': '', 'Subject_Description_19': '',
               'Subject_or_Unit_20': '', 'Subject_Objective_20': '', 'Subject_Description_20': '',
               'Subject_or_Unit_21': '', 'Subject_Objective_21': '', 'Subject_Description_21': '',
               'Subject_or_Unit_22': '', 'Subject_Objective_22': '', 'Subject_Description_22': '',
               'Subject_or_Unit_23': '', 'Subject_Objective_23': '', 'Subject_Description_23': '',
               'Subject_or_Unit_24': '', 'Subject_Objective_24': '', 'Subject_Description_24': '',
               'Subject_or_Unit_25': '', 'Subject_Objective_25': '', 'Subject_Description_25': '',
               'Subject_or_Unit_26': '', 'Subject_Objective_26': '', 'Subject_Description_26': '',
               'Subject_or_Unit_27': '', 'Subject_Objective_27': '', 'Subject_Description_27': '',
               'Subject_or_Unit_28': '', 'Subject_Objective_28': '', 'Subject_Description_28': '',
               'Subject_or_Unit_29': '', 'Subject_Objective_29': '', 'Subject_Description_29': '',
               'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': '',
               'Subject_or_Unit_31': '', 'Subject_Objective_31': '', 'Subject_Description_31': '',
               'Subject_or_Unit_32': '', 'Subject_Objective_32': '', 'Subject_Description_32': '',
               'Subject_or_Unit_33': '', 'Subject_Objective_33': '', 'Subject_Description_33': '',
               'Subject_or_Unit_34': '', 'Subject_Objective_34': '', 'Subject_Description_34': '',
               'Subject_or_Unit_35': '', 'Subject_Objective_35': '', 'Subject_Description_35': '',
               'Subject_or_Unit_36': '', 'Subject_Objective_36': '', 'Subject_Description_36': '',
               'Subject_or_Unit_37': '', 'Subject_Objective_37': '', 'Subject_Description_37': '',
               'Subject_or_Unit_38': '', 'Subject_Objective_38': '', 'Subject_Description_38': '',
               'Subject_or_Unit_39': '', 'Subject_Objective_39': '', 'Subject_Description_39': '',
               'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''}

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
                    course_data['Face_to_Face'] = 'yes'
                    course_data['Offline'] = 'yes'
                else:
                    course_data['Face_to_Face'] = 'no'
                    course_data['Offline'] = 'no'
                if 'wantirna' in temp or 'youth' in temp or 'donvale' in temp or 'heatherton' in temp or 'belgrave' \
                        in temp:
                    actual_cities.append('melbourne')
                    course_data['Face_to_Face'] = 'yes'
                    course_data['Offline'] = 'yes'
                else:
                    course_data['Face_to_Face'] = 'no'
                    course_data['Offline'] = 'no'
                if 'victory' in temp:
                    actual_cities.append('victoria')
                    course_data['Face_to_Face'] = 'yes'
                    course_data['Offline'] = 'yes'
                else:
                    course_data['Face_to_Face'] = 'no'
                    course_data['Offline'] = 'no'
    else:
        actual_cities.append('melbourne')
        course_data['Face_to_Face'] = 'yes'
        course_data['Offline'] = 'yes'
    print('LOCATION: ', actual_cities)

    # career outcomes
    outcome_title = soup.find('h3', text=re.compile('Course Outcomes', re.IGNORECASE))
    if outcome_title:
        outcome_ul = outcome_title.find_next_sibling('ul')
        temp = []
        if outcome_ul:
            outcome_list = outcome_ul.find_all('li')
            if outcome_list:
                for li in outcome_list:
                    temp.append(li.get_text().strip())
                temp = ' / '.join(temp)
                course_data['Career_Outcomes'] = temp
                print('CAREER OUTCOMES: ', temp)

    # ATAR
    atar_title = soup.find('h4', id='atar-based-admissions')
    course_data['Prerequisite_1'] = ''
    course_data['Prerequisite_1_grade'] = ''
    if atar_title:
        atar_p = atar_title.find_next_sibling('p')
        if atar_p:
            atar = re.search(r'\d+', atar_p.get_text())
            if atar is not None:
                course_data['Prerequisite_1'] = 'year 12'
                course_data['Prerequisite_1_grade'] = atar.group()
                print('ATAR: ' + str(course_data['Prerequisite_1_grade']) + ' / ' + course_data['Prerequisite_1'])

    #UNITS
    units_title = soup.find('h2', text=re.compile('Competencies attached to this course', re.IGNORECASE))
    try:
        units_title_1 = browser.find_elements_by_xpath("//*[contains(text(), 'Units attached to this course')]")
    except NoSuchElementException:
        units_title_1 = False
    if units_title:
        units_table = units_title.find_next('table', class_='newstyle-dense')
        if units_table:
            u_temp = []
            t_body = units_table.find('tbody')
            if t_body:
                t_rows = t_body.find_all('tr')
                if t_rows:
                    for index, row in enumerate(t_rows):
                        if index > 1:
                            td = row.find('td')
                            course_data['Subject_or_Unit_'+str(index)] = td.get_text().strip()
                            u_temp.append(str(course_data['Subject_or_Unit_'+str(index)]))
            print('UNITS: ', u_temp)
    elif units_title_1:
        try:
            THE_XPATH = "//*[contains(text(), 'Units attached to this course')]/following-sibling::table"
            WebDriverWait(browser, 1).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, f'{THE_XPATH}'))
            )
            units_table = browser.find_element_by_xpath(f'{THE_XPATH}')
            if units_table:
                subjects_link = []
                a_tag = units_table.find_elements_by_tag_name('a')
                if a_tag:
                    for a in a_tag:
                        link = a.get_attribute('href')
                        if link not in subjects_link:
                            subjects_link.append(link)
                        if len(subjects_link) == 40:
                            break
                    i = 1
                    for s in subjects_link:
                        browser.get(s)
                        # subject name
                        try:
                            THE_XPATH = '/html/body/div/div/h2[1]'
                            WebDriverWait(browser, 3).until(
                                EC.presence_of_all_elements_located(
                                    (By.XPATH, f'{THE_XPATH}'))
                            )
                            value = browser.find_element_by_xpath(f'{THE_XPATH}').text
                            print('UNIT NAME: ', value)
                            course_data[f'Subject_or_Unit_{i}'] = value
                        except (AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                            print(f'cant extract subject name {i}')
                        # subject description
                        try:
                            THE_XPATH = "//*[contains(text(), 'Unit Description')]/following-sibling::p[1]"
                            WebDriverWait(browser, 3).until(
                                EC.presence_of_all_elements_located(
                                    (By.XPATH, f'{THE_XPATH}'))
                            )
                            value = browser.find_element_by_xpath(f'{THE_XPATH}').text
                            print('UNIT DESCRIPTION: ', value)
                            course_data[f'Subject_Description_{i}'] = value
                        except (AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                            print(f'cant extract subject description {i}')
                        # subject objectives
                        try:
                            objectives_list = []
                            THE_XPATH = "//*[contains(text(), 'Learning Outcomes')]/following-sibling::ul[1]/li"
                            WebDriverWait(browser, 3).until(
                                EC.presence_of_all_elements_located(
                                    (By.XPATH, f'{THE_XPATH}'))
                            )
                            for elem in browser.find_elements_by_xpath(f'{THE_XPATH}'):
                                objectives_list.append(elem.text)
                            objectives_list = ' / '.join(objectives_list)
                            print('UNIT OBJECTIVES: ', objectives_list)
                            course_data[f'Subject_Objective_{i}'] = objectives_list
                        except (AttributeError, TimeoutException, NoSuchElementException,
                                ElementNotInteractableException) as e:
                            print(f'cant extract subject objective {i}')
                        i += 1
        except (AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            pass

    # duplicating entries with multiple cities for each city
    for i in actual_cities:
        course_data['City'] = possible_cities[i]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

    # TABULATE THE DATA
    desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty', 'Int_Fees', 'Local_Fees',
                          'Currency', 'Currency_Time', 'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                          'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3', 'Prerequisite_1_grade',
                          'Prerequisite_2_grade', 'Prerequisite_3_grade', 'Website', 'Course_Lang', 'Availability',
                          'Description', 'Career_Outcomes', 'Country', 'Online', 'Offline', 'Distance',
                          'Face_to_Face', 'Blended', 'Remarks','Subject_or_Unit_1', 'Subject_Objective_1',
                          'Subject_Description_1',
                          'Subject_or_Unit_2', 'Subject_Objective_2', 'Subject_Description_2',
                          'Subject_or_Unit_3', 'Subject_Objective_3', 'Subject_Description_3',
                          'Subject_or_Unit_4', 'Subject_Objective_4', 'Subject_Description_4',
                          'Subject_or_Unit_5', 'Subject_Objective_5', 'Subject_Description_5',
                          'Subject_or_Unit_6', 'Subject_Objective_6', 'Subject_Description_6',
                          'Subject_or_Unit_7', 'Subject_Objective_7', 'Subject_Description_7',
                          'Subject_or_Unit_8', 'Subject_Objective_8', 'Subject_Description_8',
                          'Subject_or_Unit_9', 'Subject_Objective_9', 'Subject_Description_9',
                          'Subject_or_Unit_10', 'Subject_Objective_10', 'Subject_Description_10',
                          'Subject_or_Unit_11', 'Subject_Objective_11', 'Subject_Description_11',
                          'Subject_or_Unit_12', 'Subject_Objective_12', 'Subject_Description_12',
                          'Subject_or_Unit_13', 'Subject_Objective_13', 'Subject_Description_13',
                          'Subject_or_Unit_14', 'Subject_Objective_14', 'Subject_Description_14',
                          'Subject_or_Unit_15', 'Subject_Objective_15', 'Subject_Description_15',
                          'Subject_or_Unit_16', 'Subject_Objective_16', 'Subject_Description_16',
                          'Subject_or_Unit_17', 'Subject_Objective_17', 'Subject_Description_17',
                          'Subject_or_Unit_18', 'Subject_Objective_18', 'Subject_Description_18',
                          'Subject_or_Unit_19', 'Subject_Objective_19', 'Subject_Description_19',
                          'Subject_or_Unit_20', 'Subject_Objective_20', 'Subject_Description_20',
                          'Subject_or_Unit_21', 'Subject_Objective_21', 'Subject_Description_21',
                          'Subject_or_Unit_22', 'Subject_Objective_22', 'Subject_Description_22',
                          'Subject_or_Unit_23', 'Subject_Objective_23', 'Subject_Description_23',
                          'Subject_or_Unit_24', 'Subject_Objective_24', 'Subject_Description_24',
                          'Subject_or_Unit_25', 'Subject_Objective_25', 'Subject_Description_25',
                          'Subject_or_Unit_26', 'Subject_Objective_26', 'Subject_Description_26',
                          'Subject_or_Unit_27', 'Subject_Objective_27', 'Subject_Description_27',
                          'Subject_or_Unit_28', 'Subject_Objective_28', 'Subject_Description_28',
                          'Subject_or_Unit_29', 'Subject_Objective_29', 'Subject_Description_29',
                          'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30',
                          'Subject_or_Unit_31', 'Subject_Objective_31', 'Subject_Description_31',
                          'Subject_or_Unit_32', 'Subject_Objective_32', 'Subject_Description_32',
                          'Subject_or_Unit_33', 'Subject_Objective_33', 'Subject_Description_33',
                          'Subject_or_Unit_34', 'Subject_Objective_34', 'Subject_Description_34',
                          'Subject_or_Unit_35', 'Subject_Objective_35', 'Subject_Description_35',
                          'Subject_or_Unit_36', 'Subject_Objective_36', 'Subject_Description_36',
                          'Subject_or_Unit_37', 'Subject_Objective_37', 'Subject_Description_37',
                          'Subject_or_Unit_38', 'Subject_Objective_38', 'Subject_Description_38',
                          'Subject_or_Unit_39', 'Subject_Objective_39', 'Subject_Description_39',
                          'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40']

    course_dict_keys = set().union(*(d.keys() for d in course_data_all))

    with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, course_dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(course_data_all)

    with open(csv_file, 'r', encoding='utf-8') as infile, open('ECA_courses_ordered.csv', 'w', encoding='utf-8',
                                                               newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)

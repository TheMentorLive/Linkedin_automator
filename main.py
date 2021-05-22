from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4.element import Tag
from time import sleep
import csv
import parameters
from itertools import zip_longest


def find_profiles():
    for r in result_div:
        try:
            link = r.find('a', href=True)
            title = r.find('h3')

            if isinstance(title, Tag):
                title = title.get_text()

            Job = r.find('h3')
            if isinstance(Job, Tag):
                Job = Job.get_text()

            Location = r.find('h3')
            if isinstance(Location, Tag):
                Location = Location.get_text()

            description = r.find('span', attrs={'class': 'st'})

            if isinstance(description, Tag):
                description = description.get_text()

            if link != '' and title != '' and Job != '' and Location != '' and description != '':
                links.append(link['href'])
                titles.append(title)
                Locations.append(Location)
                Jobs.append(Job)
                descriptions.append(description)
        except Exception as e:
            print(e)
            continue

def profiles_loop():
    find_profiles()

    next_button = driver.find_element_by_xpath('//*[@id="pnnext"]')
    next_button.click()


def repeat_fun(times, f):
    for i in range(times): f()


driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.linkedin.com')
username = driver.find_element_by_id('session_key')
username.send_keys(parameters.linkedin_username)
sleep(0.5)


password = driver.find_element_by_id('session_password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)


log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()
sleep(0.5)


driver.get('https://www.google.com')
sleep(3)


search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "python developer" AND "London"')
search_query.send_keys(Keys.RETURN)


soup = BeautifulSoup(driver.page_source, 'lxml')
result_div = soup.find_all('div', attrs={'class': 'g'})



links = []
titles = []
Jobs = []
Locations = []
descriptions = []


repeat_fun(10, profiles_loop)


titles1 = [i.split()[0:2] for i in titles]
Jobs1 = [i.split()[3:6] for i in Jobs]
Locations1 = [i.split()[6:9] for i in Locations]


print(titles1)
print(links)
print(Jobs1)
print(Locations1)
print(descriptions)



d = [titles1, links, Jobs1, Locations1]
export_data = zip_longest(*d, fillvalue = '')
with open(parameters.file_name, 'w', encoding="ISO-8859-1", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("Titles", "Links", "Current_Job", "Current_Location" ))
      wr.writerows(export_data)
myfile.close()



from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv
import os
import time
import datetime

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)



start_time = time.time()


try:
    os.remove('D:\\webscraping\\files\\csfd_27_09_2018.csv')
except:
    pass

for id in range(1,318000):

    one_row = []
    url = 'https://www.csfd.cz/film/{}'.format(id)
    raw_html = simple_get(url)
    soup = BeautifulSoup(raw_html, 'html.parser')

    one_row.append(str(id))


    try:
        one_row.append(" ".join((soup.find('div', {'class': 'header'}).find('h1', {'itemprop': 'name'}).text).split()))
    except:
        one_row.append('')

    try:
        one_row.append(soup.find('div', {'class': 'info'}).find('p', {'class': 'genre'}).text)
    except:
        one_row.append('')

    try:
        one_row.append(soup.find('div', {'id': 'rating'}).find('h2', {'class': 'average'}).text)
    except:
        one_row.append('')

    try:
        one_row.append(soup.find('div', {'class': 'count'}).text.strip().replace('\xa0',''))
    except:
        one_row.append('')

    try:
        one_row.append(soup.find('p',{'class': 'origin'}).text)
    except:
        one_row.append('')

    if (soup.find('div',{'class': 'creators'}).find('span',{'itemprop': 'director'})):
        i=0
        row_creators = []
        while True:
            try:
                row_creators.append(soup.find('div',{'class': 'creators'}).find('span',{'itemprop': 'director'}).findAll('a')[i].text)
                i += 1
            except:
                one_row.append(row_creators)
                with open('D:\\webscraping\\files\\csfd_27_09_2018.csv', 'a', newline='', encoding="utf8") as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow(one_row)

                print('processing movie id:{}'.format(id))
                print('time elapsed: {}'.format(str(datetime.timedelta(seconds=((time.time() - start_time))))).split(".")[0])
                id += 1
                break
    else:
        one_row.append('')
        with open('D:\\webscraping\\files\\csfd_27_09_2018.csv', 'a', newline='', encoding="utf8") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(one_row)

        print('processing movie id:{}'.format(id))
        print('time elapsed: {}'.format(str(datetime.timedelta(seconds=((time.time() - start_time))))).split(".")[0])
        id += 1



# print(one_row)
# print(one_row)
# print(one_row)
# print(one_row)






















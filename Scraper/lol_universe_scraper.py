import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import utility
from helium import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

base_url = 'https://universe.leagueoflegends.com'


def scrape_champion_region():
    output = []
    url = base_url + '/en_US/champions/'
    try:
        driver.get(url)
        driver.maximize_window()
        driver.implicitly_wait(5)
        html = driver.page_source
        parsed_html = BeautifulSoup(html, 'html.parser')
        champion_row_ul_list = parsed_html.find_all('ul', class_='champsListUl_2Lmb')
        for ul in champion_row_ul_list:
            li_list = ul.find_all('li')
            for li in li_list:
                result = {}
                info_div = li.find('div', class_='copy_xxN7')
                result['name'] = info_div.h1.text
                result['main_page_url'] = base_url + li.a['href']
                result['region'] = info_div.span.text
                output.append(result)
        return output
    except (AttributeError, TypeError):
        print('champion counter url scraper failed')


def scrape_background_story(info_list):
    try:
        for champion_dict in info_list:
            url = champion_dict['main_page_url']
            driver.get(url)
            driver.maximize_window()
            driver.implicitly_wait(10)
            time.sleep(2)
            html = driver.page_source
            parsed_html = BeautifulSoup(html, 'html.parser')
            story = parsed_html.find('div', class_='biographyText_3-to').text.strip()
            print(story)
            print(story == '')
            champion_dict['background_story'] = story
        return info_list
    except (AttributeError, TypeError):
        print('champion counter url scraper failed')
    # champion_dict = info_list[1]
    # url = champion_dict['main_page_url']
    # driver.get(url)
    # driver.maximize_window()
    # driver.implicitly_wait(10)
    # html = driver.page_source
    # parsed_html = BeautifulSoup(html, 'html.parser')
    # story = parsed_html.find('div', class_='biographyText_3-to').p.text
    # print(story)
    # champion_dict['background_story'] = story


if __name__ == '__main__':
    info = scrape_champion_region()
    print(info)
    final_result = scrape_background_story(info)
    utility.export_to_json('json_file/champion_region_story.json', final_result)

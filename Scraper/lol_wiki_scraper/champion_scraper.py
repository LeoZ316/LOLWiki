import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from rating_scraper import scrape_rating
from skill_scraper import scrape_skill
from champion_legacy_scraper import scrape_champion_legacy
from champion_position_scraper import scrape_champion_position


def scrape_all_champion(starting_url):
    champion_list = []
    rating_list = []
    skill_list = []
    champion_legacy_list = []
    champion_position_list = []

    driver = get_driver()
    soup = get_soup(starting_url, driver)
    if soup is None:
        return champion_list

    champion_roster = soup.find('ol', class_='champion_roster')
    champions_holder = champion_roster.find_all('li')

    for i, champion_holder in enumerate(champions_holder):
        rel_url = champion_holder.find('a')['href']
        champion_url = 'https://leagueoflegends.fandom.com/' + rel_url

        # Designed to scrape one table each time,
        # so comment out non-relevant code to scrape one part
        champion_dict = scrape_champion(champion_url, i, driver)
        image_url = champion_holder.find('img')['data-src']
        champion_dict['Image_Url'] = image_url
        champion_list.append(champion_dict)

        rating_dict = scrape_rating(champion_url, i)
        rating_list.append(rating_dict)

        skill_dict = scrape_skill(champion_url, i)
        skill_list.append(skill_dict)

        list_of_champion_legacy_dict = scrape_champion_legacy(champion_url, i, driver)
        for dic in list_of_champion_legacy_dict:
            champion_legacy_list.append(dic)

        list_of_champion_position_dict = scrape_champion_position(champion_url, i, driver)
        for dic in list_of_champion_position_dict:
            champion_position_list.append(dic)

    driver.close()
    print('-' * 20, f'Found {len(champion_list)} champion urls', '-' * 20)
    # Write to json file
    if champion_list:
        write_to_json(champion_list, 'champion.json')
    if rating_list:
        write_to_json(rating_list, 'rating.json')
    if skill_list:
        write_to_json(skill_list, 'skill.json')
    if champion_legacy_list:
        write_to_json(champion_legacy_list, 'champion_legacy.json')
    if champion_position_list:
        write_to_json(champion_position_list, 'champion_position.json')

    return champion_list, rating_list, skill_list, champion_legacy_list, champion_position_list


def scrape_champion(url, i, driver):
    print('-' * 20, f'Scraping champion {i}', '-' * 20)
    champion_dict = {'Champion_ID': i, 'Rating_ID': i, 'Skill_ID': i}
    soup = get_soup(url, driver)
    if soup is None:
        return champion_dict

    holder = soup.find('aside', {'role': 'region',
                                 'class': 'portable-infobox pi-background pi-border-color '
                                          'pi-theme-client pi-layout-default'})

    champion_name = holder.find('h2').find('span').text
    champion_dict['Name'] = champion_name

    champion_class = holder.find('div', {'data-source': 'role'}).find('span')['data-tip']
    champion_dict['Class'] = champion_class

    champion_resource = holder.find('div', {'data-source': 'resource'}).find('span')['data-tip']
    champion_dict['Resource'] = champion_resource

    champion_range_type = holder.find('div', {'data-source': 'rangetype'}).find('span')['data-tip']
    champion_dict['Range_Type'] = champion_range_type

    champion_adaptive_type = holder.find('div', {'data-source': 'adaptivetype'}).find('span').text
    champion_dict['Adaptive_Type'] = champion_adaptive_type

    return champion_dict


def get_soup(url, driver):
    """
    Get the soup by url.
    Uses webdriver object to execute javascript code and get dynamically loaded webcontent
    """
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,
                         'html.parser')  # beautiful soup object to be used for parsing html content
    return soup


def get_driver():
    """
    Create a webdriver object and set options for headless browsing
    """
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('./chromedriver', options=options)
    return driver


def write_to_json(lst, file):
    with open(file, 'w') as output_file:
        json.dump(lst, output_file, indent=4)

# dri = get_driver()
# get_soup('https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki', dri)
# dri.close()
# scrape_champion('https://leagueoflegends.fandom.com/wiki/Alistar/LoL')

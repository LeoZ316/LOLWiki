import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import utility

base_url = 'https://www.op.gg'


def scrape_champion_list():
    """
    Add Opgg_Main_Page for each champion
    """
    url = base_url + '/champion/statistics'
    output = []
    try:
        html = urlopen(url)
        parsed_html = BeautifulSoup(html, 'html.parser')
        champion_list_div = parsed_html.find('div', class_='champion-index__champion-list')
        champion_a_list = champion_list_div.find_all('a')
        for info in champion_a_list:
            champion_url = info['href']
            champion_name = info.find('div', class_='champion-index__champion-item__name').text.strip()
            output.append({'Champion_Name': champion_name, 'Opgg_Main_Page': base_url + champion_url})
        return output
    except (AttributeError, TypeError):
        print('champion list scraper failed')


def scrape_champion_counter_url(champion_list):
    """
    Add Counter_Page_URL for each champion
    """
    try:
        for champion in champion_list:
            time.sleep(0.5)
            champion_url = champion['Opgg_Main_Page']
            html = urlopen(champion_url)
            parsed_html = BeautifulSoup(html, 'html.parser')
            counter_li = parsed_html.find('li', class_='champion-stats-menu__list__item champion-stats-menu__list__item--red tabHeader')
            counter_url = counter_li.a['href']
            champion['Counter_Page_URL'] = base_url + counter_url
            print(champion)
        return champion_list
    except (AttributeError, TypeError):
        print('champion counter url scraper failed')


def scrape_match_up_win_rate(champion_opgg_list):
    """
    Create champion_matchup_win_rate.json
    """
    output = []
    try:
        for champion in champion_opgg_list:
            time.sleep(1)
            champion_name = champion['Champion_Name']
            counter_url = champion['Counter_Page_URL']
            html = urlopen(counter_url)
            parsed_html = BeautifulSoup(html, 'html.parser')
            match_up_champion_list = parsed_html.find('div', class_='champion-matchup-champion-list')
            against_info_list = match_up_champion_list.find_all('div', class_='champion-matchup-list__champion')
            for against_info in against_info_list:
                result = {'First_Champion_ID': champion_name}
                against_champion = against_info.find('span').text.strip()
                result['Second_Champion_ID'] = against_champion
                win_rate = float(against_info.find_all('span')[1].text.strip()[:-1])
                result['Win_Rate'] = win_rate
                output.append(result)
                print(result)
        print(output)
        return output
    except (AttributeError, TypeError):
        print('match_up_win_rate scraper failed')


if __name__ == '__main__':
    # first_output = scrape_champion_list()
    # print(first_output)
    # second_output = scrape_champion_counter_url(first_output)
    # print(second_output)
    # utility.export_to_json('json_file/champion_opgg_url.json', second_output)
    # opgg_data = utility.load_json('json_file/champion_opgg_url.json')
    # result = scrape_match_up_win_rate(opgg_data)
    # utility.export_to_json('json_file/champion_matchup_win_rate.json', result)




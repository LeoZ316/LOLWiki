from urllib.request import urlopen
from bs4 import BeautifulSoup


def scrape_rating(url, i):
    print('-' * 20, f'Scraping rating {i}', '-' * 20)
    rating_dict = {'Rating_ID': i}

    soup = get_soup(url)
    if soup is None:
        return rating_dict

    rating_str = soup.find('div', class_="stat-wheel")["data-values"]
    rating_list = rating_str.split(';')
    rating_dict['Damage'] =  rating_list[0]
    rating_dict['Toughness'] = rating_list[1]
    rating_dict['Control'] = rating_list[2]
    rating_dict['Mobility'] = rating_list[3]
    rating_dict['Utility'] = rating_list[4]
    return rating_dict


def get_soup(url):
    try:
        html = urlopen(url)
    except:
        print('Cannot open url')
        return None

    soup = BeautifulSoup(html, 'html.parser')
    return soup


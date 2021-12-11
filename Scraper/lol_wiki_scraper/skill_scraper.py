from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def scrape_skill(url, i):
    print('-' * 20, f'Scraping skills {i}', '-' * 20)
    skill_dict = {'Skill_ID': i}

    soup = get_soup(url)
    if soup is None:
        return skill_dict

    skill_innate = soup.find('div', class_="skill skill_innate").text
    skill_dict['Skill_Innate'] = get_text(skill_innate)

    skill_q = soup.find('div', class_="skill skill_q").text
    skill_dict['Skill_Q'] = get_text(skill_q)

    skill_w = soup.find('div', class_="skill skill_w").text
    skill_dict['Skill_W'] = get_text(skill_w)

    skill_e = soup.find('div', class_="skill skill_e").text
    skill_dict['Skill_E'] = get_text(skill_e)

    skill_r = soup.find('div', class_="skill skill_r").text
    skill_dict['Skill_R'] = get_text(skill_r)
    return skill_dict


def process_text(text):
    text = text.encode('ascii', errors='ignore').decode('utf-8')  # removes non-ascii characters
    text = re.sub('\s+', ' ', text)  # repalces repeated whitespace characters with single space
    return text


def get_text(skill_raw_text):
    count = 0
    for i, ch in enumerate(skill_raw_text):
        if count == 3:
            return process_text(skill_raw_text[i:])
        if ch == '\n':
            count += 1


def get_soup(url):
    try:
        html = urlopen(url)
    except:
        print('Cannot open url')
        return None

    soup = BeautifulSoup(html, 'html.parser')
    return soup

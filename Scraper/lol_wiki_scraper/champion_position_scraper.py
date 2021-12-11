from bs4 import BeautifulSoup


def scrape_champion_position(url, i, driver):
    list_of_champion_position_dict = []

    print('-' * 20, f'Scraping champion position {i}', '-' * 20)

    soup = get_soup(url, driver)
    if soup is None:
        return list_of_champion_position_dict

    container = soup.find('aside', {'role': 'region',
                                    'class': 'portable-infobox pi-background pi-border-color '
                                             'pi-theme-client pi-layout-default'})

    holders = container.find('div', {'data-source': 'position'})
    if holders is None:
        return list_of_champion_position_dict
    holders = holders.find('div', class_='pi-data-value pi-font').find_all('span')
    for holder in holders:
        position = holder.text.strip()
        champion_legacy_dict = {'Champion_ID': i, 'Position_Name': position}
        list_of_champion_position_dict.append(champion_legacy_dict)

    return list_of_champion_position_dict


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

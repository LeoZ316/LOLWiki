# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from champion_scraper import scrape_all_champion


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    starting_url = 'https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki'
    scrape_all_champion(starting_url)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

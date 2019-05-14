import requests
from bs4 import BeautifulSoup
import sys


def main():
    response = requests.get('https://us.soccerway.com/national/england/premier-league/20182019/regular-season/r48730'
                            '/?ICID=TN_02_01_01')
    if response.status_code != 200:
        sys.stderr.write("enable to join the web site")
        return 1

    soup = BeautifulSoup(response.text, 'html.parser')
    rank_table = soup.find("div", {"id": "page_competition_1_block_competition_tables_7-wrapper"})
    for tr in rank_table.tbody.find_all('tr'):
        td = tr.find('td', {"class": "team"})
        print(td.text)


if __name__ == '__main__':
    main()
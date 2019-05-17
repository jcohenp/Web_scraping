import requests
from bs4 import BeautifulSoup
import sys


def get_team_in_rank_table(soup):
    teams_name = []
    teams_link = []
    rank_table = soup.find("div", {"id": "page_competition_1_block_competition_tables_7-wrapper"})
    for tr in rank_table.tbody.find_all('tr'):
        # get td
        td = tr.find('td', {"class": "team"})
        team_name = td.text
        teams_name.append(team_name)
        teams_link.append(td.find("a")['href'])

    return teams_name, teams_link


def get_team_info(request_team, teams_informations, teams_name, current_team):
    soup = BeautifulSoup(request_team, 'html.parser')
    info = soup.find("div", {"class": "first-element"})
    dict_info = {}
    dl = info.find("dl")
    list_dt = dl.find_all("dt")
    list_dd = dl.find_all("dd")
    match_elem = ["Founded", "Country", "Address", "E-mail"]
    dict_address = {}
    for i in range(len(list_dt)):
        if list_dt[i].text.strip() in match_elem:
            if list_dt[i].text == "Address":
                address = list_dd[i].text.strip().split("\n")
                dict_address["Street"] = address[0].strip()
                dict_address["District"] = address[1].strip()
                dict_address["City"] = address[2].strip()
                dict_info[list_dt[i].text.strip()] = dict_address
            else:
                dict_info[list_dt[i].text.strip()] = list_dd[i].text.strip()

    info_section = {}
    info_section["Info"] = dict_info
    teams_informations[teams_name[current_team]] = info_section
    return teams_informations


def main():
    teams_informations = {}
    response = requests.get('https://us.soccerway.com/national/england/premier-league/20182019/regular-season/r48730'
                            '/?ICID=TN_02_01_01')
    if response.status_code != 200:
        sys.stderr.write("enable to join the web site")
        return 1

    soup = BeautifulSoup(response.text, 'html.parser')
    teams_name, teams_links = get_team_in_rank_table(soup)

    current_team = 0
    for team_link in teams_links:
        # new request
        request_team = requests.get("https://us.soccerway.com/" + team_link)
        teams_informations = get_team_info(request_team.text, teams_informations, teams_name, current_team)
        current_team += 1
    print(teams_informations)


if __name__ == '__main__':
    main()
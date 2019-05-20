import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd

WEBSITE = "https://us.soccerway.com"


def get_leagues(soup):
    # TODO: delete this function and use the one in teams_information.py after merging
    navbar = soup.find("div", {"id": "navbar"})
    select = navbar.find("select")
    options = select.find_all("option")
    url_league = []
    match_leagues = ["Premier League", "Bundesliga", "Serie A", "La Liga", "Ligue 1"]
    for i in range(len(options)):
        if options[i].text in match_leagues and "russia" not in options[i]["value"]:
            url_league.append(["https://us.soccerway.com" + options[i]["value"], options[i].text])
    return url_league


def get_players(league_url):
    """

    :param league_url:
    :return: list_player
    """

    players_table = league_url.find("table", {"id": "page_competition_1_block_competition_playerstats_8_block_competition_playerstats_topscores_1_table"})
    list_players = []
    for tr in players_table.tbody.find_all('tr'):
        list_players.append(get_player_info(tr))
    return list_players


def get_player_info(tr):
    """

    :param tr:
    :return:
    """
    player = tr.find('td', {"class": "player"})
    team = tr.find('td', {"class": "team"})
    number_goals = tr.find('td', {"class": "number goals"})
    #print(player.text.strip() + " " + team.text.strip() + " " + number_goals.text.strip())
    #return [player, team, number_goals]
    return[player.text.strip(), team.text.strip(), number_goals.text.strip()]


def get_all_top_players_info():
    """

    :return:
    """
    players_info = []
    general_website = requests.get(WEBSITE)
    if general_website.status_code != 200:
        sys.stderr.write("enable to join the web site")
        return -1
    soup = BeautifulSoup(general_website.text, 'lxml')
    list_leagues_url = get_leagues(soup)

    dict_top_players_by_league = {}
    for league_url in list_leagues_url:
        res_league = requests.get(league_url[0])
        soup = BeautifulSoup(res_league.text, 'lxml')
        league_players = get_players(soup)
        #player_info = [get_player_info(player) for player in league_players]
        # players_info.append(player_info)
        dict_top_players_by_league.update({league_url[1]: league_players})
    dt = pd.DataFrame(dict_top_players_by_league)
    return dt


def main():
    print(get_all_top_players_info())


if __name__ == '__main__':
    main()

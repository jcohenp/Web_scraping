import requests
from bs4 import BeautifulSoup
import sys
import Web_scraping.src.config as config
import pandas as pd

# WEBSITE = "https://us.soccerway.com"
# LEAGUE_NAME = 1
# LEAGUE_URL = 0


# def get_leagues(soup):
#     navbar = soup.find("div", {"id": "navbar"})
#     select = navbar.find("select")
#     options = select.find_all("option")
#     url_league = []
#     for i in range(len(options)):
#         if options[i].text in config.MATCHES_LEAGUES and "russia" not in options[i]["value"]:
#             url_league.append(["https://us.soccerway.com" + options[i]["value"], options[i].text])
#     return url_league


def get_players(league_url):
    """
    gets a league and returns the top players stats
    :param league_url: a specific league
    :return: list_players: a list with all the relevant info of the top players in the league
    """
    players_table = league_url.find("table", {"id": "page_competition_1_block_competition_playerstats_8_block_competition_playerstats_topscores_1_table"})
    list_players = [["NAME", "TEAM", "GOALS", "FIRST GOALS"]]
    for tr in players_table.tbody.find_all('tr'):
        list_players.append(get_player_info(tr))
    return list_players


def get_player_info(tr):
    """
    take a player and get the stats of that player
    :param tr: a line in players table
    :return: the relevant information on that player
    """
    player = tr.find('td', {"class": "player"})
    team = tr.find('td', {"class": "team"})
    number_goals = tr.find('td', {"class": "number goals"})
    first_goals = tr.find('td', {"class": "number first-goals"})
    return[player.text.strip(), team.text.strip(), number_goals.text.strip(), first_goals.text.strip()]


def get_all_top_players_info():
    """
    goes over the top five leagues
    :return: data from that contains each league and the stat of its top players
    """
    general_website = requests.get(config.WEBSITE)
    if general_website.status_code != 200:
        sys.stderr.write("enable to join the web site")
        return -1
    soup = BeautifulSoup(general_website.text, 'lxml')
    list_leagues_url = config.get_leagues(soup)

    dict_top_players_by_league = {}
    for league_url in list_leagues_url:
        res_league = requests.get(league_url[config.LEAGUE_URL])
        soup = BeautifulSoup(res_league.text, 'lxml')
        league_players = get_players(soup)
        dict_top_players_by_league[league_url[config.LEAGUE_NAME]] = league_players

    return dict_top_players_by_league

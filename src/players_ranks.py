import requests
from bs4 import BeautifulSoup
import sys
import config as config
import pandas as pd

TABLE_LEN = 15


def get_players(league_url, player_id):
    """
    gets a league and returns the top players stats
    :param league_url: a specific league
    :return: list_players: a list with all the relevant info of the top players in the league
    """

    players_table = league_url.find("table", {"class": "playerstats table"})
    list_players = []
    for tr in players_table.tbody.find_all('tr'):
        list_players.append(get_player_info(tr, player_id))
        player_id += 1
    return list_players


def get_player_info(tr, player_id):
    """
    take a player and get the stats of that player
    :param tr: a line in players table
    :return: the relevant information on that player
    """
    player_href = tr.find('td', {"class": "player"})
    player = player_href.contents[0].attrs["href"].split("/")[2].replace("-", " ")
    team_td = tr.find('td', {"class": "team"})
    team = team_td.find("a").attrs["title"]
    number_goals = tr.find('td', {"class": "number goals"})
    first_goals = tr.find('td', {"class": "number first-goals"})

    return [player_id, player, team, number_goals.text.strip(), first_goals.text.strip()]


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
    player_id = 0
    dict_top_players_by_league = {}
    for league_url in list_leagues_url:
        league_url_last_season = league_url[0].rsplit("/", 2)
        league_url[0] = league_url_last_season[0] + "/20182019/" + league_url_last_season[2]
        res_league = requests.get(league_url[config.LEAGUE_URL])
        soup = BeautifulSoup(res_league.text, 'lxml')
        league_players = get_players(soup, player_id)
        dict_top_players_by_league[league_url[config.LEAGUE_NAME]] = league_players
        player_id += TABLE_LEN
    return make_dict_to_df(dict_top_players_by_league)


def make_dict_to_df(dict_top_players_by_league):
    """make the dict of information about players to a dataframe"""
    top_players_pd = pd.DataFrame()
    for key, value in dict_top_players_by_league.items():

        df1 = pd.DataFrame(value, columns=['player_id', 'name', 'team', 'goals', 'first_goals'])
        top_players_pd = pd.concat([top_players_pd, df1], axis=0, join='outer', join_axes=None, ignore_index=True,
                                   keys=None, levels=None,
                                   names=None, verify_integrity=False, copy=True)

    return top_players_pd

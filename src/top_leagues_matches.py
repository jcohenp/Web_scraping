"""matches per league"""
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import config


# WEBSITE = "https://us.soccerway.com"
# MATCHES_LEAGUES = ["Premier League", "Bundesliga", "Serie A", "La Liga", "Ligue 1"]
# LIST_TOTAL_WEEKS_PER_LEAGUE = [38, 34, 37, 38, 38]
# COMP_ID = -2
# THE_R = -2
# LEAGUE_NAME = 1
# LEAGUE_URL = 0


# def get_leagues(soup):
#     navbar = soup.find("div", {"id": "navbar"})
#     select = navbar.find("select")
#     options = select.find_all("option")
#     leagues = []
#     for i in range(len(options)):
#         if options[i].text in config.MATCHES_LEAGUES and "russia" not in options[i]["value"]:
#             leagues.append(["https://us.soccerway.com" + options[i]["value"], options[i]["value"].split("/")[3]])
#
#     return leagues


def get_game_weeks(weeks, comp_id, the_r):
    """
    gives you all the game weeks in a specific league league
    :param weeks: number of game weeks in that league
    :param comp_id: the competition id to put in the url
    :param the_r: the league number in soccerway
    :return: list_matches_week: all the matches in that league divide by weeks
    """
    list_matches_weeks = []
    for week_mun in range(weeks):
        data = json.load(urllib.request.urlopen(
            'https://us.soccerway.com/a/block_competition_matches_summary?block_id'
            '=page_competition_1_block_competition_matches_summary_5&callback_params={"page":"37",'
            '"block_service_id":"competition_summary_block_competitionmatchessummary","round_id":"' + str(the_r) + '",'
            '"outgroup":"","view":"1","competition_id":"' + str(comp_id) + '"}&action=changePage&params={"page":' + str(week_mun) + '}'))

        list_matches_weeks.append(BeautifulSoup(data["commands"][0]["parameters"]["content"], "lxml"))

    return list_matches_weeks


def get_matches(game_week):
    """
    takes a game week table and gets you all the matched who were played (rows in the table)
    :param game_week: a specific game week table
    :return: list_matches_week: a list of all the games in that week
    """
    list_matches_week = []
    for each in game_week:
        list_matches_week.append([get_match_info(tr) for tr in each.tbody.find_all('tr')])
    return list_matches_week


def get_match_info(tr):
    """
    gets a line (match) and takes the relevant data
    :param tr: a line in the game week table
    :return: information about that game: day, date, team-a teaam-b and score
    """
    day = tr.find('td', {"class": "day"})
    date = tr.find('td', {"class": "date"})
    team_a = tr.find('td', {"class": "team-a"})
    team_b = tr.find('td', {"class": "team-b"})
    score = tr.find('td', {"class": "score"})

    return [day.text.strip(), date.text.strip(), team_a.text.strip(), team_b.text.strip(), score.text.strip()]


def get_all_matches_in_all_leagues():
    general_website = requests.get(config.WEBSITE)

    if general_website.status_code != 200:
        sys.stderr.write("enable to join the web site")
        return -1
    soup = BeautifulSoup(general_website.text, 'lxml')
    list_leagues_url = config.get_leagues(soup)

    weeks_index = 0
    dict_leagues_info = {}

    for league_url in list_leagues_url:

        comp_id = league_url[config.LEAGUE_URL].split('/')[config.COMP_ID]
        league_url_last_season = league_url[0].rsplit("/", 2)
        league_url[0] = league_url_last_season[0] + "/20182019/" + league_url_last_season[2]
        res_league = requests.get(league_url[config.LEAGUE_URL])

        the_r = res_league.url.split('/')[config.THE_R]

        game_weeks = get_game_weeks(config.LIST_TOTAL_WEEKS_PER_LEAGUE[weeks_index], comp_id, the_r[1:])
        list_game_weeks_info = [get_matches(week) for week in game_weeks]
        dict_leagues_info[league_url[config.LEAGUE_NAME]] = list_game_weeks_info
        weeks_index += 1
    return dict_leagues_info

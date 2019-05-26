"""matches per league"""
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import urllib.request


##########

    # for i in range(38):
    #     data = json.load(urllib.request.urlopen(
    #         'https://us.soccerway.com/a/block_competition_matches_summary?block_id'
    #         '=page_competition_1_block_competition_matches_summary_5&callback_params={"page":"37",'
    #         '"block_service_id":"competition_summary_block_competitionmatchessummary","round_id":"48730",'
    #         '"outgroup":"","view":"1","competition_id":"8"}&action=changePage&params={"page":' + str(i) + '}'))
    #
    #     html = data["commands"][0]["parameters"]["content"]
    #     soup = BeautifulSoup(html, 'lxml')
    #     print(soup.prettify())

#############
WEBSITE = "https://us.soccerway.com"

MATCHES_LEAGUES = ["Premier League", "Bundesliga", "Serie A", "La Liga", "Ligue 1"]
LIST_TOTAL_WEEKS_PER_LEAGUE = [38, 34, 37, 38, 38]


def get_leagues(soup):
    # TODO: delete this function and use the one in teams_information.py after merging
    navbar = soup.find("div", {"id": "navbar"})
    select = navbar.find("select")
    options = select.find_all("option")
    leagues = []
    match_leagues = ["Premier League", "Bundesliga", "Serie A", "La Liga", "Ligue 1"]
    for i in range(len(options)):
        if options[i].text in match_leagues and "russia" not in options[i]["value"]:
            leagues.append(["https://us.soccerway.com" + options[i]["value"], options[i]["value"].split("/")[3]])

    return leagues


def get_game_weeks(weeks, comp_id, the_r):
    list_matches_weeks = []
    for week_mun in range(weeks):
        print(week_mun)
        data = json.load(urllib.request.urlopen(
            'https://us.soccerway.com/a/block_competition_matches_summary?block_id'
            '=page_competition_1_block_competition_matches_summary_5&callback_params={"page":"37",'
            '"block_service_id":"competition_summary_block_competitionmatchessummary","round_id":"' + str(the_r) + '",'
            '"outgroup":"","view":"1","competition_id":"' + str(comp_id) + '"}&action=changePage&params={"page":' + str(week_mun) + '}'))

        print("comp_id" + str(comp_id))
        print("r: " + str(the_r))
        list_matches_weeks.append(BeautifulSoup(data["commands"][0]["parameters"]["content"], "lxml"))

    return list_matches_weeks
    #     data = data.find("table", {"class": "matches"})
    #
    #     data = [get_match_info(tr) for tr in data.tbody.find_all('tr')]
    #
    #     frame = pd.DataFrame(data)
    #
    #
    # return options


def get_matches(game_week):
    """

    :param game_week:
    :return:
    """
    list_matches_weeks = []
    #matches_table = game_week.find("div", {"id": "page_competition_1_block_competition_matches_summary_5-wrapper"})
    for each in game_week:
        list_matches_weeks.append([get_match_info(tr) for tr in each.tbody.find_all('tr')])
    return list_matches_weeks


def get_match_info(tr):
    """
    gets a line (match) and takes the relevant data
    :param tr:
    :return:
    """
    day = tr.find('td', {"class": "day"})
    date = tr.find('td', {"class": "date"})
    team_a = tr.find('td', {"class": "team-a"})
    team_b = tr.find('td', {"class": "team-b"})
    score = tr.find('td', {"class": "score"})

    return [day.text.strip(), date.text.strip(), team_a.text.strip(), team_b.text.strip(), score.text.strip()]


def get_all_matches_in_all_leagues():
    leagues_info = []
    general_website = requests.get(WEBSITE)
    if general_website.status_code != 200:
        sys.stderr.write("enable to join the web site")
        return -1
    soup = BeautifulSoup(general_website.text, 'lxml')
    list_leagues_url = get_leagues(soup)

    weeks_index = 0
    dict_leagues_info = {}

    for league_url in list_leagues_url:

        comp_id = league_url[0].split('/')[-2]
        res_league = requests.get(league_url[0])

        the_r = res_league.url.split('/')[-2]
        #soup = BeautifulSoup(res_league.text, 'lxml')

        game_weeks = get_game_weeks(LIST_TOTAL_WEEKS_PER_LEAGUE[weeks_index], comp_id, the_r[1:])
        list_game_weeks_info = [get_matches(week) for week in game_weeks]
        dict_leagues_info[league_url[1]] = list_game_weeks_info
        #leagues_info.append(game_weeks_info)
        weeks_index += 1
    dt = pd.DataFrame(leagues_info)
    return dt


def main():
    get_all_matches_in_all_leagues()


if __name__ == '__main__':
    main()

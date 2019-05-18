"""premier league matches"""
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd

LEAGUES = ["Premier League", "UEFA Champions League", "League Cup", "Bundesliga",
           "Super Cup", "Serie A", "La Liga", "Ligue 1", "Coupe de France"]
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
            url_league.append("https://us.soccerway.com" + options[i]["value"])
    return url_league


def get_game_weeks(league):
    """
    gets a league in returns a list with all the game weeks (by url? because here its not urls. maybe not like this)
    :param league:
    :return:
    """
    # TODO: how to navigate between game weeks and what to return for the input of get_matches
    navbar = league.find("div", {"id": "page_competition_1_block_competition_matches_summary_5-wrapper"})
    pagedropdown = navbar.find("div", {"class": "page-dropdown-container"})
    select = navbar.find("select")
    options = select.find_all("option")

    return options


def get_matches(game_week):
    """

    :param game_week:
    :return:
    """
    matches_table = game_week.find("div", {"id": "page_competition_1_block_competition_matches_summary_5-wrapper"})
    return [get_match_info(tr) for tr in matches_table.tbody.find_all('tr')]


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
    print(team_a.text.strip() + " " + score.text.strip() + " " + team_b.text.strip())
    return [day, date, team_a, team_b, score]


def get_all_matches_in_all_leagues():
    leagues_info = []
    general_website = requests.get(WEBSITE)
    if general_website.status_code != 200:
        sys.stderr.write("enable to join the web site")
        return -1
    soup = BeautifulSoup(general_website.text, 'lxml')
    list_leagues_url = get_leagues(soup)

    for league_url in list_leagues_url:
        res_league = requests.get(league_url)
        soup = BeautifulSoup(res_league.text, 'lxml')
        game_weeks = get_game_weeks(soup)
        game_weeks_info = [get_matches(week) for week in game_weeks]
        leagues_info.append(game_weeks_info)
    dt = pd.DataFrame(leagues_info)
    return dt


def main():
    get_all_matches_in_all_leagues()


if __name__ == '__main__':
    main()

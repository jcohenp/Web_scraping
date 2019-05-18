"""premier league matches"""
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd

LEAGUES = ["Premier League", "UEFA Champions League", "League Cup", "Bundesliga",
           "Super Cup", "Serie A", "La Liga", "Ligue 1", "Coupe de France"]


def get_game_weeks(league):
    pass


def get_matches(game_week):
    pass


def get_match_info(match):
    pass


def main():
    leagues_info = {}
    for league in LEAGUES:
        game_weeks = get_game_weeks(league)
        game_weeks_info = []
        for week in game_weeks:
            matches = get_matches(week)
            for match in matches:
                matches_info = get_match_info(match)
            game_weeks_info.append(matches_info)
        leagues_info.append(game_weeks_info)
    dt = pd.DataFrame(leagues_info)



def premier_league_matches():
    matches = []
    response = requests.get(
        'https://us.soccerway.com/national/england/premier-league/20182019/regular-season/r48730/?ICID=SN_01_01')
    if response.status_code != 200:
        sys.stderr.write("enable to join the web site")
        return 1

    soup = BeautifulSoup(response.text, 'html.parser')
    matches_table = soup.find("div", {"id": "page_competition_1_block_competition_matches_summary_5-wrapper"})

    for tr in matches_table.tbody.find_all('tr'):
        date = tr.find('td', {"class": "date"})
        team_a = tr.find('td', {"class": "team-a"})
        score = tr.find('td', {"class": "score"})
        team_b = tr.find('td', {"class": "team-b"})
        # matches = matches.append()
        print(team_a.text.strip() + " " + score.text.strip() + " " + team_b.text.strip())


def main():
    premier_league_matches()


if __name__ == '__main__':
    main()

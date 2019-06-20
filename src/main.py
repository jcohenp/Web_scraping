from top_leagues_matches import get_all_matches_in_all_leagues
from players_ranks import get_all_top_players_info
from teams_informations import parsing_teams_info

import sys
import argparse

OPTIONS = ('top_players', 'teams', 'matches', 'all_tables')


def top_players():
    """returns the dataframe of top players"""
    top_players_info = get_all_top_players_info()
    top_players_info.to_csv("../CSV/top_player_info.csv", index=False, sep=',', encoding='utf-8')
    return top_players_info


def teams():
    """return the dataframe of all teams"""
    teams_information, trophies = parsing_teams_info(True)
    teams_information.fillna("Null").to_csv("../CSV/teams_information.csv", index=False, sep=',', encoding='utf-8')
    trophies.to_csv("../CSV/trophies.csv",  index=False, sep=',', encoding='utf-8')
    return teams_information, trophies


def matches():
    """returns the result of number1*number2"""
    matches_info = get_all_matches_in_all_leagues()
    matches_info.to_csv("../CSV/matches_info.csv", index=False, sep=',', encoding='utf-8')
    return matches_info


def all_tables():
    """returns all the tables"""
    top_players_info = top_players()
    teams_information, trophies = teams()
    matches_info = matches()

    top_players_info.to_csv("../CSV/top_player_info.csv", index=False, sep=',', encoding='utf-8')
    teams_information.fillna("Null").to_csv("../CSV/teams_information.csv", index=False, sep=',', encoding='utf-8')
    trophies.to_csv("../CSV/trophies.csv", index=False, sep=',', encoding='utf-8')
    matches_info.to_csv("../CSV/matches_info.csv", index=False, sep=',', encoding='utf-8')

    return top_players_info, teams_information, trophies, matches_info


if __name__ == "__main__":
    """The main function - parses arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=str,
                        help="The command to use",
                        choices=OPTIONS)
    args = parser.parse_args()

    try:
        print(locals()[args.table]())
    except ValueError:
        print("only one of the options!")
        sys.exit()



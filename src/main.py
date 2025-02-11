from top_leagues_matches import get_all_matches_in_all_leagues
from players_ranks import get_all_top_players_info
from teams_informations import parsing_teams_info
from request_football_data_api import request_football_data_api

import sys
import argparse
import os

OPTIONS = ['top_players', 'teams', 'matches', 'all_tables']


def top_players():
    """returns the dataframe of top players"""
    top_players_info = get_all_top_players_info()
    top_players_info.to_csv("../CSV/top_player_info.csv", index=False, sep=',', encoding='utf-8')
    print("Done for top_players")
    return top_players_info


def teams():
    """return the dataframe of all teams"""
    teams_information, trophies = parsing_teams_info(True)
    teams_information.fillna("Null").to_csv("../CSV/teams_information.csv", index=False, sep=',', encoding='utf-8')
    trophies.to_csv("../CSV/trophies.csv",  index=False, sep=',', encoding='utf-8')
    print("Done for teams")
    return teams_information, trophies


def matches():
    """returns the result of number1*number2"""
    matches_info = get_all_matches_in_all_leagues()
    matches_info.to_csv("../CSV/matches_info.csv", index=False, sep=',', encoding='utf-8')
    print("Done for matches")
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

    if not os.path.exists("../CSV"):
        os.mkdir("../CSV")

    parser = argparse.ArgumentParser(description='Pick what you want to scrap')
    parser.add_argument("--table", type=str, help="The command to use",
                        choices=OPTIONS, default="all_tables")
    args = parser.parse_args()
    print(args)
    # if args.table != "matches":
    #     request_football_data_api("../CSV/players_info_from_api.csv")

    try:
        locals()[args.table]()
    except ValueError:
        print("only one of the options!")
        sys.exit()



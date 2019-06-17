from top_leagues_matches import get_all_matches_in_all_leagues
from players_ranks import get_all_top_players_info
from teams_informations import parsing_teams_info
import pandas as pd
import click
import sys
import argparse

OPTIONS = ('top_players', 'teams', 'matches', 'all_tables')


def top_players():
    """returns the dataframe of top players"""
    top_players_info = get_all_top_players_info()
    return top_players_info


def teams():
    """return the dataframe of all teams"""
    countries_teams = parsing_teams_info()
    return countries_teams


def matches():
    """returns the result of number1*number2"""
    matches_info = get_all_matches_in_all_leagues()
    return matches_info


def all_tables():
    """returns all the tables"""
    top_players_info = top_players()
    countries_teams = teams()
    matches_info = matches()
    return top_players_info, countries_teams, matches_info


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



from top_leagues_matches import get_all_matches_in_all_leagues
from players_ranks import get_all_top_players_info
from teams_informations import parsing_teams_info
import pandas as pd


def main():
    #df_teams_information, df_trophies_informations = parsing_teams_info()
    #print(df_teams_information)

    #top_players_info = get_all_top_players_info()
    #print(top_players_info)

    get_all_matches = get_all_matches_in_all_leagues()
    print(get_all_matches)


if __name__ == '__main__':
    main()

from teams_informations import teams_informations as teams_info
from players_ranks import players_ranks
from top_leagues_matches import top_leagues_matches


def main():
    countries_teams = teams_info.parsing_teams_info()
    print(countries_teams)

    top_players_info = players_ranks.get_all_top_players_info()
    print(top_players_info)

    get_all_matches = top_leagues_matches.get_all_matches_in_all_leagues()
    print(get_all_matches)

    #df = pd.DataFrame(data=countries_teams)
    #print(df)


if __name__ == '__main__':
    main()
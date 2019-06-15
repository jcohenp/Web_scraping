from Web_scraping.src.top_leagues_matches.top_leagues_matches import get_all_matches_in_all_leagues
from Web_scraping.src.players_ranks.players_ranks import get_all_top_players_info
from Web_scraping.src.teams_informations.teams_informations import parsing_teams_info


def main():
    countries_teams = parsing_teams_info()
    print(countries_teams)

    top_players_info = get_all_top_players_info()
    print(top_players_info)

    get_all_matches = get_all_matches_in_all_leagues()
    print(get_all_matches)


if __name__ == '__main__':
    main()

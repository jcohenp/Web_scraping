"""the teams_informations.py file get all basics informations on each team:
    - Team summary
    - Venue details
    - Trophies won"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import config


def get_team_in_rank_table(soup):
    """On each league we have a team rank. This function get all team name and team link
        :param soup => parsing html
        :returns list teams name, teams link"""
    teams_name = []
    teams_link = []
    rank_table = soup.find("div", {"id": "page_competition_1_block_competition_tables_7-wrapper"})
    for tr in rank_table.tbody.find_all('tr'):
        # get td
        td = tr.find('td', {"class": "team"})
        a = td.find("a")
        team_name = a['title']
        teams_name.append(team_name)
        teams_link.append(td.find("a")['href'])

    return teams_name, teams_link


def get_team_info(soup):
    """On each team page you have a section info, this function get all basics informations and return it as a dict
      :param soup => parsing html
      :returns info_section dict"""

    info = soup.find("div", {"class": "first-element"})
    dict_info = {}
    dl = info.find("dl")
    list_dt = dl.find_all("dt")
    list_dd = dl.find_all("dd")
    match_elem = ["Founded", "Address", "E-mail"]
    dict_address = {}
    for i in range(len(list_dt)):
        if list_dt[i].text.strip() in match_elem:
            if list_dt[i].text == "Address":
                address = list_dd[i].text.strip().split("\n")
                dict_address["Street"] = address[0].strip()
                dict_address["District"] = address[1].strip()
                dict_address["City"] = address[2].strip()
                dict_info[list_dt[i].text.strip()] = dict_address
            else:
                dict_info[list_dt[i].text.strip()] = list_dd[i].text.strip()

    return {"Info": dict_info}


def get_team_venues_info(soup):
    """On each team page you have a section Venues, this function get all basics informations and return it as a dict
      :param soup => parsing html
      :returns Venues dict"""
    venues = soup.find("div", {"class": "second-element"})
    dict_venue = {}
    dl = venues.find("dl")
    list_dt = dl.find_all("dt")
    list_dd = dl.find_all("dd")
    for i in range(len(list_dt)):
        dict_venue[list_dt[i].text.strip()] = list_dd[i].text.strip()

    return {"Venue": dict_venue}


def get_team_trophies(soup):
    """On each team page we have a trophies table and we can get all team's trophies
          :param soup => parsing html
          :return Trophies dict"""
    dict_trophies_by_league = {}

    trophies_table = soup.find("table", {"class": "table trophies"})
    if trophies_table:
        for tr in trophies_table.find_all("tr"):
            list_trophies_by_league = []
            if tr.find_all("td"):
                for td in tr.find_all("td"):
                    list_trophies_by_league.append(td.text)
                if list_trophies_by_league[0] in config.LEAGUES:
                    dict_trophies_by_league[list_trophies_by_league[0]] = list_trophies_by_league[2]

    return {"Trophies": dict_trophies_by_league}


def convert_to_dataframe(countries_teams, bool_data):
    list_team_info = []
    list_trophies_info = []
    team_id = 0
    for country, teams in countries_teams.items():
        for name_team, details_team in teams.items():
            team_info = [team_id, country, name_team]
            for info, info_detail in details_team[0].items():
                if "/" in info_detail.get("Founded"):
                    info_detail["Founded"] = info_detail.get("Founded").split("/")[0]
                team_info.append(info_detail.get("Founded"))
                team_info.append(info_detail["Address"].get("Street") + ", " + info_detail["Address"].get("City"))
                team_info.append(info_detail.get("E-mail"))
            for venue, venue_info in details_team[1].items():
                team_info.append(venue_info.get("Name"))
                team_info.append(venue_info.get("Capacity"))
            list_team_info.append(team_info)
            if bool_data:
                for trophies, trophies_info in details_team[2].items():
                    dict_trophies = {"team_id": team_id}
                    for name_trophie, nb_trophies in trophies_info.items():
                        dict_trophies[name_trophie] = nb_trophies
                    list_trophies_info.append(dict_trophies)
                team_id += 1
    if bool_data:
        return pd.DataFrame(list_team_info, columns=["team_id", "league", "name", "founded", "address", "email",
                                                     "venue_name", "venue_capacity"]), \
               pd.DataFrame(list_trophies_info).fillna(0)

    return pd.DataFrame(list_team_info,
                        columns=["team_id", "league", "name", "founded", "address", "email", "venue_name",
                                 "venue_capacity"])


def parsing_teams_info(bool_data):
    """This function is the general function for getting all basics informations
       :return a dict countries teams representing all teams summary sort by country"""
    countries_teams = {}
    general_website = requests.get("https://us.soccerway.com")
    soup = BeautifulSoup(general_website.text, 'lxml')
    list_leagues_url = config.get_leagues(soup)
    for league_url in list_leagues_url:
        league_url_last_season = league_url[0].rsplit("/", 2)
        league_url[0] = league_url_last_season[0] + "/20182019/" + league_url_last_season[2]
        teams_informations = {}
        res_league = requests.get(league_url[config.LEAGUE_URL])
        soup = BeautifulSoup(res_league.text, 'lxml')
        teams_name, teams_links = get_team_in_rank_table(soup)

        current_team = 0
        for team_link in teams_links:
            # new request
            request_team = requests.get("https://us.soccerway.com/" + team_link)

            soup = BeautifulSoup(request_team.text, 'lxml')
            info_section = get_team_info(soup)
            venues_section = get_team_venues_info(soup)
            trophies_section = get_team_trophies(soup)
            teams_informations[teams_name[current_team]] = [info_section, venues_section, trophies_section]
            countries_teams[league_url[1]] = teams_informations

            current_team += 1

    return convert_to_dataframe(countries_teams, bool_data)

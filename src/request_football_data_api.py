import http.client
import json
import time
import csv
import config as config


def request_football_data_api(csv_path):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'dc1670317fef4c13b41bc8e3d0ce1e8f'}
    players_info = []
    api_url = '/v2/competitions/code/teams?season=2018'
    for code in config.LEAGUE_CODE:
        new_api_url = api_url.replace("code", code)
        connection.request('GET', new_api_url, None, headers)
        league = json.loads(connection.getresponse().read().decode())

        for i, teams in enumerate(league["teams"]):

            id = teams["id"]
            connection.request('GET', '/v2/teams/' + str(id), None, headers)
            if i % 8 == 0 and i != 0:
                time.sleep(60)
            team = json.loads(connection.getresponse().read().decode())
            name = team["name"]
            short_name = team["shortName"]
            for players in team["squad"]:
                dict_player = {"id": players["id"], "name": players["name"], "position": players["position"],
                               "nationality": players["nationality"],
                               "role": players["role"] if players["role"] == "PLAYER" else None, "team_name": name, "short_team_name": short_name}
                players_info.append(dict_player)
        print("DONE for " + code)
        time.sleep(60)
    keys = players_info[0].keys()
    with open(csv_path, 'w', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(players_info)

#request_football_data_api("../CSV/players_info_from_api_new.csv")

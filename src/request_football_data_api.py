import http.client
import json

connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': 'dc1670317fef4c13b41bc8e3d0ce1e8f'}
connection.request('GET', '/v2/competitions/FL1/teams?season=2018', None, headers)
league = json.loads(connection.getresponse().read().decode())
for teams in league["teams"]:
    id = teams["id"]
    connection.request('GET', '/v2/teams/' + str(id), None, headers)
    team = json.loads(connection.getresponse().read().decode())
    name = team["name"]
    short_name = team["shortName"]
    squad = team["squad"]
    print("toto")
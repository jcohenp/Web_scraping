import csv
import pymysql
import os

def get_sql_from_file(filename):
    """
    Get the SQL instruction from a file

    :return: a list of each SQL query whithout the trailing ";"
    """
    with open(filename, "r") as sql_file:
        # Split file in list
        ret = sql_file.read().split(';')
        # drop last empty entry
        ret.pop()
        return ret


request_list = get_sql_from_file("sql/soccerway.sql")
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root')
cur = conn.cursor()
try:
    cur.execute("CREATE database soccerway;")
except pymysql.err.ProgrammingError:
    cur.execute("DROP database soccerway;")
    cur.execute("CREATE database soccerway;")
finally:
    cur.execute("USE soccerway;")

for request in request_list:
    cur.execute(request)
cur.close()

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', database='soccerway', charset='utf8')
cur = conn.cursor()

if os.path.isfile("CSV/teams_information.csv"):
    with open("CSV/teams_information.csv", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            values = [row["team_id"], row["league"], row["name"], row["founded"], row["address"], row["email"], row["venue_name"], row["venue_capacity"]]
            cur.execute("INSERT INTO teams_informations (team_id, league, name, founded, address, email, venue_name, venue_capacity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", values)
    conn.commit()

if os.path.isfile("CSV/trophies.csv"):
    with open("CSV/trophies.csv", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            cur.execute("select team_id from teams_informations where team_id = \"" + row["team_id"] + "\";")
            team_id = cur.fetchall()

            championships = int(row["Premier League"]) + int(row["Bundesliga"]) + int(row["Serie A"]) + int(row["La Liga"]) + int(row["Ligue 1"])
            cups = int(row["League Cup"]) + int(row["Super Cup"]) + int(row["Coupe de France"])
            UEFA_Champions_League = row["UEFA Champions League"]

            values = [team_id, championships, cups, UEFA_Champions_League]
            cur.execute("INSERT INTO trophies (team_id, championships, cups, UEFA_Champions_League) VALUES "
                        "(%s, %s, %s, %s)", values)
    conn.commit()

if os.path.isfile("CSV/matches_info.csv"):
    with open("CSV/matches_info.csv", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        id_match = 1
        for row in reader:
            cur.execute("select team_id from teams_informations where name = \"" + row["team_a"] + "\";")
            team_a_id = cur.fetchall()

            cur.execute("select team_id from teams_informations where name = \"" + row["team_b"] + "\";")
            team_b_id = cur.fetchall()
            values = [id_match, row["day"], row["date"], team_a_id, team_b_id, row["score"]]

            cur.execute("INSERT INTO matches (id_match, day, date_match, team_a_id, team_b_id, score) VALUES (%s, %s, %s, "
                        "%s, %s, %s)", values)
            id_match += 1
    conn.commit()

if os.path.isfile("CSV/top_player_info.csv"):
    with open("CSV/top_player_info.csv", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute("select team_id from teams_informations where name = \"" + row["team"] + "\";")
            team = cur.fetchall()

            values = [row["player_id"], row["name"], team[0][0], row["goals"], row["first_goals"]]
            cur.execute("INSERT INTO top_players (id_player, name, team_id, goals, first_goals) VALUES (%s, %s, %s, "
                        "%s, %s)", values)
    conn.commit()

if os.path.isfile("CSV/players_info_from_api_new.csv"):
    cur.execute("select max(id_player) from top_players;")
    number_player = cur.fetchall()[0][0] + 1
    cur.execute("select max(team_id) from teams_informations;")
    team_number = cur.fetchall()[0][0] + 1
    count = 0

    with open("CSV/players_info_from_api_new.csv", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if row["role"] == "PLAYER":
                cur.execute('SELECT team_id from teams_informations WHERE name = "' + row["team_name"] + '" or name = "' + row["short_team_name"] + '";')
                team_id = cur.fetchall()
                if len(team_id) == 0 :
                    cur.execute('SELECT team_id from teams_informations where name LIKE "%' + row["short_team_name"] + '%";')
                    team_id = cur.fetchall()
                    if len(team_id) == 0:
                        cur.execute('SELECT team_id from teams_informations WHERE "' + row["team_name"] + '" LIKE CONCAT("%", name, "%");')
                        team_id = cur.fetchall()
                        if len(team_id) == 0:
                            team_id = team_number + i

                if "-" in row["name"]:
                    row["name"] = row["name"].replace("-", " ")

                cur.execute('SELECT id_player from top_players where name = "' + row["name"] + '";')
                player_id = cur.fetchall()

                if len(player_id) == 0:
                    cur.execute('SELECT id_player from top_players where name LIKE "%' + row["name"] + '%";')
                    player_id = cur.fetchall()
                    if len(player_id) == 0:
                        player_id = number_player + i
                if type(player_id) != int:
                    player_id = player_id[0][0]
                print(player_id)
            values = [player_id, team_id, row["name"], row["position"], row["nationality"]]
            cur.execute("INSERT INTO players_from_api (id_player, team_id, player_name, player_position, nationality) "
                        "VALUES (%s, %s, %s, %s, %s)", values)
    conn.commit()


cur.close()

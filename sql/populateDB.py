import csv
import pymysql


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

with open("CSV/teams_information.csv", encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        values = [row["team_id"], row["league"], row["name"], row["founded"], row["address"], row["email"], row["venue_name"], row["venue_capacity"]]
        cur.execute("INSERT INTO teams_informations (team_id, league, name, founded, address, email, venue_name, venue_capacity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", values)
conn.commit()


with open("CSV/trophies.csv", encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("select team_id from teams_informations where team_id = \"" + row["team_id"] + "\";")
        team_id = cur.fetchall()
        values = [team_id, row["Premier League"], row["League Cup"], row["UEFA Champions League"],
                  row["Bundesliga"], row["Super Cup"], row["Serie A"], row["La Liga"], row["Ligue 1"],
                  row["Coupe de France"]]
        cur.execute("INSERT INTO trophies (team_id, Premier_League, League_Cup, UEFA_Champions_League, Bundesliga, "
                    "Super_Cup, Serie_A, La_Liga, Ligue_1, Coupe_de_France) VALUES "
                    "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)
conn.commit()


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

with open("CSV/top_player_info.csv", encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("select team_id from teams_informations where name = \"" + row["team"] + "\";")
        team = cur.fetchall()

        values = [row["player_id"], row["name"], team[0][0], row["goals"], row["first_goals"]]
        cur.execute("INSERT INTO top_players (id_player, name, team_id, goals, first_goals) VALUES (%s, %s, %s, %s, %s)", values)
conn.commit()
cur.close()


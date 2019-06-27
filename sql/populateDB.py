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
    cur.execute(request + ';')
cur.close()

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', database='soccerway', charset='utf8')
cur = conn.cursor()

with open("CSV/teams_information.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        values = [row["team_id"], row["league"], row["name"], row["founded"], row["address"], row["email"], row["venue_name"], row["venue_capacity"]]
        cur.execute("INSERT INTO teams_informations (team_id, league, name, founded, address, email, venue_name, venue_capacity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", values)
conn.commit()


with open("CSV/matches_info.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row["team_a"])
        cur.execute("select team_id from teams_informations where name = \"" + row["team_a"] + "\";")
        team_a_id = cur.fetchall()
        print(team_a_id[0][0])


        print(row["team_b"])
        cur.execute("select team_id from teams_informations where name = \"" + row["team_b"] + "\";")
        team_b_id = cur.fetchall()
        print(team_b_id[0][0])
        values = [row["day"], row["date"], team_a_id, team_b_id, row["score"]]

        cur.execute("INSERT INTO matches (day, date_match, team_a_id, team_b_id, score) VALUES (%s, %s, %s, %s, %s)", values)
conn.commit()

with open("CSV/top_player_info.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
        cur.execute("select team_id from teams_informations where name = \"" + row["team"] + "\";")
        team = cur.fetchall()
        print(team[0][0])

        values = [row["player_id"], row["name"], team[0][0], row["goals"], row["first_goals"]]
        print(values)
        cur.execute("INSERT INTO top_players (id_player, name, team_id, goals, first_goals) VALUES (%s, %s, %s, %s, %s)", values)
conn.commit()
cur.close()


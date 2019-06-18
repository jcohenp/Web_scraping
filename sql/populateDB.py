import csv
import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='soccerway', charset='utf8')
cur = conn.cursor()

with open("CSV/teams_information.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        values = [row["team_id"], row["league"], row["name"], row["founded"], row["address"], row["email"], row["venue_name"], row["venue_capacity"]]
        cur.execute("INSERT INTO teams_informations (team_id, league, name, founded, address, email, venue_name, venue_capacity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", values)
conn.commit()
cur.close()
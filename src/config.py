"""Configuration file with all the details regarding the web_scraping project"""

# [Vars]
WEBSITE = "https://us.soccerway.com"
LEAGUE_NAME = 1
LEAGUE_URL = 0
LEAGUES = ["Premier League", "UEFA Champions League", "League Cup", "Bundesliga",
           "Super Cup", "Serie A", "La Liga", "Ligue 1", "Coupe de France"]
MATCHES_LEAGUES = ["Premier League", "Bundesliga", "Serie A", "La Liga", "Ligue 1"]
LIST_TOTAL_WEEKS_PER_LEAGUE = [38, 34, 37, 38, 38]
COMP_ID = -2
THE_R = -2
LEAGUE_CODE = ["BL1", "PL", "FL1", "SA", "PD"]


# [functions]
def get_leagues(soup):
    navbar = soup.find("div", {"id": "navbar"})
    select = navbar.find("select")
    options = select.find_all("option")
    url_league = []
    for i, opt in enumerate(options):
        if options[i].text in MATCHES_LEAGUES and "russia" not in options[i]["value"]:
            url_league.append(["https://us.soccerway.com" + options[i]["value"], options[i].text])
    return url_league




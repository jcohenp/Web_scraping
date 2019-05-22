from teams_informations import teams_informations as teams_info
import pandas as pd


def main():
    countries_teams = teams_info.parsing_teams_info()
    df = pd.DataFrame(data=countries_teams)
    print(df)


if __name__ == '__main__':
    main()
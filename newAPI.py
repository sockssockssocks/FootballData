import http.client
import json
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from sqlite3 import Error
from datetime import date
from sklearn.linear_model import LinearRegression

api_connection = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "a13ddeb302mshaee1a7a8c397b20p1bbe68jsn30ba472b672e"
}


# Makes call to find all current seasons in the UK.
def current_premier_league_season():
    api_connection.request("GET", "/v2/leagues/current/England", headers=headers)
    response = json.loads(api_connection.getresponse().read().decode())

    list_of_leagues = []

    for i, values in enumerate(response.get("api").get("leagues")):
        league_id = response.get("api").get("leagues")[i].get("league_id")
        league_name = response.get("api").get("leagues")[i].get("name")
        season_start = response.get("api").get("leagues")[i].get("season_start")
        season_end = response.get("api").get("leagues")[i].get("season_end")

        list_of_leagues.append(league_id)
        list_of_leagues.append(league_name)
        list_of_leagues.append(season_start.split("-")[0] + "-" + season_end.split("-")[0])

        if "Premier League" in list_of_leagues:
            return str(list_of_leagues[i])
        else:
            print("Error occurred: Cannot find season code")


# Breaks the JSON request into a list of lists for each player which is returned at the end for this method.
# Line breaks indicate different sections of the JSON.
def request_player_data(team_id, season_id):
    api_connection.request("GET", ("/v2/players/team/" + str(team_id) + "/" + str(season_id)), headers=headers)
    response = json.loads(api_connection.getresponse().read().decode())

    player_data = []
    for i, values in enumerate(response.get("api").get("players")):
        list_to_add = []

        if response.get("api").get("players")[i].get("league") == "Premier League":
            player_id = response.get("api").get("players")[i].get("player_id")
            player_name = response.get("api").get("players")[i].get("player_name")
            player_position = response.get("api").get("players")[i].get("position")
            player_age = response.get("api").get("players")[i].get("age")
            player_birth_date = response.get("api").get("players")[i].get("birth_date")
            player_nationality = response.get("api").get("players")[i].get("nationality")
            player_height = response.get("api").get("players")[i].get("height")
            player_weight = response.get("api").get("players")[i].get("weight")
            team_id = response.get("api").get("players")[i].get("team_id")
            team_name = response.get("api").get("players")[i].get("team_name")
            player_times_captained = response.get("api").get("players")[i].get("captain")

            player_total_shots = response.get("api").get("players")[i].get("shots").get("total")
            player_shot_on_target = response.get("api").get("players")[i].get("shots").get("on")

            player_number_of_goals = response.get("api").get("players")[i].get("goals").get("total")
            player_number_of_assists = response.get("api").get("players")[i].get("goals").get("assists")

            player_number_of_passes = response.get("api").get("players")[i].get("passes").get("total")
            player_number_of_key_passes = response.get("api").get("players")[i].get("passes").get("key")
            player_passing_accuracy = response.get("api").get("players")[i].get("passes").get("accuracy")

            player_total_tackles = response.get("api").get("players")[i].get("tackles").get("total")
            player_total_blocks = response.get("api").get("players")[i].get("tackles").get("blocks")
            player_total_interceptions = response.get("api").get("players")[i].get("tackles").get("interceptions")

            player_total_duels = response.get("api").get("players")[i].get("duels").get("total")
            player_duels_won = response.get("api").get("players")[i].get("duels").get("won")

            player_dribble_attempts = response.get("api").get("players")[i].get("dribbles").get("attempts")
            player_dribble_success = response.get("api").get("players")[i].get("dribbles").get("success")

            player_fouls_drawn = response.get("api").get("players")[i].get("fouls").get("drawn")
            player_fouls_committed = response.get("api").get("players")[i].get("fouls").get("committed")

            player_yellow_cards = response.get("api").get("players")[i].get("cards").get("yellow")
            player_second_yellow_cards = response.get("api").get("players")[i].get("cards").get("yellowred")
            player_red_cards = response.get("api").get("players")[i].get("cards").get("red")

            player_penalties_won = response.get("api").get("players")[i].get("penalty").get("won")
            player_penalties_scored = response.get("api").get("players")[i].get("penalty").get("success")
            player_penalties_missed = response.get("api").get("players")[i].get("penalty").get("missed")
            player_penalties_saved = response.get("api").get("players")[i].get("penalty").get("saved")

            player_appearances = response.get("api").get("players")[i].get("games").get("appearences")
            player_minutes_played = response.get("api").get("players")[i].get("games").get("minutes_played")

            player_substitutions_in = response.get("api").get("players")[i].get("substitutes").get("in")
            player_substitutions_out = response.get("api").get("players")[i].get("substitutes").get("out")
            player_substitutions_bench = response.get("api").get("players")[i].get("substitutes").get("bench")

            list_to_add.append(player_id)
            list_to_add.append(player_name)
            list_to_add.append(player_position)
            list_to_add.append(player_age)
            list_to_add.append(player_birth_date)
            list_to_add.append(player_nationality)
            list_to_add.append(player_height)
            list_to_add.append(player_weight)
            list_to_add.append(team_id)
            list_to_add.append(team_name)
            list_to_add.append(player_times_captained)

            list_to_add.append(player_appearances)
            list_to_add.append(player_minutes_played)

            list_to_add.append(player_number_of_goals)
            list_to_add.append(player_number_of_assists)

            list_to_add.append(player_number_of_passes)
            list_to_add.append(player_number_of_key_passes)
            list_to_add.append(player_passing_accuracy)

            list_to_add.append(player_total_tackles)
            list_to_add.append(player_total_blocks)
            list_to_add.append(player_total_interceptions)

            list_to_add.append(player_total_duels)
            list_to_add.append(player_duels_won)

            list_to_add.append(player_dribble_attempts)
            list_to_add.append(player_dribble_success)

            list_to_add.append(player_fouls_drawn)
            list_to_add.append(player_fouls_committed)

            list_to_add.append(player_yellow_cards)
            list_to_add.append(player_second_yellow_cards)
            list_to_add.append(player_red_cards)

            list_to_add.append(player_total_shots)
            list_to_add.append(player_shot_on_target)

            list_to_add.append(player_penalties_won)
            list_to_add.append(player_penalties_scored)
            list_to_add.append(player_penalties_missed)
            list_to_add.append(player_penalties_saved)

            list_to_add.append(player_substitutions_in)
            list_to_add.append(player_substitutions_out)
            list_to_add.append(player_substitutions_bench)

            player_data.append(list_to_add)

    print(player_data)
    return player_data


def request_league_season(league_season_id):
    print("Making league season request.")
    try:
        api_connection.request("GET", ("/v2/teams/league/" + league_season_id), headers=headers)
        response = json.loads(api_connection.getresponse().read().decode())

        current_season_team_data = []
        for i, _ in enumerate(response.get("api").get("teams")):
            team_information = []

            team_id = response.get("api").get("teams")[i].get("team_id")
            team_name = response.get("api").get("teams")[i].get("name")
            team_city = response.get("api").get("teams")[i].get("venue_city")

            team_information.append(team_id)
            team_information.append(team_name)
            team_information.append(team_city)

            current_season_team_data.append(team_information)

        return current_season_team_data

    except http.client.CannotSendRequest:
        print("Error: Cannot send request.")
    except http.client.NotConnected:
        print("Error: Not connected.")
    except http.client.RemoteDisconnected:
        print("Error: Disconnected part way through the request.")
    except http.client.ImproperConnectionState:
        print("Error: Current status of connection will not allow successful request.")


# Returns the names of all tables in database
def get_table_names(database_connection):
    table_names = str(select_from_table(database_connection, "SELECT name FROM sqlite_master WHERE type='table';"))
    return table_names


# Returns today's date in YYYY-MM-DD format.
def get_todays_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")


# Returns the year.
def get_current_year():
    year = date.today().year
    return year


# Creates database if one does not exist. Returns the connection to be used when writing to database.
def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print("SQLite version:", sqlite3.version)
    except Error as e:
        print(e)

    return connection


# Closes the passed connection.
def close_connection(connection):
    if connection:
        connection.close()
        return print("Connection closed.")


# Inserts parsed data in the table.
def insert_into_table(connection, table_name, data):
    # Creates the questions marks and commas used next to VALUES.
    values_populator = []
    for _ in enumerate(data[0]):
        values_populator.append("?")
        values_populator.append(",")
    values_populator.pop()

    question_marks = ""
    for ele in values_populator:
        question_marks += ele

    execute_string = "INSERT INTO " + table_name + " VALUES (" + question_marks + ");"

    try:
        c = connection.cursor()
        c.executemany(execute_string, data)
        connection.commit()
    except Error as e:
        print(e)


# Should I change this from select_from_table to query_table?
def select_from_table(connection, select_command):
    try:
        c = connection.cursor()
        c.execute(select_command)
        data = c.fetchall()

        # Convert returned Tuple to String.
        formatted_data = [item for t in data for item in t]

        if formatted_data is not None:
            return formatted_data

    except Error as e:
        print(e)


# Creates table if doesn't exist already.
# Needs a better except and to change the print to only show if the table is created.
def create_table(connection, sql_create_table):
    try:
        c = connection.cursor()
        c.execute(sql_create_table)
        print("Table created.")
    except Error as e:
        print(e)


def check_table_empty(data):
    if len(data) == 0:
        return True
    else:
        return False


# If table doesn't exist it will call create_table.
def check_table_exists(database_connection, table_name, sql_creation_command):
    if (table_name + current_premier_league_season()) not in get_table_names(database_connection):
        create_table(database_connection, sql_creation_command)
        print("Table " + table_name + " has been created")
    else:
        print("Table " + table_name + "exists.")


def main():
    database = r"records.db"
    database_connection = create_connection(database)

    if database_connection is None:
        print("Error: Cannot create the database connection.")

    desired_table_list = [("team_ids_" + current_premier_league_season()),
                          ("player_ids_and_names_" + current_premier_league_season())]

    sql_create_team_ids_table = """CREATE TABLE IF NOT EXISTS """ + desired_table_list[0] + """ (
                                        team_id INTEGER,
                                        team_name TEXT,
                                        team_city TEXT,
                                        PRIMARY KEY (team_id)
                                    );"""
    sql_create_player_base_information_table = """CREATE TABLE IF NOT EXISTS """ + desired_table_list[1] + """ (
                                        player_id INTEGER,
                                        player_name TEXT,
                                        team_id TEXT,
                                        PRIMARY KEY (player_id)
                                    );"""

    sql_table_creation_lists = [sql_create_team_ids_table, sql_create_player_base_information_table]

    for index, _ in enumerate(desired_table_list):
        check_table_exists(database_connection, desired_table_list[index], sql_table_creation_lists[index])

    if check_table_empty(select_from_table(database_connection, ("SELECT * FROM " + desired_table_list[0]))):
        team_ids = [[40, 'Liverpool', 'Liverpool'], [71, 'Norwich', 'Norwich, Norfolk'], [48, 'West Ham', 'London'],
                    [50, 'Manchester City', 'Manchester'], [35, 'Bournemouth', 'Bournemouth, Dorset'],
                    [62, 'Sheffield Utd', 'Sheffield'], [44, 'Burnley', 'Burnley'],
                    [41, 'Southampton', 'Southampton, Hampshire'], [52, 'Crystal Palace', 'London'],
                    [45, 'Everton', 'Liverpool'], [46, 'Leicester', 'Leicester, Leicestershire'],
                    [39, 'Wolves', 'Wolverhampton, West Midlands'], [38, 'Watford', 'Watford'],
                    [51, 'Brighton', 'Falmer, East Sussex'], [47, 'Tottenham', 'London'],
                    [66, 'Aston Villa', 'Birmingham'], [34, 'Newcastle', 'Newcastle upon Tyne'],
                    [42, 'Arsenal', 'London'], [33, 'Manchester United', 'Manchester'], [49, 'Chelsea', 'London']]
        # team_ids = request_league_season(current_premier_league_season())
        insert_into_table(database_connection, ("team_ids_" + current_premier_league_season()), team_ids)

    print(current_premier_league_season())

    if check_table_empty(select_from_table(database_connection, ("SELECT * FROM " + desired_table_list[1]))):
        player_data = [[1756, 'R. Kent', 'Attacker', 24, '11/11/1996', 'England', '172 cm', '65 kg', 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [303, 'R. Brewster', 'Attacker', 20, '01/04/2000', 'England', '180 cm', '75 kg', 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [19613, 'O. Ejaria', 'Midfielder', 23, '18/11/1997', 'England', '183 cm', '75 kg', 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [127472, 'N. Phillips', 'Defender', 23, '21/03/1997', 'England', '190 cm', None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [280, 'Alisson', 'Goalkeeper', 28, '02/10/1992', 'Brazil', '193 cm', '91 kg', 40, 'Liverpool', 0, 20, 1735, 0, 1, 475, 1, 84, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0], [18812, 'Adrián', 'Goalkeeper', 33, '03/01/1987', 'Spain', '190 cm', '80 kg', 40, 'Liverpool', 0, 11, 873, 0, 0, 186, 0, 68, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 20], [20224, 'A. Lonergan', 'Goalkeeper', 37, '19/10/1983', 'England', '192 cm', '87 kg', 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [281, 'C. Kelleher', 'Goalkeeper', 22, '23/11/1998', 'Republic of Ireland', '188 cm', None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], [162687, 'V. Jaros', 'Goalkeeper', 19, '23/07/2001', 'Czech Republic', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [138832, 'B. Winterbottom', 'Goalkeeper', 19, '16/07/2001', 'England', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [18862, 'N. Clyne', 'Defender', 29, '05/04/1991', 'England', '175 cm', '67 kg', 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [290, 'V. van Dijk', 'Defender', 29, '08/07/1991', 'Netherlands', '193 cm', '92 kg', 40, 'Liverpool', 3, 29, 2610, 4, 1, 2203, 7, 87, 19, 11, 30, 0, 0, 3, 2, 21, 10, 1, 0, 0, 23, 11, 0, 0, 0, 0, 0, 0, 0], [287, 'D. Lovren', 'Defender', 31, '05/07/1989', 'Croatia', '188 cm', '84 kg', 40, 'Liverpool', 0, 9, 760, 0, 1, 552, 1, 82, 13, 6, 9, 0, 0, 1, 1, 7, 4, 1, 0, 0, 4, 1, 0, 0, 0, 0, 0, 1, 6], [284, 'J. Gomez', 'Defender', 23, '23/05/1997', 'England', '188 cm', '77 kg', 40, 'Liverpool', 0, 19, 1276, 0, 0, 1127, 4, 85, 16, 4, 25, 0, 0, 6, 5, 9, 13, 3, 0, 0, 1, 0, 0, 0, 0, 0, 5, 0, 14], [289, 'A. Robertson', 'Defender', 26, '11/03/1994', 'Scotland', '178 cm', '64 kg', 40, 'Liverpool', 0, 28, 2445, 1, 7, 1577, 43, 82, 40, 6, 33, 0, 0, 34, 17, 9, 15, 1, 0, 0, 17, 5, 0, 0, 0, 0, 1, 2, 1], [286, 'J. Matip', 'Defender', 29, '08/08/1991', 'Cameroon', '195 cm', '90 kg', 40, 'Liverpool', 0, 8, 630, 1, 0, 405, 1, 82, 8, 4, 11, 0, 0, 2, 2, 5, 7, 0, 0, 0, 3, 1, 0, 0, 0, 0, 1, 0, 8], [285, 'K. Hoever', 'Defender', 18, '18/01/2002', 'Netherlands', '180 cm', None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [36922, 'S. van den Berg', 'Defender', 19, '20/12/2001', 'Netherlands', '189 cm', None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [138780, 'N. Williams', 'Defender', 19, '13/04/2001', 'Wales', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], [138825, 'M. Boyes', 'Defender', 19, '22/04/2001', 'Wales', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [138831, 'T. Clayton', 'Defender', 20, '16/12/2000', 'Scotland', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [97938, 'T. Gallacher', 'Defender', 21, '23/07/1999', 'Scotland', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [152974, 'B. Koumetio', 'Defender', 18, '14/11/2002', 'France', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [138828, 'Y. Larouci', 'Defender', 19, '01/01/2001', 'France', '176 cm', '68 kg', 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [138826, 'A. Lewis', 'Defender', 21, '08/11/1999', 'England', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [152979, 'J. Norris', 'Defender', 17, '04/04/2003', 'England', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [299, 'Fabinho', 'Midfielder', 27, '23/10/1993', 'Brazil', '188 cm', '78 kg', 40, 'Liverpool', 0, 20, 1444, 1, 1, 933, 16, 78, 37, 0, 25, 0, 0, 10, 7, 14, 23, 5, 0, 0, 8, 2, 0, 0, 0, 0, 5, 0, 6], [296, 'J. Milner', 'Midfielder', 34, '04/01/1986', 'England', '175 cm', '70 kg', 40, 'Liverpool', 4, 18, 759, 2, 2, 525, 8, 80, 11, 3, 5, 0, 0, 8, 8, 9, 7, 3, 0, 0, 12, 4, 0, 2, 0, 0, 11, 1, 15], [294, 'N. Keïta', 'Midfielder', 25, '10/02/1995', 'Guinea', '172 cm', '64 kg', 40, 'Liverpool', 0, 9, 368, 1, 1, 279, 8, 90, 16, 0, 6, 0, 0, 14, 11, 8, 3, 1, 0, 0, 7, 5, 0, 0, 0, 0, 5, 3, 14], [292, 'J. Henderson', 'Midfielder', 30, '17/06/1990', 'England', '182 cm', '67 kg', 40, 'Liverpool', 22, 25, 1891, 3, 5, 1315, 26, 80, 50, 2, 24, 0, 0, 26, 15, 10, 26, 1, 0, 0, 15, 6, 0, 0, 0, 0, 3, 8, 4], [295, 'A. Lallana', 'Midfielder', 32, '10/05/1988', 'England', '172 cm', '73 kg', 40, 'Liverpool', 0, 15, 373, 1, 1, 228, 4, 82, 18, 0, 5, 0, 0, 5, 2, 8, 7, 1, 0, 0, 5, 1, 0, 0, 0, 0, 12, 3, 22], [307, 'X. Shaqiri', 'Midfielder', 29, '10/10/1991', 'Switzerland', '169 cm', '72 kg', 40, 'Liverpool', 0, 6, 174, 1, 0, 76, 3, 88, 1, 0, 0, 0, 0, 4, 2, 3, 1, 0, 0, 0, 4, 1, 0, 0, 0, 0, 4, 1, 10], [293, 'C. Jones', 'Midfielder', 19, '30/01/2001', 'England', '185 cm', '75 kg', 40, 'Liverpool', 0, 2, 19, 0, 0, 21, 0, 92, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 8], [19035, 'H. Elliott', 'Midfielder', 17, '04/04/2003', 'England', '170 cm', None, 40, 'Liverpool', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4], [138830, 'J. Bearne', 'Midfielder', 19, '15/09/2001', 'England', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [152975, 'J. Cain', 'Midfielder', 19, '02/09/2001', 'England', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [93671, 'Chirivella', 'Midfielder', 23, '23/05/1997', 'Spain', '178 cm', '66 kg', 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [151754, 'L. Clarkson', 'Midfielder', 19, '19/10/2001', 'England', '175 cm', '62 kg', 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [138829, 'E. Dixon-Bonner', 'Midfielder', 19, '01/01/2001', 'England', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [152976, 'T. Hill', 'Midfielder', 18, '13/10/2002', 'England', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [151755, 'L. Longstaff', 'Midfielder', 19, '24/02/2001', 'England', '168 cm', '60 kg', 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [302, 'Roberto Firmino', 'Attacker', 29, '02/10/1991', 'Brazil', '181 cm', '76 kg', 40, 'Liverpool', 0, 29, 2422, 8, 7, 752, 39, 79, 29, 2, 5, 0, 0, 76, 47, 13, 24, 0, 0, 0, 87, 34, 0, 0, 0, 0, 2, 14, 2], [304, 'S. Mané', 'Attacker', 28, '10/04/1992', 'Senegal', '175 cm', '69 kg', 40, 'Liverpool', 0, 26, 2084, 14, 7, 661, 41, 81, 32, 0, 11, 0, 0, 81, 49, 33, 38, 2, 0, 0, 60, 29, 2, 0, 0, 0, 2, 9, 3], [306, 'Mohamed Salah', 'Attacker', 28, '15/06/1992', 'Egypt', '175 cm', '71 kg', 40, 'Liverpool', 0, 26, 2250, 16, 6, 559, 47, 75, 12, 1, 7, 0, 0, 72, 45, 15, 14, 1, 0, 0, 98, 43, 1, 3, 0, 0, 0, 11, 2], [1101, 'T. Minamino', 'Attacker', 25, '16/01/1995', 'Japan', '174 cm', '68 kg', 40, 'Liverpool', 0, 3, 77, 0, 0, 35, 0, 98, 0, 0, 0, 0, 0, 4, 3, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 8], [196876, 'J. Hardy', 'Attacker', 22, '26/09/1998', 'England', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [152977, 'L. Stewart', 'Attacker', 18, '03/09/2002', 'England', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44798, 'L. Millar', 'Attacker', 21, '27/09/1999', 'Canada', None, None, 40, 'Liverpool', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [305, 'D. Origi', 'Attacker', 25, '18/04/1995', 'Belgium', '185 cm', '75 kg', 40, 'Liverpool', 0, 22, 516, 3, 1, 102, 6, 57, 10, 0, 3, 0, 0, 22, 10, 11, 4, 0, 0, 0, 11, 5, 1, 0, 0, 0, 17, 5, 23], [283, 'T. Alexander-Arnold', 'Defender', 22, '07/10/1998', 'England', '175 cm', '69 kg', 40, 'Liverpool', 0, 29, 2550, 2, 12, 1495, 75, 73, 44, 8, 36, 0, 0, 44, 19, 8, 20, 4, 0, 0, 36, 8, 0, 0, 0, 0, 1, 2, 1], [297, 'A. Oxlade-Chamberlain', 'Midfielder', 27, '15/08/1993', 'England', '180 cm', '70 kg', 40, 'Liverpool', 0, 21, 1108, 3, 0, 443, 14, 81, 13, 1, 17, 0, 0, 39, 21, 11, 11, 1, 0, 0, 31, 8, 0, 0, 0, 0, 8, 13, 12], [300, 'G. Wijnaldum', 'Midfielder', 30, '11/11/1990', 'Netherlands', '175 cm', '69 kg', 40, 'Liverpool', 0, 28, 2332, 3, 0, 1141, 11, 89, 24, 4, 15, 0, 0, 60, 33, 24, 11, 0, 0, 0, 27, 12, 0, 0, 0, 0, 0, 11, 0]]
        # player_data = request_player_data(40, "2019-2020")

    close_connection(database_connection)

    print("Programme complete.")


if __name__ == "__main__":
    main()


'''
Need try excepts

Get more data from request_player_data and make sure that I pass the team_id needed for the call.

API Information:
Premier League ID: 524

team_ids = [[40, 'Liverpool', 'Liverpool'], [71, 'Norwich', 'Norwich, Norfolk'], [48, 'West Ham', 'London'], [50, 'Manchester City', 'Manchester'], [35, 'Bournemouth', 'Bournemouth, Dorset'], [62, 'Sheffield Utd', 'Sheffield'], [44, 'Burnley', 'Burnley'], [41, 'Southampton', 'Southampton, Hampshire'], [52, 'Crystal Palace', 'London'], [45, 'Everton', 'Liverpool'], [46, 'Leicester', 'Leicester, Leicestershire'], [39, 'Wolves', 'Wolverhampton, West Midlands'], [38, 'Watford', 'Watford'], [51, 'Brighton', 'Falmer, East Sussex'], [47, 'Tottenham', 'London'], [66, 'Aston Villa', 'Birmingham'], [34, 'Newcastle', 'Newcastle upon Tyne'], [42, 'Arsenal', 'London'], [33, 'Manchester United', 'Manchester'], [49, 'Chelsea', 'London']]
player_data = [[1756,'R. Kent','Attacker','11/11/1996','England','172 cm','65 kg',40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[303,'R. Brewster','Attacker','01/04/2000','England','180 cm','75 kg',40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[19613,'O. Ejaria','Midfielder','18/11/1997','England','183 cm','75 kg',40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[127472,'N. Phillips','Defender','21/03/1997','England','190 cm',None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[280,'Alisson','Goalkeeper','02/10/1992','Brazil','193 cm','91 kg',40,'Liverpool',20,1735,0,1,475,1,84,0,0,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0],[18812,'Adrián','Goalkeeper','03/01/1987','Spain','190 cm','80 kg',40,'Liverpool',11,873,0,0,186,0,68,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],[20224,'A. Lonergan','Goalkeeper','19/10/1983','England','192 cm','87 kg',40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[281,'C. Kelleher','Goalkeeper','23/11/1998','Republic of Ireland','188 cm',None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[162687,'V. Jaros','Goalkeeper','23/07/2001','Czech Republic',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[138832,'B. Winterbottom','Goalkeeper','16/07/2001','England',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[18862,'N. Clyne','Defender','05/04/1991','England','175 cm','67 kg',40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[290,'V. van Dijk','Defender','08/07/1991','Netherlands','193 cm','92 kg',40,'Liverpool',29,2610,4,1,2203,7,87,19,11,30,0,0,3,2,21,10,1,0,0,23,11,0,0,0,0],[287,'D. Lovren','Defender','05/07/1989','Croatia','188 cm','84 kg',40,'Liverpool',9,760,0,1,552,1,82,13,6,9,0,0,1,1,7,4,1,0,0,4,1,0,0,0,0],[284,'J. Gomez','Defender','23/05/1997','England','188 cm','77 kg',40,'Liverpool',19,1276,0,0,1127,4,85,16,4,25,0,0,6,5,9,13,3,0,0,1,0,0,0,0,0],[289,'A. Robertson','Defender','11/03/1994','Scotland','178 cm','64 kg',40,'Liverpool',28,2445,1,7,1577,43,82,40,6,33,0,0,34,17,9,15,1,0,0,17,5,0,0,0,0],[286,'J. Matip','Defender','08/08/1991','Cameroon','195 cm','90 kg',40,'Liverpool',8,630,1,0,405,1,82,8,4,11,0,0,2,2,5,7,0,0,0,3,1,0,0,0,0],[285,'K. Hoever','Defender','18/01/2002','Netherlands','180 cm',None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[36922,'S. van den Berg','Defender','20/12/2001','Netherlands','189 cm',None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[138780,'N. Williams','Defender','13/04/2001','Wales',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[138825,'M. Boyes','Defender','22/04/2001','Wales',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[138831,'T. Clayton','Defender','16/12/2000','Scotland',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[97938,'T. Gallacher','Defender','23/07/1999','Scotland',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[152974,'B. Koumetio','Defender','14/11/2002','France',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[138828,'Y. Larouci','Defender','01/01/2001','France','176 cm','68 kg',40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[138826,'A. Lewis','Defender','08/11/1999','England',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[152979,'J. Norris','Defender','04/04/2003','England',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[299,'Fabinho','Midfielder','23/10/1993','Brazil','188 cm','78 kg',40,'Liverpool',20,1444,1,1,933,16,78,37,0,25,0,0,10,7,14,23,5,0,0,8,2,0,0,0,0],[296,'J. Milner','Midfielder','04/01/1986','England','175 cm','70 kg',40,'Liverpool',18,759,2,2,525,8,80,11,3,5,0,0,8,8,9,7,3,0,0,12,4,0,2,0,0],[294,'N. Keïta','Midfielder','10/02/1995','Guinea','172 cm','64 kg',40,'Liverpool',9,368,1,1,279,8,90,16,0,6,0,0,14,11,8,3,1,0,0,7,5,0,0,0,0],[292,'J. Henderson','Midfielder','17/06/1990','England','182 cm','67 kg',40,'Liverpool',25,1891,3,5,1315,26,80,50,2,24,0,0,26,15,10,26,1,0,0,15,6,0,0,0,0],[295,'A. Lallana','Midfielder','10/05/1988','England','172 cm','73 kg',40,'Liverpool',15,373,1,1,228,4,82,18,0,5,0,0,5,2,8,7,1,0,0,5,1,0,0,0,0],[307,'X. Shaqiri','Midfielder','10/10/1991','Switzerland','169 cm','72 kg',40,'Liverpool',6,174,1,0,76,3,88,1,0,0,0,0,4,2,3,1,0,0,0,4,1,0,0,0,0],[293,'C. Jones','Midfielder','30/01/2001','England','185 cm','75 kg',40,'Liverpool',2,19,0,0,21,0,92,2,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],[19035,'H. Elliott','Midfielder','04/04/2003','England','170 cm',None,40,'Liverpool',1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[138830,'J. Bearne','Midfielder','15/09/2001','England',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[152975,'J. Cain','Midfielder','02/09/2001','England',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[93671,'Chirivella','Midfielder','23/05/1997','Spain','178 cm','66 kg',40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[151754,'L. Clarkson','Midfielder','19/10/2001','England','175 cm','62 kg',40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[138829,'E. Dixon-Bonner','Midfielder','01/01/2001','England',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[152976,'T. Hill','Midfielder','13/10/2002','England',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[151755,'L. Longstaff','Midfielder','24/02/2001','England','168 cm','60 kg',40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[302,'Roberto Firmino','Attacker','02/10/1991','Brazil','181 cm','76 kg',40,'Liverpool',29,2422,8,7,752,39,79,29,2,5,0,0,76,47,13,24,0,0,0,87,34,0,0,0,0],[304,'S. Mané','Attacker','10/04/1992','Senegal','175 cm','69 kg',40,'Liverpool',26,2084,14,7,661,41,81,32,0,11,0,0,81,49,33,38,2,0,0,60,29,2,0,0,0],[306,'Mohamed Salah','Attacker','15/06/1992','Egypt','175 cm','71 kg',40,'Liverpool',26,2250,16,6,559,47,75,12,1,7,0,0,72,45,15,14,1,0,0,98,43,1,3,0,0],[1101,'T. Minamino','Attacker','16/01/1995','Japan','174 cm','68 kg',40,'Liverpool',3,77,0,0,35,0,98,0,0,0,0,0,4,3,0,3,0,0,0,2,0,0,0,0,0],[196876,'J. Hardy','Attacker','26/09/1998','England',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[152977,'L. Stewart','Attacker','03/09/2002','England',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[44798,'L. Millar','Attacker','27/09/1999','Canada',None,None,40,'Liverpool',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[305,'D. Origi','Attacker','18/04/1995','Belgium','185 cm','75 kg',40,'Liverpool',22,516,3,1,102,6,57,10,0,3,0,0,22,10,11,4,0,0,0,11,5,1,0,0,0],[283,'T. Alexander-Arnold','Defender','07/10/1998','England','175 cm','69 kg',40,'Liverpool',29,2550,2,12,1495,75,73,44,8,36,0,0,44,19,8,20,4,0,0,36,8,0,0,0,0],[297,'A. Oxlade-Chamberlain','Midfielder','15/08/1993','England','180 cm','70 kg',40,'Liverpool',21,1108,3,0,443,14,81,13,1,17,0,0,39,21,11,11,1,0,0,31,8,0,0,0,0],[300,'G. Wijnaldum','Midfielder','11/11/1990','Netherlands','175 cm','69 kg',40,'Liverpool',28,2332,3,0,1141,11,89,24,4,15,0,0,60,33,24,11,0,0,0,27,12,0,0,0,0]]

'''
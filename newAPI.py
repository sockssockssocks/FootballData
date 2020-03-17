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

        list_of_leagues.append(league_id)
        list_of_leagues.append(league_name)

        if "Premier League" in list_of_leagues:
            return str(list_of_leagues[i])
        else:
            print("Error occurred: Cannot find season code")


# Breaks the JSON request into a list of lists for each player which is returned at the end for this method.
# Line breaks indicate different sections of the JSON.
def request_player_data(team_id, season_id):
    api_connection.request("GET", ("/v2/players/player/" + team_id + "/" + season_id), headers=headers)
    response = json.loads(api_connection.getresponse().read().decode())

    player_data = []
    for i, values in enumerate(response.get("api").get("players")):
        list_to_add = []

        player_id = response.get("api").get("players")[i].get("player_id")
        player_name = response.get("api").get("players")[i].get("player_name")
        player_position = response.get("api").get("players")[i].get("position")
        team_id = response.get("api").get("players")[i].get("team_id")
        team_name = response.get("api").get("players")[i].get("team_name")

        player_appearances = response.get("api").get("players")[i].get("games").get("appearances")
        player_minutes_played = response.get("api").get("players")[i].get("games").get("minutes_played")

        player_number_of_goals = response.get("api").get("players")[i].get("goals").get("total")
        player_number_of_assists = response.get("api").get("players")[i].get("goals").get("assists")

        player_total_shots = response.get("api").get("players")[i].get("shots").get("total")
        player_shot_on_target = response.get("api").get("players")[i].get("shots").get("on")

        player_penalties_won = response.get("api").get("players")[i].get("penalty").get("won")
        player_penalties_scored = response.get("api").get("players")[i].get("penalty").get("success")
        player_penalties_missed = response.get("api").get("players")[i].get("penalty").get("missed")
        player_penalties_saved = response.get("api").get("players")[i].get("penalty").get("saved")

        list_to_add.append(player_id)
        list_to_add.append(player_name)
        list_to_add.append(player_position)
        list_to_add.append(team_id)
        list_to_add.append(team_name)

        list_to_add.append(player_appearances)
        list_to_add.append(player_minutes_played)

        list_to_add.append(player_number_of_goals)
        list_to_add.append(player_number_of_assists)

        list_to_add.append(player_total_shots)
        list_to_add.append(player_shot_on_target)

        list_to_add.append(player_penalties_won)
        list_to_add.append(player_penalties_scored)
        list_to_add.append(player_penalties_missed)
        list_to_add.append(player_penalties_saved)

        player_data.append(list_to_add)

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

    if check_table_empty(select_from_table(database_connection, ("SELECT * FROM " + desired_table_list[1]))):
        player_data = request_player_data(int(current_premier_league_season()))
        print(player_data)

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

'''
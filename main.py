import http.client
import json
import sqlite3
from sqlite3 import Error
from datetime import date


# Calls to the API with token. Returns the cherry-picked data to be sent to database.
def make_request(api_token):
    print("Trying to get response.")
    try:
        print("Response received.")
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': api_token}
        connection.request('GET', '/v2/competitions/PL/', None, headers)
        response = json.loads(connection.getresponse().read().decode())

        league_id = response.get("id")
        current_season = response.get("currentSeason").get("id")
        current_matchday = response.get("currentSeason").get("currentMatchday")

        information = {league_id: league_id, current_season: current_season, current_matchday: current_matchday}

        return information

        # connection.request('GET', '/v2/competitions/PL/scorers', None, headers)
        # response = json.loads(connection.getresponse().read().decode())
        # print(response)

    except http.client.CannotSendRequest:
        print("Error: Cannot send request.")
    except http.client.NotConnected:
        print("Error: Not connected.")
    except http.client.RemoteDisconnected:
        print("Error: Disconnected part way through the request.")
    except http.client.ImproperConnectionState:
        print("Error: Current status of connection will not allow successful request.")


# Returns today's date in YYYY-MM-DD format
def get_usable_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")


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


# Creates table if doesn't exist already.
def create_table(connection, sql_create_table):
    try:
        c = connection.cursor()
        c.execute(sql_create_table)
        print("Table created.")
    except Error as e:
        print(e)


# Returns the data of the SELECT command.
def select_from_table(connection, select_command):
    try:
        c = connection.cursor()
        c.execute(select_command)
        data = c.fetchall()

        # Converts the list of tuples returned to a list of integers
        formatted_data = [item for t in data for item in t]
        return formatted_data
    except Error as e:
        print(e)


# Updates the top_scorer with the new total of goals.
def update_top_scorer(connection, update_command):
    print("In update_top_scorer")
    try:
        print("Attempting to execute command:", update_command)
        c = connection.cursor()
        c.execute(update_command)
    except Error as e:
        print(e)


def main():
    database = r"records.db"
    api_token = "c66e3100c2584065b0377dd86280ae81"

    print("Today's date:", get_usable_date())

    database_connection = create_connection(database)

    sql_create_scorer_table = """CREATE TABLE IF NOT EXISTS top_scorer (
                                    player_id integer,
                                    player_name text,
                                    player_club_id integer,
                                    player_club_name text,
                                    number_of_goals integer
                                );"""

    # Not sure if this is needed, why can't I just have the code in the if.
    if database_connection is not None:
        create_table(database_connection, sql_create_scorer_table)
    else:
        print("Error: Cannot create the database connection.")

    # Can probably make this neater. Use lists and for loops?
    # SELECT commands used to get dict of player_id and the corresponding number_of_goals
    sql_goals_scored_player_id = "SELECT player_id FROM top_scorer;"
    sql_goals_scored_player_name = "SELECT player_name FROM top_scorer;"
    sql_goals_scored_number_of_goals = "SELECT number_of_goals FROM top_scorer;"

    player_id = select_from_table(database_connection, sql_goals_scored_player_id)
    player_name = select_from_table(database_connection, sql_goals_scored_player_name)
    number_of_goals = select_from_table(database_connection, sql_goals_scored_number_of_goals)

    # For debugging
    for k in player_id:
        print(player_name[k], " has scored ", number_of_goals[k])

    # Need to call the top_scorer table to get the number_of_goals
    #sql_update_top_scorer_goals_scored = "UPDATE top_scorer SET ", number_of_goals, " = ", number_of_goals, " + ", matchday_goals

    # print("Sending request.")
    # request_received = make_request(api_token)

    # Closes connection as there's no need for it to be open anymore
    close_connection(database_connection)


if __name__ == "__main__":
    main()

'''

Start my own goalscorer tally:
- create a call to the API that gets all matches played on current matchday and return playerIDs and numbers of goals scored.
- will need to check if I need to write to the db in the first place.

https://www.sqlitetutorial.net/sqlite-python/

'''

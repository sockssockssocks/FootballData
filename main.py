import http.client
import json
import sqlite3
from sqlite3 import Error
from datetime import date


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


# Simply closes the passed connection.
def close_connection(connection):
    if connection:
        connection.close()
        return print("Connection closed.")


# Executes SQL command.
def create_table(connection, create_table_sql):
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
        print("Table created.")
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

    if database_connection is not None:
        create_table(database_connection, sql_create_scorer_table)
    else:
        print("Error: Cannot create the database connection.")

    #print("Sending request.")
    #request_received = make_request(api_token)

    close_connection(database_connection)


if __name__ == "__main__":
    main()


'''

Start my own goalscorer tally - need the data from API to do this.

https://www.sqlitetutorial.net/sqlite-python/

'''
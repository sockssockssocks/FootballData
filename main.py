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
        #connection.request('GET', '/v2/competitions/PL/', None, headers)
        #response = json.loads(connection.getresponse().read().decode())

        '''
        league_id = response.get("id")
        current_season = response.get("currentSeason").get("id")
        current_matchday = response.get("currentSeason").get("currentMatchday")
        information = {league_id: league_id, current_season: current_season, current_matchday: current_matchday}
        '''

        # Limited at 200 but this could change.
        connection.request('GET', '/v2/competitions/PL/scorers?limit=200', None, headers)
        response = json.loads(connection.getresponse().read().decode())

        top_scorers = []

        # Iterate through the response and grab the player ID, player name, club ID, club name and number of goals.
        # Creates a lists of lists.
        for i in range(response.get("count")):
            list_to_add = []

            player_id = response.get("scorers")[i].get("player").get("id")
            player_name = response.get("scorers")[i].get("player").get("name")
            team_id = response.get("scorers")[i].get("team").get("id")
            team_name = response.get("scorers")[i].get("team").get("name")
            goals_scored = response.get("scorers")[i].get("numberOfGoals")

            list_to_add.append(player_id)
            list_to_add.append(player_name)
            list_to_add.append(team_id)
            list_to_add.append(team_name)
            list_to_add.append(goals_scored)

            top_scorers.append(list_to_add)

        return top_scorers

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


# Returns data of the SELECT command.
# Converts the list of tuples returned to a list of integers.
def select_from_table(connection, select_command):
    try:
        c = connection.cursor()
        c.execute(select_command)
        data = c.fetchall()

        formatted_data = [item for t in data for item in t]
        return formatted_data
    except Error as e:
        print(e)


# Updates the top_scorer with the new total of goals.
def update_top_scorer(connection, data, player_id, number_of_goals):
    try:
        c = connection.cursor()

        table_rows = c.rowcount
        print("Rows in top_scorer:", table_rows)
        print("Rows in data received:", len(data))

        for i in player_id:
            execute_command = "SELECT player_id, number_of_goals FROM top_scorer WHERE player_id=" + str(i) + ";"
            c.execute(execute_command)
            row_player_id = c.fetchall()
            print(type(row_player_id))
            print(row_player_id)

            if row_player_id[i] ==

        '''if table_rows == len(data):
            for i in data:
                row_player_id = c.execute("SELECT player_id, number_of_goals FROM top_scorer "
                                          "WHERE player_id=", id_and_goals[i][0])
                print(row_player_id)
                #if row_player_id
                #execute_string = "UPDATE top_scorer SET player_id=", data[i][0],\
                                    #"player_name=", data[i][1],\
        '''
        #c.executemany("""UPDATE top_scorer SET player_id=?, player_name=?, player_club_id=?, player_club_name=?,
                            #number_of_goals=? WHERE number_of_goals != """, id_and_goals, """); """, data)
    except Error as e:
        print(e)


# Insert the scorers to the top_scorer database. If data exists it will not
def insert_into_top_scorer(connection, data):
    try:
        c = connection.cursor()
        c.executemany("""INSERT INTO top_scorer VALUES (?,?,?,?,?);""", data)
        connection.commit()
    except Error as e:
        print(e)


def main():
    disclaimer = "Football data provided by the Football-Data.org API"
    print(disclaimer, ". Data:", get_usable_date())

    database = r"records.db"
    api_token = "c66e3100c2584065b0377dd86280ae81"

    database_connection = create_connection(database)

    sql_create_scorer_table = """CREATE TABLE IF NOT EXISTS top_scorer (
                                    player_id integer,
                                    player_name text,
                                    player_club_id integer,
                                    player_club_name text,
                                    number_of_goals integer
                                );"""

    print(select_from_table(database_connection, "SELECT * FROM top_scorer"))

    # Opens connection to the database if one does not exist.
    if database_connection is not None:
        create_table(database_connection, sql_create_scorer_table)
    else:
        print("Error: Cannot create the database connection.")

    # Can probably make this neater. Use lists and for loops?
    # SELECT commands used to get dict of player_id and the corresponding number_of_goals
    sql_goals_scored_player_id = "SELECT player_id FROM top_scorer;"
    sql_goals_scored_player_name = "SELECT player_name FROM top_scorer;"
    sql_goals_scored_number_of_goals = "SELECT number_of_goals FROM top_scorer;"

    # Call to API via function
    print("Sending request.")
    request_received = make_request(api_token)

    # If table is empty, fill with new call. If not empty then update any rows that need updating.
    # Need to check if number of rows in table is less, more or equal to the request received.
    if not select_from_table(database_connection, "SELECT * FROM top_scorer"):
        print("top_scorer is empty")
        insert_into_top_scorer(database_connection, request_received)
    else:
        player_id = select_from_table(database_connection, sql_goals_scored_player_id)
        number_of_goals = select_from_table(database_connection, sql_goals_scored_number_of_goals)

        # Commits the received request to the database
        update_top_scorer(database_connection, request_received, player_id, number_of_goals)

        # Closes connection as there's no need for it to be open anymore
        close_connection(database_connection)


if __name__ == "__main__":
    main()


'''
Start my own goalscorer tally:
- create a call to the API that gets all matches played on current matchday and return playerIDs and numbers of goals scored.
- will need to check if I need to write to the db in the first place.
https://www.sqlitetutorial.net/sqlite-python/
You shouldn't think of what you get as a "JSON object". What you have is a list. The list contains two dicts. The dicts
contain various key/value pairs, all strings. When you do json_object[0], you're asking for the first dict in the list.
When you iterate over that, with for song in json_object[0]:, you iterate over the keys of the dict. Because that's
what you get when you iterate over the dict. If you want to access the value associated with the key in that dict, you
would use, for example, json_object[0][song].
'''
'''
GRAVEYARD:
        # connection.request('GET', '/v2/competitions/PL/matches?timeFrame=n', None, headers)
        # response = json.loads(connection.getresponse().read().decode())
        # Ensures looking at the current season and matchday then looks for home team vs away team scores
        # Integer doesn't behave as expected.
        # Is this even needed? What's the point of it?
        if current_season == response["matches"][10]["season"]["id"] and \
                current_matchday == response["matches"][10]["season"]["currentMatchday"]:
            print("Found current season and matchday:", current_season, "and", current_matchday)
            print("Score:", response["matches"][21]["score"]["fullTime"])
            print(response["matches"][21]["homeTeam"]["name"])
            print(response["matches"][21]["awayTeam"]["name"])
'''

import http.client
import json
import sqlite3
import matplotlib.pyplot as plt
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

        league_id = response.get("name")
        current_season = response.get("currentSeason").get("id")
        current_matchday = response.get("currentSeason").get("currentMatchday")
        last_updated = response.get("lastUpdated")
        information = {league_id: league_id, current_season: current_season, current_matchday: current_matchday}

        # Limited at 500 but this could change.
        connection.request('GET', '/v2/competitions/PL/scorers?limit=500', None, headers)
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
            player_position = response.get("scorers")[i].get("player").get("position")

            list_to_add.append(player_id)
            list_to_add.append(player_name)
            list_to_add.append(team_id)
            list_to_add.append(team_name)
            list_to_add.append(goals_scored)
            list_to_add.append(player_position)

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


# Returns data of the SELECT command. Converts the list of tuples returned to a list of integers.
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

        table_rows = c.execute("SELECT * FROM top_scorer").rowcount
        table_rows = c.fetchall()

        changes_not_needed = 0
        changes_made = 0

        # Iterates through the table, using a SELECT command for each row
        for i, value in enumerate(table_rows):
            execute_command = "SELECT player_id, number_of_goals FROM top_scorer WHERE player_id=" + str(value[0]) + ";"
            c.execute(execute_command)
            row_player_id = [item for t in c.fetchall() for item in t]

            # Reformat this to be neater. I don't think I need to have the else if I work it differently
            # Checks to make sure won't get index out of range error as ifs look at the data received
            if i < len(data):
                # If player_id in the table matches the player_id in the request
                if row_player_id[0] == value[0] in player_id and row_player_id[0] == value[0] in data[i]:
                    # If the number of goals scored in the table matches the request
                    if row_player_id[1] == value[4] in number_of_goals and row_player_id[1] == value[4] in data[i]:
                        changes_not_needed += 1
                    else:
                        execute_command = ("UPDATE top_scorer SET player_id=?, player_name=?, player_club_id=?,"
                                            "player_club_name=?, number_of_goals=?, player_position=? WHERE player_id=" +
                                            str(row_player_id[0]))
                        execute_command = "".join(str(execute_command))
                        c.execute(execute_command, data[i])
                        connection.commit()
                        changes_made += 1

        print("Number of changes made:", changes_made)
    except Error as e:
        print(e)


# Insert the scorers to the top_scorer database. If data exists it will not
def insert_into_top_scorer(connection, data):
    try:
        c = connection.cursor()
        c.executemany("""INSERT INTO top_scorer VALUES (?,?,?,?,?,?);""", data)
        connection.commit()
    except Error as e:
        print(e)


# Idea: Create enum for club ID to primary colour on badge to represent the bar colour
def plot_top_five_scorers(data):
    # Not best way to do this for sure
    players = [data[1], data[7], data[13], data[19], data[25]]
    goals = [data[4], data[10], data[16], data[22], data[28]]
    positions = [data[5], data[11], data[17], data[23], data[29]]

    # Shortens player's full names to just surnames
    for index, names in enumerate(players):
        players[index] = names[names.index(" "):]

    # What does underscore do?
    x_pos = [i for i, _ in enumerate(players)]

    # Generates the colour of bars and the legend.
    colors = []
    legend = []
    for index, position in enumerate(positions):
        if positions[index] == "Attacker":
            colors.append("r")
            if "Red = Attacker" not in legend:
                legend.append("Red = Attacker")
        elif positions[index] == "Midfielder":
            colors.append("b")
            if "Blue = Midfielder" not in legend:
                legend.append("Blue = Midfielder")
        elif positions[index] == "Defender":
            colors.append("g")
            if "Green = Defender" not in legend:
                legend.append("Green = Defender")

    bars = plt.bar(x_pos, goals, align="center", alpha=0.3, color=colors)

    axes = plt.gca()
    axes.set_ylim([0, goals[0] + 6])  # Increase this without .5 showing on the y axis

    plt.ylabel("Goals Scored")
    plt.xlabel("Player Name")
    plt.title("Top Five Goalscorers in Premier League")
    plt.legend(bars, legend)

    plt.xticks(x_pos, players)

    plt.show()


def main():
    print("Football data provided by the Football-Data.org API. Date:", get_usable_date())

    database = r"records.db"
    api_token = "c66e3100c2584065b0377dd86280ae81"

    database_connection = create_connection(database)

    sql_create_scorer_table = """CREATE TABLE IF NOT EXISTS top_scorer (
                                    player_id integer,
                                    player_name text,
                                    player_club_id integer,
                                    player_club_name text,
                                    number_of_goals integer,
                                    player_position text
                                );"""
    sql_select_all = "SELECT * FROM top_scorer"

    # Opens connection to the database if one does not exist.
    if database_connection is not None:
        create_table(database_connection, sql_create_scorer_table)
    else:
        print("Error: Cannot create the database connection.")

    # Call to API via function
    print("Sending request.")
    request_received = make_request(api_token)

    # SELECT commands used to get dict of player_id and the corresponding number_of_goals
    sql_goals_scored_player_id = "SELECT player_id FROM top_scorer;"
    sql_goals_scored_number_of_goals = "SELECT number_of_goals FROM top_scorer;"

    # If table is empty, fill with new call. If not empty then update any rows that need updating
    if not select_from_table(database_connection, sql_select_all):
        print("top_scorer is empty")
        insert_into_top_scorer(database_connection, request_received)
        print("Table created with ", len(request_received), " rows.")
    else:
        player_id = select_from_table(database_connection, sql_goals_scored_player_id)
        number_of_goals = select_from_table(database_connection, sql_goals_scored_number_of_goals)

        # Commits the received request to the database
        update_top_scorer(database_connection, request_received, player_id, number_of_goals)

    plot_top_five_scorers(select_from_table(database_connection, sql_select_all))
    # plot_top_five_scorers(select_from_table(database_connection, "SELECT * FROM top_scorer WHERE player_position='Midfielder'"))
    # plot_top_five_scorers(select_from_table(database_connection, "SELECT * FROM top_scorer WHERE player_position='Defender'"))

    # print(select_from_table(database_connection, "SELECT * FROM top_scorer WHERE player_position='Midfielder'"))

    close_connection(database_connection)


if __name__ == "__main__":
    main()


'''
Start my own goalscorer tally:
- create a call to the API that gets all matches played on current matchday and return playerIDs and numbers of goals scored.
- will need to check if I need to write to the db in the first place.
- add a table per game week so I can see averages etc.

Create a table for each player with over 3 goals to store when they were scored. Can make graphs from that.


'''
'''
GRAVEYARD:

'''
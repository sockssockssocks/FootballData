import http.client
import json
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from sqlite3 import Error
from datetime import date
from sklearn.linear_model import LinearRegression


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

        if not formatted_data:
            return False
        else:
            return formatted_data
    except Error as e:
        print(e)


# Updates the top_scorer with the new total of goals and inserts new scorers.
def update_top_scorer(connection, data):
    try:
        c = connection.cursor()
        player_names_for_rows_created = []
        player_names_for_updates_made = []

        # Loop for length of data retrieved because it will never be shorter than the length of table.
        for i, value in enumerate(data):
            data_i_row_player_id = data[i][0]
            data_i_row_player_id_exists_check = "SELECT * FROM top_scorer WHERE player_id=" + str(data_i_row_player_id)

            data_i_row_select_all = select_from_table(connection, data_i_row_player_id_exists_check)

            # If select_from_table returns False then insert these players into the table
            if not data_i_row_select_all:
                insert_into_top_scorer(connection, data[i])
                player_names_for_rows_created.append(data[i][1])
            else:
                data_i_row_goals_scored = data[i][4]

                if data_i_row_goals_scored != data_i_row_select_all[4]:
                    execute_command = ("UPDATE top_scorer SET player_id=?, player_name=?, player_club_id=?,"
                                       "player_club_name=?, number_of_goals=?, player_position=? WHERE player_id="
                                       + str(data_i_row_player_id))
                    execute_command = "".join(str(execute_command))
                    c.execute(execute_command, data[i])
                    connection.commit()

                    player_names_for_updates_made.append(data[i][1])

        if player_names_for_rows_created:
            print("Created", len(player_names_for_rows_created), "new rows for the following player/s:")
            print(*player_names_for_rows_created, sep="\n")
        if player_names_for_updates_made:
            print("Updated", len(player_names_for_updates_made), "rows for the following player/s:")
            print(*player_names_for_updates_made, sep="\n")

    except Error as e:
        print(e)


# Insert the scorers to the top_scorer database. If data exists it will not.
def insert_into_top_scorer(connection, data):
    try:
        c = connection.cursor()
        c.executemany("""INSERT INTO top_scorer VALUES (?,?,?,?,?,?);""", data)
        connection.commit()
    except Error as e:
        print(e)


# Creates a bar chart of the top five scorers from any data given.
# Needs work
def plot_top_scorers(data, graph_title):
    players = []
    goals = []
    positions = []

    # Populates the above lists with the data passed.
    for i, value in enumerate(data):
        players.append(data[i][0])
        goals.append(int(data[i][1]))
        positions.append(data[i][2])

    # Shortens player's full names to just surnames.
    for index, names in enumerate(players):
        players[index] = names[names.index(" "):]

    # For loop without iterator which saves me from having to find the length of players.
    x_pos = [i for i, _ in enumerate(players)]

    # Generates the colour of bars and the legend.
    colors, legend = [], []
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
    axes.set_ylim([0, goals[0] + 6])

    plt.ylabel("Goals Scored")
    plt.xlabel("Player Name")
    plt.title("Top Goalscorers (" + graph_title + ") in Premier League")
    plt.legend(bars, legend)

    plt.xticks(x_pos, players)

    filename = "C:/Users/tomto/PycharmProjects/Football/" + get_usable_date() + graph_title
    plt.savefig(filename, bbox_inches='tight')

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

    # If table is empty, fill with new call. If not empty then update any rows that need updating
    if not select_from_table(database_connection, sql_select_all):
        print("top_scorer is empty")
        insert_into_top_scorer(database_connection, request_received)
        print("Table created with ", len(request_received), " rows.")
    else:
        # Commits the received request to the database
        update_top_scorer(database_connection, request_received)

    top_five_attackers = select_from_table(database_connection,
                                           "SELECT player_name, number_of_goals, player_position FROM top_scorer "
                                           "WHERE player_position='Attacker' ORDER BY number_of_goals DESC LIMIT 5")

    top_five_midfielders = select_from_table(database_connection,
                                             "SELECT player_name, number_of_goals, player_position FROM top_scorer "
                                             "WHERE player_position='Midfielder' ORDER BY number_of_goals DESC LIMIT 5")

    top_five_defenders = select_from_table(database_connection,
                                           "SELECT player_name, number_of_goals, player_position FROM top_scorer "
                                           "WHERE player_position='Defender' ORDER BY number_of_goals DESC LIMIT 5")

    plot_top_scorers(np.array(top_five_attackers).reshape(-1, 3), "Attackers")
    plot_top_scorers(np.array(top_five_midfielders).reshape(-1, 3), "Midfielders")
    plot_top_scorers(np.array(top_five_defenders).reshape(-1, 3), "Defenders")
    top_scoring_in_position = [top_five_attackers[0:3], top_five_midfielders[0:3], top_five_defenders[0:3]]
    plot_top_scorers(top_scoring_in_position, "In Each Position")

    close_connection(database_connection)


if __name__ == "__main__":
    main()

'''
Get the plots working without static indices.

Get rid of "Table created." message when table already exists

What to do on plots when there are more than one player with the number of goals. Might need dict to do this because
can't sort by number_of_goals AND alphabetical player_name.

Do the same for assists as well.

Linear Regression:
- number of goals scored on y axis
- what should be on x? clubs?
- https://towardsdatascience.com/linear-regression-in-6-lines-of-python-5e1d0cd05b8d

Start my own goalscorer tally:
- add a table per game week so I can see averages etc.
- call the API and work out number of goals scored per country

Create a table for each player with over 3 goals to store when they were scored. Can make graphs from that.

Could you connection.rollback() in excepts

'''

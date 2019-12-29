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

        print("League ID: ", league_id)
        print("Current season: ", current_season)
        print("Current matchday: ", current_matchday)

        #connection.request('GET', '/v2/competitions/PL/scorers', None, headers)
        #response = json.loads(connection.getresponse().read().decode())
        #print(response)

    except http.client.CannotSendRequest:
        print("Error: Cannot send request.")
    except http.client.NotConnected:
        print("Error: Not connected.")
    except http.client.RemoteDisconnected:
        print("Error: Disconnected part way through the request.")
    except http.client.ImproperConnectionState:
        print("Error: Current status of connection will not allow successful request.")


def get_usable_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def main():
    database = r"records.db"
    print(database)
    api_token = "c66e3100c2584065b0377dd86280ae81"

    print("Today's date: ", get_usable_date())

    create_connection(database)

    print("Sending request.")
    make_request(api_token)


if __name__ == "__main__":
    main()


'''

Start my own goalscorer tally


'''
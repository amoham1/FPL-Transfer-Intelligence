
import requests

# STEP 1: Connect to the Fantasy Premier League API
# requests.get() sends a GET request to the API URL.
# The response variable stores the server's reply.

api_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(api_url)

# Status code 200 means the request was successful.
print(response.status_code)


# STEP 2: Convert the JSON response into Python data
# .json() converts the response into a Python dictionary.
# type() helps us identify what kind of data we're working with.

fpl_data = response.json()
print(type(fpl_data))


# STEP 3: Extract the player information
# The "elements" key contains a list of player dictionaries.
# Each dictionary stores one player's information and statistics.

players = fpl_data["elements"]


# STEP 4: Loop through all players
# A for loop lets us access every player without repeating code.
# Dictionary keys let us retrieve specific player statistics.

for player in players:
    print(player["web_name"], player["total_points"], player["minutes"])


# STEP 5: Convert a string into a float
# Some FPL statistics, such as ownership percentage, are stored as text.
# float() converts these values into decimal numbers.

ownership_percentage = float(players[0]["selected_by_percent"])

print(ownership_percentage)


# STEP 6: Collect player form values in a list
# Start with an empty list.
# Loop through each player, convert their form to a float,
# and append a tuple containing their name and form.

player_forms = []

for player in players:
    player_form = float(player["form"])
    player_forms.append((player["web_name"], player_form))

# Display the completed list of player names and form values.
print(player_forms)

from extract import get_fpl_data
import pandas as pd

# STEP 1: Retrieve the FPL data
# Call the function we created in extract.py.
# The function returns a dictionary containing the FPL API data.

fpl_data = get_fpl_data()


# STEP 2: Understand the API data
# type() checks the data type of a variable.
# Our API data is stored as a Python dictionary.

print(type(fpl_data))


# STEP 3: Extract the player information
# The "elements" key contains a list of players.
# Each player is stored as a dictionary with their statistics.

players = fpl_data["elements"]


# STEP 4: Explore individual player information
# A for loop goes through every player in the list.
# We use dictionary keys to access names, points, and minutes.

for player in players:
    print(player["web_name"], player["total_points"], player["minutes"])


# STEP 5: Convert a string into a float
# The API stores some numbers as text.
# float() converts text into a decimal number.
# We use players[0] to access the first player.

ownership_percentage = float(players[0]["selected_by_percent"])

print(ownership_percentage)


# STEP 6: Store player names and form values in a list
# Start with an empty list.
# Convert each player's form into a float.
# append() adds a tuple containing the player's name and form.

player_forms = []

for player in players:
    player_form = float(player["form"])
    player_forms.append((player["web_name"], player_form))

print(player_forms)


# STEP 7: Create a pandas DataFrame
# A DataFrame organizes our data into rows and columns.
# Each row represents one player.
# Each column represents a statistic.

players_df = pd.DataFrame(players)

# Display the first five rows.
print(players_df.head())

# Check the total number of rows and columns.
print(players_df.shape)

# Display the available column names.
print(players_df.columns)

# Check the data types of four important columns.
print(players_df[["web_name", "total_points", "form", "minutes"]].dtypes)


# STEP 8: Convert the form column into numerical data
# astype(float) converts an entire column into decimal numbers.
# This is important because machine learning needs numerical inputs.

players_df["form"] = players_df["form"].astype(float)

# Confirm that the conversion worked.
print(players_df["form"].dtypes)


# STEP 9: Check for missing values
# isna() checks whether values are missing.
# sum() counts the missing values in each column.

print(players_df["form"].isna().sum())

print(players_df[["web_name", "total_points", "minutes"]].isna().sum())


# STEP 10: Create a smaller DataFrame
# Select the columns we want to analyze.
# copy() creates a separate DataFrame so we can modify it safely.

clean_players_df = players_df[
    ["web_name", "total_points", "form", "minutes"]
].copy()


# STEP 11: Filter players based on minutes played
# This condition checks whether each player has played more than zero minutes.
# The result contains True or False for each player.

has_played = clean_players_df["minutes"] > 0

# Display the first five players who have played.
print(clean_players_df[has_played].head())


# STEP 12: Apply multiple filtering conditions
# We want players with more than 20 FPL points AND over 300 minutes.
# The & operator means both conditions must be true.
# count() counts non-missing values in each column.

print(
    clean_players_df[
        (clean_players_df["total_points"] > 20) &
        (clean_players_df["minutes"] > 300)
    ].count()
)


# STEP 13: Store the filtered players
# Create a separate DataFrame containing players who meet both conditions.
# len() tells us how many players are included.

filtered_players_df = clean_players_df[
    (clean_players_df["total_points"] > 20) &
    (clean_players_df["minutes"] > 300)
].copy()

print(len(filtered_players_df))


# STEP 14: Sort players by total points
# sort_values() arranges the rows based on a column.
# ascending=False sorts from highest to lowest.
# head() displays the first five results.

print(
    filtered_players_df.sort_values(
        by="total_points",
        ascending=False
    ).head()
)


# STEP 15: Calculate average points and minutes
# mean() calculates the average.
# round() limits the displayed decimal places.

print(round(filtered_players_df["total_points"].mean(), 2))
print(round(filtered_players_df["minutes"].mean(), 2))


# STEP 16: Explore descriptive statistics
# describe() summarizes a numerical column.
# It includes count, mean, standard deviation, min, max, and quartiles.

print(filtered_players_df["total_points"].describe().round(2))
print(filtered_players_df["minutes"].describe().round(2))


# STEP 17: Calculate FPL points per 90 minutes
# Players have different amounts of playing time.
# Points per 90 helps us compare their scoring rates.
# Formula: (total points / minutes played) * 90

filtered_players_df["points_per_90"] = (
    filtered_players_df["total_points"] /
    filtered_players_df["minutes"] * 90
)


# STEP 18: Rank players by points per 90
# Sort from highest to lowest scoring rate.
# Display the top five players.
# round(2) makes the results easier to read.

print(
    filtered_players_df.sort_values(
        by="points_per_90",
        ascending=False
    ).head().round(2)
)


# STEP 19: Analyze points-per-90 statistics
# describe() helps us understand the average, spread, and range.

print(filtered_players_df["points_per_90"].describe().round(2))


# STEP 20: Compare total points by player position
# element_type identifies a player's position in FPL:
# 1 = Goalkeeper, 2 = Defender, 3 = Midfielder, 4 = Forward.
# groupby() divides players into groups based on their position.

position_df = players_df[
    ["web_name", "element_type", "total_points", "minutes"]
].copy()

# Calculate average total points for each position.
print(
    position_df.groupby("element_type")["total_points"].mean().round(2)
)


# STEP 21: Analyze players with more than 180 minutes
# loc[] lets us filter rows and select columns together.
# We use 180 minutes as one threshold for comparing positions.

active_position_df = players_df.loc[
    players_df["minutes"] > 180,
    ["web_name", "element_type", "total_points", "minutes"]
].copy()

# Calculate points per 90 for these players.
active_position_df["points_per_90"] = (
    active_position_df["total_points"] /
    active_position_df["minutes"] * 90
)

# Find the average points per 90 for each position.
print(
    active_position_df.groupby("element_type")["points_per_90"]
    .mean().round(2)
)

# Count how many players are included in each position.
print(active_position_df.groupby("element_type").size())


# STEP 22: Analyze players with more than 90 minutes
# Lowering the threshold includes players with less playing time.
# This helps us see whether our results change.

active_position_90_df = players_df.loc[
    players_df["minutes"] > 90,
    ["web_name", "element_type", "total_points", "minutes"]
].copy()

active_position_90_df["points_per_90"] = (
    active_position_90_df["total_points"] /
    active_position_90_df["minutes"] * 90
)

# Compare average scoring rates and player counts.
print(
    active_position_90_df.groupby("element_type")["points_per_90"]
    .mean().round(2)
)

print(active_position_90_df.groupby("element_type").size())


# STEP 23: Analyze players with more than 300 minutes
# A higher threshold focuses on players with more playing time.
# We compare this against our 90-minute and 180-minute results.

active_position_300_df = players_df.loc[
    players_df["minutes"] > 300,
    ["web_name", "element_type", "total_points", "minutes"]
].copy()

active_position_300_df["points_per_90"] = (
    active_position_300_df["total_points"] /
    active_position_300_df["minutes"] * 90
)

# Compare average scoring rates and player counts.
print(
    active_position_300_df.groupby("element_type")["points_per_90"]
    .mean().round(2)
)

print(active_position_300_df.groupby("element_type").size())


# STEP 24: Compare standard deviation across positions
# std() measures how spread out the players' scoring rates are.
# We calculate it for each of our three minute thresholds.

print(
    active_position_df.groupby("element_type")["points_per_90"]
    .std().round(2)
)

print(
    active_position_90_df.groupby("element_type")["points_per_90"]
    .std().round(2)
)

print(
    active_position_300_df.groupby("element_type")["points_per_90"]
    .std().round(2)
)


# STEP 25: Calculate multiple statistics at once
# agg() allows us to combine several calculations.
# mean = average points per 90
# std = standard deviation
# count = number of players in each position

print(
    active_position_df.groupby("element_type")["points_per_90"]
    .agg(["mean", "std", "count"])
    .round(2)
)

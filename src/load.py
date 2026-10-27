
import sqlite3
from pathlib import Path
from extract import get_fpl_data


# STEP 1: Set up the database file paths
# __file__ gives us the location of this Python file.
# parent.parent moves from src/ to the main project folder.
# This allows the paths to work regardless of the working directory.

project_dir = Path(__file__).resolve().parent.parent

db_path = project_dir / "database" / "fpl_data.db"
schema_path = project_dir / "database" / "schema.sql"


# STEP 2: Retrieve player data from the FPL API
# get_fpl_data() is the function we created in extract.py.
# The "elements" key contains the list of FPL players.

fpl_data = get_fpl_data()
players = fpl_data["elements"]


# STEP 3: Prepare player records for SQLite
# The players table contains four columns:
# player_id, web_name, total_points, and minutes.
#
# Each player is converted into a tuple.
# append() adds each tuple to our player_records list.

player_records = []

for player in players:
    player_record = (
        player["id"],
        player["web_name"],
        player["total_points"],
        player["minutes"]
    )

    player_records.append(player_record)


# STEP 4: Create a reusable database connection function
# sqlite3.connect() opens an existing database or creates a new one.
# The function returns the connection.

def load_db(db_path):
    return sqlite3.connect(db_path)


# STEP 5: Connect to our FPL database
connection = load_db(db_path)

try:
    # STEP 6: Read and execute the SQL schema
    # schema.sql contains the CREATE TABLE statement.
    # executescript() runs the SQL instructions.
    # IF NOT EXISTS prevents an error if the table already exists.

    with open(schema_path, "r", encoding="utf-8") as schema_file:
        contents = schema_file.read()

    connection.executescript(contents)


    # STEP 7: Insert or update player information
    # INSERT INTO adds new player records.
    # ON CONFLICT checks whether a player ID already exists.
    # DO UPDATE updates an existing player's information.
    #
    # excluded refers to the incoming values we attempted to insert.

    upsert_query = """
    INSERT INTO players (player_id, web_name, total_points, minutes)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(player_id)
    DO UPDATE SET
        web_name = excluded.web_name,
        total_points = excluded.total_points,
        minutes = excluded.minutes
    """


    # STEP 8: Load all player records into SQLite
    # executemany() runs the same SQL statement for every tuple.
    # This lets us load hundreds of players without separate queries.

    connection.executemany(upsert_query, player_records)


    # STEP 9: Save our changes
    # commit() saves the inserted or updated player information.

    connection.commit()


    # STEP 10: Verify the database
    # COUNT(*) returns the number of records in the players table.
    # fetchone() returns the first result from the query.

    result = connection.execute(
        "SELECT COUNT(*) FROM players"
    )

    print("Total players in database:", result.fetchone()[0])


    # STEP 11: Check David Raya's record
    # WHERE filters the results by player_id.
    # The ? placeholder safely supplies the player ID.

    result = connection.execute(
        "SELECT * FROM players WHERE player_id = ?",
        (1,)
    )

    print("Player ID 1:", result.fetchone())


finally:
    # STEP 12: Close the database connection
    # finally ensures the connection is closed even if an error occurs.

    connection.close()

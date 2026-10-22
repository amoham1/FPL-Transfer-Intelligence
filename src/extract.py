import requests


# STEP 1: Retrieve data from the FPL API
# This function sends a request and returns the JSON data as a dictionary.

def get_fpl_data():
    print("Retrieving FPL data...")

    api_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(api_url, timeout=30)

    # Raise an error if the API request was unsuccessful.
    response.raise_for_status()

    # Convert the JSON response into Python data.
    fpl_data = response.json()

    return fpl_data


# Run this only when extract.py is executed directly.
# Importing the function from explore.py won't run this block.
if __name__ == "__main__":
    fpl_data = get_fpl_data()
    print(type(fpl_data))
import requests

API_BASE_URL = "https://api.football-data.org/v4/matches"

def fetcher(endpoint):
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from football-data.org API. Status code: {response.status_code}")

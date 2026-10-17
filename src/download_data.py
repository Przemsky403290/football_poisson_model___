import time

import requests
from pathlib import Path

RAW_DIR = Path("data/raw")
LEAGUE = "E0"
START_YEAR = 2018
END_YEAR = 2025

def season_code(year):
    return str(year)[2:] + str(year+1)[2:]

def season_codes(season_start, season_end):
    codes = []
    for year in range(season_start, season_end+1):
        codes.append(season_code(year))
    return codes

def download_season(league, season):
    url = f"https://www.football-data.co.uk/mmz4281/{season}/{league}.csv"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Nie udało się pobrać {league} {season}, kod odpowiedzi: {response.status_code}")
        return

    file_path = RAW_DIR / f"{league}_{season}.csv"
    file_path.write_bytes(response.content)
    print(f"Zapisano {file_path.name}")

if __name__ == '__main__':
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for season in season_codes(START_YEAR, END_YEAR):
        download_season(LEAGUE, season)
        time.sleep(1)


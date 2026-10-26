from operator import truediv
from os.path import exists

import pandas
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
MY_COLLS = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "B365H", "B365D", "B365A", "HC", "AC", "HST", "AST", "HS", "AS"]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"   # make new directory

RENAME = {
    "Date" : "date",
    "HomeTeam": "Home_team",
    "AwayTeam" : "Away_team",
    "FTHG" : "Home_goals",
    "FTAG" : "Away_goals",
    "FTR" : "Result",
    "B365H": "Home_odd",
    "B365D" : "Draw_odd",
    "B365A" : "Away_odd",
    "HC" : "Home_corners",
    "AC" : "Away_corners",
    "HST" : "Home_shots_on_target",
    "AST": "Away_shots_on_target",
    "HS" : "Home_shots",
    "AS" : "Away_shots"

}


def load_season(file_path):
    df = pd.read_csv(file_path, usecols = MY_COLLS)
    df["season"] = file_path.stem.split("_")[1]
    return df


def load_all_seasons():
    files = sorted(RAW_DIR.glob("*.csv"))
    seasons = []
    for file_path in files:
        seasons.append(load_season(file_path))
    return pd.concat(seasons, ignore_index= True)

def clean(df):
    df = df.rename(columns = RENAME)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)   # we can sort chronologically
    df = df.sort_values(by = "date").reset_index(drop=True)  # we have to reset indexes because hey are mixed
    return df

if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    matches = clean(load_all_seasons())

    output_path = PROCESSED_DIR / "matches.csv"
    matches.to_csv(output_path, index = False)
    print(f"Saved {len(matches)} matches to {output_path} ")
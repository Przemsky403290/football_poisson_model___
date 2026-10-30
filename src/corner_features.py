import pandas as pd


WINDOW = 5
STAT_COLS = ["corners_for", "corners_against", "shots_for", "shots_against"]
FEATURE_COLS = ["is_home", "win_prob", "corners_for_avg5", "corners_against_avg5", "shots_for_avg5", "shots_against_avg5",
                "opp_corners_for_avg5", "opp_corners_against_avg5", "opp_shots_for_avg5", "opp_shots_against_avg5"]
TARGET_COL = "corners_for"



matches = pd.read_csv("../data/processed/matches.csv", parse_dates = ["date"], dtype = {"season": str})


def to_team_matches(matches):
    """Converts a match table (one row per match) into a team-match table (two rows per match) one from home and one from away perspective"""
    matches = matches.copy()
    matches["match_id"] = matches.index
    home = pd.DataFrame({
        "match_id": matches["match_id"],
        "date": matches["date"],
        "season": matches["season"],
        "team": matches["Home_team"],
        "opponent": matches["Away_team"],
        "is_home": 1,  # from home team perspective
        "corners_for": matches["Home_corners"],
        "corners_against": matches["Away_corners"],
        "shots_for": matches["Home_shots"],
        "shots_against": matches["Away_shots"],
        "win_prob": 1 / matches["Home_odd"],

    })

    away = pd.DataFrame({
        "match_id": matches["match_id"],
        "date": matches["date"],
        "season": matches["season"],
        "team": matches["Away_team"],
        "opponent": matches["Home_team"],
        "is_home": 0,  # from away team perspective
        "corners_for": matches["Away_corners"],
        "corners_against": matches["Home_corners"],
        "shots_for": matches["Away_shots"],
        "shots_against": matches["Home_shots"],
        "win_prob": 1 / matches["Away_odd"],

    })

    return (pd.concat([home, away], ignore_index=True).sort_values(["team", "date"]).reset_index(drop=True))




def add_rolling_features(team_matches, window):
    """Adds rolling features"""
    team_matches = team_matches.copy()
    for col in STAT_COLS:
        team_matches[f"{col}_avg{window}"] = team_matches.groupby("team")[col].transform(lambda x: x.shift(1)
        .rolling(window, min_periods=3).mean())
    return team_matches



def add_opponent_features(team_matches, window):
    """Adds rolling features"""
    avg_colls = [f"{col}_avg{window}" for col in STAT_COLS]
    opponent_stats = team_matches[["match_id", "team"] + avg_colls].reanme(columns={"team": "opponent", **{col: f"opp_{col}" for col in avg_colls}})
    return team_matches.merge(opponent_stats, on = ["match_id", "opponent"], how = "left")



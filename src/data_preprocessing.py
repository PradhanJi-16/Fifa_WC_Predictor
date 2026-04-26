import pandas as pd

def load_and_preprocess():
    df= pd.read_csv('data/results.csv')

    df = df.rename(columns={
        "home_team":"Team_A",
        "away_team":"Team_B",
        "home_score":"Team_A_goals",
        "away_score":"Team_B_goals"
    })

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")
    
    def get_result(row):
        if row["Team_A_goals"] > row["Team_B_goals"]:
            return "Win"
        elif row["Team_A_goals"] < row["Team_B_goals"]:
            return "Loss"
        else:
            return "Draw"
        
    df["Result"] = df.apply(get_result, axis=1)

    teams = pd.concat([df["Team_A"], df["Team_B"]]).unique()

    team_stats = {}

    for team in teams:
        team_matches = df[(df["Team_A"] == team) | (df["Team_B"] == team)]

        recent = team_matches.tail(5)

        goals_scored = 0
        goals_conceded = 0
        wins = 0
        draws = 0

        for _, row in recent.iterrows():
            if row["Team_A"] == team:
                goals_scored += row["Team_A_goals"]
                goals_conceded += row["Team_B_goals"]

                if row["Team_A_goals"] > row["Team_B_goals"]:
                    wins += 1
                elif row["Team_A_goals"] == row["Team_B_goals"]:
                    draws += 1
            else:
                goals_scored += row["Team_B_goals"]
                goals_conceded += row["Team_A_goals"]

                if row["Team_B_goals"] > row["Team_A_goals"]:
                    wins += 1
                elif row["Team_B_goals"] == row["Team_A_goals"]:
                    draws += 1

        total_matches = len(recent)

        if total_matches == 0:
            avg_scored = 0
            avg_conceded = 0
            win_rate = 0
        else:
            avg_scored = goals_scored / total_matches
            avg_conceded = goals_conceded / total_matches
            win_rate = wins / total_matches

        
        rating = (win_rate * 1000) + (avg_scored * 100)

        team_stats[team] = {
            "avg_scored": avg_scored,
            "avg_conceded": avg_conceded,
            "goal_diff": avg_scored - avg_conceded,
            "rating": rating
        }

    df["A_avg_scored"] = df["Team_A"].apply(lambda x: team_stats[x]["avg_scored"])
    df["A_avg_conceded"] = df["Team_A"].apply(lambda x: team_stats[x]["avg_conceded"])
    df["A_goal_diff"] = df["Team_A"].apply(lambda x: team_stats[x]["goal_diff"])

    df["B_avg_scored"] = df["Team_B"].apply(lambda x: team_stats[x]["avg_scored"])
    df["B_avg_conceded"] = df["Team_B"].apply(lambda x: team_stats[x]["avg_conceded"])
    df["B_goal_diff"] = df["Team_B"].apply(lambda x: team_stats [x]["goal_diff"])

    df["A_rating"] = df["Team_A"].apply(lambda x: team_stats[x]["rating"])
    df["B_rating"] = df["Team_B"].apply(lambda x: team_stats[x]["rating"])

    df["is_home"] = df["neutral"].apply(lambda x: 0 if x else 1)
    return df, team_stats



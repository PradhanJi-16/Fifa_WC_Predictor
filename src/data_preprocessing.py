import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess():
    df= pd.read_csv('data/matches.csv')
    
    def get_result(row):
        if row["Team_A_goals"] > row["Team_B_goals"]:
            return "Win"
        elif row["Team_A_goals"] < row["Team_B_goals"]:
            return "Loss"
        else:
            return "Draw"
        
    df["Result"] = df.apply(get_result, axis=1)

    # le = LabelEncoder()
    # teams = pd.concat([df["Team_A"], df["Team_B"]])
    # le.fit(teams)

    # df["Team_A_enc"] = le.transform(df["Team_A"])
    # df["Team_B_enc"] = le.transform(df["Team_B"])

    # return df, le

    teams = pd.concat([df["Team_A"], df["Team_B"]]).unique()

    team_stats = {}

    for team in teams:
        matches_a = df[df["Team_A"]== team]
        matches_b = df[df["Team_B"]== team]

        goals_scored = matches_a["Team_A_goals"].sum() + matches_b["Team_B_goals"].sum()
        goals_conceded = matches_a["Team_B_goals"].sum() + matches_b["Team_A_goals"].sum()

        total_matches = len(matches_a) + len(matches_b)

        if total_matches == 0:
            avg_scored = 0
            avg_conceded = 0
        else:
            avg_scored = goals_scored / total_matches
            avg_conceded = goals_conceded / total_matches

        team_stats[team] = {
            "avg_scored": avg_scored,
            "avg_conceded": avg_conceded,
            "goal_diff": avg_scored - avg_conceded
        }

    df["A_avg_scored"] = df["Team_A"].apply(lambda x: team_stats[x]["avg_scored"])
    df["A_avg_conceded"] = df["Team_A"].apply(lambda x: team_stats[x]["avg_conceded"])
    df["A_goal_diff"] = df["Team_A"].apply(lambda x: team_stats[x]["goal_diff"])

    df["B_avg_scored"] = df["Team_B"].apply(lambda x: team_stats[x]["avg_scored"])
    df["B_avg_conceded"] = df["Team_B"].apply(lambda x: team_stats[x]["avg_conceded"])
    df["B_goal_diff"] = df["Team_B"].apply(lambda x: team_stats [x]["goal_diff"])

    return df, team_stats



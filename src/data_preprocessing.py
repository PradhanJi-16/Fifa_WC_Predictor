import pandas as pd
from src.elo import update_elo

# team_base_strength = {
#     # 🔥 Top Tier
#     "Argentina": 95,
#     "Brazil": 96,
#     "France": 95,
#     "England": 90,
#     "Spain": 90,
#     "Germany": 89,
#     "Portugal": 88,
#     "Netherlands": 88,
#     "Belgium": 87,

#     # 🟡 Strong Teams
#     "Croatia": 85,
#     "Uruguay": 84,
#     "Italy": 86,
#     "Denmark": 83,
#     "Switzerland": 82,
#     "Mexico": 80,
#     "USA": 80,
#     "United States": 80,
#     "Japan": 82,
#     "South Korea": 80,
#     "Korea Republic": 80,
#     "Morocco": 83,
#     "Senegal": 82,
#     "Iran": 78,
#     "Australia": 78,

#     # 🟠 Mid Tier
#     "Turkey": 77,
#     "Austria": 78,
#     "Serbia": 79,
#     "Poland": 79,
#     "Ukraine": 78,
#     "Norway": 78,
#     "Sweden": 80,
#     "Czech Republic": 78,
#     "Ghana": 78,
#     "Nigeria": 79,
#     "Cameroon": 78,
#     "Ivory Coast": 80,
#     "Côte d'Ivoire": 80,
#     "Egypt": 79,
#     "Algeria": 78,
#     "Tunisia": 77,
#     "Colombia": 82,
#     "Chile": 80,
#     "Peru": 78,
#     "Ecuador": 80,
#     "Paraguay": 79,

#     # 🔵 Lower Mid
#     "Canada": 76,
#     "Saudi Arabia": 75,
#     "Qatar": 72,
#     "UAE": 70,
#     "China": 70,
#     "Uzbekistan": 72,
#     "Jordan": 70,
#     "Bolivia": 70,
#     "Panama": 74,
#     "Jamaica": 74,

#     # ⚪ Weak Teams
#     "Haiti": 56,
#     "Curacao": 55,
#     "Cape Verde": 58,
#     "New Zealand": 59,
#     "South Africa": 65,
#     "Scotland": 75,
#     "Albania": 72,
#     "Finland": 74,
#     "Iceland": 75
# }
def compute_elo(df):
    elo = {}

    # Initialize all teams
    teams = set(df["Team_A"]).union(set(df["Team_B"]))
    for team in teams:
        elo[team] = 1500  # base rating

    # Sort by date (VERY IMPORTANT)
    df = df.sort_values("date")

    for _, row in df.iterrows():
        team_a = row["Team_A"]
        team_b = row["Team_B"]

        rating_a = elo[team_a]
        rating_b = elo[team_b]

        # Determine result
        if row["Team_A_goals"] > row["Team_B_goals"]:
            result = 1
        elif row["Team_A_goals"] < row["Team_B_goals"]:
            result = 0
        else:
            result = 0.5

        new_a, new_b = update_elo(rating_a, rating_b, result)

        elo[team_a] = new_a
        elo[team_b] = new_b

    return elo

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

    elo_ratings = compute_elo(df)

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
        for _, row in recent.iterrows():
            if row["Team_A"] == team:
                goals_scored += row["Team_A_goals"]
                goals_conceded += row["Team_B_goals"]
            else:
                goals_scored += row["Team_B_goals"]
                goals_conceded += row["Team_A_goals"]

        total_matches = len(recent)

        if total_matches == 0:
            avg_scored = 0
            avg_conceded = 0
            win_rate = 0
        else:
            avg_scored = goals_scored / total_matches
            avg_conceded = goals_conceded / total_matches
            win_rate = wins / total_matches

        

        rating = elo_ratings.get(team, 1500)

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



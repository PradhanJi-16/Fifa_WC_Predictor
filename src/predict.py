import pandas as pd

def predict_match(model,team_stats,team_a, team_b, is_home=1):

    if team_a not in team_stats or team_b not in team_stats:
        return "Draw"
    
    a = team_stats[team_a]
    b = team_stats[team_b]

    # features = [[
    #     a["avg_scored"], a["avg_conceded"], a["goal_diff"],
    #     b["avg_scored"], b["avg_conceded"], b["goal_diff"],
    #     a["rating"], b["rating"],
    #     is_home
    # ]]

    # prediction = model.predict(features)

    # return prediction[0]

    data = pd.DataFrame([{
        "A_avg_scored": a["avg_scored"],
        "A_avg_conceded": a["avg_conceded"],
        "A_goal_diff": a["goal_diff"],
        "B_avg_scored": b["avg_scored"],
        "B_avg_conceded": b["avg_conceded"],
        "B_goal_diff": b["goal_diff"],
        "A_rating": a["rating"],
        "B_rating": b["rating"],
        "is_home": is_home
    }])

    return model.predict(data)[0]
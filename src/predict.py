def predict_match(model,team_stats,team_a, team_b):
    a = team_stats[team_a]
    b = team_stats[team_b]

    features = [[
        a["avg_scored"], a["avg_conceded"], a["goal_diff"],
        b["avg_scored"], b["avg_conceded"], b["goal_diff"]
    ]]

    prediction = model.predict(features)

    return prediction[0]
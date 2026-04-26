def predict_match(model,team_stats,team_a, team_b, is_home=1):
    a = team_stats[team_a]
    b = team_stats[team_b]

    features = [[
        a["avg_scored"], a["avg_conceded"], a["goal_diff"],
        b["avg_scored"], b["avg_conceded"], b["goal_diff"],
        a["rating"], b["rating"],
        is_home
    ]]

    prediction = model.predict(features)

    return prediction[0]
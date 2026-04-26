from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_model(df):
    X = df[[
        "A_avg_scored", "A_avg_conceded", "A_goal_diff",
        "B_avg_scored", "B_avg_conceded", "B_goal_diff",
        "A_rating", "B_rating",
        "is_home"
    ]]

    y = df["Result"]

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train,y_train)

    return model
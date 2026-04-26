from src.data_preprocessing import load_and_preprocess
from src.model import train_model
from src.predict import predict_match

df, team_stats = load_and_preprocess()

model = train_model(df)

team_a = "France"
team_b = "Germany"

result = predict_match(model, team_stats, team_a, team_b)

if result == "Win":
    print(f"{team_a} will WIN against {team_b}")
elif result == "Loss":
    print(f"{team_b} will WIN against {team_a}")
else:
    print(f"{team_a} vs {team_b} will be a DRAW")
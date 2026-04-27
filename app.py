import streamlit as st
from src.data_preprocessing import load_and_preprocess
from src.model import train_model
from src.predict import predict_match
from src.tournament import simulate_multiple
from src.visualize import plot_probabilities
from src.tournament import simulate_once

st.title("⚽ FIFA World Cup Predictor")

st.write("Predict match outcomes and simulate full tournament")

# Load model once
@st.cache_resource
def load_model():
    df, team_stats = load_and_preprocess()
    model = train_model(df)
    return model, team_stats

model, team_stats = load_model()

teams = sorted(team_stats.keys())

st.header("🔮 Match Prediction")

team_a = st.selectbox("Select Team A", teams)
team_b = st.selectbox("Select Team B", teams)

if st.button("Predict Match"):
    probs = predict_match(model, team_stats, team_a, team_b)

    st.write(f"### {team_a} vs {team_b}")

    st.write("Win probability:")
    st.write({
        f"{team_a} wins": round(probs.get("Win", 0) * 100, 2),
        f"{team_b} wins": round(probs.get("Loss", 0) * 100, 2),
        "Draw": round(probs.get("Draw", 0) * 100, 2)
    })


st.header("🏆 World Cup Simulation")

num_simulations = st.slider("Number of simulations", 50, 500, 100)

if st.button("Run Simulation"):
    winners = {}

    for _ in range(num_simulations):
        winner = simulate_once(model, team_stats)
        winners[winner] = winners.get(winner, 0) + 1

    st.write("### Winning Probabilities")

    total = sum(winners.values())

    probs = {team: (count / total) * 100 for team, count in winners.items()}

    st.bar_chart(probs)


import streamlit as st
from src.data_preprocessing import load_and_preprocess
from src.model import train_model
from src.predict import predict_match
from src.tournament import simulate_once

st.set_page_config(page_title="FIFA Predictor", layout="wide")

st.title("⚽ FIFA World Cup Predictor")
st.write("Predict matches and simulate full tournament")

# Load model
@st.cache_resource
def load_model():
    df, team_stats = load_and_preprocess()
    model = train_model(df)
    return model, team_stats

model, team_stats = load_model()
teams = sorted(team_stats.keys())

# 🔥 Create 2 columns
col1, col2 = st.columns(2)

# =========================
# LEFT: MATCH PREDICTOR
# =========================
with col1:
    st.header("🔮 Match Predictor")

    team_a = st.selectbox("Team A", teams, key="team_a")
    team_b = st.selectbox("Team B", teams, key="team_b")

    if st.button("Predict Match"):
        probs = predict_match(model, team_stats, team_a, team_b)

        st.subheader(f"{team_a} vs {team_b}")

        st.write({
            f"{team_a} Win %": round(probs.get("Win", 0) * 100, 2),
            f"{team_b} Win %": round(probs.get("Loss", 0) * 100, 2),
            "Draw %": round(probs.get("Draw", 0) * 100, 2)
        })


# =========================
# RIGHT: TOURNAMENT SIMULATION
# =========================
with col2:
    st.header("🏆 World Cup Simulation")

    num_simulations = st.slider("Simulations", 50, 500, 100)

    if st.button("Run Simulation"):
        winners = {}

        with st.spinner("Simulating tournament..."):
            for _ in range(num_simulations):
                winner = simulate_once(model, team_stats)
                winners[winner] = winners.get(winner, 0) + 1

        st.subheader("Winning Probabilities")

        total = sum(winners.values())
        probs = {team: (count / total) * 100 for team, count in winners.items()}

        st.bar_chart(probs)
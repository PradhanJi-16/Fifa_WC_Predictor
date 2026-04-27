import streamlit as st
from src.data_preprocessing import load_and_preprocess
from src.model import train_model
from src.predict import predict_match
from src.tournament import simulate_once
import plotly.graph_objects as go


flag_urls = {
    "Argentina": "https://flagcdn.com/w40/ar.png",
    "Brazil": "https://flagcdn.com/w40/br.png",
    "France": "https://flagcdn.com/w40/fr.png",
    "Germany": "https://flagcdn.com/w40/de.png",
    "Spain": "https://flagcdn.com/w40/es.png",
    "England": "https://flagcdn.com/w40/gb-eng.png",
    "Portugal": "https://flagcdn.com/w40/pt.png",
    "Netherlands": "https://flagcdn.com/w40/nl.png",
    "Italy": "https://flagcdn.com/w40/it.png",
    "Belgium": "https://flagcdn.com/w40/be.png",
    "Croatia": "https://flagcdn.com/w40/hr.png",
    "Uruguay": "https://flagcdn.com/w40/uy.png",
    "Mexico": "https://flagcdn.com/w40/mx.png",
    "USA": "https://flagcdn.com/w40/us.png",
    "United States": "https://flagcdn.com/w40/us.png",
    "Japan": "https://flagcdn.com/w40/jp.png",
    "South Korea": "https://flagcdn.com/w40/kr.png",
    "Morocco": "https://flagcdn.com/w40/ma.png",
    "Senegal": "https://flagcdn.com/w40/sn.png",
    "Qatar": "https://flagcdn.com/w40/qa.png"
    
}

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

    if team_a == team_b:
        st.warning("Select two different teams")

    if st.button("Predict Match"):
        probs = predict_match(model, team_stats, team_a, team_b)

        colA, colMid, colB = st.columns([1, 2, 1])

        with colA:
            st.image(flag_urls.get(team_a, ""), width=80)
            st.markdown(f"**{team_a}**")

        with colMid:
            st.markdown("### ⚔️ Match Result")

            st.markdown(f"## {team_a} vs {team_b}")

            st.markdown(f"""
            <div style='text-align: center; font-size:18px;'>
                <b>{team_a} Win:</b> {round(probs.get("Win", 0) * 100, 2)}%<br>
                <b>{team_b} Win:</b> {round(probs.get("Loss", 0) * 100, 2)}%<br>
                <b>Draw:</b> {round(probs.get("Draw", 0) * 100, 2)}%
            </div>
            """, unsafe_allow_html=True)

        with colB:
            st.image(flag_urls.get(team_b, ""), width=80)
            st.markdown(f"**{team_b}**")

        # st.write({
        #     f"{team_a} Win %": round(probs.get("Win", 0) * 100, 2),
        #     f"{team_b} Win %": round(probs.get("Loss", 0) * 100, 2),
        #     "Draw %": round(probs.get("Draw", 0) * 100, 2)
        # })

        st.success(f"Most likely winner: {max(probs, key=probs.get)}")


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

        sorted_probs = dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))

        teams = list(sorted_probs.keys())
        values = list(sorted_probs.values())

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=values,
            y=teams,
            orientation='h'
        ))

        # Add flags as images
        for i, team in enumerate(teams):
            if team in flag_urls:
                fig.add_layout_image(
                    dict(
                        source=flag_urls[team],
                        x=values[i] + 1,
                        y=i,
                        xref="x",
                        yref="y",
                        sizex=2,
                        sizey=0.5,
                        xanchor="left",
                        yanchor="middle"
                    )
                )

        fig.update_layout(
            title="World Cup Winning Probabilities",
            xaxis_title="Probability (%)",
            yaxis_title="Teams",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
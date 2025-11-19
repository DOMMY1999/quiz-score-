import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="RESOVATE 2025", layout="wide")

# -------------------------------- HEADER WITH LOGOS --------------------------------
st.markdown("""
<style>
.logo-img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
.score-card {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.total-badge {
    background: #0078ff;
    padding: 5px 10px;
    border-radius: 8px;
    color: white;
    display: inline-block;
    font-size: 16px;
    margin-top: 5px;
}
.small-input input {
    border-radius: 10px !important;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------- LOGO ROW --------------------------------
left_col, mid_col, right_col = st.columns([1, 2, 1])



with left_col:
    st.image("logo_left.png", width=150)  # LEFT LOGO

with mid_col:
    st.image("resovate_logo.jpeg", width=400)  # CENTER LOGO, bigger

with right_col:
    st.image("logo_right.png", width=150)  # RIGHT LOGO


# ---------------------------- SESSION STATE --------------------------------
if "team_names" not in st.session_state:
    st.session_state.team_names = [f"Team {i}" for i in range(1, 11)]

NUM_TEAMS = 10
NUM_ROUNDS = 10
NUM_BOXES = 10
EXCEL_FILE = "RESOVATE_scores.xlsx"

# ---------------------------- TEAM NAMES INPUT --------------------------------
st.markdown("## ✏️ Enter Team Names")
team_cols = st.columns(NUM_TEAMS)
for i in range(NUM_TEAMS):
    st.session_state.team_names[i] = team_cols[i].text_input(
        f"Team {i+1} Name",
        value=st.session_state.team_names[i],
        key=f"team_name_{i}"
    )

# ---------------------------- ROUND INPUT TABLES --------------------------------
st.markdown("## 🎯 Enter Scores for Each Round")

# Dictionary to store round scores
round_scores = {}

for r in range(1, NUM_ROUNDS + 1):
    with st.expander(f"Round {r}", expanded=True):
        round_scores[r] = {}
        # Create table input for 10 teams × 10 boxes
        for t in range(NUM_TEAMS):
            st.markdown(f"### {st.session_state.team_names[t]}")
            cols = st.columns(NUM_BOXES)
            scores = []
            for b in range(NUM_BOXES):
                val = cols[b].text_input(
                    "", key=f"round{r}_team{t}_box{b}", placeholder="0", label_visibility="collapsed"
                )
                val = val.strip()
                if val == "":
                    val = "0"
                scores.append(int(val))
            total = sum(scores)
            round_scores[r][st.session_state.team_names[t]] = scores + [total]
            st.markdown(f"<div class='total-badge'>Total: {total}</div>", unsafe_allow_html=True)

# ---------------------------- SAVE BUTTON --------------------------------
if st.button("💾 Save All Rounds"):
    # Create Excel writer
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        for r in range(1, NUM_ROUNDS + 1):
            data = []
            for t_name in st.session_state.team_names:
                row = round_scores[r][t_name]
                # Add total as last column
                data.append([t_name] + row)
            columns = ["Team Name"] + [f"Score {i+1}" for i in range(NUM_BOXES)] + ["Total"]
            df = pd.DataFrame(data, columns=columns)
            df.to_excel(writer, sheet_name=f"Round {r}", index=False)
    st.success(f"All rounds saved to {EXCEL_FILE} successfully!")

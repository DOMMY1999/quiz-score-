import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="RESOVATE 2025", layout="wide")

# -------------------------------- HEADER WITH LOGOS + STYLING -------------------------------
st.markdown("""
<style>
/* Main title background */
.header-box {
    background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

/* Score card styling */
.score-card {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* Total score badge */
.total-badge {
    background: #0078ff;
    padding: 8px 14px;
    border-radius: 8px;
    color: white;
    display: inline-block;
    font-size: 18px;
    margin-top: 10px;
}

/* Input boxes small */
.small-input input {
    border-radius: 10px !important;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------- LOGO ROW --------------------------------------
left_col, mid_col, right_col = st.columns([1, 3, 1])

with left_col:
    st.image("logo_left.png", width=110)

with mid_col:
    st.markdown("""
        <div class='header-box'>
            <h1>RESOVATE 2025</h1>
            <h3>Yenepoya Research Centre</h3>
        </div>
    """, unsafe_allow_html=True)

with right_col:
    st.image("logo_right.png", width=110)

# --------------------------------- SCORE FILE ------------------------------------
EXCEL_FILE = "scores.xlsx"

if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame()
    df.to_excel(EXCEL_FILE, index=False)

# --------------------------------- SESSION STATE ---------------------------------
if "round" not in st.session_state:
    st.session_state.round = 1

if "num_teams" not in st.session_state:
    st.session_state.num_teams = 4

# --------------------------------- ROUND SECTION ---------------------------------
st.markdown(f"## 🎯 Round {st.session_state.round}")

st.session_state.num_teams = st.number_input(
    "Number of Teams:",
    min_value=1, max_value=20,
    value=st.session_state.num_teams
)

team_scores = {}
st.write("")

# --------------------------------- TEAM SCORE UI --------------------------------
for t in range(1, st.session_state.num_teams + 1):

    st.markdown(f"### 🟦 Team {t}")
    st.markdown("<div class='score-card'>", unsafe_allow_html=True)

    cols = st.columns(10)
    scores = []

    for i in range(10):
        with cols[i]:
            val = st.text_input(
                "",
                key=f"team{t}_box{i}_round{st.session_state.round}",
                placeholder="0",
                label_visibility="collapsed"
            )
            if val.strip() == "":
                val = "0"

            scores.append(int(val))

    total = sum(scores)
    team_scores[f"Team {t}"] = total

    st.markdown(f"<div class='total-badge'>Total Score: {total}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------- SAVE BUTTON ------------------------------------
if st.button("💾 Save This Round", use_container_width=True):

    old_df = pd.read_excel(EXCEL_FILE)

    new_row = {"Round": st.session_state.round}
    for t in range(1, st.session_state.num_teams + 1):
        new_row[f"Team {t}"] = team_scores[f"Team {t}"]

    new_df = pd.concat([old_df, pd.DataFrame([new_row])], ignore_index=True)
    new_df.to_excel(EXCEL_FILE, index=False)

    st.session_state.round += 1

    st.success("Round saved successfully!")
    st.rerun()

# -------------------------------- SCORE TABLE ------------------------------------
st.markdown("## 📊 All Rounds Scoreboard")
st.dataframe(pd.read_excel(EXCEL_FILE), use_container_width=True)

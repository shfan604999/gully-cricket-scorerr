import streamlit as st

st.set_page_config(page_title="Gully Cricket Scorer", layout="centered")

st.title("🏏 Gully Cricket Pro Scorer")

# ---------------- INIT ----------------
if "players" not in st.session_state:
    st.session_state.players = {}

# ---------------- TEAM SETUP ----------------
st.header("👥 Team Setup")

player_names = st.text_input(
    "Enter player names (comma separated)",
    "Rahul, Aman, Rohan, Sameer, Arjun"
)

if st.button("Create Players"):
    st.session_state.players = {}
    for name in player_names.split(","):
        name = name.strip()
        st.session_state.players[name] = {
            "runs": 0,
            "balls": 0,
            "wickets": 0,
            "overs": 0.0,
            "runs_conceded": 0,
            "catches": 0
        }
    st.success("Players created!")

# ---------------- LIVE SCORING ----------------
if st.session_state.players:
    st.header("📊 Live Scoring")

    batter = st.selectbox("Batsman", st.session_state.players.keys())
    bowler = st.selectbox("Bowler", st.session_state.players.keys())

    runs = st.selectbox("Runs", [0, 1, 2, 3, 4, 6])
    wicket = st.checkbox("Wicket")
    fielder = st.selectbox(
        "Fielder (if catch)",
        ["None"] + list(st.session_state.players.keys())
    )

    if st.button("Add Ball"):
        st.session_state.players[batter]["runs"] += runs
        st.session_state.players[batter]["balls"] += 1

        st.session_state.players[bowler]["runs_conceded"] += runs
        st.session_state.players[bowler]["overs"] += 1/6

        if wicket:
            st.session_state.players[bowler]["wickets"] += 1
            if fielder != "None":
                st.session_state.players[fielder]["catches"] += 1

        st.success("Ball added!")

# ---------------- SCORECARD ----------------
if st.session_state.players:
    st.header("📋 Scorecard")

    for p, s in st.session_state.players.items():
        st.write(
            f"**{p}** | Runs: {s['runs']} | Balls: {s['balls']} | "
            f"Wickets: {s['wickets']} | Catches: {s['catches']}"
        )

# ---------------- AWARDS ----------------
if st.session_state.players:
    st.header("🏆 Match Awards")

    potm = max(
        st.session_state.players.items(),
        key=lambda x: x[1]["runs"] + x[1]["wickets"] * 25 + x[1]["catches"] * 10
    )[0]

    best_batsman = max(
        st.session_state.players.items(),
        key=lambda x: x[1]["runs"]
    )[0]

    best_bowler = max(
        st.session_state.players.items(),
        key=lambda x: x[1]["wickets"]
    )[0]

    best_fielder = max(
        st.session_state.players.items(),
        key=lambda x: x[1]["catches"]
    )[0]

    st.success(f"🏆 Player of the Match: {potm}")
    st.info(f"🏏 Best Batsman: {best_batsman}")
    st.info(f"🎯 Best Bowler: {best_bowler}")
    st.info(f"🧤 Best Fielder: {best_fielder}")

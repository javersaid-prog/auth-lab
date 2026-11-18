import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="AUTH-LAB",
    page_icon="🔐",
    layout="wide",
)

# -------------------- STİL --------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #080e1b 0%, #101b2d 55%, #0b1424 100%);
        color: #e6edf7;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    [data-testid="stSidebar"] {
        background: #0a1220;
        border-right: 1px solid #1d3049;
    }

    [data-testid="stSidebar"] h1 {
        color: #42b9ff;
        font-weight: 800;
        letter-spacing: 2px;
    }

    [data-testid="stSidebar"] p {
        color: #8298b4;
    }

    h1 {
        color: #f0f6ff !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #dceaff !important;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #172943, #101d30);
        border: 1px solid #284564;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
    }

    [data-testid="stMetricLabel"] {
        color: #91a9c5 !important;
    }

    [data-testid="stMetricValue"] {
        color: #42b9ff !important;
        font-weight: 800;
    }

    .stButton > button {
        background: linear-gradient(90deg, #087cc1, #16a5d9);
        color: white;
        border: none;
        border-radius: 9px;
        padding: 10px 20px;
        font-weight: 700;
        transition: 0.25s;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #109cdb, #35c6ed);
        color: white;
        border: none;
        box-shadow: 0 0 18px rgba(32, 174, 235, 0.35);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #304967;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #29415e;
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: #253b56 !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #d5e3f5;
    }

    .stDownloadButton > button {
        background: #126b55;
        color: white;
        border-radius: 9px;
        border: 1px solid #258b70;
    }

    .stDownloadButton > button:hover {
        background: #168568;
        color: white;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- MƏLUMATLAR --------------------

attack_data = {
    "Stolen Password": {
        "1FA": ("Compromised", 5, 5),
        "2FA": ("Blocked", 2, 3),
        "MFA": ("Blocked", 1, 2),
    },
    "SIM Swap": {
        "1FA": ("Not applicable", 1, 1),
        "2FA": ("Compromised", 5, 5),
        "MFA": ("Blocked", 2, 3),
    },
    "Real-time Phishing": {
        "1FA": ("Compromised", 5, 5),
        "2FA": ("Compromised", 5, 5),
        "MFA": ("Blocked", 1, 2),
    },
    "Session Hijacking": {
        "1FA": ("Compromised", 5, 5),
        "2FA": ("Compromised", 5, 5),
        "MFA": ("Compromised", 5, 5),
    },
}

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------- NAVİQASİYA --------------------

st.sidebar.title("🔐 AUTH-LAB")
st.sidebar.caption("AUTHENTICATION UNDER ATTACK")
st.sidebar.caption("Simulation data is kept for this session only.")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Authentication Lab",
        "Attack Simulator",
        "Risk Analyzer",
        "Security Report",
    ],
)

# -------------------- KÖMƏKÇİ FUNKSİYALAR --------------------


def add_result(authentication, attack):
    """Simulyasiya nəticəsini sessiya tarixçəsinə əlavə edir."""
    outcome, likelihood, impact = attack_data[attack][authentication]
    risk_score = likelihood * impact

    result = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Authentication": authentication,
        "Attack": attack,
        "Outcome": outcome,
        "Likelihood": likelihood,
        "Impact": impact,
        "Risk Score": risk_score,
    }
    st.session_state.history.append(result)
    return result


def style_chart(fig):
    """Qrafiklərə tünd mövzu tətbiq edir."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf7",
    )
    return fig


# -------------------- DASHBOARD --------------------

if page == "Dashboard":
    st.title("🔐 AUTH-LAB Dashboard")
    st.write("Authentication security overview and recent simulation results.")

    history_df = pd.DataFrame(st.session_state.history)
    total_tests = len(history_df)

    if total_tests:
        breaches = int((history_df["Outcome"] == "Compromised").sum())
        blocked = int((history_df["Outcome"] == "Blocked").sum())
        average_risk = round(float(history_df["Risk Score"].mean()), 1)
    else:
        breaches = 0
        blocked = 0
        average_risk = None

    metric_cols = st.columns(4)
    metric_cols[0].metric("Tests run", total_tests)
    metric_cols[1].metric("Breaches", breaches)
    metric_cols[2].metric("Attacks blocked", blocked)
    metric_cols[3].metric(
        "Average risk",
        f"{average_risk}/25" if average_risk is not None else "—",
    )

    st.divider()
    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("Recent simulation activity")
        if total_tests:
            chart = px.bar(
                history_df,
                x="Attack",
                y="Risk Score",
                color="Authentication",
                barmode="group",
                hover_data=["Outcome", "Likelihood", "Impact"],
                title="Risk score by attack and authentication method",
            )
            style_chart(chart)
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("No simulation results yet. Run a test on another page.")

    with right:
        st.subheader("Latest results")
        if total_tests:
            st.dataframe(history_df.tail(5), use_container_width=True, hide_index=True)
        else:
            st.info("The results table will appear after your first simulation.")

# -------------------- AUTHENTICATION LAB --------------------

elif page == "Authentication Lab":
    st.title("🔑 Authentication Lab")
    st.write("Compare the illustrative outcomes of different authentication methods.")

    selected_attack = st.selectbox("Choose an attack", list(attack_data.keys()))

    comparison_rows = []
    for authentication, values in attack_data[selected_attack].items():
        outcome, likelihood, impact = values
        comparison_rows.append(
            {
                "Authentication": authentication,
                "Outcome": outcome,
                "Likelihood": likelihood,
                "Impact": impact,
                "Risk Score": likelihood * impact,
            }
        )

    comparison_df = pd.DataFrame(comparison_rows)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    chart = px.bar(
        comparison_df,
        x="Authentication",
        y="Risk Score",
        color="Outcome",
        title=f"Risk comparison: {selected_attack}",
        color_discrete_map={
            "Compromised": "#ef5350",
            "Blocked": "#26a69a",
            "Not applicable": "#78909c",
        },
    )
    style_chart(chart)
    st.plotly_chart(chart, use_container_width=True)

# -------------------- ATTACK SIMULATOR --------------------

elif page == "Attack Simulator":
    st.title("🧪 Attack Simulator")
    st.write("Run an illustrative attack simulation and save its result.")

    attack = st.selectbox("Select attack type", list(attack_data.keys()))
    authentication = st.selectbox(
        "Select authentication method",
        ["1FA", "2FA", "MFA"],
    )

    if st.button("Run simulation"):
        result = add_result(authentication, attack)
        message = f"Result: {result['Outcome']} — risk score {result['Risk Score']}/25"

        if result["Outcome"] == "Compromised":
            st.error(message)
        elif result["Outcome"] == "Blocked":
            st.success(message)
        else:
            st.info(message)

        st.dataframe(
            pd.DataFrame([result]),
            use_container_width=True,
            hide_index=True,
        )

# -------------------- RISK ANALYZER --------------------

elif page == "Risk Analyzer":
    st.title("📊 Risk Analyzer")
    st.write("Review the illustrative likelihood and impact scores for each scenario.")

    rows = []
    for attack, methods in attack_data.items():
        for authentication, values in methods.items():
            outcome, likelihood, impact = values
            rows.append(
                {
                    "Attack": attack,
                    "Authentication": authentication,
                    "Outcome": outcome,
                    "Likelihood": likelihood,
                    "Impact": impact,
                    "Risk Score": likelihood * impact,
                }
            )

    risk_df = pd.DataFrame(rows)
    st.dataframe(risk_df, use_container_width=True, hide_index=True)

    chart = px.scatter(
        risk_df,
        x="Likelihood",
        y="Impact",
        size="Risk Score",
        color="Authentication",
        hover_name="Attack",
        hover_data=["Outcome", "Risk Score"],
        title="Likelihood and impact by scenario",
        size_max=35,
    )
    style_chart(chart)
    st.plotly_chart(chart, use_container_width=True)

# -------------------- SECURITY REPORT --------------------

elif page == "Security Report":
    st.title("🛡️ Security Report")
    st.write("View and download the simulations run during this session.")

    if st.session_state.history:
        report_df = pd.DataFrame(st.session_state.history)
        st.dataframe(report_df, use_container_width=True, hide_index=True)

        csv_data = report_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download report as CSV",
            data=csv_data,
            file_name="auth_lab_security_report.csv",
            mime="text/csv",
        )

        if st.button("Clear session results"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No report data yet. Run a simulation first.")
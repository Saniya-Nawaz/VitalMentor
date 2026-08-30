import streamlit as st
import plotly.express as px
import os

from database import load_data, init_db
from alerts import get_alerts
from chatbot import respond


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Vital Mentor",
    page_icon="💙",
    layout="wide"
)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

try:
    init_db()
except Exception as e:
    st.error(f"Database initialization failed: {e}")
    st.stop()


# =========================================================
# USERS
# =========================================================

USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    }
}

# Create 50 parent + child accounts automatically
for i in range(1, 51):

    USERS[f"parent{i}"] = {
        "password": "parent123",
        "role": "parent",
        "child_id": f"C{i}"
    }

    USERS[f"child{i}"] = {
        "password": "child123",
        "role": "child",
        "child_id": f"C{i}"
    }


# =========================================================
# LOGIN FUNCTION
# =========================================================

def login(username, password):

    username = username.strip()
    password = password.strip()

    user = USERS.get(username)

    if user and user["password"] == password:
        return user

    return None


# =========================================================
# SESSION STATE
# =========================================================

if "user" not in st.session_state:
    st.session_state["user"] = None


# =========================================================
# LOGIN PAGE
# =========================================================

if st.session_state["user"] is None:
    # Put the actual Streamlit form in a centered column
    left, center, right = st.columns([1, 2, 1])

    with center:

        with st.form("login_form"):
            username = st.text_input(
                "👤 Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "🔑 Password",
                type="password",
                placeholder="Enter password"
            )

            submit = st.form_submit_button(
                "🚀 Login",
                use_container_width=True
            )

            if submit:

                user = login(
                    username,
                    password
                )

                if user:

                    st.session_state["user"] = user

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password"
                    )

    st.stop()

# =========================================================
# CURRENT USER
# =========================================================

user = st.session_state["user"]

role = user["role"]


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data()

except Exception as e:

    st.error(
        f"Unable to load health data: {e}"
    )

    st.stop()


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if df is None or df.empty:

    st.warning(
        "⚠ No health data available."
    )

    st.info(
        "Run data_collector.py first."
    )

    if st.sidebar.button("🚪 Logout"):

        st.session_state["user"] = None
        st.rerun()

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("💙 Vital Mentor")

st.sidebar.write(
    f"👤 **Role:** {role}"
)

if role in ["parent", "child"]:

    st.sidebar.write(
        f"👧 **Child ID:** {user['child_id']}"
    )

st.sidebar.write(
    f"📊 **Records:** {len(df)}"
)


if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state["user"] = None
    st.rerun()


# =========================================================
# FILTER DATA FOR PARENT / CHILD
# =========================================================

if role in ["parent", "child"]:

    child_id = user.get("child_id")

    if "child_id" not in df.columns:

        st.error(
            "Health data does not contain child_id column."
        )

        st.stop()

    df = df[
        df["child_id"].astype(str) == str(child_id)
    ].copy()


# =========================================================
# CHECK FILTERED DATA
# =========================================================

if role in ["parent", "child"] and df.empty:

    st.warning(
        f"No health data found for {user['child_id']}."
    )

    st.stop()


# =========================================================
# LATEST RECORD
# =========================================================

if role in ["parent", "child"]:

    latest = df.iloc[-1]


# =========================================================
# =========================================================
# CHILD DASHBOARD
# =========================================================
# =========================================================

if role == "child":


    st.success(
        f"Welcome back! 🌟 Child ID: {user['child_id']}"
    )


    # =====================================================
    # HEALTH METRICS
    # =====================================================

    st.subheader("💙 Today's Health")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💧 Water",
        f"{latest.get('water_intake', 0)} ml"
    )

    col2.metric(
        "😴 Sleep",
        f"{latest.get('sleep_hours', 0)} hrs"
    )

    col3.metric(
        "👣 Steps",
        latest.get("steps", 0)
    )

    col4.metric(
        "❤️ Heart Rate",
        latest.get("heart_rate", 0)
    )


    # =====================================================
    # DAILY PROGRESS
    # =====================================================

    st.subheader("🎮 Daily Progress")

    try:

        steps = float(
            latest.get("steps", 0)
        )

        progress = min(
            1.0,
            max(0.0, steps / 10000)
        )

        st.progress(progress)

        st.write(
            f"👣 {int(steps):,} / 10,000 steps"
        )

    except Exception:

        st.warning(
            "Unable to calculate progress."
        )


    # =====================================================
    # HEALTH TRENDS
    # =====================================================

    st.subheader("📊 Health Trends")

    required_columns = [
        "steps",
        "heart_rate",
        "water_intake"
    ]

    if all(
        col in df.columns
        for col in required_columns
    ):

        fig = px.line(
            df,
            y=[
                "steps",
                "heart_rate",
                "water_intake"
            ],
            template="plotly_dark",
            title="Your Health Trends"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =====================================================
    # ALERTS
    # =====================================================

    st.subheader("🚨 Alerts")

    try:

        alerts = get_alerts(latest)

        if alerts:

            for alert in alerts:
                st.error(alert)

        else:

            st.success(
                "Everything looks good! 👍"
            )

    except Exception as e:

        st.warning(
            f"Unable to load alerts: {e}"
        )


    # =====================================================
    # AI COMPANION
    # =====================================================

    st.subheader("🤖 AI Companion")

    st.write(
        "Ask VitalMentor about your health, "
        "sleep, water, activity or symptoms."
    )

    q = st.text_input(
        "Ask something...",
        placeholder="Example: How is my health today?"
    )

    if q:

        try:

            response = respond(
                q,
                latest
            )

            st.success(response)

        except Exception as e:

            st.error(
                f"AI Companion error: {e}"
            )


# =========================================================
# =========================================================
# PARENT DASHBOARD
# =========================================================
# =========================================================

elif role == "parent":

    st.success(
        f"Welcome! 🌟 Monitoring child: {user['child_id']}"
    )


    # =====================================================
    # LATEST DATA
    # =====================================================

    st.subheader("📋 Latest Child Health Data")

    st.dataframe(
        latest.to_frame().T,
        use_container_width=True
    )


    # =====================================================
    # HEALTH SUMMARY
    # =====================================================

    st.subheader("💙 Child Health Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💧 Water",
        f"{latest.get('water_intake', 0)} ml"
    )

    col2.metric(
        "😴 Sleep",
        f"{latest.get('sleep_hours', 0)} hrs"
    )

    col3.metric(
        "👣 Steps",
        latest.get("steps", 0)
    )

    col4.metric(
        "❤️ Heart Rate",
        latest.get("heart_rate", 0)
    )


    # =====================================================
    # TRENDS
    # =====================================================

    st.subheader("📊 Child Health Trends")

    graph_columns = [
        "heart_rate",
        "temperature",
        "steps"
    ]

    if all(
        col in df.columns
        for col in graph_columns
    ):

        fig = px.line(
            df,
            y=graph_columns,
            template="plotly_dark",
            title="Child Health Trends"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =====================================================
    # ALERTS
    # =====================================================

    st.subheader("🚨 Alerts")

    try:

        alerts = get_alerts(latest)

        if alerts:

            for alert in alerts:
                st.error(alert)

        else:

            st.success(
                "Child is healthy 👍"
            )

    except Exception as e:

        st.warning(
            f"Unable to load alerts: {e}"
        )


    # =====================================================
    # AI COMPANION
    # =====================================================

    st.subheader("🤖 AI Companion")

    st.write(
        "Ask VitalMentor about your child's health, "
        "sleep, water, activity or symptoms."
    )

    q = st.text_input(
        "Ask something...",
        placeholder="Example: How is my child's health today?"
    )

    if q:

        try:

            response = respond(
                q,
                latest
            )

            st.success(response)

        except Exception as e:

            st.error(
                f"AI Companion error: {e}"
            )


# =========================================================
# =========================================================
# ADMIN DASHBOARD
# =========================================================
# =========================================================

elif role == "admin":
    st.success(
        "Welcome, Administrator! 👋"
    )

    st.write(
        "Monitor groups of children, compare health metrics "
        "and identify unusual patterns using machine learning."
    )


    # =====================================================
    # OVERALL STATISTICS
    # =====================================================

    st.subheader("📊 Overall Statistics")

    total_children = (
        df["child_id"].nunique()
        if "child_id" in df.columns
        else 0
    )

    total_records = len(df)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👧 Total Children",
        total_children
    )

    col2.metric(
        "📋 Total Health Records",
        total_records
    )

    col3.metric(
        "👨‍👩‍👧 Parent Accounts",
        total_children
    )


    # =====================================================
    # CHILD GROUP SELECTION
    # =====================================================

    st.subheader("👧 Select Children Group")

    if "child_id" not in df.columns:

        st.error(
            "child_id column is missing from the database."
        )

        st.stop()


    # Convert IDs into C1, C2, C3...
    child_ids = sorted(
        df["child_id"]
        .dropna()
        .astype(str)
        .unique(),
        key=lambda x: int(
            x.replace("C", "")
        )
    )


    # =====================================================
    # GROUP SIZE
    # =====================================================

    group_size = st.selectbox(
        "How many children should be shown together?",
        [5, 10],
        index=0
    )


    # =====================================================
    # CREATE GROUPS
    # =====================================================

    groups = []

    for i in range(
        0,
        len(child_ids),
        group_size
    ):

        group = child_ids[
            i:i + group_size
        ]

        if group:

            groups.append(
                f"{group[0]} - {group[-1]}"
            )


    if not groups:

        st.warning(
            "No child groups available."
        )

        st.stop()


    # =====================================================
    # SELECT GROUP
    # =====================================================

    selected_group = st.selectbox(
        "Choose a child group",
        groups
    )


    # =====================================================
    # GET SELECTED IDs
    # =====================================================

    start_id = int(
        selected_group
        .split("-")[0]
        .strip()
        .replace("C", "")
    )

    end_id = int(
        selected_group
        .split("-")[1]
        .strip()
        .replace("C", "")
    )


    selected_ids = [
        f"C{i}"
        for i in range(
            start_id,
            end_id + 1
        )
    ]


    # =====================================================
    # FILTER DATA
    # =====================================================

    filtered_df = df[
        df["child_id"]
        .astype(str)
        .isin(selected_ids)
    ].copy()


    st.success(
        f"Currently viewing children: "
        f"C{start_id} → C{end_id}"
    )


    # =====================================================
    # SELECTED CHILDREN CARDS
    # =====================================================

    st.subheader("👧 Selected Children")

    selected_children = sorted(
        filtered_df["child_id"]
        .dropna()
        .astype(str)
        .unique(),
        key=lambda x: int(
            x.replace("C", "")
        )
    )


    if selected_children:

        cols = st.columns(
            len(selected_children)
        )

        for col, child in zip(
            cols,
            selected_children
        ):

            child_data = filtered_df[
                filtered_df["child_id"]
                .astype(str) == child
            ]

            col.metric(
                child,
                f"{len(child_data)} records"
            )


    # =====================================================
    # DATA TABLE
    # =====================================================

    st.subheader("📋 Selected Children Health Data")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


    # =====================================================
    # GROUP HEALTH SUMMARY
    # =====================================================

    st.subheader("📈 Group Health Summary")

    if not filtered_df.empty:

        col1, col2, col3, col4 = st.columns(4)


        if "steps" in filtered_df.columns:

            col1.metric(
                "👣 Average Steps",
                f"{filtered_df['steps'].mean():.0f}"
            )


        if "sleep_hours" in filtered_df.columns:

            col2.metric(
                "😴 Average Sleep",
                f"{filtered_df['sleep_hours'].mean():.1f} hrs"
            )


        if "water_intake" in filtered_df.columns:

            col3.metric(
                "💧 Average Water",
                f"{filtered_df['water_intake'].mean():.0f} ml"
            )


        if "heart_rate" in filtered_df.columns:

            col4.metric(
                "❤️ Average Heart Rate",
                f"{filtered_df['heart_rate'].mean():.0f} BPM"
            )


    # =====================================================
    # STEPS COMPARISON
    # =====================================================

    st.subheader("👣 Steps Comparison")

    if (
        not filtered_df.empty
        and "steps" in filtered_df.columns
    ):

        fig = px.line(
            filtered_df,
            x=filtered_df.index,
            y="steps",
            color="child_id",
            markers=True,
            title=(
                f"Steps Comparison: "
                f"C{start_id} → C{end_id}"
            ),
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =====================================================
    # HEART RATE
    # =====================================================

    st.subheader("❤️ Heart Rate Comparison")

    if (
        not filtered_df.empty
        and "heart_rate" in filtered_df.columns
    ):

        fig = px.line(
            filtered_df,
            x=filtered_df.index,
            y="heart_rate",
            color="child_id",
            markers=True,
            title="Heart Rate Comparison",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =====================================================
    # WATER
    # =====================================================

    st.subheader("💧 Water Intake Comparison")

    if (
        not filtered_df.empty
        and "water_intake" in filtered_df.columns
    ):

        fig = px.line(
            filtered_df,
            x=filtered_df.index,
            y="water_intake",
            color="child_id",
            markers=True,
            title="Water Intake Comparison",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =====================================================
    # SLEEP
    # =====================================================

    st.subheader("😴 Sleep Comparison")

    if (
        not filtered_df.empty
        and "sleep_hours" in filtered_df.columns
    ):

        fig = px.line(
            filtered_df,
            x=filtered_df.index,
            y="sleep_hours",
            color="child_id",
            markers=True,
            title="Sleep Comparison",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =====================================================
    # MACHINE LEARNING
    # ISOLATION FOREST
    # =====================================================

    st.subheader("🧠 AI Health Pattern Detection")

    st.info(
        "Isolation Forest detects records that differ significantly "
        "from the selected group's normal patterns. "
        "An unusual pattern is NOT a medical diagnosis."
    )


    try:

        from sklearn.ensemble import IsolationForest

    except ImportError:

        st.error(
            "scikit-learn is not installed."
        )

        st.code(
            "pip install scikit-learn"
        )

        st.stop()


    # =====================================================
    # ML FEATURES
    # =====================================================

    ml_columns = [
        "heart_rate",
        "temperature",
        "steps",
        "water_intake",
        "sleep_hours"
    ]


    missing_columns = [
        col
        for col in ml_columns
        if col not in filtered_df.columns
    ]


    if missing_columns:

        st.warning(
            "Missing ML columns: "
            + ", ".join(missing_columns)
        )

    else:

        ml_data = filtered_df[
            ml_columns
        ].apply(
            lambda x: __import__("pandas").to_numeric(
                x,
                errors="coerce"
            )
        ).dropna()


        # =================================================
        # ENOUGH DATA?
        # =================================================

        if len(ml_data) >= 5:

            model = IsolationForest(
                n_estimators=100,
                contamination="auto",
                random_state=42
            )


            predictions = model.fit_predict(
                ml_data
            )


            scores = model.decision_function(
                ml_data
            )


            result_df = filtered_df.loc[
                ml_data.index
            ].copy()


            result_df[
                "AI Prediction"
            ] = predictions


            result_df[
                "Anomaly Score"
            ] = scores


            result_df[
                "AI Status"
            ] = result_df[
                "AI Prediction"
            ].map(
                {
                    1: "🟢 Normal Pattern",
                    -1: "🟠 Unusual Pattern"
                }
            )


            # =================================================
            # COUNTS
            # =================================================

            normal_count = (
                result_df[
                    "AI Prediction"
                ] == 1
            ).sum()


            unusual_count = (
                result_df[
                    "AI Prediction"
                ] == -1
            ).sum()


            col1, col2 = st.columns(2)


            col1.metric(
                "🟢 Normal Records",
                normal_count
            )


            col2.metric(
                "🟠 Unusual Records",
                unusual_count
            )


            # =================================================
            # AI RESULTS
            # =================================================

            st.subheader(
                "🔍 AI Analysis Results"
            )


            display_columns = [
                "child_id",
                "heart_rate",
                "temperature",
                "steps",
                "water_intake",
                "sleep_hours",
                "AI Status",
                "Anomaly Score"
            ]


            st.dataframe(
                result_df[
                    display_columns
                ],
                use_container_width=True
            )


            # =================================================
            # UNUSUAL CHILDREN
            # =================================================

            unusual_children = (
                result_df[
                    result_df[
                        "AI Prediction"
                    ] == -1
                ]["child_id"]
                .astype(str)
                .unique()
            )


            if len(unusual_children) > 0:

                st.warning(
                    "⚠ Unusual patterns detected for: "
                    + ", ".join(
                        unusual_children
                    )
                )

            else:

                st.success(
                    "✅ No unusual patterns detected."
                )


            # =================================================
            # ANOMALY GRAPH
            # =================================================

            st.subheader(
                "🧠 AI Anomaly Visualization"
            )


            fig = px.scatter(
                result_df,
                x="steps",
                y="heart_rate",
                color="AI Status",
                hover_data=[
                    "child_id",
                    "temperature",
                    "water_intake",
                    "sleep_hours",
                    "Anomaly Score"
                ],
                title="AI Detected Health Patterns",
                template="plotly_dark"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        else:

            st.warning(
                "Not enough records for ML analysis. "
                "At least 5 valid health records are required."
            )


    # =====================================================
    # COMBINED HEALTH GRAPH
    # =====================================================

    st.subheader("📊 Combined Health Trends")

    combined_columns = [
        "heart_rate",
        "water_intake",
        "steps"
    ]


    if all(
        col in filtered_df.columns
        for col in combined_columns
    ):

        fig = px.line(
            filtered_df,
            x=filtered_df.index,
            y=combined_columns,
            color="child_id",
            title="Combined Health Metrics",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# UNKNOWN ROLE
# =========================================================

else:

    st.error(
        "Unknown user role ❌"
    )

    st.session_state["user"] = None

    st.rerun()
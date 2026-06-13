import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

from backend.auth import *
from backend.save_data import save_expense_data
from backend.load_data import load_expense_data

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Smart Expense Analyzer",
    layout="wide"
)

# ======================================================
# SESSION STATE
# ======================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "expense_rows" not in st.session_state:
    st.session_state.expense_rows = 1

if "budget_rows" not in st.session_state:
    st.session_state.budget_rows = 1

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

.main{
    background:linear-gradient(135deg,#0f172a,#111827,#1e293b);
}

/* PAGE WIDTH */
.block-container{
    padding-top:1rem;
    max-width:1200px;
    margin:auto;
}

/* LOGIN CONTAINER */
.login-container{
    min-height:90vh;
    display:flex;
    justify-content:center;
    align-items:center;
}

/* LOGIN BOX */
.login-box{
    width:100%;
    max-width:420px;
    margin:auto;
    background:rgba(255,255,255,0.06);
    padding:40px;
    border-radius:24px;
    border:1px solid rgba(255,255,255,0.10);
    backdrop-filter:blur(12px);
    box-shadow:0 8px 30px rgba(0,0,0,0.35);
}

/* LOGIN TITLE */
.login-title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:white;
    margin-bottom:10px;
}

/* SUBTITLE */
.login-subtitle{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:30px;
    font-size:16px;
}

/* LABELS */
label{
    color:white !important;
    font-size:15px !important;
}

/* TEXT INPUT */
.stTextInput input{
    height:48px;
    border-radius:12px;
    background:#1e293b;
    color:white;
    border:1px solid #334155;
    padding-left:14px;
    font-size:15px;
}

/* BUTTON */
.stButton>button{
    width:100%;
    height:48px;
    border:none;
    border-radius:12px;
    background:#475569;
    color:white;
    font-size:15px;
    font-weight:600;
    transition:0.3s;
    margin-top:10px;
}

.stButton>button:hover{
    background:#64748b;
    transform:translateY(-2px);
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background:#111827;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* SUMMARY BOX */
.summary-box{
    background:rgba(255,255,255,0.08);
    padding:20px;
    border-radius:15px;
    margin-top:20px;
    border:1px solid rgba(255,255,255,0.1);
}

/* MOBILE */
@media (max-width:768px){

    .login-box{
        max-width:95%;
        padding:28px 20px;
    }

    .login-title{
        font-size:32px;
    }

    .login-subtitle{
        font-size:14px;
    }

    .block-container{
        padding-top:0.5rem;
    }
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN PAGE
# ======================================================

if not st.session_state.logged_in:

    st.markdown("""
    <style>

    .login-title{
        text-align:center;
        font-size:42px;
        font-weight:700;
        color:white;
        margin-bottom:8px;
    }

    .login-subtitle{
        text-align:center;
        color:#cbd5e1;
        margin-bottom:25px;
        font-size:16px;
    }

    .login-wrapper{
        background:rgba(255,255,255,0.06);
        padding:40px;
        border-radius:24px;
        border:1px solid rgba(255,255,255,0.10);
        backdrop-filter:blur(12px);
        box-shadow:0 8px 30px rgba(0,0,0,0.35);
        margin-top:40px;
    }

    .stTextInput input{
        height:48px;
        border-radius:12px;
        background:#1e293b;
        color:white;
        border:1px solid #334155;
        padding-left:14px;
        font-size:15px;
    }

    .stButton > button{
        width:100%;
        height:48px;
        border:none;
        border-radius:12px;
        background:#475569;
        color:white;
        font-size:15px;
        font-weight:600;
        margin-top:10px;
    }

    .stButton > button:hover{
        background:#64748b;
    }

    @media (max-width:768px){

        .login-wrapper{
            padding:25px;
            margin-top:20px;
        }

        .login-title{
            font-size:30px;
        }

        .login-subtitle{
            font-size:14px;
        }
    }

    </style>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1.5,2,1.5])

    with center:

        st.markdown("""
        <div class="login-wrapper">

        <div class="login-title">
            Smart Expense Analyzer
        </div>

        <div class="login-subtitle">
            Multi User Expense Tracking System
        </div>
        """, unsafe_allow_html=True)

        login_type = st.radio(
            "Select",
            ["Login", "Signup"],
            horizontal=True
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        # ==================================================
        # SIGNUP
        # ==================================================

        if login_type == "Signup":

            if st.button("Create Account"):

                success = create_user(
                    username,
                    password
                )

                if success:

                    st.success(
                        "Account Created Successfully"
                    )

                else:

                    st.error(
                        "Username Already Exists"
                    )

        # ==================================================
        # LOGIN
        # ==================================================

        else:

            if st.button("Login"):

                result = login_user(
                    username,
                    password
                )

                if result:

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.rerun()

                else:

                    st.error(
                        "Invalid Username or Password"
                    )

        st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# MAIN APPLICATION
# ======================================================

else:

    # ==================================================
    # SIDEBAR
    # ==================================================

    st.sidebar.success(
        f"Welcome {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Expense Tracker",
            "Budget Planner",
            "Expense Analysis"
        ]
    )

    # ==================================================
    # TITLE
    # ==================================================

    st.markdown("""
    <h1 style='text-align:center;font-size:55px;color:white;'>
    Smart Expense Analyzer
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # DASHBOARD
    # ==================================================

    if page == "Dashboard":

        st.markdown("""
        <h2 style='text-align:center;color:white;'>
        Financial Dashboard
        </h2>
        """, unsafe_allow_html=True)

        st.info(
            f"Welcome {st.session_state.username}"
        )

        st.write("""
        Features Available:
        - Expense Tracking
        - Budget Planning
        - Monthly Comparison
        - Weekly Analysis
        - Date Wise Analysis
        """)

    # ==================================================
    # EXPENSE TRACKER
    # ==================================================

    elif page == "Expense Tracker":

        center_col1, center_col2, center_col3 = st.columns([1,5,1])

        with center_col2:

            st.markdown("""
            <h2 style='text-align:center;font-size:42px;color:white;'>
            Expense Tracker
            </h2>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Upload Excel",
                type=["xlsx", "xls"]
            )

            st.markdown("### Manual Entry")

            manual_entries = []

            for i in range(st.session_state.expense_rows):

                st.markdown(f"### Entry {i+1}")

                c1, c2 = st.columns(2)

                with c1:

                    category = st.text_input(
                        f"Category {i+1}",
                        key=f"cat_{i}"
                    )

                with c2:

                    amount = st.number_input(
                        f"Amount {i+1}",
                        min_value=0.0,
                        key=f"amt_{i}"
                    )

                manual_date = st.date_input(
                    f"Date {i+1}",
                    key=f"date_{i}"
                )

                manual_entries.append({
                    "Date": pd.to_datetime(manual_date),
                    "Month": pd.to_datetime(manual_date).month_name(),
                    "Year": pd.to_datetime(manual_date).year,
                    "Category": category,
                    "Withdrawal Amt.": amount,
                    "Username": st.session_state.username
                })

            if st.button("➕ Add Category"):

                st.session_state.expense_rows += 1
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            track_button = st.button("Track It")

        # ==================================================
        # TRACK LOGIC
        # ==================================================

        if track_button:

            manual_df = pd.DataFrame(manual_entries)

            manual_df = manual_df[
                manual_df["Category"] != ""
            ]

            if uploaded_file is not None:

                df = pd.read_excel(
                    uploaded_file,
                    header=20
                )

                possible_date_cols = [
                    "Value Date",
                    "Date",
                    "Txn Date",
                    "Transaction Date",
                    "VALUE DATE"
                ]

                date_col = None

                for col in possible_date_cols:

                    if col in df.columns:
                        date_col = col
                        break

                if date_col is None:

                    st.error("Date column not found")
                    st.stop()

                df = df[df["Narration"].notna()]

                df["Withdrawal Amt."] = pd.to_numeric(
                    df["Withdrawal Amt."],
                    errors="coerce"
                )

                df = df[
                    df["Withdrawal Amt."].notna()
                ]

                df["Date"] = pd.to_datetime(
                    df[date_col],
                    errors="coerce"
                )

                df["Month"] = df["Date"].dt.month_name()

                df["Year"] = df["Date"].dt.year

                df["Category"] = (
                    df["Narration"]
                    .astype(str)
                    .str.rsplit("-", n=1)
                    .str[-1]
                    .str.strip()
                    .str.upper()
                )

                df["Username"] = st.session_state.username

                file_df = df[[
                    "Date",
                    "Month",
                    "Year",
                    "Category",
                    "Withdrawal Amt.",
                    "Username"
                ]]

                final_df = pd.concat(
                    [file_df, manual_df],
                    ignore_index=True
                )

            else:

                final_df = manual_df

            save_expense_data(final_df)

            category_expense = (
                final_df.groupby("Category")[
                    "Withdrawal Amt."
                ]
                .sum()
                .reset_index()
            )

            st.markdown("## Category Wise Expense")

            st.dataframe(category_expense)

            total_expense = category_expense[
                "Withdrawal Amt."
            ].sum()

            st.markdown(f"""
            <div class='summary-box'>
                <h3>Total Expense : ₹ {total_expense}</h3>
            </div>
            """, unsafe_allow_html=True)

            bar_fig = px.bar(
                category_expense,
                x="Category",
                y="Withdrawal Amt.",
                title="Category Wise Spending"
            )

            st.plotly_chart(
                bar_fig,
                use_container_width=True
            )

            pie_fig = px.pie(
                category_expense,
                names="Category",
                values="Withdrawal Amt.",
                title="Expense Distribution"
            )

            st.plotly_chart(
                pie_fig,
                use_container_width=True
            )

    # ==================================================
    # BUDGET PLANNER
    # ==================================================

    elif page == "Budget Planner":

        st.markdown("""
        <h2 style='text-align:center;font-size:42px;'>
        Budget Planner
        </h2>
        """, unsafe_allow_html=True)

        salary = st.number_input(
            "Enter Salary",
            min_value=0.0
        )

        budget_entries = []

        for i in range(st.session_state.budget_rows):

            bc1,bc2 = st.columns(2)

            with bc1:

                budget_category = st.text_input(
                    f"Budget Category {i+1}",
                    key=f"budget_cat_{i}"
                )

            with bc2:

                budget_amount = st.number_input(
                    f"Expected Amount {i+1}",
                    min_value=0.0,
                    key=f"budget_amt_{i}"
                )

            budget_entries.append({
                "Category": budget_category,
                "Budget": budget_amount
            })

        if st.button("➕ Add Budget Category"):

            st.session_state.budget_rows += 1
            st.rerun()

        compare_button = st.button(
            "Compare With Budget"
        )

        if compare_button:

            budget_df = pd.DataFrame(
                budget_entries
            )

            budget_df = budget_df[
                budget_df["Category"] != ""
            ]

            st.dataframe(budget_df)

            total_budget = budget_df[
                "Budget"
            ].sum()

            savings = salary - total_budget

            st.markdown(f"""
            <div class='summary-box'>
                <h3>Planned Expense : ₹ {total_budget}</h3>
                <h3>Savings : ₹ {savings}</h3>
            </div>
            """, unsafe_allow_html=True)

    # ==================================================
    # EXPENSE ANALYSIS
    # ==================================================

    elif page == "Expense Analysis":

        st.markdown("""
        <h2 style='text-align:center;'>
        Smart Expense Analysis
        </h2>
        """, unsafe_allow_html=True)

        df = load_expense_data()

        if df.empty:

            st.warning("No expense data available")

        else:

            df = df[
                df["Username"] ==
                st.session_state.username
            ]

            if df.empty:

                st.warning(
                    "No data for this user"
                )

            else:

                df["Date"] = pd.to_datetime(
                    df["Date"]
                )

                df["MonthYear"] = (
                    df["Month"] + " " +
                    df["Year"].astype(str)
                )

                df["Week"] = (
                    "Week " +
                    (
                        ((df["Date"].dt.day - 1)//7)+1
                    ).astype(str)
                )

                df["MonthNumber"] = (
                    df["Date"].dt.month
                )

                month_order_df = (
                    df[
                        ["MonthYear","Year","MonthNumber"]
                    ]
                    .drop_duplicates()
                    .sort_values(
                        by=["Year","MonthNumber"]
                    )
                )

                month_options = (
                    month_order_df["MonthYear"]
                    .tolist()
                )

                col1,col2,col3 = st.columns([3,1,1])

                with col1:

                    selected_months = st.multiselect(
                        "Select Months",
                        month_options,
                        default=month_options[-1:]
                    )

                with col2:

                    show_weekly = st.checkbox(
                        "Weekly"
                    )

                with col3:

                    show_datewise = st.checkbox(
                        "Date Wise"
                    )

                if len(selected_months)==0:

                    st.warning(
                        "Select at least one month"
                    )

                else:

                    filtered_df = df[
                        df["MonthYear"]
                        .isin(selected_months)
                    ]

                    total_expense = filtered_df[
                        "Withdrawal Amt."
                    ].sum()

                    st.markdown(f"""
                    <div class='summary-box'>
                        <h3>
                        Total Selected Expense :
                        ₹ {total_expense}
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)

                    # CATEGORY

                    st.markdown(
                        "## Category Wise Comparison"
                    )

                    category_compare = (
                        filtered_df.groupby(
                            ["MonthYear","Category"]
                        )["Withdrawal Amt."]
                        .sum()
                        .reset_index()
                    )

                    category_fig = px.bar(
                        category_compare,
                        x="Category",
                        y="Withdrawal Amt.",
                        color="MonthYear",
                        barmode="group"
                    )

                    st.plotly_chart(
                        category_fig,
                        use_container_width=True
                    )

                    # MONTH

                    st.markdown(
                        "## Monthly Comparison"
                    )

                    month_compare = (
                        filtered_df.groupby(
                            "MonthYear"
                        )["Withdrawal Amt."]
                        .sum()
                        .reset_index()
                    )

                    month_fig = px.bar(
                        month_compare,
                        x="MonthYear",
                        y="Withdrawal Amt.",
                        color="MonthYear"
                    )

                    st.plotly_chart(
                        month_fig,
                        use_container_width=True
                    )

                    # WEEKLY

                    if show_weekly:

                        st.markdown(
                            "## Weekly Analysis"
                        )

                        weekly_df = (
                            filtered_df.groupby(
                                ["MonthYear","Week"]
                            )["Withdrawal Amt."]
                            .sum()
                            .reset_index()
                        )

                        weekly_fig = px.line(
                            weekly_df,
                            x="Week",
                            y="Withdrawal Amt.",
                            color="MonthYear",
                            markers=True
                        )

                        st.plotly_chart(
                            weekly_fig,
                            use_container_width=True
                        )

                    # DATE WISE

                    if show_datewise:

                        st.markdown(
                            "## Date Wise Analysis"
                        )

                        date_df = (
                            filtered_df.groupby(
                                ["Date","MonthYear"]
                            )["Withdrawal Amt."]
                            .sum()
                            .reset_index()
                        )

                        date_fig = px.line(
                            date_df,
                            x="Date",
                            y="Withdrawal Amt.",
                            color="MonthYear",
                            markers=True
                        )

                        st.plotly_chart(
                            date_fig,
                            use_container_width=True
                        )

                    # PIE

                    st.markdown(
                        "## Expense Distribution"
                    )

                    pie_df = (
                        filtered_df.groupby(
                            "Category"
                        )["Withdrawal Amt."]
                        .sum()
                        .reset_index()
                    )

                    pie_fig = px.pie(
                        pie_df,
                        names="Category",
                        values="Withdrawal Amt."
                    )

                    st.plotly_chart(
                        pie_fig,
                        use_container_width=True
                    )
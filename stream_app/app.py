import streamlit as st
from db import run_query
import pandas as pd

# Import all pages
from pages import (
    students_page,
    resources_page,
    loans_page,
    mentorship_page,
    borrow_requests_page,
    student_portal_page,
    student_dashboard
)

# ----------------------------
# App Configuration
# ----------------------------
st.set_page_config(page_title="University Resource & Alumni Hub", layout="wide")

st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #2b8a3e;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 University Resource & Alumni Hub")

# ----------------------------
# Role Selection / Login
# ----------------------------
st.sidebar.title("🔐 Login Panel")

role = st.sidebar.selectbox("Select your role", ["Select", "Admin", "Student"])

if role == "Select":
    st.info("Please choose a role from the sidebar to continue.")

# ----------------------------
# ADMIN VIEW
# ----------------------------
elif role == "Admin":
    st.sidebar.success("Logged in as Admin")

    page = st.sidebar.radio(
        "📂 Go to:",
        ["Dashboard", "Students", "Resources", "Loans", "Borrow Requests", "Mentorship Sessions"]
    )

    if page == "Dashboard":
        st.header("📊 Admin Dashboard Overview")

        # --- Top metrics ---
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Students", run_query("SELECT COUNT(*) AS c FROM Student")[0]['c'])
        col2.metric("Total Resources", run_query("SELECT COUNT(*) AS c FROM Resource")[0]['c'])
        col3.metric("Active Loans", run_query("SELECT COUNT(*) AS c FROM Loan WHERE Return_Date IS NULL")[0]['c'])
        col4.metric("Borrow Requests", run_query("SELECT COUNT(*) AS c FROM Borrow_Request")[0]['c'])
        col5.metric("Total Fines Collected", run_query("SELECT IFNULL(SUM(fn_calculate_fine(Due_Date, Return_Date)), 0) AS total_fine FROM Loan")[0]['total_fine'])

        st.markdown("---")

        # --- Overdue Loans Table ---
        st.subheader("📅 Overdue Loans (>14 days)")
        df = run_query('''SELECT Name, Student_ID
                        FROM Student
                        WHERE Student_ID IN (
                        SELECT Student_ID
                        FROM Loan
                        WHERE Return_Date IS NULL
                        AND CURDATE() > Due_Date
                        );''')
        st.dataframe(df, use_container_width=True)


    elif page == "Students":
        students_page.show()

    elif page == "Resources":
        resources_page.show()

    elif page == "Loans":
        loans_page.show()

    elif page == "Borrow Requests":
        borrow_requests_page.show()

    elif page == "Mentorship Sessions":
        mentorship_page.show()

# ----------------------------
# STUDENT VIEW
# ----------------------------
elif role == "Student":
    st.sidebar.success("Logged in as Student")

    # Simulate login by Student ID (simple input for demo)
    student_id = st.sidebar.number_input("Enter your Student ID", min_value=1, step=1)

    page = st.sidebar.radio(
        "🎓 Student Menu:",
        ["Dashboard", "Browse Resources"]
    )

    if page == "Dashboard":
        student_dashboard.show(student_id)

    elif page == "Browse Resources":
        student_portal_page.show(student_id)

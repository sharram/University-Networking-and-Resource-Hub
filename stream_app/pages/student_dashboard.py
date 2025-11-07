import streamlit as st
from db import run_query
import pandas as pd

def show(student_id):
    st.title("🎓 Student Dashboard")

    if not student_id:
        st.warning("Please enter your Student ID in the sidebar to view your dashboard.")
        return

    # Student Info
    student_info = run_query("SELECT * FROM Student WHERE Student_ID = %s", (student_id,))
    if not student_info:
        st.error("No student found with that ID.")
        return

    st.subheader(f"👋 Welcome, {student_info[0]['Name']}")

    # Active Borrowed Resources
    st.markdown("### 📚 Borrowed Resources")
    loans = run_query("""
        SELECT l.Loan_ID, r.Resource_Details, l.Issue_Date, l.Due_Date, l.Return_Date,
               fn_calculate_fine(l.Due_Date, l.Return_Date) AS Fine
        FROM Loan l
        JOIN Resource r ON l.Resource_ID = r.Resource_ID
        WHERE l.Student_ID = %s;
    """, (student_id,))

    if loans:
        st.dataframe(loans, use_container_width=True)
    else:
        st.info("You currently have no borrowed resources.")

    # Mentorship Sessions
    st.markdown("### 🤝 Mentorship Sessions")
    sessions = run_query("""
        CALL sp_view_student_sessions(%s);
    """, (student_id,))

    if sessions:
        st.dataframe(sessions, use_container_width=True)
    else:
        st.info("No mentorship sessions scheduled yet.")

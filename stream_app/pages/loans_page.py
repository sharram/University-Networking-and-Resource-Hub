import streamlit as st
from db import run_query
import pandas as pd

def show():
    st.title("💳 Loan Management")

    # 🔹 Display all active and completed loans
    st.subheader("📋 All Loans")
    df = run_query("""
        SELECT 
            l.Loan_ID, 
            s.Name AS Student, 
            r.Resource_Details, 
            l.Issue_Date, 
            l.Due_Date, 
            l.Return_Date,
            fn_calculate_fine(l.Due_Date, l.Return_Date) AS Fine
        FROM Loan l
        JOIN Student s ON l.Student_ID = s.Student_ID
        JOIN Resource r ON l.Resource_ID = r.Resource_ID
        ORDER BY l.Loan_ID DESC;
    """)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # 🔹 Mark a resource as returned
    st.subheader("📦 Mark Loan as Returned")

    loan_id = st.number_input("Enter Loan ID to mark as returned", min_value=1, step=1)

    if st.button("✅ Mark Returned"):
        try:
            run_query(
                "UPDATE Loan SET Return_Date = CURDATE() WHERE Loan_ID = %s",
                (loan_id,),
                fetch=False
            )
            st.success(f"Loan {loan_id} marked as returned successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")

    st.markdown("---")



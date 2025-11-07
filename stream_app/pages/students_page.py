import streamlit as st
from db import run_query
import pandas as pd
import datetime

def show():
    st.title("👩‍🎓 Student Management")

    st.subheader("All Students")
    df = run_query("SELECT * FROM Student;")
    st.dataframe(df)

    st.markdown("---")
    st.subheader("➕ Add New Student")

    with st.form("add_student"):
        name = st.text_input("Full Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        # ✅ Fixed date selector — allows older birthdates
        min_date = datetime.date(1980, 1, 1)
        max_date = datetime.date.today()
        dob = st.date_input("Date of Birth", min_value=min_date, max_value=max_date)
        year = st.number_input("Year of Study", min_value=1, max_value=6)
        courses = st.text_input("Previous Courses")
        phone = st.text_input("Contact Number")
        submit = st.form_submit_button("Add Student")

        if submit:
            run_query(
                "INSERT INTO Student (Name, Gender, DOB, Year_Of_Study, Previous_Courses, Contact_No) VALUES (%s,%s,%s,%s,%s,%s)",
                (name, gender, dob, year, courses, phone),
                fetch=False
            )
            st.success(f"✅ Added {name} successfully!")
            st.rerun()

    st.markdown("---")
    st.subheader("❌ Delete Student")

    delete_id = st.number_input("Enter Student ID to delete", min_value=1)
    if st.button("Delete Student"):
        run_query("DELETE FROM Student WHERE Student_ID = %s", (delete_id,), fetch=False)
        st.warning(f"🗑️ Student ID {delete_id} deleted.")
        st.rerun()

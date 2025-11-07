import streamlit as st 
from db import run_query 
import pandas as pd 
def show(): 
    st.title("🤝 Mentorship Sessions") 
    st.subheader("All Sessions") 
    df = run_query(""" 
                   SELECT m.Session_ID, s.Name AS Student, 
                   a.Name AS Alumni, m.Date, m.Time, m.Mode, 
                   m.Duration FROM Mentorship_Session m JOIN Student s ON m.Student_ID = s.Student_ID 
                   JOIN Alumni a ON m.Alumni_ID = a.Alumni_ID; """) 
    st.dataframe(df) 
    st.markdown("---") 
    st.subheader("📅 Schedule New Session") 
    with st.form("add_session"): 
        student_id = st.number_input("Student ID", min_value=1) 
        alumni_id = st.number_input("Alumni ID", min_value=1) 
        date = st.date_input("Date") 
        time = st.time_input("Time") 
        mode = st.selectbox("Mode", ["Online", "Offline", "Hybrid"]) 
        duration = st.number_input("Duration (minutes)", min_value=15, max_value=240) 
        submit = st.form_submit_button("Schedule Session") 
        if submit: 
            run_query( "CALL sp_schedule_mentorship(%s,%s,%s,%s,%s,%s)", (student_id, alumni_id, date, time, mode, duration), fetch=False ) 
            st.success("✅ Mentorship session scheduled successfully!") 
            st.rerun() 
            st.markdown("---") 
            st.subheader("❌ Delete Mentorship Session") 
            delete_id = st.number_input("Enter Session ID to delete", min_value=1) 
            if st.button("Delete Session"): 
                run_query("DELETE FROM Mentorship_Session WHERE Session_ID = %s", (delete_id,), fetch=False) 
                st.warning(f"🗑️ Session ID {delete_id} deleted.") 
                st.rerun()
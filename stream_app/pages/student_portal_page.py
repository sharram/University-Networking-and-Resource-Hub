import streamlit as st
from db import run_query
import pandas as pd

def show(student_id):
    st.title("📚 Browse & Request Resources")

    # -------------------------
    # Display available resources
    # -------------------------
    st.subheader("Available Resources")
    df = run_query("""
        SELECT 
            Resource_ID,
            Type,
            Resource_Details,
            Condition_Status,
            Availability_Status,
            Tag
        FROM Resource
        WHERE Availability_Status = 'Available';
    """)

    if not df:
        st.info("No resources available right now.")
    else:
        st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # -------------------------
    # Borrow Request Form
    # -------------------------
    st.subheader("📝 Request to Borrow a Resource")

    with st.form("borrow_request_form"):
        resource_id = st.number_input("Enter Resource ID you want to borrow", min_value=1)
        submit = st.form_submit_button("Submit Borrow Request")

        if submit:
            # Check if the resource exists and is available
            check = run_query("SELECT Availability_Status FROM Resource WHERE Resource_ID=%s;", (resource_id,))
            if not check:
                st.error("❌ Resource not found.")
            elif check[0]["Availability_Status"] != "Available":
                st.warning("⚠️ This resource is not currently available.")
            else:
                # Insert borrow request
                run_query(
                    "INSERT INTO Borrow_Request (Student_ID, Resource_ID) VALUES (%s,%s);",
                    (student_id, resource_id),
                    fetch=False
                )
                st.success(f"✅ Borrow request submitted for Resource ID {resource_id}.")
                st.info("Your request will be reviewed by an Admin.")
                st.rerun()

import streamlit as st
from db import run_query
import pandas as pd

def show():
    st.title("📚 Resource Inventory")

    st.subheader("All Resources")
    df = run_query("SELECT * FROM Resource;")
    st.dataframe(df)

    st.markdown("---")
    st.subheader("➕ Add New Resource")

    with st.form("add_resource"):
        type_ = st.text_input("Type (Book/Laptop/Project Report)")
        condition = st.selectbox("Condition", ["New", "Good", "Fair", "Poor"])
        details = st.text_area("Resource Details")
        tag = st.text_input("Tag (e.g. DBMS, AI)")
        admin_id = st.number_input("Admin ID", min_value=1)
        submit = st.form_submit_button("Add Resource")

        if submit:
            run_query(
                "INSERT INTO Resource (Type, Condition_Status, Resource_Details, Tag, Admin_ID) VALUES (%s,%s,%s,%s,%s)",
                (type_, condition, details, tag, admin_id),
                fetch=False
            )
            st.success(f"✅ Added {type_} resource successfully!")
            st.rerun()

    st.markdown("---")
    st.subheader("❌ Delete Resource")

    delete_id = st.number_input("Enter Resource ID to delete", min_value=1)
    if st.button("Delete Resource"):
        run_query("DELETE FROM Resource WHERE Resource_ID = %s", (delete_id,), fetch=False)
        st.warning(f"🗑️ Resource ID {delete_id} deleted.")
        st.rerun()

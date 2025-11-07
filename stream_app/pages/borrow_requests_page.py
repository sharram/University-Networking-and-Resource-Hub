import streamlit as st
from db import run_query
import pandas as pd

def show():
    st.title("📬 Borrow Request Management")

    # 🔹 Filter by status
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Pending", "Approved", "Rejected"],
        index=0
    )

    # Build query dynamically
    query = """
        SELECT 
            br.Request_ID,
            s.Name AS Student,
            r.Resource_Details AS Resource,
            br.Status,
            br.Request_Date
        FROM Borrow_Request br
        JOIN Student s ON br.Student_ID = s.Student_ID
        JOIN Resource r ON br.Resource_ID = r.Resource_ID
    """
    if status_filter != "All":
        query += f" WHERE br.Status = '{status_filter}'"
    query += " ORDER BY br.Request_ID DESC;"

    df = run_query(query)

    if not df:
        st.info("No borrow requests found.")
    else:
        # Add color-coded status labels
        def color_status(status):
            if status == "Approved":
                return "🟢 Approved"
            elif status == "Rejected":
                return "🔴 Rejected"
        for d in df:
            d["Status"] = color_status(d["Status"])
        st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # 🔹 Approve / Reject requests
    st.subheader("⚙️ Manage Requests")

    with st.form("manage_requests"):
        request_id = st.number_input("Enter Request ID", min_value=1)
        admin_id = st.number_input("Enter Your Admin ID", min_value=1)
        col1, col2 = st.columns(2)
        approve = col1.form_submit_button("✅ Approve Request")
        reject = col2.form_submit_button("❌ Reject Request")

        if approve:
            try:
                run_query("CALL sp_approve_borrow_request(%s, %s)", (request_id, admin_id), fetch=False)
                st.success(f"✅ Request {request_id} approved successfully!")
                st.info("Resource status updated and loan created automatically.")
                st.rerun()
            except Exception as e:
                st.error(f"Error approving request: {e}")

        elif reject:
            try:
                run_query("CALL sp_reject_borrow_request(%s)", (request_id,), fetch=False)
                st.warning(f"❌ Request {request_id} rejected.")
                st.rerun()
            except Exception as e:
                st.error(f"Error rejecting request: {e}")

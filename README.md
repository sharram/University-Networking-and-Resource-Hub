# 🎓 University Networking & Resource Hub

## 📘 Project Overview
The **University Networking & Resource Hub** is a web-based platform that enables students to share resources (books, lab equipment, etc.) and connect with alumni for mentorship.  
It manages borrowing requests, tracks loans and returns, schedules mentorship sessions, gathers feedback, and promotes efficient resource utilization and knowledge exchange within the academic community.

---

## 🧠 Key Features
- **Student & Alumni Profiles** — Manage student and alumni information.  
- **Resource Library** — Add, view, update, delete resources; track availability and condition.  
- **Borrow Request Flow** — Students submit requests; admin approves or rejects via stored procedures and triggers.  
- **Loan Management** — Loans are created automatically, due dates are calculated, and returns update availability and fines.  
- **Mentorship Scheduling** — Students connect with alumni and schedule sessions via stored procedures.  
- **Database Automation** — Implements MySQL triggers, stored procedures, and functions for backend workflows.  
- **Interactive UI** — Built with Streamlit for an intuitive, fast, and responsive design.

---

## ⚙️ Technology Stack

| Layer | Technology Used |
|-------|------------------|
| **Frontend** | Streamlit (Python) |
| **Backend DB** | MySQL |
| **Language** | Python 3.12 |
| **Libraries** | mysql-connector-python, pandas, python-dotenv |
| **Tools/IDE** | Visual Studio Code, MySQL Workbench |
| **Version Control** | Git & GitHub |

---

## 🗄️ Database Design & Concepts

### Key Entities
- Student  
- Alumni  
- Resource  
- Borrow_Request  
- Loan  
- Mentorship_Session  
- Admin  

### Core Database Components
- **Triggers** — Automatically set due dates and update resource availability.  
- **Stored Procedures** — Approve or reject borrow requests; schedule mentorship sessions.  
- **Functions** — Calculate fines for late returns.  
- **Queries** — Include nested subqueries, aggregate functions, and joins for analytics and reports.

---

| Name               | Role                          | USN           |
| ------------------ | ----------------------------- | ------------- |
| **Sharvari V Ram** | Developer & Database Designer | PES1UG23AM281 |
| **Shraddha Rao**   | Developer & UI Designer       | PES1UG23AM289   |




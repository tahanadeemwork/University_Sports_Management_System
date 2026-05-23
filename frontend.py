# frontend.py
# Streamlit Frontend - University Sports Management System

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, time, datetime

# ============================================================
# PAGE CONFIGURATION — Must be the FIRST Streamlit call
# ============================================================

st.set_page_config(
    page_title="University Sports Management System",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SAFE IMPORTS - Database and Backend
# ============================================================

try:
    from database_connection import db
    _DB_IMPORT_OK = True
    _DB_IMPORT_ERROR = None
except Exception as e:
    _DB_IMPORT_OK = False
    _DB_IMPORT_ERROR = str(e)
    db = None

try:
    from backend import services
    _BACKEND_IMPORT_OK = True
    _BACKEND_IMPORT_ERROR = None
except Exception as e:
    _BACKEND_IMPORT_OK = False
    _BACKEND_IMPORT_ERROR = str(e)
    services = None

# Show import errors and stop if critical files are missing
if not _DB_IMPORT_OK:
    st.error(f"❌ Failed to import database_connection.py: {_DB_IMPORT_ERROR}")
    st.info("Make sure database_connection.py is in the same folder as frontend.py")
    st.stop()

if not _BACKEND_IMPORT_OK:
    st.error(f"❌ Failed to import backend.py: {_BACKEND_IMPORT_ERROR}")
    st.info("Make sure backend.py is in the same folder as frontend.py")
    st.stop()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
        padding: 10px 0;
        border-bottom: 3px solid #4CAF50;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1E3A5F;
        border-left: 4px solid #4CAF50;
        padding-left: 10px;
        margin: 15px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E3A5F, #2E6DA4);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 5px;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-msg {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .sidebar-menu {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def show_success(msg):
    st.success(f"✅ {msg}")


def show_error(msg):
    st.error(f"❌ {msg}")


def show_warning(msg):
    st.warning(f"⚠️ {msg}")


def show_info(msg):
    st.info(f"ℹ️ {msg}")


def display_dataframe(df, title=None):
    """Display a dataframe with optional title"""
    if title:
        st.markdown(f'<p class="section-header">{title}</p>', unsafe_allow_html=True)
    if df is None or df.empty:
        show_info("No records found.")
        return
    st.dataframe(df, use_container_width=True, hide_index=True)


def check_connection():
    """Check and display connection status"""
    if not db.is_connected():
        success, msg = db.connect()
        if not success:
            st.error(f"❌ Database Connection Failed: {msg}")
            st.info("Go to **🔌 DB Connection** page to troubleshoot.")
            st.stop()


# ============================================================
# DATABASE CONNECTION PAGE
# ============================================================

def page_db_connection():
    st.markdown('<p class="main-header">🔌 Database Connection</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Connection Settings")
        st.markdown("""
        Edit `database_connection.py` to configure:
        - **Server**: Your SQL Server name
        - **Database**: UniversitySportsDB  
        - **Authentication**: Windows or SQL Server
        """)

        st.markdown("### Current Settings")
        st.code(f"""
Server: {db.server}
Database: {db.database}
Driver: {db.driver}
Auth: {'Windows (Trusted)' if db.trusted_connection == 'yes' else 'SQL Server Auth'}
        """, language="text")

    with col2:
        st.markdown("### Test Connection")
        st.markdown("Click the button below to test your database connection:")

        if st.button("🔗 Test Connection", use_container_width=True, type="primary"):
            with st.spinner("Testing connection..."):
                success, msg = db.test_connection()
            if success:
                show_success(msg)
                st.balloons()
            else:
                show_error(msg)
                st.markdown("""
                **Troubleshooting:**
                1. Make sure SQL Server is running
                2. Check server name (try `localhost`, `.\\SQLEXPRESS`, or `(local)`)
                3. Ensure ODBC Driver 17 for SQL Server is installed
                4. Verify UniversitySportsDB exists
                5. Check firewall settings
                """)

        if db.is_connected():
            st.markdown("### Connection Status")
            st.success("🟢 **Connected** to UniversitySportsDB")
        else:
            st.info("🔴 **Not Connected** - Click Test Connection above")


# ============================================================
# DASHBOARD PAGE
# ============================================================

def page_dashboard():
    st.markdown('<p class="main-header">🏆 University Sports Management System</p>', unsafe_allow_html=True)
    check_connection()

    stats = services.dashboard.get_summary_stats()

    st.markdown("### 📊 System Overview")

    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        (col1, "👨‍🎓 Students", stats.get('total_students', 0), "#1E88E5"),
        (col2, "🏋️ Coaches", stats.get('total_coaches', 0), "#43A047"),
        (col3, "⚽ Teams", stats.get('total_teams', 0), "#FB8C00"),
        (col4, "🏆 Tournaments", stats.get('total_tournaments', 0), "#8E24AA"),
        (col5, "🎯 Matches", stats.get('total_matches', 0), "#E53935"),
    ]
    for col, label, value, color in metrics:
        with col:
            st.metric(label=label, value=value)

    col6, col7, col8 = st.columns(3)
    with col6:
        st.metric("🏅 Sports", stats.get('total_sports', 0))
    with col7:
        st.metric("🔔 Unread Alerts", stats.get('unread_reminders', 0))
    with col8:
        st.metric("🤕 Active Injuries", stats.get('active_injuries', 0))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏅 Players per Sport")
        df_sport, err = services.dashboard.get_sports_distribution()
        if df_sport is not None and not df_sport.empty:
            fig = px.pie(df_sport, values='PlayerCount', names='SportName',
                         color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🏆 Tournament Status")
        df_tourn, err = services.dashboard.get_tournament_status_summary()
        if df_tourn is not None and not df_tourn.empty:
            fig = px.bar(df_tourn, x='Status', y='Count',
                         color='Status', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 💰 Expenses by Category")
        df_exp, err = services.dashboard.get_expense_by_category()
        if df_exp is not None and not df_exp.empty:
            fig = px.bar(df_exp, x='Category', y='TotalAmount',
                         color='Category', color_discrete_sequence=px.colors.qualitative.Set1)
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("### 📋 Attendance Summary")
        df_att, err = services.dashboard.get_attendance_summary()
        if df_att is not None and not df_att.empty:
            colors = {'Present': '#4CAF50', 'Absent': '#F44336', 'Late': '#FF9800'}
            fig = px.pie(df_att, values='Count', names='Status',
                         color='Status', color_discrete_map=colors)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col5, col6 = st.columns(2)

    with col5:
        st.markdown("### 🎯 Recent Matches")
        df_matches, err = services.dashboard.get_recent_matches(5)
        if df_matches is not None and not df_matches.empty:
            st.dataframe(df_matches, use_container_width=True, hide_index=True)
        else:
            show_info("No recent matches found.")

    with col6:
        st.markdown("### ⭐ Top Scorers")
        df_scorers, err = services.dashboard.get_top_scorers(5)
        if df_scorers is not None and not df_scorers.empty:
            st.dataframe(df_scorers, use_container_width=True, hide_index=True)
        else:
            show_info("No performance data found.")

    st.markdown("### 🏛️ Department Performance")
    df_dept, err = services.dashboard.get_department_performance()
    if df_dept is not None and not df_dept.empty:
        fig = px.bar(df_dept, x='DepartmentName',
                     y=['TotalWins', 'TotalLosses'],
                     barmode='group',
                     color_discrete_map={'TotalWins': '#4CAF50', 'TotalLosses': '#F44336'},
                     labels={'value': 'Count', 'variable': 'Type'})
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# DEPARTMENTS PAGE
# ============================================================

def page_departments():
    st.markdown('<p class="main-header">🏛️ Departments Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "✏️ Edit / Delete"])

    with tab1:
        st.markdown("### All Departments")
        df, err = services.departments.get_all_departments()
        if err:
            show_error(err)
        else:
            display_dataframe(df)

    with tab2:
        st.markdown("### Add New Department")
        with st.form("add_dept_form"):
            col1, col2 = st.columns(2)
            with col1:
                dept_name = st.text_input("Department Name *", placeholder="e.g., Computer Science")
                dean_name = st.text_input("Dean Name", placeholder="Dr. John Smith")
            with col2:
                contact_email = st.text_input("Contact Email", placeholder="dept@university.edu")
                established_year = st.number_input("Established Year",
                                                   min_value=1900, max_value=date.today().year,
                                                   value=2000)

            submitted = st.form_submit_button("➕ Add Department", type="primary", use_container_width=True)
            if submitted:
                if not dept_name:
                    show_error("Department Name is required!")
                else:
                    success, msg = services.departments.add_department(
                        dept_name, dean_name, contact_email, established_year
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        st.markdown("### Edit / Delete Department")
        df, err = services.departments.get_all_departments()
        if err or df is None or df.empty:
            show_info("No departments to edit.")
            return

        dept_options = dict(zip(df['DepartmentName'], df['DepartmentID']))
        selected_name = st.selectbox("Select Department", list(dept_options.keys()))

        if selected_name:
            selected_id = dept_options[selected_name]
            row = df[df['DepartmentID'] == selected_id].iloc[0]

            col1, col2 = st.columns([3, 1])
            with col1:
                with st.form("edit_dept_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        new_name = st.text_input("Department Name", value=str(row['DepartmentName']))
                        new_dean = st.text_input("Dean Name", value=str(row['DeanName'] or ''))
                    with c2:
                        new_email = st.text_input("Contact Email", value=str(row['ContactEmail'] or ''))
                        new_year = st.number_input("Established Year",
                                                   min_value=1900, max_value=date.today().year,
                                                   value=int(row['EstablishedYear'] or 2000))

                    if st.form_submit_button("💾 Update Department", type="primary", use_container_width=True):
                        success, msg = services.departments.update_department(
                            selected_id, new_name, new_dean, new_email, new_year
                        )
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)

            with col2:
                st.markdown("### ⚠️ Delete")
                if st.button(f"🗑️ Delete '{selected_name}'",
                             type="secondary", use_container_width=True):
                    st.session_state['confirm_delete_dept'] = selected_id

                if st.session_state.get('confirm_delete_dept') == selected_id:
                    st.warning("Are you sure?")
                    if st.button("✅ Yes, Delete", type="primary", use_container_width=True):
                        success, msg = services.departments.delete_department(selected_id)
                        if success:
                            show_success(msg)
                            del st.session_state['confirm_delete_dept']
                            st.rerun()
                        else:
                            show_error(msg)


# ============================================================
# SPORTS PAGE
# ============================================================

def page_sports():
    st.markdown('<p class="main-header">⚽ Sports Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "✏️ Edit / Delete"])

    with tab1:
        df, err = services.sports.get_all_sports()
        if err:
            show_error(err)
        else:
            display_dataframe(df, "All Sports")

    with tab2:
        st.markdown("### Add New Sport")
        with st.form("add_sport_form"):
            col1, col2 = st.columns(2)
            with col1:
                sport_name = st.text_input("Sport Name *", placeholder="e.g., Cricket")
                sport_type = st.selectbox("Sport Type *", ["Team", "Individual"])
            with col2:
                description = st.text_area("Description", placeholder="Brief description of the sport")

            if st.form_submit_button("➕ Add Sport", type="primary", use_container_width=True):
                if not sport_name:
                    show_error("Sport Name is required!")
                else:
                    success, msg = services.sports.add_sport(sport_name, sport_type, description)
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        df, err = services.sports.get_all_sports()
        if err or df is None or df.empty:
            show_info("No sports to edit.")
            return

        sport_options = dict(zip(df['SportName'], df['SportID']))
        selected_name = st.selectbox("Select Sport", list(sport_options.keys()))

        if selected_name:
            selected_id = sport_options[selected_name]
            row = df[df['SportID'] == selected_id].iloc[0]

            col1, col2 = st.columns([3, 1])
            with col1:
                with st.form("edit_sport_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        new_name = st.text_input("Sport Name", value=str(row['SportName']))
                        type_options = ["Team", "Individual"]
                        current_type = str(row['SportType']) if row['SportType'] else "Team"
                        type_idx = type_options.index(current_type) if current_type in type_options else 0
                        new_type = st.selectbox("Sport Type", type_options, index=type_idx)
                    with c2:
                        new_desc = st.text_area("Description", value=str(row['Description'] or ''))

                    if st.form_submit_button("💾 Update Sport", type="primary", use_container_width=True):
                        success, msg = services.sports.update_sport(selected_id, new_name, new_type, new_desc)
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)

            with col2:
                st.markdown("### ⚠️ Delete")
                if st.button(f"🗑️ Delete '{selected_name}'", type="secondary", use_container_width=True):
                    success, msg = services.sports.delete_sport(selected_id)
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)


# ============================================================
# VENUES PAGE
# ============================================================

def page_venues():
    st.markdown('<p class="main-header">🏟️ Venues Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "✏️ Edit / Delete"])

    with tab1:
        df, err = services.venues.get_all_venues()
        if err:
            show_error(err)
        else:
            display_dataframe(df, "All Venues")

    with tab2:
        st.markdown("### Add New Venue")
        with st.form("add_venue_form"):
            col1, col2 = st.columns(2)
            with col1:
                venue_name = st.text_input("Venue Name *", placeholder="e.g., Main Cricket Ground")
                location = st.text_input("Location", placeholder="e.g., Block A")
            with col2:
                capacity = st.number_input("Capacity", min_value=0, max_value=100000, value=500)
                venue_type = st.selectbox("Venue Type", ["Indoor", "Outdoor"])

            if st.form_submit_button("➕ Add Venue", type="primary", use_container_width=True):
                if not venue_name:
                    show_error("Venue Name is required!")
                else:
                    success, msg = services.venues.add_venue(venue_name, location, capacity, venue_type)
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        df, err = services.venues.get_all_venues()
        if err or df is None or df.empty:
            show_info("No venues to edit.")
            return

        venue_opts = dict(zip(df['VenueName'], df['VenueID']))
        sel_name = st.selectbox("Select Venue", list(venue_opts.keys()))

        if sel_name:
            sel_id = venue_opts[sel_name]
            row = df[df['VenueID'] == sel_id].iloc[0]

            col1, col2 = st.columns([3, 1])
            with col1:
                with st.form("edit_venue_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        new_name = st.text_input("Venue Name", value=str(row['VenueName']))
                        new_loc = st.text_input("Location", value=str(row['Location'] or ''))
                    with c2:
                        new_cap = st.number_input("Capacity", min_value=0, value=int(row['Capacity'] or 0))
                        vt_opts = ["Indoor", "Outdoor"]
                        cur_vt = str(row['VenueType']) if row['VenueType'] else "Indoor"
                        vt_idx = vt_opts.index(cur_vt) if cur_vt in vt_opts else 0
                        new_vt = st.selectbox("Venue Type", vt_opts, index=vt_idx)

                    if st.form_submit_button("💾 Update Venue", type="primary", use_container_width=True):
                        success, msg = services.venues.update_venue(sel_id, new_name, new_loc, new_cap, new_vt)
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)
            with col2:
                st.markdown("### ⚠️ Delete")
                if st.button(f"🗑️ Delete", type="secondary", use_container_width=True):
                    success, msg = services.venues.delete_venue(sel_id)
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)


# ============================================================
# SEMESTERS PAGE
# ============================================================

def page_semesters():
    st.markdown('<p class="main-header">📅 Semesters Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "✏️ Edit / Delete"])

    with tab1:
        df, err = services.semesters.get_all_semesters()
        if err:
            show_error(err)
        else:
            display_dataframe(df, "All Semesters")

    with tab2:
        with st.form("add_sem_form"):
            col1, col2 = st.columns(2)
            with col1:
                sem_name = st.text_input("Semester Name *", placeholder="Fall 2024")
                start_date = st.date_input("Start Date *", value=date.today())
            with col2:
                academic_year = st.text_input("Academic Year", placeholder="2024-2025")
                end_date = st.date_input("End Date *", value=date.today())

            if st.form_submit_button("➕ Add Semester", type="primary", use_container_width=True):
                if not sem_name:
                    show_error("Semester Name is required!")
                elif end_date < start_date:
                    show_error("End date must be after start date!")
                else:
                    success, msg = services.semesters.add_semester(
                        sem_name, start_date, end_date, academic_year
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        df, err = services.semesters.get_all_semesters()
        if err or df is None or df.empty:
            show_info("No semesters to edit.")
            return

        sem_opts = dict(zip(df['SemesterName'], df['SemesterID']))
        sel_name = st.selectbox("Select Semester", list(sem_opts.keys()))

        if sel_name:
            sel_id = sem_opts[sel_name]
            row = df[df['SemesterID'] == sel_id].iloc[0]

            with st.form("edit_sem_form"):
                c1, c2 = st.columns(2)
                with c1:
                    new_name = st.text_input("Semester Name", value=str(row['SemesterName']))
                    new_start = st.date_input("Start Date",
                                              value=pd.to_datetime(row['StartDate']).date())
                with c2:
                    new_acad = st.text_input("Academic Year", value=str(row['AcademicYear'] or ''))
                    new_end = st.date_input("End Date",
                                            value=pd.to_datetime(row['EndDate']).date())

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.form_submit_button("💾 Update Semester", type="primary", use_container_width=True):
                        success, msg = services.semesters.update_semester(
                            sel_id, new_name, new_start, new_end, new_acad
                        )
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)
                with col_b:
                    if st.form_submit_button("🗑️ Delete Semester", type="secondary", use_container_width=True):
                        success, msg = services.semesters.delete_semester(sel_id)
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)


# ============================================================
# STUDENTS PAGE
# ============================================================

def page_students():
    st.markdown('<p class="main-header">👨‍🎓 Students Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "🔍 Search", "➕ Add New", "✏️ Edit / Delete"])

    with tab1:
        df, err = services.students.get_all_students()
        if err:
            show_error(err)
        else:
            display_dataframe(df, f"All Students ({len(df) if df is not None else 0} records)")

    with tab2:
        st.markdown("### Search Students")
        search_term = st.text_input("Search by Name or Registration No", placeholder="Enter search term...")
        if search_term:
            df, err = services.students.search_students(search_term)
            if err:
                show_error(err)
            else:
                display_dataframe(df, f"Search Results ({len(df) if df is not None else 0} found)")

    with tab3:
        st.markdown("### Add New Student")
        dept_opts = services.departments.get_department_options()
        sem_opts = services.semesters.get_semester_options()

        if not dept_opts:
            show_warning("Please add departments first!")
            return
        if not sem_opts:
            show_warning("Please add semesters first!")
            return

        with st.form("add_student_form"):
            col1, col2 = st.columns(2)
            with col1:
                reg_no = st.text_input("Registration No *", placeholder="CS-2024-001")
                full_name = st.text_input("Full Name *", placeholder="John Doe")
                gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
                dob = st.date_input("Date of Birth", value=date(2000, 1, 1))
                contact = st.text_input("Contact No", placeholder="0300-1234567")
            with col2:
                email = st.text_input("Email", placeholder="john@university.edu")
                address = st.text_area("Address", placeholder="City, Country")
                enrollment_year = st.number_input("Enrollment Year",
                                                  min_value=2000, max_value=date.today().year,
                                                  value=date.today().year)
                dept_name = st.selectbox("Department *", list(dept_opts.keys()))
                sem_name = st.selectbox("Semester *", list(sem_opts.keys()))

            if st.form_submit_button("➕ Add Student", type="primary", use_container_width=True):
                if not reg_no or not full_name:
                    show_error("Registration No and Full Name are required!")
                else:
                    success, msg = services.students.add_student(
                        reg_no, full_name, gender, dob, contact, email,
                        address, enrollment_year, dept_opts[dept_name], sem_opts[sem_name]
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab4:
        df, err = services.students.get_all_students()
        if err or df is None or df.empty:
            show_info("No students to edit.")
            return

        dept_opts = services.departments.get_department_options()
        sem_opts = services.semesters.get_semester_options()

        student_opts = dict(zip(
            df['FullName'] + ' (' + df['RegistrationNo'] + ')',
            df['StudentID']
        ))
        sel_display = st.selectbox("Select Student", list(student_opts.keys()))

        if sel_display:
            sel_id = student_opts[sel_display]
            row_df, _ = services.students.get_by_id("Student", "StudentID", sel_id)
            if row_df is not None and not row_df.empty:
                row = row_df.iloc[0]

                col1, col2 = st.columns([3, 1])
                with col1:
                    with st.form("edit_student_form"):
                        c1, c2 = st.columns(2)
                        with c1:
                            new_reg = st.text_input("Registration No", value=str(row['RegistrationNo']))
                            new_name = st.text_input("Full Name", value=str(row['FullName']))
                            gender_opts = ["Male", "Female", "Other"]
                            g_idx = gender_opts.index(str(row['Gender'])) if row['Gender'] in gender_opts else 0
                            new_gender = st.selectbox("Gender", gender_opts, index=g_idx)
                            new_dob = st.date_input("Date of Birth",
                                                    value=pd.to_datetime(row['DateOfBirth']).date()
                                                    if row['DateOfBirth'] else date(2000, 1, 1))
                            new_contact = st.text_input("Contact No", value=str(row['ContactNo'] or ''))
                        with c2:
                            new_email = st.text_input("Email", value=str(row['Email'] or ''))
                            new_address = st.text_area("Address", value=str(row['Address'] or ''))
                            new_year = st.number_input("Enrollment Year",
                                                       min_value=2000, max_value=date.today().year,
                                                       value=int(row['EnrollmentYear'] or 2024))
                            new_dept = st.selectbox("Department", list(dept_opts.keys()))
                            new_sem = st.selectbox("Semester", list(sem_opts.keys()))

                        if st.form_submit_button("💾 Update Student", type="primary", use_container_width=True):
                            success, msg = services.students.update_student(
                                sel_id, new_reg, new_name, new_gender, new_dob,
                                new_contact, new_email, new_address, new_year,
                                dept_opts[new_dept], sem_opts[new_sem]
                            )
                            if success:
                                show_success(msg)
                                st.rerun()
                            else:
                                show_error(msg)

                with col2:
                    st.markdown("### ⚠️ Delete")
                    if st.button("🗑️ Delete Student", type="secondary", use_container_width=True):
                        success, msg = services.students.delete_student(sel_id)
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)


# ============================================================
# COACHES PAGE
# ============================================================

def page_coaches():
    st.markdown('<p class="main-header">🏋️ Coaches Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "✏️ Edit / Delete"])

    with tab1:
        df, err = services.coaches.get_all_coaches()
        if err:
            show_error(err)
        else:
            display_dataframe(df, "All Coaches")

    with tab2:
        dept_opts = services.departments.get_department_options()
        sport_opts = services.sports.get_sport_options()

        if not dept_opts or not sport_opts:
            show_warning("Please add departments and sports first!")
            return

        with st.form("add_coach_form"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name *", placeholder="Coach Name")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                contact = st.text_input("Contact No", placeholder="0310-1234567")
                email = st.text_input("Email", placeholder="coach@uni.edu")
            with col2:
                qualification = st.text_input("Qualification", placeholder="MSc Sports Science")
                exp_years = st.number_input("Experience Years", min_value=0, max_value=50, value=5)
                dept_name = st.selectbox("Department *", list(dept_opts.keys()))
                sport_name = st.selectbox("Sport *", list(sport_opts.keys()))

            if st.form_submit_button("➕ Add Coach", type="primary", use_container_width=True):
                if not full_name:
                    show_error("Full Name is required!")
                else:
                    success, msg = services.coaches.add_coach(
                        full_name, gender, contact, email, qualification,
                        exp_years, dept_opts[dept_name], sport_opts[sport_name]
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        df, err = services.coaches.get_all_coaches()
        if err or df is None or df.empty:
            show_info("No coaches to edit.")
            return

        dept_opts = services.departments.get_department_options()
        sport_opts = services.sports.get_sport_options()

        coach_opts = dict(zip(df['FullName'], df['CoachID']))
        sel_name = st.selectbox("Select Coach", list(coach_opts.keys()))

        if sel_name:
            sel_id = coach_opts[sel_name]
            row_df, _ = services.coaches.get_by_id("Coach", "CoachID", sel_id)
            if row_df is not None and not row_df.empty:
                row = row_df.iloc[0]

                col1, col2 = st.columns([3, 1])
                with col1:
                    with st.form("edit_coach_form"):
                        c1, c2 = st.columns(2)
                        with c1:
                            new_name = st.text_input("Full Name", value=str(row['FullName']))
                            g_opts = ["Male", "Female", "Other"]
                            g_idx = g_opts.index(str(row['Gender'])) if row['Gender'] in g_opts else 0
                            new_gender = st.selectbox("Gender", g_opts, index=g_idx)
                            new_contact = st.text_input("Contact", value=str(row['ContactNo'] or ''))
                            new_email = st.text_input("Email", value=str(row['Email'] or ''))
                        with c2:
                            new_qual = st.text_input("Qualification", value=str(row['Qualification'] or ''))
                            new_exp = st.number_input("Experience Years", min_value=0,
                                                      value=int(row['ExperienceYears'] or 0))
                            new_dept = st.selectbox("Department", list(dept_opts.keys()))
                            new_sport = st.selectbox("Sport", list(sport_opts.keys()))

                        if st.form_submit_button("💾 Update Coach", type="primary", use_container_width=True):
                            success, msg = services.coaches.update_coach(
                                sel_id, new_name, new_gender, new_contact, new_email,
                                new_qual, new_exp, dept_opts[new_dept], sport_opts[new_sport]
                            )
                            if success:
                                show_success(msg)
                                st.rerun()
                            else:
                                show_error(msg)

                with col2:
                    st.markdown("### ⚠️ Delete")
                    if st.button("🗑️ Delete Coach", type="secondary", use_container_width=True):
                        success, msg = services.coaches.delete_coach(sel_id)
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)


# ============================================================
# TEAMS PAGE
# ============================================================

def page_teams():
    st.markdown('<p class="main-header">👥 Teams Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "➕ Add New", "✏️ Edit / Delete", "👤 Players"])

    with tab1:
        df, err = services.teams.get_all_teams()
        if err:
            show_error(err)
        else:
            display_dataframe(df, "All Teams")

    with tab2:
        dept_opts = services.departments.get_department_options()
        sport_opts = services.sports.get_sport_options()
        coach_opts = services.coaches.get_coach_options()
        coach_opts_with_none = {"-- No Coach --": None}
        coach_opts_with_none.update(coach_opts)

        with st.form("add_team_form"):
            col1, col2 = st.columns(2)
            with col1:
                team_name = st.text_input("Team Name *", placeholder="CS Cricket XI")
                gender = st.selectbox("Gender", ["Male", "Female", "Mixed"])
                formation_year = st.number_input("Formation Year",
                                                 min_value=2000, max_value=date.today().year,
                                                 value=date.today().year)
            with col2:
                dept_name = st.selectbox("Department *", list(dept_opts.keys()))
                sport_name = st.selectbox("Sport *", list(sport_opts.keys()))
                coach_name = st.selectbox("Coach", list(coach_opts_with_none.keys()))

            if st.form_submit_button("➕ Add Team", type="primary", use_container_width=True):
                if not team_name:
                    show_error("Team Name is required!")
                else:
                    coach_id = coach_opts_with_none[coach_name]
                    success, msg = services.teams.add_team(
                        team_name, gender, formation_year,
                        dept_opts[dept_name], sport_opts[sport_name], coach_id
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        df, err = services.teams.get_all_teams()
        if err or df is None or df.empty:
            show_info("No teams to edit.")
            return

        dept_opts = services.departments.get_department_options()
        sport_opts = services.sports.get_sport_options()
        coach_opts = services.coaches.get_coach_options()
        coach_opts_with_none = {"-- No Coach --": None}
        coach_opts_with_none.update(coach_opts)

        team_opts = dict(zip(df['TeamName'], df['TeamID']))
        sel_name = st.selectbox("Select Team", list(team_opts.keys()))

        if sel_name:
            sel_id = team_opts[sel_name]
            row_df, _ = services.teams.get_by_id("Team", "TeamID", sel_id)
            if row_df is not None and not row_df.empty:
                row = row_df.iloc[0]

                col1, col2 = st.columns([3, 1])
                with col1:
                    with st.form("edit_team_form"):
                        c1, c2 = st.columns(2)
                        with c1:
                            new_tname = st.text_input("Team Name", value=str(row['TeamName']))
                            g_opts = ["Male", "Female", "Mixed"]
                            g_idx = g_opts.index(str(row['Gender'])) if row['Gender'] in g_opts else 0
                            new_gender = st.selectbox("Gender", g_opts, index=g_idx)
                            new_year = st.number_input("Formation Year", min_value=2000,
                                                       value=int(row['FormationYear'] or 2024))
                        with c2:
                            new_dept = st.selectbox("Department", list(dept_opts.keys()))
                            new_sport = st.selectbox("Sport", list(sport_opts.keys()))
                            new_coach = st.selectbox("Coach", list(coach_opts_with_none.keys()))

                        if st.form_submit_button("💾 Update Team", type="primary", use_container_width=True):
                            success, msg = services.teams.update_team(
                                sel_id, new_tname, new_gender, new_year,
                                dept_opts[new_dept], sport_opts[new_sport],
                                coach_opts_with_none[new_coach]
                            )
                            if success:
                                show_success(msg)
                                st.rerun()
                            else:
                                show_error(msg)

                with col2:
                    st.markdown("### ⚠️ Delete")
                    if st.button("🗑️ Delete Team", type="secondary", use_container_width=True):
                        success, msg = services.teams.delete_team(sel_id)
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)

    with tab4:
        st.markdown("### 👤 Team Players Management")
        team_opts = services.teams.get_team_options()

        if not team_opts:
            show_info("No teams available.")
            return

        sel_team = st.selectbox("Select Team", list(team_opts.keys()), key="player_team")

        if sel_team:
            team_id = team_opts[sel_team]

            df_players, err = services.teams.get_team_players(team_id)
            st.markdown(f"#### Current Players in {sel_team}")
            if df_players is not None and not df_players.empty:
                st.dataframe(df_players, use_container_width=True, hide_index=True)

                st.markdown("#### Remove Player")
                player_id_opts = dict(zip(
                    df_players['FullName'] + ' - ' + df_players['Position'].fillna(''),
                    df_players['TeamPlayerID']
                ))
                sel_player = st.selectbox("Select Player to Remove", list(player_id_opts.keys()))
                if st.button("🗑️ Remove Player", type="secondary"):
                    success, msg = services.teams.remove_player_from_team(player_id_opts[sel_player])
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)
            else:
                show_info("No players in this team yet.")

            st.markdown("#### Add Player to Team")
            student_opts = services.students.get_student_options()
            with st.form("add_player_form"):
                c1, c2 = st.columns(2)
                with c1:
                    sel_student = st.selectbox("Select Student", list(student_opts.keys()))
                    position = st.text_input("Position", placeholder="Captain / Player / etc.")
                with c2:
                    join_date = st.date_input("Join Date", value=date.today())

                if st.form_submit_button("➕ Add to Team", type="primary", use_container_width=True):
                    success, msg = services.teams.add_player_to_team(
                        team_id, student_opts[sel_student], join_date, position
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)


# ============================================================
# EQUIPMENT PAGE
# ============================================================

def page_equipment():
    st.markdown('<p class="main-header">🏏 Equipment Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 View Equipment", "➕ Add Equipment", "✏️ Edit/Delete",
        "📤 Issue Equipment", "📥 Returns & Issues"
    ])

    with tab1:
        df, err = services.equipment.get_all_equipment()
        if err:
            show_error(err)
        else:
            if df is not None and not df.empty:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Equipment Types", len(df))
                with col2:
                    st.metric("Total Items", int(df['TotalQuantity'].sum()))
                with col3:
                    st.metric("Available Items", int(df['AvailableQty'].sum()))
            display_dataframe(df, "All Equipment")

    with tab2:
        sport_opts = services.sports.get_sport_options()
        with st.form("add_equip_form"):
            col1, col2 = st.columns(2)
            with col1:
                equip_name = st.text_input("Equipment Name *", placeholder="Cricket Bat")
                category = st.text_input("Category", placeholder="Batting")
                total_qty = st.number_input("Total Quantity *", min_value=0, value=10)
                available_qty = st.number_input("Available Quantity *", min_value=0, value=10)
            with col2:
                condition = st.selectbox("Condition", ["New", "Good", "Fair", "Poor"])
                purchase_date = st.date_input("Purchase Date", value=date.today())
                sport_name = st.selectbox("Sport *", list(sport_opts.keys()))

            if st.form_submit_button("➕ Add Equipment", type="primary", use_container_width=True):
                if not equip_name:
                    show_error("Equipment Name is required!")
                else:
                    success, msg = services.equipment.add_equipment(
                        equip_name, category, total_qty, available_qty,
                        condition, purchase_date, sport_opts[sport_name]
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        df, err = services.equipment.get_all_equipment()
        if err or df is None or df.empty:
            show_info("No equipment to edit.")
            return

        sport_opts = services.sports.get_sport_options()
        equip_opts = dict(zip(df['EquipmentName'], df['EquipmentID']))
        sel_equip = st.selectbox("Select Equipment", list(equip_opts.keys()))

        if sel_equip:
            sel_id = equip_opts[sel_equip]
            row_df, _ = services.equipment.get_by_id("Equipment", "EquipmentID", sel_id)
            if row_df is not None and not row_df.empty:
                row = row_df.iloc[0]

                col1, col2 = st.columns([3, 1])
                with col1:
                    with st.form("edit_equip_form"):
                        c1, c2 = st.columns(2)
                        with c1:
                            new_name = st.text_input("Equipment Name", value=str(row['EquipmentName']))
                            new_cat = st.text_input("Category", value=str(row['Category'] or ''))
                            new_total = st.number_input("Total Qty", min_value=0, value=int(row['TotalQuantity']))
                            new_avail = st.number_input("Available Qty", min_value=0, value=int(row['AvailableQty']))
                        with c2:
                            cond_opts = ["New", "Good", "Fair", "Poor"]
                            cond_idx = cond_opts.index(str(row['Condition'])) if row['Condition'] in cond_opts else 0
                            new_cond = st.selectbox("Condition", cond_opts, index=cond_idx)
                            new_pdate = st.date_input("Purchase Date",
                                                      value=pd.to_datetime(row['PurchaseDate']).date()
                                                      if row['PurchaseDate'] else date.today())
                            new_sport = st.selectbox("Sport", list(sport_opts.keys()))

                        if st.form_submit_button("💾 Update Equipment", type="primary", use_container_width=True):
                            success, msg = services.equipment.update_equipment(
                                sel_id, new_name, new_cat, new_total, new_avail,
                                new_cond, new_pdate, sport_opts[new_sport]
                            )
                            if success:
                                show_success(msg)
                                st.rerun()
                            else:
                                show_error(msg)
                with col2:
                    st.markdown("### ⚠️ Delete")
                    if st.button("🗑️ Delete Equipment", type="secondary", use_container_width=True):
                        success, msg = services.equipment.delete_equipment(sel_id)
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)

    with tab4:
        st.markdown("### Issue Equipment to Student")
        equip_opts = services.equipment.get_equipment_options()
        student_opts = services.students.get_student_options()

        with st.form("issue_equip_form"):
            col1, col2 = st.columns(2)
            with col1:
                sel_equip = st.selectbox("Equipment *", list(equip_opts.keys()))
                sel_student = st.selectbox("Student *", list(student_opts.keys()))
            with col2:
                issue_date = st.date_input("Issue Date", value=date.today())
                remarks = st.text_area("Remarks", placeholder="Issued for practice")

            if st.form_submit_button("📤 Issue Equipment", type="primary", use_container_width=True):
                success, msg = services.equipment.issue_equipment(
                    equip_opts[sel_equip], student_opts[sel_student], issue_date, remarks
                )
                if success:
                    show_success(msg)
                    st.rerun()
                else:
                    show_error(msg)

    with tab5:
        st.markdown("### Equipment Issues & Returns")
        df, err = services.equipment.get_equipment_issues()
        if err:
            show_error(err)
        else:
            display_dataframe(df, "All Equipment Issues")

        st.divider()
        st.markdown("### Process Return")

        if df is not None and not df.empty:
            pending = df[df['IsReturned'] == False] if 'IsReturned' in df.columns else df
            if not pending.empty:
                issue_opts = dict(zip(
                    pending.apply(lambda r: f"#{r['IssueID']} - {r['EquipmentName']} ({r['StudentName']})", axis=1),
                    pending['IssueID']
                ))
                with st.form("return_equip_form"):
                    sel_issue = st.selectbox("Select Issue to Return", list(issue_opts.keys()))
                    col1, col2 = st.columns(2)
                    with col1:
                        return_date = st.date_input("Return Date", value=date.today())
                    with col2:
                        fine_amount = st.number_input("Fine Amount (PKR)", min_value=0.0, value=0.0)
                    ret_remarks = st.text_input("Return Remarks", placeholder="Returned in good condition")

                    if st.form_submit_button("📥 Process Return", type="primary", use_container_width=True):
                        success, msg = services.equipment.return_equipment(
                            issue_opts[sel_issue], return_date, fine_amount, ret_remarks
                        )
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)


# ============================================================
# TOURNAMENTS PAGE
# ============================================================

def page_tournaments():
    st.markdown('<p class="main-header">🏆 Tournaments Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 View All", "➕ Add New", "✏️ Edit/Delete",
        "👥 Register Teams", "💰 Expenses"
    ])

    with tab1:
        df, err = services.tournaments.get_all_tournaments()
        if err:
            show_error(err)
        else:
            if df is not None and not df.empty:
                status_filter = st.multiselect("Filter by Status",
                                               df['Status'].unique().tolist() if 'Status' in df.columns else [],
                                               default=df['Status'].unique().tolist() if 'Status' in df.columns else [])
                if status_filter:
                    df = df[df['Status'].isin(status_filter)]
            display_dataframe(df, "All Tournaments")

    with tab2:
        sport_opts = services.sports.get_sport_options()
        sem_opts = services.semesters.get_semester_options()

        with st.form("add_tourn_form"):
            col1, col2 = st.columns(2)
            with col1:
                tourn_name = st.text_input("Tournament Name *", placeholder="Cricket Cup 2025")
                start_date = st.date_input("Start Date *", value=date.today())
                end_date = st.date_input("End Date *", value=date.today())
                organizer = st.text_input("Organizer", placeholder="Sports Committee")
            with col2:
                status = st.selectbox("Status", ["Upcoming", "Ongoing", "Completed", "Cancelled"])
                sport_name = st.selectbox("Sport *", list(sport_opts.keys()))
                sem_name = st.selectbox("Semester *", list(sem_opts.keys()))

            if st.form_submit_button("➕ Add Tournament", type="primary", use_container_width=True):
                if not tourn_name:
                    show_error("Tournament Name is required!")
                elif end_date < start_date:
                    show_error("End date must be after start date!")
                else:
                    success, msg = services.tournaments.add_tournament(
                        tourn_name, start_date, end_date, status,
                        organizer, sport_opts[sport_name], sem_opts[sem_name]
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        df, err = services.tournaments.get_all_tournaments()
        if err or df is None or df.empty:
            show_info("No tournaments to edit.")
            return

        sport_opts = services.sports.get_sport_options()
        sem_opts = services.semesters.get_semester_options()

        tourn_sel_opts = dict(zip(df['TournamentName'], df['TournamentID']))
        sel_tourn = st.selectbox("Select Tournament", list(tourn_sel_opts.keys()))

        if sel_tourn:
            sel_id = tourn_sel_opts[sel_tourn]
            row_df, _ = services.tournaments.get_by_id("Tournament", "TournamentID", sel_id)
            if row_df is not None and not row_df.empty:
                row = row_df.iloc[0]

                col1, col2 = st.columns([3, 1])
                with col1:
                    with st.form("edit_tourn_form"):
                        c1, c2 = st.columns(2)
                        with c1:
                            new_tname = st.text_input("Tournament Name", value=str(row['TournamentName']))
                            new_start = st.date_input("Start Date",
                                                      value=pd.to_datetime(row['StartDate']).date())
                            new_end = st.date_input("End Date",
                                                    value=pd.to_datetime(row['EndDate']).date())
                            new_org = st.text_input("Organizer", value=str(row['OrganizerName'] or ''))
                        with c2:
                            st_opts = ["Upcoming", "Ongoing", "Completed", "Cancelled"]
                            st_idx = st_opts.index(str(row['Status'])) if row['Status'] in st_opts else 0
                            new_status = st.selectbox("Status", st_opts, index=st_idx)
                            new_sport = st.selectbox("Sport", list(sport_opts.keys()))
                            new_sem = st.selectbox("Semester", list(sem_opts.keys()))

                        if st.form_submit_button("💾 Update Tournament", type="primary", use_container_width=True):
                            success, msg = services.tournaments.update_tournament(
                                sel_id, new_tname, new_start, new_end, new_status,
                                new_org, sport_opts[new_sport], sem_opts[new_sem]
                            )
                            if success:
                                show_success(msg)
                                st.rerun()
                            else:
                                show_error(msg)
                with col2:
                    st.markdown("### ⚠️ Delete")
                    if st.button("🗑️ Delete Tournament", type="secondary", use_container_width=True):
                        success, msg = services.tournaments.delete_tournament(sel_id)
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)

    with tab4:
        st.markdown("### Register Team in Tournament")
        tourn_opts = services.tournaments.get_tournament_options()
        team_opts = services.teams.get_team_options()

        sel_tourn = st.selectbox("Select Tournament", list(tourn_opts.keys()), key="reg_tourn")

        if sel_tourn:
            df_teams, err = services.tournaments.get_tournament_teams(tourn_opts[sel_tourn])
            st.markdown(f"#### Registered Teams in {sel_tourn}")
            display_dataframe(df_teams)

            st.divider()
            with st.form("reg_team_form"):
                col1, col2 = st.columns(2)
                with col1:
                    sel_team = st.selectbox("Select Team", list(team_opts.keys()))
                    group_name = st.text_input("Group Name", placeholder="Group A")
                with col2:
                    reg_date = st.date_input("Registration Date", value=date.today())

                if st.form_submit_button("👥 Register Team", type="primary", use_container_width=True):
                    success, msg = services.tournaments.register_team_in_tournament(
                        tourn_opts[sel_tourn], team_opts[sel_team], reg_date, group_name
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab5:
        st.markdown("### Tournament Expenses")
        tourn_opts = services.tournaments.get_tournament_options()

        sel_tourn = st.selectbox("Select Tournament", list(tourn_opts.keys()), key="exp_tourn")

        if sel_tourn:
            tourn_id = tourn_opts[sel_tourn]
            df_exp, err = services.tournaments.get_tournament_expenses(tourn_id)

            if df_exp is not None and not df_exp.empty:
                total = float(df_exp['Amount'].sum())
                st.metric("Total Tournament Expenses", f"PKR {total:,.2f}")

            display_dataframe(df_exp, f"Expenses for {sel_tourn}")

            st.divider()
            st.markdown("#### Add Expense")
            with st.form("add_expense_form"):
                col1, col2 = st.columns(2)
                with col1:
                    exp_title = st.text_input("Expense Title *", placeholder="Ground Booking Fee")
                    category = st.selectbox("Category",
                                            ["Transport", "Food", "Equipment", "Prize", "Venue", "Other"])
                    amount = st.number_input("Amount (PKR) *", min_value=0.01, value=1000.0)
                with col2:
                    exp_date = st.date_input("Expense Date", value=date.today())
                    paid_by = st.text_input("Paid By", placeholder="Sports Dept")

                if st.form_submit_button("💰 Add Expense", type="primary", use_container_width=True):
                    if not exp_title:
                        show_error("Expense Title is required!")
                    else:
                        success, msg = services.tournaments.add_expense(
                            exp_title, category, amount, exp_date, paid_by, tourn_id
                        )
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)


# ============================================================
# MATCHES PAGE
# ============================================================

def page_matches():
    st.markdown('<p class="main-header">🎯 Matches Management</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 View All", "➕ Add Match", "✏️ Edit/Delete", "📊 Performance"
    ])

    with tab1:
        df, err = services.matches.get_all_matches()
        if err:
            show_error(err)
        else:
            if df is not None and not df.empty:
                status_filter = st.multiselect("Filter by Status",
                                               df['Status'].unique().tolist(),
                                               default=df['Status'].unique().tolist())
                if status_filter:
                    df = df[df['Status'].isin(status_filter)]
            display_dataframe(df, "All Matches")

    with tab2:
        team_opts = services.teams.get_team_options()
        tourn_opts = services.tournaments.get_tournament_options()
        venue_opts = services.venues.get_venue_options()
        team_with_none = {"-- No Winner Yet --": None}
        team_with_none.update(team_opts)

        with st.form("add_match_form"):
            col1, col2 = st.columns(2)
            with col1:
                match_date = st.date_input("Match Date *", value=date.today())
                match_time = st.time_input("Match Time", value=time(9, 0))
                round_name = st.text_input("Round", placeholder="Final / Semi Final / etc.")
                status = st.selectbox("Status", ["Scheduled", "Ongoing", "Completed", "Postponed"])
            with col2:
                home_team = st.selectbox("Home Team *", list(team_opts.keys()))
                away_team = st.selectbox("Away Team *", list(team_opts.keys()))
                home_score = st.number_input("Home Team Score", min_value=0, value=0)
                away_score = st.number_input("Away Team Score", min_value=0, value=0)

            col3, col4, col5 = st.columns(3)
            with col3:
                winner = st.selectbox("Winner", list(team_with_none.keys()))
            with col4:
                tourn_sel = st.selectbox("Tournament *", list(tourn_opts.keys()))
            with col5:
                venue_sel = st.selectbox("Venue *", list(venue_opts.keys()))

            if st.form_submit_button("➕ Add Match", type="primary", use_container_width=True):
                if team_opts[home_team] == team_opts[away_team]:
                    show_error("Home team and away team must be different!")
                else:
                    success, msg = services.matches.add_match(
                        match_date, match_time, round_name, status,
                        team_opts[home_team], team_opts[away_team],
                        home_score, away_score,
                        team_with_none[winner],
                        tourn_opts[tourn_sel], venue_opts[venue_sel]
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        df, err = services.matches.get_all_matches()
        if err or df is None or df.empty:
            show_info("No matches to edit.")
            return

        match_opts = services.matches.get_match_options()
        team_opts = services.teams.get_team_options()
        tourn_opts = services.tournaments.get_tournament_options()
        venue_opts = services.venues.get_venue_options()
        team_with_none = {"-- No Winner Yet --": None}
        team_with_none.update(team_opts)

        sel_match = st.selectbox("Select Match", list(match_opts.keys()))

        if sel_match:
            sel_id = match_opts[sel_match]
            col1, col2 = st.columns([3, 1])
            with col1:
                # FIX: Fetch from the raw Match table to get HomeTeamID / AwayTeamID
                row_df, _ = services.matches.get_by_id("Match", "MatchID", sel_id)
                if row_df is not None and not row_df.empty:
                    row = row_df.iloc[0]
                    with st.form("edit_match_form"):
                        c1, c2 = st.columns(2)
                        with c1:
                            new_date = st.date_input("Match Date",
                                                     value=pd.to_datetime(row['MatchDate']).date())
                            new_round = st.text_input("Round", value=str(row['Round'] or ''))
                            st_opts = ["Scheduled", "Ongoing", "Completed", "Postponed"]
                            st_idx = st_opts.index(str(row['Status'])) if row['Status'] in st_opts else 0
                            new_status = st.selectbox("Status", st_opts, index=st_idx)
                            new_home_score = st.number_input("Home Score", min_value=0,
                                                             value=int(row['HomeTeamScore'] or 0))
                        with c2:
                            new_away_score = st.number_input("Away Score", min_value=0,
                                                             value=int(row['AwayTeamScore'] or 0))
                            new_winner = st.selectbox("Winner", list(team_with_none.keys()))
                            new_tourn = st.selectbox("Tournament", list(tourn_opts.keys()))
                            new_venue = st.selectbox("Venue", list(venue_opts.keys()))

                        if st.form_submit_button("💾 Update Match", type="primary", use_container_width=True):
                            success, msg = services.matches.update_match(
                                sel_id, new_date, None, new_round, new_status,
                                int(row['HomeTeamID']), int(row['AwayTeamID']),
                                new_home_score, new_away_score,
                                team_with_none[new_winner],
                                tourn_opts[new_tourn], venue_opts[new_venue]
                            )
                            if success:
                                show_success(msg)
                                st.rerun()
                            else:
                                show_error(msg)
            with col2:
                st.markdown("### ⚠️ Delete")
                if st.button("🗑️ Delete Match", type="secondary", use_container_width=True):
                    success, msg = services.matches.delete_match(sel_id)
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab4:
        st.markdown("### Match Performance Records")
        match_opts = services.matches.get_match_options()

        if not match_opts:
            show_info("No matches available.")
            return

        sel_match = st.selectbox("Select Match", list(match_opts.keys()), key="perf_match")

        if sel_match:
            match_id = match_opts[sel_match]
            df_perf, err = services.matches.get_match_performances(match_id)
            display_dataframe(df_perf, f"Performances in: {sel_match}")

            st.divider()
            st.markdown("#### Add Performance Record")
            student_opts = services.students.get_student_options()
            team_opts = services.teams.get_team_options()

            with st.form("add_perf_form"):
                col1, col2 = st.columns(2)
                with col1:
                    sel_student = st.selectbox("Player *", list(student_opts.keys()))
                    sel_team = st.selectbox("Team *", list(team_opts.keys()))
                    goals = st.number_input("Goals/Runs Scored", min_value=0, value=0)
                    assists = st.number_input("Assists", min_value=0, value=0)
                with col2:
                    yellow_cards = st.number_input("Yellow Cards", min_value=0, value=0)
                    red_cards = st.number_input("Red Cards", min_value=0, value=0)
                    minutes = st.number_input("Minutes Played", min_value=0, max_value=120, value=90)
                    note = st.text_area("Performance Note", placeholder="Outstanding performance...")

                if st.form_submit_button("➕ Add Performance", type="primary", use_container_width=True):
                    success, msg = services.matches.add_match_performance(
                        match_id, student_opts[sel_student], team_opts[sel_team],
                        goals, assists, yellow_cards, red_cards, minutes, note
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)


# ============================================================
# PRACTICE SESSIONS PAGE
# ============================================================

def page_practice_sessions():
    st.markdown('<p class="main-header">🏃 Practice Sessions</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 View All", "➕ Add Session", "✏️ Edit/Delete", "📋 Attendance"
    ])

    with tab1:
        df, err = services.practice_sessions.get_all_sessions()
        if err:
            show_error(err)
        else:
            display_dataframe(df, "All Practice Sessions")

    with tab2:
        team_opts = services.teams.get_team_options()
        coach_opts = services.coaches.get_coach_options()
        venue_opts = services.venues.get_venue_options()

        with st.form("add_session_form"):
            col1, col2 = st.columns(2)
            with col1:
                session_date = st.date_input("Session Date *", value=date.today())
                start_time = st.time_input("Start Time *", value=time(8, 0))
                end_time = st.time_input("End Time *", value=time(10, 0))
            with col2:
                notes = st.text_area("Notes", placeholder="Practice session notes...")
                sel_team = st.selectbox("Team *", list(team_opts.keys()))
                sel_coach = st.selectbox("Coach *", list(coach_opts.keys()))
                sel_venue = st.selectbox("Venue *", list(venue_opts.keys()))

            if st.form_submit_button("➕ Add Session", type="primary", use_container_width=True):
                if end_time <= start_time:
                    show_error("End time must be after start time!")
                else:
                    success, msg = services.practice_sessions.add_session(
                        session_date, start_time, end_time, notes,
                        team_opts[sel_team], coach_opts[sel_coach], venue_opts[sel_venue]
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab3:
        df, err = services.practice_sessions.get_all_sessions()
        if err or df is None or df.empty:
            show_info("No sessions to edit.")
            return

        sess_opts = services.practice_sessions.get_session_options()
        team_opts = services.teams.get_team_options()
        coach_opts = services.coaches.get_coach_options()
        venue_opts = services.venues.get_venue_options()

        sel_sess = st.selectbox("Select Session", list(sess_opts.keys()))

        if sel_sess:
            sel_id = sess_opts[sel_sess]
            col1, col2 = st.columns([3, 1])
            with col1:
                row_df, _ = services.practice_sessions.get_by_id("PracticeSession", "SessionID", sel_id)
                if row_df is not None and not row_df.empty:
                    row = row_df.iloc[0]
                    with st.form("edit_sess_form"):
                        c1, c2 = st.columns(2)
                        with c1:
                            new_date = st.date_input("Session Date",
                                                     value=pd.to_datetime(row['SessionDate']).date())
                            new_start = st.time_input("Start Time")
                            new_end = st.time_input("End Time")
                        with c2:
                            new_notes = st.text_area("Notes", value=str(row['Notes'] or ''))
                            new_team = st.selectbox("Team", list(team_opts.keys()))
                            new_coach = st.selectbox("Coach", list(coach_opts.keys()))
                            new_venue = st.selectbox("Venue", list(venue_opts.keys()))

                        if st.form_submit_button("💾 Update Session", type="primary", use_container_width=True):
                            success, msg = services.practice_sessions.update_session(
                                sel_id, new_date, new_start, new_end, new_notes,
                                team_opts[new_team], coach_opts[new_coach], venue_opts[new_venue]
                            )
                            if success:
                                show_success(msg)
                                st.rerun()
                            else:
                                show_error(msg)
            with col2:
                st.markdown("### ⚠️ Delete")
                if st.button("🗑️ Delete Session", type="secondary", use_container_width=True):
                    success, msg = services.practice_sessions.delete_session(sel_id)
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)

    with tab4:
        st.markdown("### Attendance Management")
        sess_opts = services.practice_sessions.get_session_options()

        if not sess_opts:
            show_info("No sessions available.")
            return

        sel_sess = st.selectbox("Select Session", list(sess_opts.keys()), key="att_session")

        if sel_sess:
            sess_id = sess_opts[sel_sess]
            df_att, err = services.practice_sessions.get_session_attendance(sess_id)
            display_dataframe(df_att, f"Attendance for: {sel_sess}")

            st.divider()
            st.markdown("#### Mark Attendance")
            student_opts = services.students.get_student_options()

            with st.form("mark_attendance_form"):
                col1, col2 = st.columns(2)
                with col1:
                    sel_student = st.selectbox("Select Student", list(student_opts.keys()))
                    status = st.selectbox("Status", ["Present", "Absent", "Late"])
                with col2:
                    remarks = st.text_input("Remarks", placeholder="Good batting session")

                if st.form_submit_button("✅ Mark Attendance", type="primary", use_container_width=True):
                    success, msg = services.practice_sessions.mark_attendance(
                        sess_id, student_opts[sel_student], status, remarks
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)


# ============================================================
# INJURIES PAGE
# ============================================================

def page_injuries():
    st.markdown('<p class="main-header">🤕 Injury Records</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add Record", "✏️ Update/Delete"])

    with tab1:
        df, err = services.injuries.get_all_injuries()
        if err:
            show_error(err)
        else:
            if df is not None and not df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    active = len(df[df['IsRecovered'] == False]) if 'IsRecovered' in df.columns else 0
                    st.metric("🤕 Active Injuries", active)
                with col2:
                    recovered = len(df[df['IsRecovered'] == True]) if 'IsRecovered' in df.columns else 0
                    st.metric("✅ Recovered", recovered)
            display_dataframe(df, "All Injury Records")

    with tab2:
        student_opts = services.students.get_student_options()
        match_opts = services.matches.get_match_options()
        match_with_none = {"-- Not Match Related --": None}
        match_with_none.update(match_opts)

        with st.form("add_injury_form"):
            col1, col2 = st.columns(2)
            with col1:
                injury_date = st.date_input("Injury Date *", value=date.today())
                injury_type = st.text_input("Injury Type", placeholder="Sprain / Fracture / etc.")
                severity = st.selectbox("Severity", ["Minor", "Moderate", "Severe"])
                description = st.text_area("Description", placeholder="Ankle sprain during match")
            with col2:
                recovery_days = st.number_input("Estimated Recovery Days", min_value=0, value=7)
                is_recovered = st.checkbox("Already Recovered?")
                sel_student = st.selectbox("Student *", list(student_opts.keys()))
                sel_match = st.selectbox("Related Match (Optional)", list(match_with_none.keys()))

            if st.form_submit_button("➕ Add Injury Record", type="primary", use_container_width=True):
                success, msg = services.injuries.add_injury(
                    injury_date, injury_type, severity, description,
                    recovery_days, is_recovered, student_opts[sel_student],
                    match_with_none[sel_match]
                )
                if success:
                    show_success(msg)
                    st.rerun()
                else:
                    show_error(msg)

    with tab3:
        df, err = services.injuries.get_all_injuries()
        if err or df is None or df.empty:
            show_info("No injury records to edit.")
            return

        injury_id_opts = dict(zip(
            df.apply(lambda r: f"#{r['InjuryID']} - {r['StudentName']} ({r['InjuryType']})", axis=1),
            df['InjuryID']
        ))
        sel_inj = st.selectbox("Select Injury Record", list(injury_id_opts.keys()))

        if sel_inj:
            inj_id = injury_id_opts[sel_inj]
            row = df[df['InjuryID'] == inj_id].iloc[0]

            col1, col2 = st.columns([3, 1])
            with col1:
                with st.form("update_injury_form"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        new_recovered = st.checkbox("Recovered", value=bool(row['IsRecovered']))
                    with col_b:
                        new_days = st.number_input("Recovery Days", min_value=0,
                                                   value=int(row['RecoveryDays'] or 0))

                    if st.form_submit_button("💾 Update Recovery Status", type="primary", use_container_width=True):
                        success, msg = services.injuries.update_injury_recovery(inj_id, new_recovered, new_days)
                        if success:
                            show_success(msg)
                            st.rerun()
                        else:
                            show_error(msg)

            with col2:
                st.markdown("### ⚠️ Delete")
                if st.button("🗑️ Delete Record", type="secondary", use_container_width=True):
                    success, msg = services.injuries.delete_injury(inj_id)
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)


# ============================================================
# PLAYER RATINGS PAGE
# ============================================================

def page_player_ratings():
    st.markdown('<p class="main-header">⭐ Player Ratings</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2, tab3 = st.tabs(["📋 All Ratings", "🏆 Top Rated", "➕ Add Rating"])

    with tab1:
        df, err = services.ratings.get_all_ratings()
        if err:
            show_error(err)
        else:
            display_dataframe(df, "All Player Ratings")

    with tab2:
        st.markdown("### 🏆 Top Rated Players")
        limit = st.slider("Number of players", 5, 20, 10)
        df, err = services.ratings.get_top_rated_players(limit)
        if err:
            show_error(err)
        elif df is not None and not df.empty:
            fig = px.bar(df, x='PlayerName', y='AvgRating',
                         color='SportName', text='AvgRating',
                         color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig.update_layout(height=400, xaxis_title="Player", yaxis_title="Average Rating")
            st.plotly_chart(fig, use_container_width=True)
            display_dataframe(df)

    with tab3:
        student_opts = services.students.get_student_options()
        coach_opts = services.coaches.get_coach_options()
        sport_opts = services.sports.get_sport_options()

        with st.form("add_rating_form"):
            col1, col2 = st.columns(2)
            with col1:
                sel_student = st.selectbox("Player *", list(student_opts.keys()))
                sel_coach = st.selectbox("Coach *", list(coach_opts.keys()))
                sel_sport = st.selectbox("Sport *", list(sport_opts.keys()))
            with col2:
                rating = st.slider("Rating (1.0 - 10.0)", min_value=1.0, max_value=10.0,
                                   value=7.0, step=0.5)
                review = st.text_area("Review", placeholder="Excellent performance, needs to improve...")
                rating_date = st.date_input("Rating Date", value=date.today())

            if st.form_submit_button("⭐ Add Rating", type="primary", use_container_width=True):
                success, msg = services.ratings.add_rating(
                    student_opts[sel_student], coach_opts[sel_coach],
                    sport_opts[sel_sport], rating, review, rating_date
                )
                if success:
                    show_success(msg)
                    st.rerun()
                else:
                    show_error(msg)


# ============================================================
# POINTS TABLE PAGE
# ============================================================

def page_points_table():
    st.markdown('<p class="main-header">📊 Tournament Points Table</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2 = st.tabs(["📊 View Points Table", "✏️ Manage Points"])

    with tab1:
        tourn_opts = services.tournaments.get_tournament_options()

        if not tourn_opts:
            show_info("No tournaments available.")
            return

        sel_tourn = st.selectbox("Select Tournament", list(tourn_opts.keys()))

        if sel_tourn:
            tourn_id = tourn_opts[sel_tourn]
            df, err = services.points_table.get_points_table(tourn_id)

            if err:
                show_error(err)
            elif df is not None and not df.empty:
                fig = px.bar(df, x='TeamName', y='Points',
                             color='Points',
                             color_continuous_scale='RdYlGn',
                             text='Points',
                             title=f"Points Table: {sel_tourn}")
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

                df_display = df.copy()
                df_display.insert(0, 'Rank', range(1, len(df_display) + 1))
                display_dataframe(df_display, "Standings")
            else:
                show_info("No points data for this tournament.")

    with tab2:
        st.markdown("### Add Points Entry")
        tourn_opts = services.tournaments.get_tournament_options()
        team_opts = services.teams.get_team_options()

        col1, col2 = st.columns(2)
        with col1:
            sel_tourn = st.selectbox("Tournament", list(tourn_opts.keys()), key="pts_tourn")
        with col2:
            sel_team = st.selectbox("Team", list(team_opts.keys()), key="pts_team")

        if st.button("➕ Add Points Entry", type="primary"):
            success, msg = services.points_table.add_points_entry(
                tourn_opts[sel_tourn], team_opts[sel_team]
            )
            if success:
                show_success(msg)
                st.rerun()
            else:
                show_error(msg)

        st.divider()
        st.markdown("### Update Points")

        tourn_sel_update = st.selectbox("Select Tournament to Update", list(tourn_opts.keys()), key="update_pts_tourn")
        if tourn_sel_update:
            df_pts, err = services.points_table.get_points_table(tourn_opts[tourn_sel_update])
            if df_pts is not None and not df_pts.empty:
                pts_entry_opts = dict(zip(df_pts['TeamName'], df_pts['PointsTableID']))
                sel_entry = st.selectbox("Select Team Entry", list(pts_entry_opts.keys()))

                if sel_entry:
                    entry_id = pts_entry_opts[sel_entry]
                    entry_row = df_pts[df_pts['PointsTableID'] == entry_id].iloc[0]

                    with st.form("update_pts_form"):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            mp = st.number_input("Matches Played", min_value=0,
                                                 value=int(entry_row['MatchesPlayed'] or 0))
                            wins = st.number_input("Wins", min_value=0, value=int(entry_row['Wins'] or 0))
                        with col2:
                            losses = st.number_input("Losses", min_value=0, value=int(entry_row['Losses'] or 0))
                            draws = st.number_input("Draws", min_value=0, value=int(entry_row['Draws'] or 0))
                        with col3:
                            gf = st.number_input("Goals For", min_value=0, value=int(entry_row['GoalsFor'] or 0))
                            ga = st.number_input("Goals Against", min_value=0,
                                                 value=int(entry_row['GoalsAgainst'] or 0))
                        with col4:
                            pts = st.number_input("Points", min_value=0, value=int(entry_row['Points'] or 0))

                        if st.form_submit_button("💾 Update Points", type="primary", use_container_width=True):
                            success, msg = services.points_table.update_points(
                                entry_id, mp, wins, losses, draws, gf, ga, pts
                            )
                            if success:
                                show_success(msg)
                                st.rerun()
                            else:
                                show_error(msg)


# ============================================================
# DEPARTMENT RANKINGS PAGE
# ============================================================

def page_rankings():
    st.markdown('<p class="main-header">🥇 Department Rankings</p>', unsafe_allow_html=True)
    check_connection()

    tab1, tab2 = st.tabs(["📋 View Rankings", "➕ Add Ranking"])

    with tab1:
        df, err = services.rankings.get_all_rankings()
        if err:
            show_error(err)
        elif df is not None and not df.empty:
            sport_filter = st.selectbox("Filter by Sport", ["All"] + df['SportName'].unique().tolist())
            if sport_filter != "All":
                df = df[df['SportName'] == sport_filter]

            if not df.empty:
                fig = px.bar(df, x='DepartmentName', y='TotalPoints',
                             color='SportName', barmode='group',
                             title="Department Rankings by Points")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            display_dataframe(df, "Department Rankings")
        else:
            show_info("No rankings data available.")

    with tab2:
        dept_opts = services.departments.get_department_options()
        sport_opts = services.sports.get_sport_options()
        sem_opts = services.semesters.get_semester_options()

        with st.form("add_ranking_form"):
            col1, col2 = st.columns(2)
            with col1:
                rank_pos = st.number_input("Rank Position *", min_value=1, value=1)
                total_points = st.number_input("Total Points", min_value=0, value=0)
                total_wins = st.number_input("Total Wins", min_value=0, value=0)
                total_losses = st.number_input("Total Losses", min_value=0, value=0)
            with col2:
                season = st.text_input("Season", placeholder="Fall 2024")
                dept_name = st.selectbox("Department *", list(dept_opts.keys()))
                sport_name = st.selectbox("Sport *", list(sport_opts.keys()))
                sem_name = st.selectbox("Semester *", list(sem_opts.keys()))

            if st.form_submit_button("➕ Add Ranking", type="primary", use_container_width=True):
                success, msg = services.rankings.add_ranking(
                    rank_pos, total_points, total_wins, total_losses,
                    season, dept_opts[dept_name], sport_opts[sport_name], sem_opts[sem_name]
                )
                if success:
                    show_success(msg)
                    st.rerun()
                else:
                    show_error(msg)


# ============================================================
# REMINDERS PAGE
# ============================================================

def page_reminders():
    st.markdown('<p class="main-header">🔔 Reminders & Notifications</p>', unsafe_allow_html=True)
    check_connection()

    unread_count = services.reminders.get_unread_count()
    if unread_count > 0:
        st.warning(f"🔔 You have **{unread_count}** unread reminder(s)!")

    tab1, tab2 = st.tabs(["📋 All Reminders", "➕ Add Reminder"])

    with tab1:
        df, err = services.reminders.get_all_reminders()
        if err:
            show_error(err)
        elif df is not None and not df.empty:
            unread = df[df['IsRead'] == False] if 'IsRead' in df.columns else pd.DataFrame()
            if not unread.empty:
                st.markdown("### 🔴 Unread Reminders")
                for _, row in unread.iterrows():
                    with st.expander(f"🔔 {row['Title']} - {row['ReminderType']}"):
                        st.write(f"**Message:** {row['Message']}")
                        st.write(f"**Date:** {row['ReminderDate']}")
                        st.write(f"**For:** {row['StudentName']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"✅ Mark as Read", key=f"read_{row['ReminderID']}"):
                                services.reminders.mark_as_read(row['ReminderID'])
                                st.rerun()
                        with col2:
                            if st.button(f"🗑️ Delete", key=f"del_{row['ReminderID']}"):
                                services.reminders.delete_reminder(row['ReminderID'])
                                st.rerun()

            st.markdown("### All Reminders")
            display_dataframe(df)

    with tab2:
        student_opts = services.students.get_student_options()
        student_with_all = {"-- All Students --": None}
        student_with_all.update(student_opts)

        with st.form("add_reminder_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title *", placeholder="Match Tomorrow")
                message = st.text_area("Message", placeholder="Cricket semi-final at 9AM...")
                reminder_type = st.selectbox("Type", ["Match", "Practice", "Tournament", "General"])
            with col2:
                reminder_date = st.date_input("Reminder Date", value=date.today())
                reminder_time = st.time_input("Reminder Time", value=time(9, 0))
                sel_student = st.selectbox("For Student (Optional)", list(student_with_all.keys()))

            if st.form_submit_button("🔔 Add Reminder", type="primary", use_container_width=True):
                if not title:
                    show_error("Title is required!")
                else:
                    reminder_dt = datetime.combine(reminder_date, reminder_time)
                    success, msg = services.reminders.add_reminder(
                        title, message, reminder_dt, reminder_type,
                        student_with_all[sel_student]
                    )
                    if success:
                        show_success(msg)
                        st.rerun()
                    else:
                        show_error(msg)


# ============================================================
# MAIN APP - NAVIGATION
# ============================================================

def main():
    with st.sidebar:
        st.markdown("## 🏆 Sports Management")
        st.markdown("---")

        pages = {
            "🏠 Dashboard": "Dashboard",
            "🔌 DB Connection": "DB Connection",
            "─── MASTER DATA ───": None,
            "🏛️ Departments": "Departments",
            "⚽ Sports": "Sports",
            "🏟️ Venues": "Venues",
            "📅 Semesters": "Semesters",
            "─── PEOPLE ───": None,
            "👨‍🎓 Students": "Students",
            "🏋️ Coaches": "Coaches",
            "─── TEAMS ───": None,
            "👥 Teams & Players": "Teams",
            "─── EVENTS ───": None,
            "🏆 Tournaments": "Tournaments",
            "🎯 Matches": "Matches",
            "🏃 Practice Sessions": "Practice Sessions",
            "─── ANALYTICS ───": None,
            "🏏 Equipment": "Equipment",
            "🤕 Injury Records": "Injuries",
            "⭐ Player Ratings": "Player Ratings",
            "📊 Points Table": "Points Table",
            "🥇 Dept Rankings": "Rankings",
            "🔔 Reminders": "Reminders",
        }

        if 'selected_page' not in st.session_state:
            st.session_state.selected_page = "Dashboard"

        for label, page_key in pages.items():
            if page_key is None:
                st.markdown(f"**{label}**")
            else:
                if st.button(label, key=f"nav_{page_key}", use_container_width=True,
                             type="primary" if st.session_state.selected_page == page_key else "secondary"):
                    st.session_state.selected_page = page_key

        st.markdown("---")

        if db.is_connected():
            st.markdown("🟢 **DB Connected**")
        else:
            st.markdown("🔴 **DB Disconnected**")
            if st.button("🔗 Connect", use_container_width=True):
                success, msg = db.connect()
                if success:
                    st.success("Connected!")
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("---")
        st.markdown("**University Sports DB**")
        st.markdown("*All Rights Reserved*")

    page = st.session_state.selected_page

    page_routes = {
        "Dashboard": page_dashboard,
        "DB Connection": page_db_connection,
        "Departments": page_departments,
        "Sports": page_sports,
        "Venues": page_venues,
        "Semesters": page_semesters,
        "Students": page_students,
        "Coaches": page_coaches,
        "Teams": page_teams,
        "Equipment": page_equipment,
        "Tournaments": page_tournaments,
        "Matches": page_matches,
        "Practice Sessions": page_practice_sessions,
        "Injuries": page_injuries,
        "Player Ratings": page_player_ratings,
        "Points Table": page_points_table,
        "Rankings": page_rankings,
        "Reminders": page_reminders,
    }

    if page in page_routes:
        page_routes[page]()
    else:
        page_dashboard()


if __name__ == "__main__":
    main()
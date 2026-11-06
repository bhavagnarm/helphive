import streamlit as st
import pandas as pd

st.set_page_config(page_title="HelpHive 🐝", page_icon="🐝", layout="wide")

# Persistent in-memory state
if "requests" not in st.session_state:
    st.session_state.requests = [
        {
            "id": 1,
            "title": "Urgent O+ Blood Needed",
            "category": "Blood Donation",
            "urgency": "Critical",
            "location": "City General Hospital",
            "phone": "+91 9876543210",
            "description": "Patient in ICU requires 2 units of O+ whole blood immediately for surgery.",
            "status": "Open",
            "volunteers": []
        },
        {
            "id": 2,
            "title": "2nd Year Engineering Study Textbooks",
            "category": "Study Materials",
            "urgency": "Medium",
            "location": "Central Campus Library",
            "phone": "+91 9123456789",
            "description": "Looking for Operating Systems and Data Structures reference textbooks.",
            "status": "Open",
            "volunteers": []
        }
    ]

if "volunteers" not in st.session_state:
    st.session_state.volunteers = [
        {
            "name": "Community Volunteer",
            "city": "Guntur",
            "blood_group": "O+",
            "skills": "Blood Donor, First Aid, Driving",
            "availability": "Available"
        }
    ]

st.sidebar.title("🐝 HelpHive Platform")
menu = st.sidebar.radio(
    "Navigation",
    ["Browse Requests", "Ask for Help", "Volunteer Directory", "Register as Volunteer", "Admin Dashboard"]
)

# 1. BROWSE REQUESTS
if menu == "Browse Requests":
    st.title("🐝 Community Help Requests")
    st.write("Browse active community needs or pledge assistance directly.")

    col1, col2, col3 = st.columns(3)
    with col1:
        cat_filter = st.selectbox("Category", ["All", "Blood Donation", "Study Materials", "Essential Services", "Food & Clothing", "Emergency Assistance"])
    with col2:
        urg_filter = st.selectbox("Urgency", ["All", "Critical", "High", "Medium", "Low"])
    with col3:
        status_filter = st.selectbox("Status", ["All", "Open", "In Progress", "Resolved"])

    filtered = st.session_state.requests
    if cat_filter != "All":
        filtered = [r for r in filtered if r["category"] == cat_filter]
    if urg_filter != "All":
        filtered = [r for r in filtered if r["urgency"] == urg_filter]
    if status_filter != "All":
        filtered = [r for r in filtered if r["status"] == status_filter]

    st.divider()

    if not filtered:
        st.info("No requests match the selected filters.")
    else:
        for req in filtered:
            with st.expander(f"[{req['urgency']}] {req['title']} ({req['status']})"):
                st.write(f"**Category:** {req['category']} | **Location:** {req['location']}")
                st.write(f"**Contact:** {req['phone']}")
                st.write(f"**Description:** {req['description']}")
                st.write(f"**Pledged Helpers:** {len(req['volunteers'])}")

                with st.form(key=f"pledge_{req['id']}"):
                    helper = st.text_input("Your Name / Volunteer Note")
                    submit = st.form_submit_button("Pledge Help")
                    if submit and helper:
                        req["volunteers"].append(helper)
                        if req["status"] == "Open":
                            req["status"] = "In Progress"
                        st.success(f"Thank you {helper}! Your support has been recorded.")
                        st.rerun()

# 2. ASK FOR HELP
elif menu == "Ask for Help":
    st.title("📢 Post a Help Request")
    with st.form("new_request_form"):
        title = st.text_input("Request Title *", placeholder="e.g. Urgent requirement for O+ blood")
        col_a, col_b = st.columns(2)
        with col_a:
            category = st.selectbox("Category *", ["Blood Donation", "Study Materials", "Essential Services", "Food & Clothing", "Emergency Assistance"])
            location = st.text_input("Location / City *", placeholder="e.g. Guntur")
        with col_b:
            urgency = st.selectbox("Urgency *", ["Critical", "High", "Medium", "Low"])
            phone = st.text_input("Contact Phone *", placeholder="+91...")
        description = st.text_area("Detailed Description *")
        submit = st.form_submit_button("Publish Request")

        if submit:
            if title and location and phone and description:
                st.session_state.requests.insert(0, {
                    "id": len(st.session_state.requests) + 1,
                    "title": title,
                    "category": category,
                    "urgency": urgency,
                    "location": location,
                    "phone": phone,
                    "description": description,
                    "status": "Open",
                    "volunteers": []
                })
                st.success("Help request posted successfully!")
            else:
                st.error("Please fill in all mandatory fields.")

# 3. VOLUNTEER DIRECTORY
elif menu == "Volunteer Directory":
    st.title("🤝 Community Volunteer Directory")
    city = st.text_input("Search by City", "")
    bg = st.selectbox("Blood Group Filter", ["All", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

    vols = st.session_state.volunteers
    if city:
        vols = [v for v in vols if city.lower() in v["city"].lower()]
    if bg != "All":
        vols = [v for v in vols if v["blood_group"] == bg]

    st.dataframe(pd.DataFrame(vols), use_container_width=True)

# 4. REGISTER AS VOLUNTEER
elif menu == "Register as Volunteer":
    st.title("🐝 Join the Volunteer Hive")
    with st.form("vol_reg"):
        v_name = st.text_input("Full Name *")
        v_city = st.text_input("City *")
        v_bg = st.selectbox("Blood Group", ["N/A", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        v_skills = st.text_input("Skills (e.g. Blood Donor, Driving, First Aid)")
        v_avail = st.selectbox("Availability", ["Available", "Weekends Only", "Emergency Only"])
        reg_btn = st.form_submit_button("Register")

        if reg_btn:
            if v_name and v_city:
                st.session_state.volunteers.append({
                    "name": v_name,
                    "city": v_city,
                    "blood_group": v_bg,
                    "skills": v_skills,
                    "availability": v_avail
                })
                st.success("Registered as an active volunteer!")
            else:
                st.error("Name and City are required.")

# 5. ADMIN DASHBOARD
elif menu == "Admin Dashboard":
    st.title("🛡️ Admin Moderation Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Requests", len(st.session_state.requests))
    c2.metric("Active Volunteers", len(st.session_state.volunteers))
    c3.metric("Resolved Aid", len([r for r in st.session_state.requests if r["status"] == "Resolved"]))

    st.subheader("Manage Help Requests")
    for req in list(st.session_state.requests):
        col_x, col_y, col_z = st.columns([3, 2, 1])
        col_x.write(f"**{req['title']}** ({req['category']})")
        req["status"] = col_y.selectbox(
            "Status",
            ["Open", "In Progress", "Resolved", "Cancelled"],
            index=["Open", "In Progress", "Resolved", "Cancelled"].index(req["status"]),
            key=f"status_{req['id']}"
        )
        if col_z.button("Delete", key=f"del_{req['id']}"):
            st.session_state.requests.remove(req)
            st.rerun()

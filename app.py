import streamlit as st

st.set_page_config(page_title="NGO App", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #dbeafe 0%, #e9d5ff 50%, #c7d2fe 100%);
}

h1 {
    text-align: center;
    font-size: 50px;
    font-weight: 800;
    color: #312e81;
}

.section-title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    color: #3730a3;
    margin-bottom: 10px;
}

.text {
    text-align: center;
    font-size: 18px;
    color: #4c1d95;
    margin-bottom: 25px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    padding: 12px;
    font-size: 17px;
    font-weight: 600;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
}

div[data-testid="stTextInput"] input {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "login"

st.title("NGO Finance AI")

if st.session_state.page == "login":

    st.markdown('<div class="section-title">Login</div>', unsafe_allow_html=True)

    user = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if user == "" or password == "":
            st.warning("Complete all fields")
        else:
            st.session_state.page = "dashboard"
            st.rerun()

    if st.button("Create Account"):
        st.session_state.page = "create"
        st.rerun()


elif st.session_state.page == "create":

    st.markdown('<div class="section-title">Create Account</div>', unsafe_allow_html=True)

    user = st.text_input("Username", key="create_user")
    password = st.text_input("Password", type="password", key="create_pass")
    org = st.text_input("Organization", key="create_org")

    if st.button("Create Account Now"):
        if user == "" or password == "" or org == "":
            st.warning("Complete all fields")
        else:
            st.success("Account created")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


elif st.session_state.page == "dashboard":

    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)

    st.markdown('<div class="text">Here you can manage your financial data.</div>', unsafe_allow_html=True)

    st.markdown('<div class="text">View reports to see summaries of your data.</div>', unsafe_allow_html=True)

    st.markdown('<div class="text">Edit data to modify or update existing information.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("View Reports"):
            st.session_state.page = "reports"
            st.rerun()

    with col2:
        if st.button("Edit Data"):
            st.session_state.page = "edit"
            st.rerun()

    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()


elif st.session_state.page == "reports":

    st.markdown('<div class="section-title">Reports</div>', unsafe_allow_html=True)

    st.markdown('<div class="text">This section will display financial reports.</div>', unsafe_allow_html=True)

    st.markdown('<div class="text">You will be able to filter and analyze data here.</div>', unsafe_allow_html=True)

    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


elif st.session_state.page == "edit":

    st.markdown('<div class="section-title">Edit Data</div>', unsafe_allow_html=True)

    st.markdown('<div class="text">Here you can modify existing data entries.</div>', unsafe_allow_html=True)

    st.markdown('<div class="text">Changes will be saved in the database later.</div>', unsafe_allow_html=True)

    value = st.text_input("Modify something")

    if st.button("Save Changes"):
        if value == "":
            st.warning("Write something first")
        else:
            st.success("Changes saved")

    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
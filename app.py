import streamlit as st

st.set_page_config(page_title="ngo app", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #dbeafe, #ede9fe);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

h1, h2, h3 {
    color: #1e1b4b;
    text-align: center;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
    justify-content: center;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: white;
    border-radius: 10px 10px 0px 0px;
    padding: 10px 20px;
    color: #1e1b4b;
    font-weight: 600;
}

.stButton > button {
    background-color: #6366f1;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-size: 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #4f46e5;
    color: white;
}

div[data-testid="stTextInput"] input {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("NGO Finance AI")

tab1, tab2 = st.tabs(["login", "create account"])

with tab1:
    st.subheader("login")

    login_user = st.text_input("username or email", key="login_user")
    login_pass = st.text_input("password", type="password", key="login_pass")

    if st.button("login"):
        if login_user == "" or login_pass == "":
            st.warning("complete all fields")
        else:
            st.success("login pressed")

with tab2:
    st.subheader("create account")

    create_user = st.text_input("username", key="create_user")
    create_pass = st.text_input("password", type="password", key="create_pass")
    create_org = st.text_input("organization", key="create_org")

    if st.button("create account"):
        if create_user == "" or create_pass == "" or create_org == "":
            st.warning("complete all fields")
        else:
            st.success("account created")
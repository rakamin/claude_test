import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def load_config():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def main():
    st.set_page_config(page_title="Multi-page Streamlit App", layout="wide")

    # Load configuration
    config = load_config()

    # Create an authentication object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # Add login widget
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        authenticator.logout('Logout', 'sidebar')
        st.sidebar.title(f"Welcome {name}")
        
        # Sidebar for navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Home", "About"])

        if page == "Home":
            home_page()
        elif page == "About":
            about_page()

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

def home_page():
    st.title("Home Page")
    st.write("Welcome to the home page of our Streamlit app!")
    st.write("This is where you can put your main content.")

def about_page():
    st.title("About Page")
    st.write("This is the about page of our Streamlit app.")
    st.write("Here you can provide information about your app or yourself.")

if __name__ == "__main__":
    main()

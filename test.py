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

    # Custom CSS for OneNote-style navigation
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        background-color: transparent;
        color: #000000;
        border: none;
        text-align: left;
        padding: 10px 15px;
        font-size: 16px;
        border-radius: 0;
    }
    .stButton > button:hover {
        background-color: #f0f0f0;
    }
    .stButton > button:focus {
        background-color: #e0e0e0;
        color: #0078d4;
        box-shadow: none;
    }
    </style>
    """, unsafe_allow_html=True)

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
        
        # Use session state to keep track of the current page
        if 'page' not in st.session_state:
            st.session_state.page = 'Home'

        # Create OneNote-style navigation buttons
        pages = ['Home', 'About']
        for page in pages:
            button_style = "background-color: #e0e0e0; color: #0078d4;" if st.session_state.page == page else ""
            if st.sidebar.button(page, key=page, help=f"Go to {page} page", 
                                 on_click=lambda p=page: setattr(st.session_state, 'page', p)):
                st.rerun()

        # Display the selected page
        if st.session_state.page == 'Home':
            home_page()
        elif st.session_state.page == 'About':
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

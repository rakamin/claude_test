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

    # Custom CSS for panel-style navigation
    st.markdown("""
    <style>
    .nav-link {
        padding: 15px 20px;
        margin: 5px 0;
        border-radius: 5px 0 0 5px;
        text-decoration: none;
        display: block;
        text-align: left;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    .nav-link:hover {
        background-color: #f0f0f0;
    }
    .nav-link.active {
        background-color: #ffffff;
        color: #0078d4;
        font-weight: bold;
        border-right: 5px solid #0078d4;
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

        # Create panel-style navigation
        pages = ['Home', 'About']
        for page in pages:
            active_class = "active" if st.session_state.page == page else ""
            if st.sidebar.markdown(f"""
                <a href="#" class="nav-link {active_class}" id="{page}-link">{page}</a>
                """, unsafe_allow_html=True):
                st.session_state.page = page
                st.experimental_rerun()

        # JavaScript to handle click events
        st.sidebar.markdown("""
        <script>
        const links = document.querySelectorAll('.nav-link');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                window.streamlitPyRerun();
            });
        });
        </script>
        """, unsafe_allow_html=True)

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

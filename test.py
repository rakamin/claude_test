import streamlit as st

def main():
    st.set_page_config(page_title="My Streamlit App", layout="wide")

    # Custom CSS to style the sidebar and buttons
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        background-color: #ffffff;
        color: #31333F;
        border: 1px solid #d0d3d9;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        transition: background-color 0.3s, box-shadow 0.3s;
    }
    .stButton > button:hover {
        background-color: #f0f2f6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button:focus {
        box-shadow: 0 0 0 0.2rem rgba(49, 51, 63, 0.25);
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a sidebar for navigation
    st.sidebar.title("Navigation")

    # Use session state to keep track of the current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    # Create navigation buttons styled as panels
    if st.sidebar.button("📁 Home"):
        st.session_state.current_page = "Home"
    if st.sidebar.button("ℹ️ About"):
        st.session_state.current_page = "About"

    # Display the selected page
    if st.session_state.current_page == "Home":
        home_page()
    elif st.session_state.current_page == "About":
        about_page()

def home_page():
    st.title("Home Page")
    st.write("Welcome to the home page of our Streamlit app!")
    st.write("This is where you can put your main content.")
    
    # Add some example content
    st.header("Sample Data")
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'San Francisco', 'London']
    }
    st.dataframe(data)

def about_page():
    st.title("About Page")
    st.write("This is the about page of our Streamlit app.")
    st.write("Here you can provide information about your app or yourself.")
    
    # Add some example content
    st.header("Contact Information")
    st.write("Email: example@email.com")
    st.write("GitHub: https://github.com/yourusername")

if __name__ == "__main__":
    main()

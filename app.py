import streamlit as st
from  schema_download import get_data_dictionary
from main import input_request
hunt_schema = get_data_dictionary()



def main():
    st.title("KQL Generator")

    # Text input
    user_input = st.text_input("Enter your KQL request:")

    if user_input:
        # Process the input
        result = input_request(request=user_input,hunt_schema=hunt_schema)

        # Display the output in a scrollable text area
        st.text_area("Output:", value=result, height=300)

if __name__ == "__main__":
    main()
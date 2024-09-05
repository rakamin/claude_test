import streamlit as st
import yaml
from pathlib import Path

def load_folder_structure(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

def display_folder_structure(structure, indent=0):
    for key, value in structure.items():
        st.write('  ' * indent + f"- {key}")
        if isinstance(value, dict):
            display_folder_structure(value, indent + 1)

def main():
    st.set_page_config(layout="wide")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Input and Output")
        user_input = st.text_area("Enter your text here:", height=200)
        if st.button("Process"):
            st.subheader("Output:")
            st.write(f"You entered: {user_input}")

    with col2:
        st.header("Folder Structure")
        if st.button("Show Folder Structure"):
            yaml_file = "folder_structure.yaml"
            if Path(yaml_file).is_file():
                folder_structure = load_folder_structure(yaml_file)
                st.subheader("Folder Structure from YAML:")
                display_folder_structure(folder_structure)
            else:
                st.error(f"YAML file '{yaml_file}' not found.")

if __name__ == "__main__":
    main()

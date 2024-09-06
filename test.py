import streamlit as st
import yaml
from pathlib import Path

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def display_yaml_structure(data, prefix=''):
    if not isinstance(data, dict):
        st.error(f"Expected a dictionary, but got {type(data)}. Data: {data}")
        return

    for key, value in data.items():
        if isinstance(value, dict):
            if st.button(f"{prefix}{key}", key=f"btn_{prefix}{key}"):
                st.write(f"Contents of {key}:")
                for script, query in value.items():
                    st.write(f"- {script}: {query}")
        else:
            st.write(f"{prefix}{key}: {value}")

def main():
    st.set_page_config(layout="wide")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.title("Main App Operations")
        st.write("Your main app content goes here.")

    with col2:
        st.title("YAML Source")
        yaml_file = "example_structure.yaml"
        
        if st.button("Source", key="source_button"):
            yaml_data = load_yaml(yaml_file)
      

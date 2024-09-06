import streamlit as st
import yaml
from pathlib import Path

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def display_yaml_structure(data, prefix=''):
    for key, value in data.items():
        if isinstance(value, dict):
            if st.button(f"{prefix}{key}", key=f"{prefix}{key}"):
                st.write("Scripts:")
                for script in value.keys():
                    st.write(f"- {script}")
        else:
            st.write(f"{prefix}{key}")

def main():
    st.set_page_config(layout="wide")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.title("Main App Operations")
        # Your main app operations go here
        st.write("Your main app content goes here.")

    with col2:
        st.title("YAML Source")
        yaml_file = "example_structure.yaml"  # We'll create this file
        
        if st.button("Source"):
            yaml_data = load_yaml(yaml_file)
            st.write("YAML Structure:")
            display_yaml_structure(yaml_data)

if __name__ == "__main__":
    # Create example YAML file
    example_yaml = """
    source:
      team_a:
        script1: SELECT * FROM table_a
        script2: SELECT COUNT(*) FROM table_b
      team_b:
        script3: SELECT DISTINCT column FROM table_c
      team_c:
        script4: SELECT AVG(column) FROM table_d
        script5: SELECT * FROM table_e WHERE condition
    """
    
    with open("example_structure.yaml", "w") as f:
        f.write(example_yaml)
    
    main()

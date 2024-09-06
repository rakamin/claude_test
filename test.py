import streamlit as st
import os

def get_folder_structure(path):
    structure = {}
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            structure[item] = get_folder_structure(item_path)
        else:
            structure[item] = None
    return structure

def display_structure(structure, path=""):
    for key, value in structure.items():
        if value is None:  # It's a file
            if st.button(f"📄 {key}", key=os.path.join(path, key)):
                st.write(f"Selected file: {os.path.join(path, key)}")
                # Here you can add logic to display file contents or metadata
        else:  # It's a directory
            if st.button(f"📁 {key}", key=os.path.join(path, key)):
                st.write(f"Selected directory: {os.path.join(path, key)}")
                display_structure(value, os.path.join(path, key))

def main():
    st.title("Data Dictionary Navigator")
    
    # Replace this with the path to your data dictionary folder
    root_path = "/path/to/your/data/dictionary"
    
    structure = get_folder_structure(root_path)
    display_structure(structure)

if __name__ == "__main__":
    main()





import os

def create_sample_data_dictionary(root_path):
    structure = {
        "HR": {
            "employee_data.csv": "Employee ID,Name,Department,Salary",
            "performance_reviews": {
                "2023_reviews.xlsx": "Annual performance review data for 2023",
                "review_template.docx": "Template for conducting performance reviews"
            },
            "policies": {
                "employee_handbook.pdf": "Company policies and procedures",
                "leave_policy.txt": "Guidelines for requesting and approving leave"
            }
        },
        "Finance": {
            "financial_statements": {
                "income_statement_2023.xlsx": "Annual income statement for 2023",
                "balance_sheet_2023.xlsx": "Balance sheet as of Dec 31, 2023"
            },
            "budgets": {
                "department_budgets_2024.xlsx": "Projected budgets for all departments",
                "budget_guidelines.pdf": "Instructions for budget preparation"
            },
            "tax_documents": {
                "tax_return_2023.pdf": "Corporate tax return for 2023",
                "tax_id_info.txt": "Company tax identification numbers"
            }
        },
        "Marketing": {
            "campaigns": {
                "summer_sale_2024.pptx": "Presentation for upcoming summer sale campaign",
                "social_media_calendar.xlsx": "Planned social media posts for Q2 2024"
            },
            "market_research": {
                "competitor_analysis.pdf": "Detailed analysis of main competitors",
                "customer_survey_results.csv": "Raw data from recent customer satisfaction survey"
            },
            "brand_assets": {
                "logo_guidelines.pdf": "Official logo usage and brand guidelines",
                "product_images": {
                    "product_a.jpg": "High-resolution image of Product A",
                    "product_b.jpg": "High-resolution image of Product B"
                }
            }
        },
        "IT": {
            "network_diagrams": {
                "company_network.vsdx": "Visio diagram of company network architecture",
                "server_rack_layout.png": "Diagram of physical server rack layout"
            },
            "software_licenses": {
                "license_inventory.xlsx": "Inventory of all software licenses",
                "renewal_calendar.pdf": "Schedule of upcoming license renewals"
            },
            "security_policies": {
                "data_protection_policy.docx": "Company data protection and privacy policy",
                "incident_response_plan.pdf": "Procedures for responding to security incidents"
            }
        }
    }

    def create_structure(path, structure):
        for key, value in structure.items():
            new_path = os.path.join(path, key)
            if isinstance(value, dict):
                os.makedirs(new_path, exist_ok=True)
                create_structure(new_path, value)
            else:
                with open(new_path, 'w') as f:
                    f.write(value)

    create_structure(root_path, structure)
    print(f"Sample data dictionary created at: {root_path}")

# Usage
# create_sample_data_dictionary("/path/to/your/data/dictionary")

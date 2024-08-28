# filename: extract_table_to_dataframe.py

import re
import pandas as pd

# Define the table data as a multi-line string
table_data = """
| Column name | Data type | Description |
|-------------|-----------|-------------|
| `Timestamp` | `datetime` | Date and time when the event was recorded |
| `ActionType` | `string` | Type of activity that triggered the event |
| `Application` | `string` | Application that performed the recorded action |
| `ApplicationId` | `int` | Unique identifier for the application |
| `AppInstanceId` | `int` | Unique identifier for the instance of an application. To convert this to Microsoft Defender for Cloud Apps App-connector-ID, use `CloudAppEvents | distinct ApplicationId,AppInstanceId,binary_or(binary_shift_left(AppInstanceId,20),ApplicationId |order by ApplicationId,AppInstanceId` |
| `AccountObjectId` | `string` | Unique identifier for the account in Microsoft Entra ID |
| `AccountId` | `string` | An identifier for the account as found by Microsoft Defender for Cloud Apps. Could be Microsoft Entra ID, user principal name, or other identifiers. |
| `AccountDisplayName` | `string` | Name displayed in the address book entry for the account user. This is usually a combination of the given name, middle initial, and surname of the user. |
| `IsAdminOperation` | `bool` | Indicates whether the activity was performed by an administrator |
| `AuditSource` | `string` | Audit data source, including one of the following: <br>- Defender for Cloud Apps access control <br>- Defender for Cloud Apps session control <br>- Defender for Cloud Apps app connector |
| `SessionData` |`dynamic` | The Defender for Cloud Apps session ID for access or session control. For example: `{InLineSessionId:"232342"}` |
|`OAuthAppId`|`string`| A unique identifier that's assigned to an application when it's registered to Entra with OAuth 2.0 |
"""

# Use regex to extract the table contents
pattern = r'\|\s*`?(\w+)`?\s*\|\s*`?(\w+)`?\s*\|\s*(.+?)\s*\|'
matches = re.findall(pattern, table_data, re.DOTALL)

# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(matches, columns=['Column name', 'Data type', 'Description'])

# Clean up the Description column by removing newlines and extra spaces
df['Description'] = df['Description'].apply(lambda x: ' '.join(x.split()))

# Print the DataFrame
print(df.to_string(index=False))

# Verify the number of rows
print(f"\nNumber of rows: {len(df)}")

# Verify that all column names are present
column_names = ['Timestamp', 'ActionType', 'Application', 'ApplicationId', 'AppInstanceId', 'AccountObjectId', 'AccountId', 'AccountDisplayName', 'IsAdminOperation', 'AuditSource', 'SessionData', 'OAuthAppId']
missing_columns = [col for col in column_names if col not in df['Column name'].values]
if missing_columns:
    print(f"\nMissing columns: {', '.join(missing_columns)}")
else:
    print("\nAll expected columns are present.")

# Print unique values in the 'Column name' column to check for any unexpected entries
print("\nUnique values in 'Column name' column:")
print(df['Column name'].unique())

# Additional verifications
print("\nVerifying data types:")
expected_data_types = {
    'Timestamp': 'datetime',
    'ActionType': 'string',
    'Application': 'string',
    'ApplicationId': 'int',
    'AppInstanceId': 'int',
    'AccountObjectId': 'string',
    'AccountId': 'string',
    'AccountDisplayName': 'string',
    'IsAdminOperation': 'bool',
    'AuditSource': 'string',
    'SessionData': 'dynamic',
    'OAuthAppId': 'string'
}

for col, expected_type in expected_data_types.items():
    actual_type = df[df['Column name'] == col]['Data type'].values[0]
    if actual_type == expected_type:
        print(f"✓ {col}: {actual_type}")
    else:
        print(f"✗ {col}: Expected {expected_type}, got {actual_type}")

print("\nVerifying descriptions (first 50 characters):")
expected_descriptions = {
    'Timestamp': 'Date and time when the event was recorded',
    'ActionType': 'Type of activity that triggered the event',
    'Application': 'Application that performed the recorded action',
    'ApplicationId': 'Unique identifier for the application',
    'AppInstanceId': 'Unique identifier for the instance of an application',
    'AccountObjectId': 'Unique identifier for the account in Microsoft Entra',
    'AccountId': 'An identifier for the account as found by Microsoft',
    'AccountDisplayName': 'Name displayed in the address book entry for the a',
    'IsAdminOperation': 'Indicates whether the activity was performed by an',
    'AuditSource': 'Audit data source, including one of the following:',
    'SessionData': 'The Defender for Cloud Apps session ID for access',
    'OAuthAppId': 'A unique identifier that\'s assigned to an applicati'
}

for col, expected_desc in expected_descriptions.items():
    actual_desc = df[df['Column name'] == col]['Description'].values[0][:50]
    if actual_desc.startswith(expected_desc[:50]):
        print(f"✓ {col}: {actual_desc}")
    else:
        print(f"✗ {col}: Expected '{expected_desc[:50]}', got '{actual_desc}'")
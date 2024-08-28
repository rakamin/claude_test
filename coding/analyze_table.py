# filename: analyze_table.py

import pandas as pd
import re

# Define the table string (same as before)
table_string = """
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

# Extract data using regex (same as before)
pattern = r'\|[ `]*(\w+)[ `]*\|[ `]*(\w+)[ `]*\|(.*?)\|(?=\n|\Z)'
matches = re.findall(pattern, table_string, re.DOTALL)

# Create pandas DataFrame
df = pd.DataFrame(matches, columns=['Column name', 'Data type', 'Description'])
df['Description'] = df['Description'].str.strip()

print("Original DataFrame:")
print(df)
print("\n")

# 1. Get basic information about the DataFrame
print("DataFrame Info:")
df.info()
print("\n")

# 2. Get summary statistics for string length of descriptions
df['Description_Length'] = df['Description'].str.len()
print("Description Length Statistics:")
print(df['Description_Length'].describe())
print("\n")

# 3. Group by data type and count
print("Count of Columns by Data Type:")
print(df['Data type'].value_counts())
print("\n")

# 4. Find columns with 'ID' or 'Id' in the name
id_columns = df[df['Column name'].str.contains('ID|Id')]
print("Columns with 'ID' or 'Id' in the name:")
print(id_columns[['Column name', 'Data type']])
print("\n")

# 5. Search for a specific keyword in descriptions
keyword = "Microsoft Defender"
matching_rows = df[df['Description'].str.contains(keyword, case=False)]
print(f"Columns with '{keyword}' in the description:")
print(matching_rows[['Column name', 'Description']])
print("\n")

# 6. Create a new column with a simplified data type
def simplify_data_type(data_type):
    if data_type in ['string', 'datetime']:
        return 'text'
    elif data_type in ['int', 'bool']:
        return 'numeric'
    else:
        return 'other'

df['Simplified_Type'] = df['Data type'].apply(simplify_data_type)
print("DataFrame with Simplified Data Types:")
print(df[['Column name', 'Data type', 'Simplified_Type']])
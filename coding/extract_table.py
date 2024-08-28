# filename: extract_table.py

import re
import pandas as pd

# Define the table string
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

# Extract data using regex
pattern = r'\|[ `]*(\w+)[ `]*\|[ `]*(\w+)[ `]*\|(.*?)\|(?=\n|\Z)'
matches = re.findall(pattern, table_string, re.DOTALL)

# Create pandas DataFrame
df = pd.DataFrame(matches, columns=['Column name', 'Data type', 'Description'])

# Clean up the Description column
df['Description'] = df['Description'].str.strip()

# Display the DataFrame
print(df)
print("\n")

# Verify data
original_data = [
    ('Timestamp', 'datetime', 'Date and time when the event was recorded'),
    ('ActionType', 'string', 'Type of activity that triggered the event'),
    ('Application', 'string', 'Application that performed the recorded action'),
    ('ApplicationId', 'int', 'Unique identifier for the application'),
    ('AppInstanceId', 'int', 'Unique identifier for the instance of an application. To convert this to Microsoft Defender for Cloud Apps App-connector-ID, use `CloudAppEvents | distinct ApplicationId,AppInstanceId,binary_or(binary_shift_left(AppInstanceId,20),ApplicationId |order by ApplicationId,AppInstanceId`'),
    ('AccountObjectId', 'string', 'Unique identifier for the account in Microsoft Entra ID'),
    ('AccountId', 'string', 'An identifier for the account as found by Microsoft Defender for Cloud Apps. Could be Microsoft Entra ID, user principal name, or other identifiers.'),
    ('AccountDisplayName', 'string', 'Name displayed in the address book entry for the account user. This is usually a combination of the given name, middle initial, and surname of the user.'),
    ('IsAdminOperation', 'bool', 'Indicates whether the activity was performed by an administrator'),
    ('AuditSource', 'string', 'Audit data source, including one of the following: <br>- Defender for Cloud Apps access control <br>- Defender for Cloud Apps session control <br>- Defender for Cloud Apps app connector'),
    ('SessionData', 'dynamic', 'The Defender for Cloud Apps session ID for access or session control. For example: `{InLineSessionId:"232342"}`'),
    ('OAuthAppId', 'string', 'A unique identifier that\'s assigned to an application when it\'s registered to Entra with OAuth 2.0')
]

# Compare DataFrame with original data
for i, row in enumerate(original_data):
    if i < len(df):
        if (df.iloc[i]['Column name'] == row[0] and 
            df.iloc[i]['Data type'] == row[1] and 
            df.iloc[i]['Description'].strip() == row[2].strip()):
            print(f"Row {i} matches.")
        else:
            print(f"Row {i} does not match.")
            print("Original:", row)
            print("DataFrame:", df.iloc[i].tolist())
    else:
        print(f"Row {i} is missing in the DataFrame.")
        print("Original:", row)

# Check if all rows match
if (len(df) == len(original_data) and
    all(df.iloc[i]['Column name'] == row[0] and 
        df.iloc[i]['Data type'] == row[1] and 
        df.iloc[i]['Description'].strip() == row[2].strip() 
        for i, row in enumerate(original_data))):
    print("\nAll data in the DataFrame matches the original string.")
else:
    print("\nSome data in the DataFrame does not match the original string.")
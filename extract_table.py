# filename: extract_table.py

import pandas as pd
import re

# Define the table as a multi-line string
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

# Split the table into lines
lines = table_data.strip().split('\n')

# Extract header
header = ['Column name', 'Data type', 'Description']

# Parse the data
data = []
current_row = []
for line in lines[2:]:  # Skip the header and separator lines
    if line.strip().startswith('|'):
        if current_row:
            data.append(current_row)
            current_row = []
        parts = [part.strip() for part in line.split('|')[1:-1]]
        current_row = parts[:3]  # Take only the first three columns
        if len(parts) > 3:
            current_row[2] += ' ' + ' '.join(parts[3:])
    else:
        # This is a continuation of the previous description
        current_row[2] += ' ' + line.strip()

# Add the last row
if current_row:
    data.append(current_row)

# Create DataFrame
df = pd.DataFrame(data, columns=header)

# Clean up the DataFrame
df['Column name'] = df['Column name'].str.replace('`', '')
df['Data type'] = df['Data type'].str.replace('`', '')

# Display the resulting DataFrame
print(df)

# Optional: Save the DataFrame to a CSV file
df.to_csv('table_data.csv', index=False)
print("\nDataFrame has been saved to 'table_data.csv'")
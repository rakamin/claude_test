import pandas as pd
import re

table = """
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
|`OAuthAppId`|`string`| A unique identifier that's assigned to an application when it’s registered to Entra with OAuth 2.0 | 
"""

# Remove the markers for the markdown table and separate the lines
lines = table.replace("|", "").split('\n')

# Remove any leading/tailing white space and ignore empty lines or line with only '-'
lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('-')]

# Split each line by multiple spaces into a list, while also removing unnecessary ` characters
data = []
for line in lines:
    row = [elem.replace("`", "").strip() for elem in re.split('  +', line)]
    data.append(row)

# The first row will be the headers and rest will be data
headers = data[0]
data_rows = data[1:]

# Create a DataFrame
df = pd.DataFrame(data_rows, columns=headers)
print(df)
import re
import pandas as pd

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

table_data = []
for line in table.split("\n"):
  # Skip empty lines or lines with only "-"
  if line.strip() and not line.startswith("|---"):
    row_data = []

    cell_data = ""
    in_backticks = False
    for char in line:
      if char == "`":
        in_backticks = not in_backticks
      elif char == "|" and not in_backticks:
        # End of a cell
        row_data.append(cell_data.strip())
        cell_data = ""
      else:
        cell_data += char
    table_data.append(row_data)

# The first row is the header of the dataframe
df = pd.DataFrame(table_data[1:], columns=table_data[0])
print(df)
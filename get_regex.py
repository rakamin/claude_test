import autogen
from autogen.coding import LocalCommandLineCodeExecutor
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())


assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": [{"model": "claude-3-5-sonnet-20240620", "api_key": os.environ["ANTHROPIC_API_KEY"],"api_type": "anthropic",}]},
)


# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
    },
)
# the assistant receives a message from the user_proxy, which contains the task description
# chat_res = user_proxy.initiate_chat(
#     assistant,
#     message="""Create a python code that extracts the table from the  url into a json object.
#     https://raw.githubusercontent.com/MicrosoftDocs/defender-docs/public/defender-xdr/advanced-hunting-cloudappevents-table.md""",
#     summary_method="reflection_with_llm",
# )

chat_res = user_proxy.initiate_chat(
    assistant,
    message="""Create a python code that extracts the table below into a pandas dataframe using regex. Make sure the data values in the string matches with all the values with the pandas dataframe and make sure to compare the full description text.
   
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
    """,
    summary_method="reflection_with_llm",
)
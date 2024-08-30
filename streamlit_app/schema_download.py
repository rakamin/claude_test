import requests
import re
import pandas as pd
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# def get_fields(url):
#     response = requests.get(url)
#     markdown_content = response.text
#     if url == "https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-xdr/advanced-hunting-cloudappevents-table.md":
#         markdown_content = markdown_content.replace("To convert this to Microsoft Defender for Cloud Apps App-connector-ID, use `CloudAppEvents | distinct ApplicationId,AppInstanceId,binary_or(binary_shift_left(AppInstanceId,20),ApplicationId |order by ApplicationId,AppInstanceId`","")
#     matches = re.findall(r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|",markdown_content)
#     # Create Dataframe
#     df = pd.DataFrame(matches, columns=["Column name", "Data type", "Description"])
#     df = df[2:]
#     df["Column name"] = df["Column name"].str.strip("`")
#     df["Data type"] = df["Data type"].str.strip("`")
#     dict_out = df.to_dict(orient="records")
#     return dict_out

def get_fields(url):
    response = requests.get(url)
    markdown_content = response.text
    pattern = r'\|[ `]*(\w+)[ `]*\|[ `]*(\w+)[ `]*\|(.*?)\|(?=\n|\Z)'
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    # Create Dataframe
    df = pd.DataFrame(matches, columns=['Column name', 'Data type', 'Description'])
    dict_out = df.to_dict(orient="records")
    return dict_out



raw_url = "https://raw.githubusercontent.com/MicrosoftDocs/defender-docs/public/defender-xdr/"
schema_url = raw_url + "advanced-hunting-schema-tables.md"

response = requests.get(schema_url)

markdown_content = response.text

# Extract table name and description
matches = re.findall(r"\| \*\*(.*)\*\* \| (.*) \|", markdown_content, re.MULTILINE)

df = pd.DataFrame(matches, columns = ["table_name", "description"])

# Get data dictionaries from table urls
df[['table_name','file_name']] = df['table_name'].str.extract(r'\[(.*)\]\((.*)\)')
df['file_path'] = raw_url + df["file_name"].apply(lambda x: x.lower())
df["data_dictionary"] = df["file_path"].apply(get_fields)
df["field_count"] = df["data_dictionary"].apply(len)

df_schema = df.drop(columns=["file_name","file_path","field_count"])


def get_data_dictionary():
    metadata_out = df_schema.to_json(orient="records")
    return metadata_out

token_count_lambda = lambda row: num_tokens_from_string(row.to_json(),"cl100k_base")

df_schema["token_count"] = df_schema.apply(token_count_lambda, axis=1)

def split_data_dictionary(df_schema,token_limit):
    datasets = []
    current_dataset = []
    current_token_count = 0
    metadata_list = []
    for index, row in df_schema.iterrows():
        current_dataset.append(row)
        current_token_count +=row["token_count"]
        if current_token_count > token_limit:
            datasets.append(pd.DataFrame(current_dataset))
            json_list = pd.DataFrame(current_dataset).drop('token_count', axis=1).to_json(orient="records")
            metadata_list.append(json_list)
            current_dataset = []
            current_token_count = 0
    if current_dataset:
        datasets.append(pd.DataFrame(current_dataset))
        json_list = pd.DataFrame(current_dataset).drop('token_count', axis=1).to_json(orient="records")
        metadata_list.append(json_list)
    return metadata_list

def get_metadata_list():
    metadata_list = split_data_dictionary(df_schema,5000)
    return metadata_list

def get_tables_wo_timestamp():
    df_timestamp = df_schema.copy(deep=True)
    df_timestamp['data_dictionary'] = df_timestamp['data_dictionary'].astype(str)
    df_timestamp = df_timestamp.loc[~df_timestamp["data_dictionary"]].str.contains("'Column name': 'Timestamp'", case=False, na=False)
    tables_wo_timestamp = df_timestamp["table_name"].to_list()
    return tables_wo_timestamp



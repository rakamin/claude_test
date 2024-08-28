import anthropic
from schema_download import get_data_dictionary
import pprint
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())

data_dictionary = get_data_dictionary()


client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=5000,
    temperature=0,
    system="You are an expert KQL agent who strictly works off the below data dictionary. You are helping SOC analyst find the relevant data acorss the tenant so consider all possible scenarios where the data can exist. Try to maximize the scenarios where it can exist.\n\n"
    f"{data_dictionary}",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Crafr a KQL query to look across the tenant for the presence of this file FileName 'oTXDSrHkVj.exe' or hash for it '62d26873Cda8d6e99f1e93c3a6efd00dcc50f3fe8554e910ecfa28021f75a66d' in the past 7 days."
                }
            ]
        }
    ]
)
print(message.content)

print(message)

pprint.pprint(message.content)

pprint.pprint(message.content[0].text)



message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=5000,
    temperature=0,
    system="You are an expert KQL agent who strictly works off the below data dictionary. You are helping SOC analyst find the relevant data acorss the tenant so consider all possible scenarios where the data can exist. Try to maximize the scenarios where the data can be available.\n\n"
    f"{data_dictionary}",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Return a list of all the hosts with Zerto installed."
                }
            ]
        }
    ]
)
print(message.content)

print(message)

pprint.pprint(message.content)

pprint.pprint(message.content[0].text)




message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=5000,
    temperature=0,
    system="You are a helpful agent.\n\n"
    f"{data_dictionary}",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What model are you?"
                }
            ]
        }
    ]
)
print(message.content)

print(message)

pprint.pprint(message.content)

pprint.pprint(message.content[0].text)
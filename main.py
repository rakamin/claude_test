import anthropic
from dotenv import load_dotenv,find_dotenv
from schema_download import get_data_dictionary
load_dotenv(find_dotenv())

hunt_schema = get_data_dictionary()

sys_prompt = open(r"./prompts/system.md","r",encoding="utf-8")
system_message = sys_prompt.read()

client = anthropic.Anthropic()

def input_request(request,hunt_schema):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=f"{system_message}\n\n"
        f"{hunt_schema}",
        messages=[
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": request
                }
            ]
        }
        ]

    )

    return message.content[0].text

#request = input("Enter your request to generate KQL: ")
#print(input_request(request=request,hunt_schema=hunt_schema))
import streamlit as st
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

def create_agents():
    # Load LLM inference endpoints from an env file
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    
    # Create an AssistantAgent instance
    assistant = AssistantAgent(
        name="assistant",
        llm_config={"config_list": config_list},
    )
    
    # Create a UserProxyAgent instance
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
    )
    
    return assistant, user_proxy

def initiate_chat(user_proxy, assistant, user_message):
    chat_result = user_proxy.initiate_chat(
        assistant,
        message=user_message,
    )
    return chat_result

def display_chat_messages(chat_result):
    for message in chat_result:
        with st.chat_message(message['name']):
            st.write(message['content'])

def main():
    st.set_page_config(layout="wide")
    st.title("AutoGen Chat Display")

    # Create agents
    assistant, user_proxy = create_agents()

    # User input
    user_message = st.text_area("Enter your message for the AI assistant:", height=100)

    if st.button("Start Chat"):
        if user_message:
            with st.spinner("Processing..."):
                chat_result = initiate_chat(user_proxy, assistant, user_message)
            
            st.subheader("Chat Result:")
            display_chat_messages(chat_result)
        else:
            st.warning("Please enter a message before starting the chat.")

if __name__ == "__main__":
    main()

import openai
import os
from dotenv import find_dotenv, load_dotenv
import time
import requests
import json
import streamlit as st

load_dotenv()
client = openai.OpenAI()
model = "gpt-4"

#I want to find a saint that is less well-known and is very intellectual/ is a theologian

def get_response(client, thread_id):
    messages = client.beta.threads.messages.list(
        thread_id = thread_id
    )
    summary = []
            
    # Get the latest message
    last_message = messages.data[0]
    role = last_message.role
    response = last_message.content[0].text.value

    # Append its response to the summary list
    summary.append(response)
    summary = "\n".join(summary)

    return summary

def wait_for_completion(client, thread_id, run_id):
    while True:
        time.sleep(5)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        print(f"RUN STATUS: {run.status}")
        #print(f"RUN STATUS: {run_status.model_dump_json(indent=4)}")

        if run.status == "completed":
            response = get_response(client, thread_id)
            if response and client.beta.threads.messages.list(
                thread_id=thread_id
            ).data[0].role == "assistant":
                return response  
        elif run.status == "failed":
            print("RUN FAILED")
            break     

def main():

    st.title("Find your patron saint!")

    gender = st.radio(
        "Would you like a saint of a particular gender? ",
        ["Male", "Female", "Both are fine"],
        index=2,  # Default to 'Both'
        horizontal= True
    )

    with st.form(key="user_input_form"):
        instructions = st.text_input("Enter topic")
        submit_button = st.form_submit_button(label= "Run")

        if submit_button:
            # Create assistant
            assis = client.beta.assistants.create(
                name="Patron-saint-finder",
                instructions="You help people find their catholic patron saints",
                model=model
            )
            assistant_id = assis.id
            print("\nCREATED ASSISTANT\n")
        
            # Create thread
            thread = client.beta.threads.create()
            thread_id = thread.id
            print("\nCREATED THREAD\n")

            # Add message
            client.beta.threads.messages.create(
                thread_id = thread.id,
                role = "user",
                content = f"Recommend to the user 5 catholic patron saints of gender {gender} best suited to their preferences: {instructions}. "
            )
            print("\nADDED MESSAGE\n")

            # Run assistant
            run = client.beta.threads.runs.create(
                thread_id = thread.id,
                assistant_id = assis.id
            )
            print("\nRUN THREAD\n")

            response = wait_for_completion(client, thread_id, run.id)
            st.write(response)


if __name__ == "__main__":
    main()

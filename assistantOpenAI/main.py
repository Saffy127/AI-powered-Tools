import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime


load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"

'''
#Create our Assistant
crypto_trainer = client.beta.assistants.create(
    name="Crypto Trainer",
    instructions="""You are a helpful assistant, who is an expert in crypto currencies.""",
    model=model,
)

assistant_id = crypto_trainer.id
print(assistant_id)
#print(personal_trainer_assis.id)
"""

#Thread
"""
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "How do I get started in crypto?"
        }
    ]
)

thread_id = thread.id
print(thread_id)
'''

# Hardcode our ids
assistant_id = "asst_SnZ2LbWJhZYtQTckfzjfJJ1t"
thread_id = "thread_FscPpHMLegjJ9YP2HJcEC0sv"


message = "What are the basics of crypto currencies?"
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message
)


# === Run our Assistant === 
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="Please address the user as Iron Man"
)


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

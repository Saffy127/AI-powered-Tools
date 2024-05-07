import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime


load_dotenv()

client = openai.OpenAI()
#model = "gpt-3.5-turbo-16k"

#Create our Assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-turbo",
)

# Now we create a thread. A Thread represents a conversation with a user and one or many Assistants. You can create a thread when a user (or your AI application) starts a conversation with your Assistant
thread = client.beta.threads.create()

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

import os
from dotenv import load_dotenv
from agentmail import AgentMail

load_dotenv()
api_key = os.getenv("AGENT_MAIL_API_KEY")

# Initialize the client
client = AgentMail(api_key=api_key)

# Create an inbox
print("Creating inbox...")
inbox = client.inboxes.create() # domain is optional
print("Inbox created successfully!")
print(inbox)

# fairartist543@agentmail.to - Email generated
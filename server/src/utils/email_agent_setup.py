import os
from dotenv import load_dotenv
from agentmail import AgentMail
import os

# Get the variable, returning None if not found
load_dotenv()

api_key = os.getenv("AGENT_MAIL_API_KEY")
ngrok_url = os.getenv("NGROK_URL")
client = AgentMail(api_key=api_key)

def email_setup():
    print("Setting up email webhook...")

    all_webhooks = client.webhooks.list()
    if any(webhook.url == f"{ngrok_url}/email/webhook" for webhook in all_webhooks.webhooks):
        print("Email webhook already exists.")
        return

    client.webhooks.create(
        url=f"{ngrok_url}/email/webhook",
        event_types=['message.received'],
    )
    print("Email webhook setup complete.")
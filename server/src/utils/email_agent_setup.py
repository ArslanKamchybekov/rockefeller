import os
from dotenv import load_dotenv
from agentmail import AgentMail

load_dotenv()

api_key = os.getenv("AGENT_MAIL_API_KEY")
ngrok_url = os.getenv("NGROK_URL")
client = AgentMail(api_key=api_key)

def email_setup():
    print("Setting up email webhook...")

    client.webhooks.create(
        url=f"{ngrok_url}/email/webhook",
        event_types=['message.received'],
    )

    print("Email webhook setup complete.")
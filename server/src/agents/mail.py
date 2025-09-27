import os
from dotenv import load_dotenv
from agentmail import AgentMail
import json
from email.utils import parseaddr
from src.utils.create_gemini import create_gemini_client

load_dotenv()

api_key = os.getenv("AGENT_MAIL_API_KEY")
ngrok_url = os.getenv("NGROK_URL")
client = AgentMail(api_key=api_key)

def respond_to_support_email(body):
    text = body.decode("utf-8")
    payload = json.loads(text)

    subject = payload['message']['subject']
    sender = payload['message']['from_']
    name, address = parseaddr(sender)
    message_body = payload['message']['text']

    prompt = f"""
        You are a customer support assistant for an e-commerce platform. A user has sent the following email:
        Subject: {subject}
        From: {name} <{address}>
        Message: {message_body}
        Please draft a polite and helpful response addressing their concerns. Keep the response concise and professional.
    """

    gemini_client = create_gemini_client()
    response = gemini_client.generate_content(
        prompt,
        generation_config={"temperature": 0.5},
    )

    reply_text = response.text
    reply_subject = f"Hey {name}! Re: {subject}"
    reply_to = address

    client.inboxes.messages.send(
        inbox_id=os.getenv("AGENT_MAIL"),
        to=reply_to,
        labels=["support"],
        subject=reply_subject,
        text=reply_text,
    )


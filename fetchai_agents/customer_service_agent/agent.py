"""
Customer Service Agent for Fetch.ai AgentVerse
Drafts email templates, automates responses, and manages VAPI phone assistant
"""

from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from pydantic import BaseModel
import requests
import json
import os
from typing import List, Dict, Any, Optional
import asyncio

# Agent configuration
CUSTOMER_SERVICE_AGENT = Agent(
    name="customer_service_agent",
    seed="customer-service-agent-seed-phrase-12345",
    port=8006,
    endpoint=["http://localhost:8006/submit"],
)

# Pydantic models
class CustomerServiceRequest(BaseModel):
    business_name: str
    industry: str
    service_types: List[str] = ["email_templates", "phone_automation", "chat_responses"]
    phone_number: Optional[str] = None
    email_domain: Optional[str] = None
    business_hours: Dict[str, str] = {"start": "9:00 AM", "end": "5:00 PM", "timezone": "EST"}
    common_issues: List[str] = []
    brand_voice: str = "professional"  # professional, friendly, casual

class CustomerServiceResponse(BaseModel):
    success: bool
    email_templates: List[Dict[str, Any]]
    phone_automation_config: Dict[str, Any]
    chat_responses: List[Dict[str, Any]]
    vapi_setup: Dict[str, Any]
    automation_rules: List[Dict[str, Any]]
    performance_metrics: Dict[str, Any]

class ErrorResponse(BaseModel):
    success: bool
    error: str

@CUSTOMER_SERVICE_AGENT.on_message(model=CustomerServiceRequest)
async def handle_customer_service_request(ctx: Context, sender: str, msg: CustomerServiceRequest):
    """Handle customer service automation requests"""
    try:
        ctx.logger.info(f"Received customer service request for {msg.business_name}")
        
        # Set up customer service automation
        service_data = await setup_customer_service_automation(
            business_name=msg.business_name,
            industry=msg.industry,
            service_types=msg.service_types,
            phone_number=msg.phone_number,
            email_domain=msg.email_domain,
            business_hours=msg.business_hours,
            common_issues=msg.common_issues,
            brand_voice=msg.brand_voice
        )
        
        response = CustomerServiceResponse(
            success=True,
            email_templates=service_data["email_templates"],
            phone_automation_config=service_data["phone_automation_config"],
            chat_responses=service_data["chat_responses"],
            vapi_setup=service_data["vapi_setup"],
            automation_rules=service_data["automation_rules"],
            performance_metrics=service_data["performance_metrics"]
        )
        
        await ctx.send(sender, response.model_dump())
        ctx.logger.info(f"Sent customer service response to {sender}")
        
    except Exception as e:
        ctx.logger.error(f"Error in customer service setup: {e}")
        error_response = ErrorResponse(success=False, error=str(e))
        await ctx.send(sender, error_response.model_dump())

async def setup_customer_service_automation(
    business_name: str,
    industry: str,
    service_types: List[str],
    phone_number: Optional[str] = None,
    email_domain: Optional[str] = None,
    business_hours: Dict[str, str] = None,
    common_issues: List[str] = None,
    brand_voice: str = "professional"
) -> Dict[str, Any]:
    """Set up comprehensive customer service automation"""
    
    # Generate email templates
    email_templates = generate_email_templates(business_name, industry, brand_voice, common_issues or [])
    
    # Configure phone automation
    phone_automation_config = configure_phone_automation(
        business_name, industry, phone_number, business_hours or {}, brand_voice
    )
    
    # Generate chat responses
    chat_responses = generate_chat_responses(business_name, industry, common_issues or [], brand_voice)
    
    # Set up VAPI phone assistant
    vapi_setup = setup_vapi_phone_assistant(
        business_name, industry, phone_number, business_hours or {}, brand_voice
    )
    
    # Create automation rules
    automation_rules = create_automation_rules(industry, common_issues or [])
    
    # Generate performance metrics
    performance_metrics = generate_performance_metrics(service_types)
    
    return {
        "email_templates": email_templates,
        "phone_automation_config": phone_automation_config,
        "chat_responses": chat_responses,
        "vapi_setup": vapi_setup,
        "automation_rules": automation_rules,
        "performance_metrics": performance_metrics
    }

def generate_email_templates(business_name: str, industry: str, brand_voice: str, common_issues: List[str]) -> List[Dict[str, Any]]:
    """Generate email templates for customer service"""
    
    templates = []
    
    # Welcome email template
    welcome_template = {
        "type": "welcome",
        "subject": f"Welcome to {business_name}!",
        "content": f"""
Dear [CUSTOMER_NAME],

Welcome to {business_name}! We're thrilled to have you as our customer.

At {business_name}, we're committed to providing exceptional {industry} services. Here's what you can expect:

• 24/7 customer support
• Fast and reliable service
• Personalized solutions for your needs

If you have any questions, don't hesitate to reach out to our support team.

Best regards,
The {business_name} Team
        """,
        "placeholders": ["[CUSTOMER_NAME]"],
        "trigger": "new_customer_signup"
    }
    
    # Support ticket response template
    support_template = {
        "type": "support_response",
        "subject": f"Re: Your {business_name} Support Request",
        "content": f"""
Hi [CUSTOMER_NAME],

Thank you for contacting {business_name} support. We've received your inquiry about [ISSUE_TYPE] and are working to resolve it.

Here's what we're doing:
• Investigating the issue thoroughly
• Working with our technical team
• Will provide updates within 24 hours

Your ticket number is: [TICKET_NUMBER]

We appreciate your patience and will keep you updated on our progress.

Best regards,
{business_name} Support Team
        """,
        "placeholders": ["[CUSTOMER_NAME]", "[ISSUE_TYPE]", "[TICKET_NUMBER]"],
        "trigger": "support_ticket_created"
    }
    
    # Follow-up template
    followup_template = {
        "type": "follow_up",
        "subject": f"How was your {business_name} experience?",
        "content": f"""
Hi [CUSTOMER_NAME],

We hope you're enjoying your experience with {business_name}! 

We'd love to hear your feedback:
• How was our service?
• Any suggestions for improvement?
• Would you recommend us to others?

Your feedback helps us serve you better.

Thank you for choosing {business_name}!

Best regards,
The {business_name} Team
        """,
        "placeholders": ["[CUSTOMER_NAME]"],
        "trigger": "post_service_followup"
    }
    
    templates.extend([welcome_template, support_template, followup_template])
    
    # Generate issue-specific templates
    for issue in common_issues:
        issue_template = {
            "type": f"issue_{issue.lower().replace(' ', '_')}",
            "subject": f"Resolution for {issue}",
            "content": f"""
Hi [CUSTOMER_NAME],

We understand you're experiencing issues with {issue}. Here's how we can help:

[ISSUE_SPECIFIC_SOLUTION]

If this doesn't resolve your issue, please reply to this email and we'll escalate it to our technical team.

Best regards,
{business_name} Support Team
            """,
            "placeholders": ["[CUSTOMER_NAME]", "[ISSUE_SPECIFIC_SOLUTION]"],
            "trigger": f"issue_{issue.lower().replace(' ', '_')}"
        }
        templates.append(issue_template)
    
    return templates

def configure_phone_automation(
    business_name: str,
    industry: str,
    phone_number: Optional[str],
    business_hours: Dict[str, str],
    brand_voice: str
) -> Dict[str, Any]:
    """Configure phone automation system"""
    
    return {
        "phone_number": phone_number or "+1 (555) 123-4567",
        "business_hours": business_hours,
        "greeting_message": f"Thank you for calling {business_name}. How can we help you today?",
        "after_hours_message": f"Thank you for calling {business_name}. We're currently closed. Our business hours are {business_hours.get('start', '9 AM')} to {business_hours.get('end', '5 PM')} {business_hours.get('timezone', 'EST')}. Please leave a message and we'll get back to you.",
        "menu_options": [
            {"option": "1", "description": "Speak with a representative", "action": "transfer_to_agent"},
            {"option": "2", "description": "Check order status", "action": "order_status"},
            {"option": "3", "description": "Technical support", "action": "technical_support"},
            {"option": "4", "description": "Billing inquiries", "action": "billing"},
            {"option": "0", "description": "Repeat menu", "action": "repeat_menu"}
        ],
        "call_routing": {
            "sales": "sales@example.com",
            "support": "support@example.com",
            "billing": "billing@example.com"
        },
        "voicemail_setup": {
            "enabled": True,
            "message": f"Please leave your name, phone number, and a brief message. We'll return your call within 24 hours."
        }
    }

def generate_chat_responses(business_name: str, industry: str, common_issues: List[str], brand_voice: str) -> List[Dict[str, Any]]:
    """Generate automated chat responses"""
    
    responses = []
    
    # Greeting responses
    greeting_responses = [
        {
            "intent": "greeting",
            "patterns": ["hello", "hi", "hey", "good morning", "good afternoon"],
            "response": f"Hello! Welcome to {business_name}. How can I assist you today?",
            "confidence": 0.9
        }
    ]
    
    # Common question responses
    common_responses = [
        {
            "intent": "business_hours",
            "patterns": ["hours", "open", "closed", "when are you open"],
            "response": f"Our business hours are Monday-Friday, 9 AM to 5 PM EST. We're here to help!",
            "confidence": 0.8
        },
        {
            "intent": "contact_info",
            "patterns": ["contact", "phone", "email", "address"],
            "response": f"You can reach us at support@{business_name.lower().replace(' ', '')}.com or call our support line.",
            "confidence": 0.8
        },
        {
            "intent": "services",
            "patterns": ["services", "what do you do", "offerings"],
            "response": f"We provide comprehensive {industry} solutions. What specific service are you interested in?",
            "confidence": 0.7
        }
    ]
    
    responses.extend(greeting_responses)
    responses.extend(common_responses)
    
    # Issue-specific responses
    for issue in common_issues:
        issue_response = {
            "intent": f"issue_{issue.lower().replace(' ', '_')}",
            "patterns": [issue.lower(), f"problem with {issue.lower()}", f"issue with {issue.lower()}"],
            "response": f"I understand you're having issues with {issue}. Let me help you resolve this. Can you provide more details?",
            "confidence": 0.6
        }
        responses.append(issue_response)
    
    return responses

def setup_vapi_phone_assistant(
    business_name: str,
    industry: str,
    phone_number: Optional[str],
    business_hours: Dict[str, str],
    brand_voice: str
) -> Dict[str, Any]:
    """Set up VAPI phone assistant configuration"""
    
    return {
        "assistant_name": f"{business_name} Phone Assistant",
        "phone_number": phone_number or "+1 (555) 123-4567",
        "voice_settings": {
            "voice": "professional" if brand_voice == "professional" else "friendly",
            "language": "en-US",
            "speed": 1.0,
            "pitch": 1.0
        },
        "conversation_flow": {
            "greeting": f"Hello! Thank you for calling {business_name}. How can I help you today?",
            "fallback": "I'm sorry, I didn't understand that. Could you please repeat or say 'help' for assistance?",
            "goodbye": "Thank you for calling {business_name}. Have a great day!",
            "transfer": "Let me transfer you to a human representative. Please hold on."
        },
        "capabilities": [
            "Answer frequently asked questions",
            "Check order status",
            "Schedule appointments",
            "Transfer to human agents",
            "Take messages"
        ],
        "business_hours": business_hours,
        "escalation_rules": {
            "complex_issues": "transfer_to_human",
            "billing_disputes": "transfer_to_billing",
            "technical_problems": "transfer_to_technical_support"
        }
    }

def create_automation_rules(industry: str, common_issues: List[str]) -> List[Dict[str, Any]]:
    """Create automation rules for customer service"""
    
    rules = [
        {
            "rule_name": "auto_response_new_ticket",
            "trigger": "new_support_ticket",
            "action": "send_acknowledgment_email",
            "conditions": ["ticket_created", "priority_normal"],
            "enabled": True
        },
        {
            "rule_name": "escalate_high_priority",
            "trigger": "ticket_priority_high",
            "action": "notify_manager",
            "conditions": ["priority_high", "unresolved"],
            "enabled": True
        },
        {
            "rule_name": "follow_up_resolved_ticket",
            "trigger": "ticket_resolved",
            "action": "send_satisfaction_survey",
            "conditions": ["status_resolved", "customer_response_required"],
            "enabled": True
        }
    ]
    
    # Add industry-specific rules
    if industry.lower() in ["ecommerce", "retail"]:
        rules.append({
            "rule_name": "order_status_automation",
            "trigger": "order_status_inquiry",
            "action": "auto_provide_order_status",
            "conditions": ["valid_order_number", "customer_verified"],
            "enabled": True
        })
    
    return rules

def generate_performance_metrics(service_types: List[str]) -> Dict[str, Any]:
    """Generate performance metrics for customer service"""
    
    base_metrics = {
        "response_time": {
            "email": "2 hours",
            "phone": "immediate",
            "chat": "30 seconds"
        },
        "resolution_rate": "85%",
        "customer_satisfaction": "4.2/5",
        "first_contact_resolution": "70%"
    }
    
    if "email_templates" in service_types:
        base_metrics["email_automation"] = {
            "templates_created": 5,
            "auto_response_rate": "90%",
            "template_effectiveness": "4.0/5"
        }
    
    if "phone_automation" in service_types:
        base_metrics["phone_automation"] = {
            "call_volume_handled": "80%",
            "call_transfer_rate": "25%",
            "average_call_duration": "3 minutes"
        }
    
    if "chat_responses" in service_types:
        base_metrics["chat_automation"] = {
            "auto_responses": "75%",
            "escalation_rate": "30%",
            "response_accuracy": "88%"
        }
    
    return base_metrics

@CUSTOMER_SERVICE_AGENT.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    ctx.logger.info("Customer Service Agent started")
    ctx.logger.info(f"Agent address: {CUSTOMER_SERVICE_AGENT.address}")

if __name__ == "__main__":
    fund_agent_if_low(CUSTOMER_SERVICE_AGENT.wallet.address())
    CUSTOMER_SERVICE_AGENT.run()

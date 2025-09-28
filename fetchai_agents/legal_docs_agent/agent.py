"""
Legal Docs Agent for Fetch.ai AgentVerse
Auto-generates LLC docs, policies, and Terms of Service
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
LEGAL_DOCS_AGENT = Agent(
    name="legal_docs_agent",
    seed="legal-docs-agent-seed-phrase-12345",
    port=8005,
    endpoint=["http://localhost:8005/submit"],
)

# Pydantic models
class LegalDocsRequest(BaseModel):
    business_name: str
    business_type: str = "LLC"
    industry: str
    state: str = "Delaware"
    business_address: Dict[str, str]
    owner_info: Dict[str, str]
    required_documents: List[str] = ["privacy_policy", "terms_of_service", "llc_formation"]
    custom_requirements: Optional[Dict[str, Any]] = None

class LegalDocsResponse(BaseModel):
    success: bool
    documents_generated: List[Dict[str, Any]]
    filing_requirements: Dict[str, Any]
    compliance_checklist: List[str]
    next_steps: List[str]
    estimated_costs: Dict[str, float]

class ErrorResponse(BaseModel):
    success: bool
    error: str

@LEGAL_DOCS_AGENT.on_message(model=LegalDocsRequest)
async def handle_legal_docs_request(ctx: Context, sender: str, msg: LegalDocsRequest):
    """Handle legal documents generation requests"""
    try:
        ctx.logger.info(f"Received legal docs request for {msg.business_name}")
        
        # Generate legal documents
        docs_data = await generate_legal_documents(
            business_name=msg.business_name,
            business_type=msg.business_type,
            industry=msg.industry,
            state=msg.state,
            business_address=msg.business_address,
            owner_info=msg.owner_info,
            required_documents=msg.required_documents,
            custom_requirements=msg.custom_requirements
        )
        
        response = LegalDocsResponse(
            success=True,
            documents_generated=docs_data["documents_generated"],
            filing_requirements=docs_data["filing_requirements"],
            compliance_checklist=docs_data["compliance_checklist"],
            next_steps=docs_data["next_steps"],
            estimated_costs=docs_data["estimated_costs"]
        )
        
        await ctx.send(sender, response.model_dump())
        ctx.logger.info(f"Sent legal docs response to {sender}")
        
    except Exception as e:
        ctx.logger.error(f"Error in legal docs generation: {e}")
        error_response = ErrorResponse(success=False, error=str(e))
        await ctx.send(sender, error_response.model_dump())

async def generate_legal_documents(
    business_name: str,
    business_type: str,
    industry: str,
    state: str,
    business_address: Dict[str, str],
    owner_info: Dict[str, str],
    required_documents: List[str],
    custom_requirements: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generate comprehensive legal documents"""
    
    documents_generated = []
    
    # Generate each required document
    for doc_type in required_documents:
        if doc_type == "privacy_policy":
            doc = generate_privacy_policy(business_name, industry, business_address)
        elif doc_type == "terms_of_service":
            doc = generate_terms_of_service(business_name, industry, business_address)
        elif doc_type == "llc_formation":
            doc = generate_llc_formation_docs(business_name, state, business_address, owner_info)
        elif doc_type == "nda":
            doc = generate_nda_template(business_name, industry)
        elif doc_type == "employment_contract":
            doc = generate_employment_contract_template(business_name, industry)
        else:
            doc = generate_generic_document(doc_type, business_name, industry)
        
        documents_generated.append(doc)
    
    # Generate filing requirements
    filing_requirements = get_filing_requirements(business_type, state)
    
    # Generate compliance checklist
    compliance_checklist = generate_compliance_checklist(industry, state, required_documents)
    
    # Generate next steps
    next_steps = generate_next_steps(business_type, state, required_documents)
    
    # Calculate estimated costs
    estimated_costs = calculate_estimated_costs(business_type, state, required_documents)
    
    return {
        "documents_generated": documents_generated,
        "filing_requirements": filing_requirements,
        "compliance_checklist": compliance_checklist,
        "next_steps": next_steps,
        "estimated_costs": estimated_costs
    }

def generate_privacy_policy(business_name: str, industry: str, business_address: Dict[str, str]) -> Dict[str, Any]:
    """Generate privacy policy document"""
    return {
        "type": "privacy_policy",
        "title": f"{business_name} Privacy Policy",
        "content": f"""
# Privacy Policy

**Effective Date:** [DATE]

## Information We Collect

{business_name} collects information you provide directly to us, such as when you create an account, make a purchase, or contact us for support.

### Personal Information
- Name and contact information
- Payment information (processed securely through third-party processors)
- Account credentials
- Communication preferences

### Automatically Collected Information
- Device information and identifiers
- Usage data and analytics
- Cookies and similar technologies

## How We Use Your Information

We use the information we collect to:
- Provide, maintain, and improve our services
- Process transactions and send related information
- Send technical notices and support messages
- Respond to your comments and questions
- Develop new products and services

## Information Sharing

We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this policy.

## Data Security

We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.

## Your Rights

You have the right to:
- Access your personal information
- Correct inaccurate information
- Delete your personal information
- Object to processing
- Data portability

## Contact Us

If you have questions about this Privacy Policy, contact us at:
{business_address.get('email', 'privacy@example.com')}
{business_address.get('address', 'Your Business Address')}
        """,
        "placeholders": ["[DATE]", "Your Business Address", "privacy@example.com"],
        "status": "draft"
    }

def generate_terms_of_service(business_name: str, industry: str, business_address: Dict[str, str]) -> Dict[str, Any]:
    """Generate terms of service document"""
    return {
        "type": "terms_of_service",
        "title": f"{business_name} Terms of Service",
        "content": f"""
# Terms of Service

**Effective Date:** [DATE]

## Acceptance of Terms

By accessing and using {business_name}'s services, you accept and agree to be bound by the terms and provision of this agreement.

## Use License

Permission is granted to temporarily download one copy of {business_name}'s materials for personal, non-commercial transitory viewing only.

## Disclaimer

The materials on {business_name}'s website are provided on an 'as is' basis. {business_name} makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties.

## Limitations

In no event shall {business_name} or its suppliers be liable for any damages arising out of the use or inability to use the materials on {business_name}'s website.

## Accuracy of Materials

The materials appearing on {business_name}'s website could include technical, typographical, or photographic errors.

## Links

{business_name} has not reviewed all of the sites linked to our website and is not responsible for the contents of any such linked site.

## Modifications

{business_name} may revise these terms of service at any time without notice.

## Governing Law

These terms and conditions are governed by and construed in accordance with the laws of [STATE] and you irrevocably submit to the exclusive jurisdiction of the courts in that state or location.

## Contact Information

{business_address.get('email', 'legal@example.com')}
{business_address.get('address', 'Your Business Address')}
        """,
        "placeholders": ["[DATE]", "[STATE]", "Your Business Address", "legal@example.com"],
        "status": "draft"
    }

def generate_llc_formation_docs(business_name: str, state: str, business_address: Dict[str, str], owner_info: Dict[str, str]) -> Dict[str, Any]:
    """Generate LLC formation documents"""
    return {
        "type": "llc_formation",
        "title": f"{business_name} LLC Formation Documents",
        "content": f"""
# LLC Formation Documents

## Articles of Organization

**Entity Name:** {business_name}, LLC
**State of Formation:** {state}
**Principal Address:** {business_address.get('address', 'Your Business Address')}
**Registered Agent:** {owner_info.get('name', 'Your Name')}
**Registered Agent Address:** {business_address.get('address', 'Your Business Address')}

## Operating Agreement

### Company Information
- **Name:** {business_name}, LLC
- **Formation Date:** [DATE]
- **State of Formation:** {state}
- **Principal Office:** {business_address.get('address', 'Your Business Address')}

### Member Information
- **Member Name:** {owner_info.get('name', 'Your Name')}
- **Ownership Percentage:** 100%
- **Capital Contribution:** $[AMOUNT]

### Management
The LLC shall be managed by its members.

### Dissolution
The LLC may be dissolved upon the unanimous consent of all members.

## EIN Application
- **Business Name:** {business_name}, LLC
- **Address:** {business_address.get('address', 'Your Business Address')}
- **Responsible Party:** {owner_info.get('name', 'Your Name')}
- **SSN/EIN:** [SSN_OR_EIN]
        """,
        "placeholders": ["[DATE]", "[AMOUNT]", "[SSN_OR_EIN]", "Your Business Address", "Your Name"],
        "status": "draft"
    }

def generate_nda_template(business_name: str, industry: str) -> Dict[str, Any]:
    """Generate NDA template"""
    return {
        "type": "nda",
        "title": f"{business_name} Non-Disclosure Agreement",
        "content": f"""
# Non-Disclosure Agreement

**Disclosing Party:** {business_name}
**Receiving Party:** [PARTY_NAME]
**Effective Date:** [DATE]

## Confidential Information

The term "Confidential Information" means all non-public, proprietary, or confidential information disclosed by {business_name}.

## Obligations

The Receiving Party agrees to:
- Hold all Confidential Information in strict confidence
- Not disclose Confidential Information to any third parties
- Use Confidential Information solely for the purpose of [PURPOSE]
- Return all Confidential Information upon request

## Term

This Agreement shall remain in effect for [DURATION] years from the Effective Date.

## Governing Law

This Agreement shall be governed by the laws of [STATE].
        """,
        "placeholders": ["[PARTY_NAME]", "[DATE]", "[PURPOSE]", "[DURATION]", "[STATE]"],
        "status": "template"
    }

def generate_employment_contract_template(business_name: str, industry: str) -> Dict[str, Any]:
    """Generate employment contract template"""
    return {
        "type": "employment_contract",
        "title": f"{business_name} Employment Contract Template",
        "content": f"""
# Employment Agreement

**Employer:** {business_name}
**Employee:** [EMPLOYEE_NAME]
**Position:** [POSITION]
**Start Date:** [START_DATE]

## Terms of Employment

### Position and Duties
The Employee shall serve as [POSITION] and perform duties as assigned by the Employer.

### Compensation
- **Base Salary:** $[SALARY] per [PERIOD]
- **Benefits:** [BENEFITS]
- **Overtime:** [OVERTIME_POLICY]

### Work Schedule
- **Hours:** [HOURS] per week
- **Schedule:** [SCHEDULE]
- **Location:** [WORK_LOCATION]

### Confidentiality
Employee agrees to maintain confidentiality of all proprietary information.

### Termination
Either party may terminate this agreement with [NOTICE_PERIOD] notice.
        """,
        "placeholders": ["[EMPLOYEE_NAME]", "[POSITION]", "[START_DATE]", "[SALARY]", "[PERIOD]", "[BENEFITS]", "[OVERTIME_POLICY]", "[HOURS]", "[SCHEDULE]", "[WORK_LOCATION]", "[NOTICE_PERIOD]"],
        "status": "template"
    }

def generate_generic_document(doc_type: str, business_name: str, industry: str) -> Dict[str, Any]:
    """Generate generic document template"""
    return {
        "type": doc_type,
        "title": f"{business_name} {doc_type.replace('_', ' ').title()}",
        "content": f"# {doc_type.replace('_', ' ').title()}\n\nThis is a template for {doc_type} for {business_name} in the {industry} industry.",
        "placeholders": [],
        "status": "template"
    }

def get_filing_requirements(business_type: str, state: str) -> Dict[str, Any]:
    """Get filing requirements for the business type and state"""
    return {
        "state": state,
        "business_type": business_type,
        "required_filings": [
            "Articles of Organization/Incorporation",
            "Operating Agreement/Bylaws",
            "EIN Application",
            "State Business License",
            "Local Business License"
        ],
        "filing_fees": {
            "state_filing": 100.0,
            "registered_agent": 50.0,
            "business_license": 25.0,
            "total_estimated": 175.0
        },
        "timeline": "2-4 weeks"
    }

def generate_compliance_checklist(industry: str, state: str, required_documents: List[str]) -> List[str]:
    """Generate compliance checklist"""
    checklist = [
        "File Articles of Organization/Incorporation",
        "Obtain EIN from IRS",
        "Register for state taxes",
        "Obtain necessary business licenses",
        "Set up business bank account",
        "Purchase business insurance",
        "Register domain name",
        "Set up business email"
    ]
    
    if "privacy_policy" in required_documents:
        checklist.append("Publish privacy policy on website")
    
    if "terms_of_service" in required_documents:
        checklist.append("Publish terms of service on website")
    
    if industry.lower() in ["healthcare", "finance", "legal"]:
        checklist.append("Obtain industry-specific licenses")
    
    return checklist

def generate_next_steps(business_type: str, state: str, required_documents: List[str]) -> List[str]:
    """Generate next steps for the business"""
    return [
        "Review all generated documents for accuracy",
        "Customize placeholders with your specific information",
        "File Articles of Organization with the state",
        "Apply for EIN with the IRS",
        "Register for state and local taxes",
        "Obtain necessary business licenses",
        "Set up business banking and insurance",
        "Launch your business operations"
    ]

def calculate_estimated_costs(business_type: str, state: str, required_documents: List[str]) -> Dict[str, float]:
    """Calculate estimated costs for business formation"""
    costs = {
        "state_filing": 100.0,
        "registered_agent": 50.0,
        "business_license": 25.0,
        "legal_review": 200.0 if len(required_documents) > 3 else 100.0,
        "total": 0.0
    }
    
    costs["total"] = sum(costs.values())
    return costs

@LEGAL_DOCS_AGENT.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    ctx.logger.info("Legal Docs Agent started")
    ctx.logger.info(f"Agent address: {LEGAL_DOCS_AGENT.address}")

if __name__ == "__main__":
    fund_agent_if_low(LEGAL_DOCS_AGENT.wallet.address())
    LEGAL_DOCS_AGENT.run()

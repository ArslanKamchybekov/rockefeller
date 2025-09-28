from src.models.docs import LegalDocsInput, LegalDocsOutput
from src.utils.create_gemini import create_gemini_client

def generate_legal_docs(input: LegalDocsInput) -> LegalDocsOutput:
    prompt = f"""
        Act as a legal-docs drafting assistant for a simple online store MVP. Input is a single-sentence business idea only. Output exactly a JSON array of three items: Privacy Policy, Website Terms of Use, and Mutual NDA. Do not include explanations, comments, or extra keys outside the schema. Follow these strict rules:

        Interpret the idea to infer the store name and what it sells; if absent, set [Store Name] and keep descriptions generic.

        Use conservative, jurisdiction-agnostic defaults; include placeholders for missing fields.

        Return Markdown content ready to render, with headings and short sections.

        JSON schema per item:

        doc_type: one of 'privacy_policy_bootstrap' | 'website_terms_bootstrap' | 'nda_mutual_short'

        title: human-readable title

        summary: 1–2 sentence purpose

        placeholders: array of strings chosen from: ['Company Name','Store Name','Website URL','Contact Email','Physical Address','Effective Date','Governing Law','DMCA Agent Email','Counterparty Name','Signatory Name']

        defaults_used: small object listing key defaults applied

        content: Markdown string (no code fences)

        Defaults to apply:

        Privacy Policy: collect 'account info','order details','payment tokens (via processor)','basic analytics'; cookies = 'essential + analytics'; sell_data=false; share_with=['payment processors','shipping carriers','analytics providers']; retention='as long as needed for orders and legal obligations'.

        Website Terms: license='limited, revocable, non-transferable'; liability_cap='amount paid in last 12 months'; arbitration=true; class_waiver=true.

        NDA: term_years=3; survival_years=5; residuals_clause=false; injunctive_relief=true.

        Now generate the output for this idea:
        IDEA: {input['idea']}
    """
    client = create_gemini_client()

    response = client.generate_content(
        prompt,
        generation_config={"temperature": 0.3},
    )

    # Clean the response to ensure it's valid JSON
    cleaned_response = response.text.strip()
    
    # Remove markdown code blocks if present
    if cleaned_response.startswith('```json'):
        cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
    elif cleaned_response.startswith('```'):
        cleaned_response = cleaned_response.replace('```', '').strip()
    
    # Remove any leading/trailing backticks
    import re
    cleaned_response = re.sub(r'^`+|`+$', '', cleaned_response)
    
    return { "docs": cleaned_response }
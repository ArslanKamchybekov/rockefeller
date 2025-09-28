from src.models.docs import LegalDocsInput, LegalDocsOutput
from src.utils.create_gemini import create_gemini_client
import json 

def generate_legal_docs(input: LegalDocsInput) -> LegalDocsOutput:
    prompt = f"""
        You are a legal-docs drafting assistant for a simple online store MVP. 

        Input: a one-sentence business idea.  
        Output: exactly a JSON array of two items: Privacy Policy and Website Terms of Use. Do not include explanations, comments, or extra keys outside the schema.

        Rules:
        - Infer the store name and what it sells from the idea; if missing, set [Store Name] and keep content generic.
        - Use conservative, jurisdiction-agnostic defaults; add placeholders where needed.
        - Write content in Markdown, with clear headings and short sections.

        Each JSON item follows this schema:
        doc_type: 'privacy_policy_bootstrap' | 'website_terms_bootstrap'
        title: human-readable title
        summary: 1–2 sentence purpose
        placeholders: array of strings chosen from ['Company Name','Store Name','Website URL','Contact Email','Physical Address','Effective Date','Governing Law','DMCA Agent Email']
        defaults_used: small object listing key defaults applied
        content: Markdown string (no code fences)

        Defaults:
        - Privacy Policy: collects ['account info','order details','payment tokens (via processor)','basic analytics']; cookies = 'essential + analytics'; sell_data = false; share_with = ['payment processors','shipping carriers','analytics providers']; retention = 'as long as needed for orders and legal obligations'.
        - Website Terms: license = 'limited, revocable, non-transferable'; liability_cap = 'amount paid in last 12 months'; arbitration = true; class_waiver = true.

        Now generate the output for this idea:
        IDEA: {input['idea']}
    """
    client = create_gemini_client()

    response = client.generate_content(
        prompt,
        generation_config={"temperature": 0.3},
    )

    data = json.loads(response.text)

    for doc in data:
        print(f"# {doc['title']}\n")
        print(doc['content'])
        print("\n" + "="*60 + "\n")

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

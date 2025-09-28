from src.models.docs import LegalDocsInput, LegalDocsOutput, LegalDocument
from src.utils.create_gemini import create_gemini_client
import json
import base64
import os
import tempfile
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import markdown 

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

    # Parse the JSON response
    try:
        # Clean the response - remove markdown code blocks if present
        cleaned_docs = response.text.strip()
        if cleaned_docs.startswith('```json'):
            cleaned_docs = cleaned_docs.replace('```json', '').replace('```', '').strip()
        elif cleaned_docs.startswith('```'):
            cleaned_docs = cleaned_docs.replace('```', '').strip()
        
        # Find JSON array
        json_start = cleaned_docs.find('[')
        json_end = cleaned_docs.rfind(']') + 1
        json_string = cleaned_docs[json_start:json_end]
        
        docs_data = json.loads(json_string)
        
        # Generate PDFs for each document
        pdfs = []
        for doc_data in docs_data:
            pdf_info = create_pdf_from_doc(doc_data)
            pdfs.append(pdf_info)
        
        return {
            "docs": response.text,
            "pdfs": pdfs
        }
        
    except Exception as e:
        print(f"Error processing legal docs: {e}")
        return { "docs": response.text }

def create_pdf_from_doc(doc_data: dict) -> dict:
    """Convert a legal document to PDF and return base64 encoded data"""
    try:
        # Convert markdown to HTML
        html_content = markdown.markdown(
            doc_data['content'],
            extensions=['tables', 'fenced_code', 'toc']
        )
        
        # Create a complete HTML document with styling
        html_document = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{doc_data['title']}</title>
            <style>
                body {{
                    font-family: 'Times New Roman', serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 40px 20px;
                    color: #333;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                    margin-bottom: 30px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                    margin-bottom: 15px;
                }}
                h3 {{
                    color: #7f8c8d;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }}
                p {{
                    margin-bottom: 15px;
                    text-align: justify;
                }}
                ul, ol {{
                    margin-bottom: 15px;
                    padding-left: 30px;
                }}
                li {{
                    margin-bottom: 5px;
                }}
                strong {{
                    font-weight: bold;
                }}
                em {{
                    font-style: italic;
                }}
                .summary {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-left: 4px solid #3498db;
                    margin-bottom: 30px;
                    font-style: italic;
                }}
                @page {{
                    margin: 1in;
                    size: A4;
                }}
            </style>
        </head>
        <body>
            <h1>{doc_data['title']}</h1>
            <div class="summary">
                <strong>Summary:</strong> {doc_data['summary']}
            </div>
            {html_content}
        </body>
        </html>
        """
        
        # Generate PDF using WeasyPrint
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            font_config = FontConfiguration()
            HTML(string=html_document).write_pdf(
                temp_file.name,
                font_config=font_config
            )
            
            # Read the PDF file and encode as base64
            with open(temp_file.name, 'rb') as pdf_file:
                pdf_data = pdf_file.read()
                pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
            
            # Clean up temp file
            os.unlink(temp_file.name)
            
            return {
                "title": doc_data['title'],
                "filename": f"{doc_data['title'].replace(' ', '_').lower()}.pdf",
                "pdf_data": pdf_base64,
                "size": len(pdf_data)
            }
            
    except Exception as e:
        print(f"Error creating PDF for {doc_data.get('title', 'Unknown')}: {e}")
        return {
            "title": doc_data.get('title', 'Unknown'),
            "filename": "error.pdf",
            "pdf_data": None,
            "error": str(e)
        }

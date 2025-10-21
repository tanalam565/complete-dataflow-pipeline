import os
import requests
from typing import Literal

# Get API key from environment
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')


def classify_document(text: str) -> Literal['invoice', 'insurance', 'id', 'unknown']:
    """
    Classify document using OpenRouter API
    Falls back to rule-based if API fails
    """
    
    if OPENROUTER_API_KEY:
        return classify_with_openrouter(text)
    else:
        print("Warning: OPENROUTER_API_KEY not set, using fallback classification")
        return fallback_classify(text)


def classify_with_openrouter(text: str) -> str:
    """
    Classify using OpenRouter API
    Uses free models like Google Gemini Flash or Meta Llama
    """
    text_sample = text[:2000]
    
    prompt = f"""You are a document classifier for a property management company.

Analyze the following document and classify it into ONE of these categories:
- invoice (vendor bills, payment requests)
- insurance (renters insurance policies, coverage documents)
- id (driver's license, passport, state ID, tenant identification)
- unknown (if none of the above)

Document text:
{text_sample}

Respond with ONLY the category name in lowercase, nothing else."""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemini-2.0-flash-exp:free",  # Updated free model
                # Alternative free models:
                # "meta-llama/llama-3.2-3b-instruct:free"
                # "qwen/qwen-2-7b-instruct:free"
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 10
            }
        )
        
        response.raise_for_status()
        result = response.json()
        
        classification = result['choices'][0]['message']['content'].strip().lower()
        
        # Validate response
        valid_types = ['invoice', 'insurance', 'id', 'unknown']
        for doc_type in valid_types:
            if doc_type in classification:
                return doc_type
        
        return 'unknown'
        
    except Exception as e:
        print(f"OpenRouter API error: {e}")
        return fallback_classify(text)


def fallback_classify(text: str) -> str:
    """
    Rule-based fallback if API fails or no API key
    """
    text_lower = text.lower()
    
    # Check for invoice keywords
    invoice_keywords = ['invoice', 'bill', 'payment', 'amount due', 'vendor', 'total:', 'subtotal', 'remit to']
    invoice_score = sum(1 for keyword in invoice_keywords if keyword in text_lower)
    
    # Check for insurance keywords
    insurance_keywords = ['insurance', 'policy', 'coverage', 'premium', 'insured', 'policyholder', 'deductible', 'liability']
    insurance_score = sum(1 for keyword in insurance_keywords if keyword in text_lower)
    
    # Check for ID keywords
    id_keywords = ['driver license', 'drivers license', 'passport', 'state id', 'identification', 'date of birth', 'license number', 'dl number', 'sex:', 'height:', 'eyes:']
    id_score = sum(1 for keyword in id_keywords if keyword in text_lower)
    
    # Return type with highest score
    scores = {
        'invoice': invoice_score,
        'insurance': insurance_score,
        'id': id_score
    }
    
    max_score = max(scores.values())
    if max_score >= 2:  # At least 2 keyword matches
        return max(scores, key=scores.get)
    
    return 'unknown'
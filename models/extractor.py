import os
import requests
import json
import re
from datetime import datetime

# Get API key from environment
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')


def extract_entities(text: str, doc_type: str) -> dict:
    """
    Extract entities using OpenRouter API based on document type
    """
    
    if doc_type == 'invoice':
        return extract_invoice_entities(text)
    elif doc_type == 'insurance':
        return extract_insurance_entities(text)
    elif doc_type == 'id':
        return extract_id_entities(text)
    else:
        return {'error': 'Unknown document type'}


def call_openrouter(prompt: str) -> str:
    """
    Call OpenRouter API with prompt
    """
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemini-2.0-flash-exp:free",  # Free model
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 500
            }
        )
        
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
        
    except Exception as e:
        print(f"OpenRouter API error: {e}")
        return None


def extract_invoice_entities(text: str) -> dict:
    """
    Extract invoice-specific fields using OpenRouter
    """
    
    if not OPENROUTER_API_KEY:
        print("Warning: OPENROUTER_API_KEY not set, using fallback extraction")
        return fallback_extract_invoice(text)
    
    prompt = f"""Extract the following information from this invoice document. Return ONLY valid JSON with these exact keys:

{{
  "invoice_number": "string or null",
  "vendor_name": "string or null",
  "invoice_date": "YYYY-MM-DD or null",
  "due_date": "YYYY-MM-DD or null",
  "total_amount": "number or null",
  "subtotal": "number or null",
  "tax_amount": "number or null",
  "service_description": "string or null",
  "vendor_address": "string or null",
  "vendor_phone": "string or null"
}}

Document:
{text[:3000]}

Return ONLY the JSON object, no explanation or markdown formatting."""

    content = call_openrouter(prompt)
    
    if content:
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                entities = json.loads(json_match.group())
                return clean_entities(entities)
        except Exception as e:
            print(f"Error parsing invoice JSON: {e}")
    
    return fallback_extract_invoice(text)


def extract_insurance_entities(text: str) -> dict:
    """
    Extract insurance-specific fields using OpenRouter
    """
    
    if not OPENROUTER_API_KEY:
        print("Warning: OPENROUTER_API_KEY not set, using fallback extraction")
        return fallback_extract_insurance(text)
    
    prompt = f"""Extract the following information from this insurance document. Return ONLY valid JSON with these exact keys:

{{
  "policy_number": "string or null",
  "policyholder_name": "string or null",
  "insurance_company": "string or null",
  "policy_type": "string or null",
  "coverage_amount": "number or null",
  "premium_amount": "number or null",
  "effective_date": "YYYY-MM-DD or null",
  "expiry_date": "YYYY-MM-DD or null",
  "property_address": "string or null",
  "deductible": "number or null"
}}

Document:
{text[:3000]}

Return ONLY the JSON object, no explanation or markdown formatting."""

    content = call_openrouter(prompt)
    
    if content:
        try:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                entities = json.loads(json_match.group())
                return clean_entities(entities)
        except Exception as e:
            print(f"Error parsing insurance JSON: {e}")
    
    return fallback_extract_insurance(text)


def extract_id_entities(text: str) -> dict:
    """
    Extract ID-specific fields using OpenRouter
    """
    
    if not OPENROUTER_API_KEY:
        print("Warning: OPENROUTER_API_KEY not set, using fallback extraction")
        return fallback_extract_id(text)
    
    prompt = f"""Extract the following information from this ID document. Return ONLY valid JSON with these exact keys:

{{
  "document_type": "string (driver_license, passport, state_id) or null",
  "id_number": "string or null",
  "full_name": "string or null",
  "date_of_birth": "YYYY-MM-DD or null",
  "issue_date": "YYYY-MM-DD or null",
  "expiry_date": "YYYY-MM-DD or null",
  "address": "string or null",
  "state": "string or null",
  "country": "string or null",
  "gender": "string or null"
}}

Document:
{text[:3000]}

Return ONLY the JSON object, no explanation or markdown formatting."""

    content = call_openrouter(prompt)
    
    if content:
        try:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                entities = json.loads(json_match.group())
                return clean_entities(entities)
        except Exception as e:
            print(f"Error parsing ID JSON: {e}")
    
    return fallback_extract_id(text)


def clean_entities(entities: dict) -> dict:
    """
    Clean and validate extracted entities
    """
    cleaned = {}
    for key, value in entities.items():
        if isinstance(value, str):
            value = value.strip()
            if value.lower() in ['null', 'none', 'n/a', '', 'unknown']:
                value = None
        cleaned[key] = value
    return cleaned


# Fallback regex-based extractors
def fallback_extract_invoice(text: str) -> dict:
    """Regex-based fallback for invoice extraction"""
    return {
        'invoice_number': extract_pattern(text, r'invoice\s*#?\s*:?\s*(\S+)', re.IGNORECASE),
        'vendor_name': extract_pattern(text, r'(?:from|vendor)\s*:?\s*([^\n]+)', re.IGNORECASE),
        'total_amount': extract_amount(text),
        'invoice_date': extract_date(text),
        'due_date': extract_pattern(text, r'due\s+date\s*:?\s*([^\n]+)', re.IGNORECASE),
        'subtotal': None,
        'tax_amount': None,
        'service_description': None,
        'vendor_address': None,
        'vendor_phone': extract_phone(text)
    }


def fallback_extract_insurance(text: str) -> dict:
    """Regex-based fallback for insurance extraction"""
    return {
        'policy_number': extract_pattern(text, r'policy\s*#?\s*:?\s*(\S+)', re.IGNORECASE),
        'policyholder_name': extract_pattern(text, r'(?:insured|policyholder)\s*:?\s*([^\n]+)', re.IGNORECASE),
        'insurance_company': extract_pattern(text, r'(?:company|insurer)\s*:?\s*([^\n]+)', re.IGNORECASE),
        'policy_type': None,
        'coverage_amount': extract_amount(text),
        'premium_amount': None,
        'effective_date': extract_date(text),
        'expiry_date': extract_pattern(text, r'expir(?:y|ation)\s+date\s*:?\s*([^\n]+)', re.IGNORECASE),
        'property_address': None,
        'deductible': None
    }


def fallback_extract_id(text: str) -> dict:
    """Regex-based fallback for ID extraction"""
    doc_type = 'unknown'
    if 'driver' in text.lower() or 'license' in text.lower():
        doc_type = 'driver_license'
    elif 'passport' in text.lower():
        doc_type = 'passport'
    elif 'state id' in text.lower():
        doc_type = 'state_id'
    
    return {
        'document_type': doc_type,
        'id_number': extract_pattern(text, r'(?:DL|ID|License|Passport)\s*#?\s*:?\s*(\S+)', re.IGNORECASE),
        'full_name': extract_pattern(text, r'name\s*:?\s*([^\n]+)', re.IGNORECASE),
        'date_of_birth': extract_pattern(text, r'(?:dob|date of birth)\s*:?\s*([^\n]+)', re.IGNORECASE),
        'issue_date': extract_pattern(text, r'issue\s+date\s*:?\s*([^\n]+)', re.IGNORECASE),
        'expiry_date': extract_pattern(text, r'exp(?:iry)?\s+date\s*:?\s*([^\n]+)', re.IGNORECASE),
        'address': extract_pattern(text, r'address\s*:?\s*([^\n]+)', re.IGNORECASE),
        'state': extract_pattern(text, r'state\s*:?\s*([A-Z]{2})', re.IGNORECASE),
        'country': None,
        'gender': extract_pattern(text, r'sex\s*:?\s*([MF])', re.IGNORECASE)
    }


# Helper functions
def extract_pattern(text: str, pattern: str, flags=0) -> str:
    """Extract first match of regex pattern"""
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None


def extract_amount(text: str) -> float:
    """Extract dollar amount"""
    pattern = r'\$\s*([\d,]+\.?\d*)'
    matches = re.findall(pattern, text)
    if matches:
        try:
            # Get the largest amount found
            amounts = [float(m.replace(',', '')) for m in matches]
            return max(amounts)
        except:
            return None
    return None


def extract_date(text: str) -> str:
    """Extract date in various formats"""
    patterns = [
        r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
        r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
        r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_phone(text: str) -> str:
    """Extract phone number"""
    pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
    match = re.search(pattern, text)
    return match.group(1) if match else None
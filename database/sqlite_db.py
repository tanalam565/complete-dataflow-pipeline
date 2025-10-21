import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/property_data.db")

def init_db():
    """
    Initialize SQLite database with tables for invoices, insurance, and IDs
    """
    # Create data directory if it doesn't exist
    DB_PATH.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Invoices table
    c.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT,
        vendor_name TEXT,
        invoice_date TEXT,
        due_date TEXT,
        total_amount REAL,
        subtotal REAL,
        tax_amount REAL,
        service_description TEXT,
        vendor_address TEXT,
        vendor_phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Insurance table
    c.execute('''CREATE TABLE IF NOT EXISTS insurance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_number TEXT,
        policyholder_name TEXT,
        insurance_company TEXT,
        policy_type TEXT,
        coverage_amount REAL,
        premium_amount REAL,
        effective_date TEXT,
        expiry_date TEXT,
        property_address TEXT,
        deductible REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # IDs table
    c.execute('''CREATE TABLE IF NOT EXISTS ids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_type TEXT,
        id_number TEXT,
        full_name TEXT,
        date_of_birth TEXT,
        issue_date TEXT,
        expiry_date TEXT,
        address TEXT,
        state TEXT,
        country TEXT,
        gender TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()


def insert_data(doc_type: str, entities: dict):
    """
    Insert extracted entities into appropriate table
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        if doc_type == 'invoice':
            c.execute('''INSERT INTO invoices 
                (invoice_number, vendor_name, invoice_date, due_date, 
                 total_amount, subtotal, tax_amount, service_description,
                 vendor_address, vendor_phone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (entities.get('invoice_number'),
                 entities.get('vendor_name'),
                 entities.get('invoice_date'),
                 entities.get('due_date'),
                 entities.get('total_amount'),
                 entities.get('subtotal'),
                 entities.get('tax_amount'),
                 entities.get('service_description'),
                 entities.get('vendor_address'),
                 entities.get('vendor_phone'))
            )
        
        elif doc_type == 'insurance':
            c.execute('''INSERT INTO insurance 
                (policy_number, policyholder_name, insurance_company, 
                 policy_type, coverage_amount, premium_amount, 
                 effective_date, expiry_date, property_address, deductible)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (entities.get('policy_number'),
                 entities.get('policyholder_name'),
                 entities.get('insurance_company'),
                 entities.get('policy_type'),
                 entities.get('coverage_amount'),
                 entities.get('premium_amount'),
                 entities.get('effective_date'),
                 entities.get('expiry_date'),
                 entities.get('property_address'),
                 entities.get('deductible'))
            )
        
        elif doc_type == 'id':
            c.execute('''INSERT INTO ids 
                (document_type, id_number, full_name, date_of_birth,
                 issue_date, expiry_date, address, state, country, gender)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (entities.get('document_type'),
                 entities.get('id_number'),
                 entities.get('full_name'),
                 entities.get('date_of_birth'),
                 entities.get('issue_date'),
                 entities.get('expiry_date'),
                 entities.get('address'),
                 entities.get('state'),
                 entities.get('country'),
                 entities.get('gender'))
            )
        
        conn.commit()
        
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        conn.close()


def get_all_data(doc_type: str) -> pd.DataFrame:
    """
    Retrieve all data for a specific document type
    """
    conn = sqlite3.connect(DB_PATH)
    
    table_map = {
        'invoice': 'invoices',
        'insurance': 'insurance',
        'id': 'ids'
    }
    
    table_name = table_map.get(doc_type)
    if not table_name:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name} ORDER BY created_at DESC", conn)
        return df
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def get_record_by_id(doc_type: str, record_id: int) -> dict:
    """
    Get a specific record by ID
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    table_map = {
        'invoice': 'invoices',
        'insurance': 'insurance',
        'id': 'ids'
    }
    
    table_name = table_map.get(doc_type)
    if not table_name:
        return {}
    
    try:
        c.execute(f"SELECT * FROM {table_name} WHERE id = ?", (record_id,))
        row = c.fetchone()
        
        if row:
            columns = [description[0] for description in c.description]
            return dict(zip(columns, row))
        return {}
        
    except Exception as e:
        print(f"Error retrieving record: {e}")
        return {}
    finally:
        conn.close()


def delete_record(doc_type: str, record_id: int):
    """
    Delete a record by ID
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    table_map = {
        'invoice': 'invoices',
        'insurance': 'insurance',
        'id': 'ids'
    }
    
    table_name = table_map.get(doc_type)
    if not table_name:
        return False
    
    try:
        c.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting record: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
import streamlit as st
import sys
from pathlib import Path
from dotenv import load_dotenv
import sqlite3
import pandas as pd

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from utils.ocr import extract_text
from models.classifier import classify_document
from models.extractor import extract_entities
from database.sqlite_db import init_db, insert_data, get_all_data
from database.vector_db import store_embedding, search_documents

# Initialize databases
init_db()

st.set_page_config(page_title="Property Document Processor", layout="wide")
st.title("🏢 Property Management Document Processor")

# Sidebar
with st.sidebar:
    st.header("📋 Menu")
    page = st.radio("Navigate", ["Upload Documents", "Search Documents", "View Database"])

# Page 1: Upload Documents
if page == "Upload Documents":
    st.header("📤 Upload Document")
    
    uploaded_file = st.file_uploader(
        "Upload Insurance, ID, or Invoice", 
        type=['pdf', 'png', 'jpg', 'jpeg']
    )
    
    if uploaded_file:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Document Preview")
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, use_column_width=True)
            else:
                st.info("PDF uploaded - processing...")
        
        with col2:
            st.subheader("🔄 Processing Status")
            
            with st.spinner("Extracting text..."):
                text = extract_text(uploaded_file)
                st.success("✅ Text extracted")
                with st.expander("View extracted text"):
                    st.text(text[:1000] + "..." if len(text) > 1000 else text)
            
            with st.spinner("Classifying document..."):
                doc_type = classify_document(text)
                st.success(f"✅ Document Type: **{doc_type.upper()}**")
            
            with st.spinner("Extracting entities..."):
                entities = extract_entities(text, doc_type)
                st.success("✅ Entities extracted")
                
                # Show confidence score
                confidence = entities.get('confidence_score', 0)
                needs_review = entities.get('needs_review', False)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if confidence >= 0.7:
                        st.success(f"Confidence: {confidence*100:.0f}%")
                    else:
                        st.warning(f"Confidence: {confidence*100:.0f}%")
                
                with col_b:
                    if needs_review:
                        st.error("⚠️ NEEDS HUMAN REVIEW")
                    else:
                        st.success("✅ Auto-approved")
        
        # Display extracted data
        st.subheader("📊 Extracted Data")
        
        # Highlight review status
        if entities.get('needs_review'):
            st.warning("⚠️ This document requires human review due to low confidence in extraction.")
        
        st.json(entities)
        
        # Save to databases
        if st.button("💾 Save to Database", type="primary"):
            with st.spinner("Saving..."):
                # Save to SQLite
                insert_data(doc_type, entities)
                
                # Save to ChromaDB
                store_embedding(text, entities, doc_type)
                
                st.success("✅ Document saved successfully!")
                st.balloons()

# Page 2: Search Documents
elif page == "Search Documents":
    st.header("🔍 Semantic Document Search")
    
    query = st.text_input("Enter search query", 
                         placeholder="e.g., Find all invoices from HVAC vendors")
    
    n_results = st.slider("Number of results", 1, 10, 5)
    
    if st.button("Search", type="primary"):
        if query:
            with st.spinner("Searching..."):
                results = search_documents(query, n_results)
                
                if results and results['documents'][0]:
                    st.subheader(f"Found {len(results['documents'][0])} results")
                    
                    for i, (doc, metadata) in enumerate(zip(results['documents'][0], 
                                                            results['metadatas'][0])):
                        with st.expander(f"Result {i+1} - {metadata.get('type', 'unknown').upper()}"):
                            st.write("**Metadata:**")
                            st.json(metadata)
                            st.write("**Document Preview:**")
                            st.text(doc[:500] + "..." if len(doc) > 500 else doc)
                else:
                    st.warning("No results found")
        else:
            st.warning("Please enter a search query")

# Page 3: View Database
elif page == "View Database":
    st.header("📊 Database Contents")
    
    tab1, tab2, tab3 = st.tabs(["Invoices", "Insurance", "IDs"])
    
    with tab1:
        st.subheader("📄 Invoices")
        invoices = get_all_data('invoice')
        if not invoices.empty:
            st.dataframe(invoices, width='stretch')
            st.download_button(
                "Download CSV",
                invoices.to_csv(index=False),
                "invoices.csv",
                "text/csv"
            )
        else:
            st.info("No invoices found")
    
    with tab2:
        st.subheader("🛡️ Insurance Policies")
        insurance = get_all_data('insurance')
        if not insurance.empty:
            st.dataframe(insurance, width='stretch')
            st.download_button(
                "Download CSV",
                insurance.to_csv(index=False),
                "insurance.csv",
                "text/csv"
            )
        else:
            st.info("No insurance records found")
    
    with tab3:
        st.subheader("🪪 IDs")
        ids = get_all_data('id')
        if not ids.empty:
            st.dataframe(ids, width='stretch')
            st.download_button(
                "Download CSV",
                ids.to_csv(index=False),
                "ids.csv",
                "text/csv"
            )
        else:
            st.info("No ID records found")
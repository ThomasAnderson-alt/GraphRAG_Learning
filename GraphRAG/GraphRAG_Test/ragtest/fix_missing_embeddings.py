#!/usr/bin/env python3
"""
Fix missing community report embeddings for DRIFT search.
This script generates embeddings for community reports that lack them.
"""

import os
import pandas as pd
from openai import OpenAI
import lancedb
from lancedb import connect
import numpy as np

# Configuration
BASE_DIR = os.path.join('ragtest', 'output')
API_KEY = os.environ.get('GRAPHRAG_API_KEY') or os.environ.get('OPENAI_API_KEY')
API_BASE = 'https://api.siliconflow.cn/v1'
EMBEDDING_MODEL = 'Qwen/Qwen3-Embedding-0.6B'
LANCEDB_URI = os.path.join(BASE_DIR, 'lancedb')

assert API_KEY, 'GRAPHRAG_API_KEY or OPENAI_API_KEY environment variable not set.'

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY, base_url=API_BASE)

def get_embedding(text, model=EMBEDDING_MODEL):
    """Get embedding for text using OpenAI API"""
    try:
        response = client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

def main():
    print("Fixing missing community report embeddings...")
    
    # Load community reports
    reports_path = os.path.join(BASE_DIR, 'community_reports.parquet')
    reports = pd.read_parquet(reports_path)
    
    # Check which reports are missing from vector store
    conn = connect(LANCEDB_URI)
    try:
        table = conn.open_table('default-community-full_content')
        existing_df = table.to_pandas()
        existing_ids = set(existing_df['id'].tolist())
        print(f"Found {len(existing_ids)} existing embeddings in vector store")
    except Exception as e:
        print(f"Error accessing vector store: {e}")
        return
    
    # Find missing report embeddings
    missing_reports = reports[~reports['id'].isin(existing_ids)]
    print(f"Found {len(missing_reports)} reports missing embeddings")
    
    if len(missing_reports) == 0:
        print("No missing embeddings found. DRIFT search should work.")
        return
    
    # Process each missing report
    new_embeddings = []
    for _, report in missing_reports.iterrows():
        print(f"Processing community {report['community']} (ID: {report['id']})")
        
        # Use full_content for embedding
        text_to_embed = report.get('full_content', '') or report.get('summary', '') or report.get('title', '')
        if not text_to_embed:
            print(f"  No content found for report {report['id']}, skipping")
            continue
            
        # Get embedding
        embedding = get_embedding(text_to_embed)
        if embedding is None:
            print(f"  Failed to get embedding for report {report['id']}")
            continue
            
        # Prepare record for LanceDB
        new_embeddings.append({
            'id': report['id'],
            'text': text_to_embed,
            'vector': embedding
        })
        print(f"  Generated embedding (dim: {len(embedding)})")
    
    if not new_embeddings:
        print("No valid embeddings generated")
        return
    
    # Add new embeddings to vector store
    try:
        new_df = pd.DataFrame(new_embeddings)
        table.add(new_df)
        print(f"Added {len(new_embeddings)} missing embeddings to vector store")
        print("DRIFT search should now work properly!")
    except Exception as e:
        print(f"Error adding embeddings to vector store: {e}")
        return

if __name__ == '__main__':
    main()

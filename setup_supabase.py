import os
import requests
from dotenv import load_dotenv

# Import the existing data
from knowledge_base import KNOWLEDGE_BASE, CONTRADICTION_GROUPS

def setup_supabase():
    print("Loading environment variables...")
    load_dotenv()
    
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("[!] SUPABASE_URL or SUPABASE_KEY is missing from .env file.")
        return
        
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    print("Connecting to Supabase via REST API...")
    
    # 1. Insert kb_entries
    print(f"Inserting {len(KNOWLEDGE_BASE)} entries into kb_entries...")
    
    # Try deleting all
    requests.delete(f"{url}/rest/v1/kb_entries?id=not.eq.dummy", headers=headers)

    for entry in KNOWLEDGE_BASE:
        row = {
            "id": entry["id"],
            "question": entry["question"],
            "answer": entry["answer"],
            "source": entry["source"],
            "trust_level": entry["trust_level"],
            "category": entry["category"],
            "keywords": entry.get("keywords", []),
            "intents": entry.get("intents", []),
            "controversial": entry.get("controversial", False)
        }
        r = requests.post(f"{url}/rest/v1/kb_entries", json=row, headers=headers)
        if r.status_code not in (200, 201, 204, 205):
            print(f"[!] Error inserting {entry['id']}: {r.text}")
            
    print("[+] Successfully populated kb_entries.")

    # 2. Insert contradiction_groups
    print("Inserting contradiction groups...")
    requests.delete(f"{url}/rest/v1/contradiction_groups?group_name=not.eq.dummy", headers=headers)
        
    for group_name, entry_ids in CONTRADICTION_GROUPS.items():
        row = {
            "group_name": group_name,
            "entry_ids": entry_ids
        }
        r = requests.post(f"{url}/rest/v1/contradiction_groups", json=row, headers=headers)
        if r.status_code not in (200, 201, 204, 205):
            print(f"[!] Error inserting {group_name}: {r.text}")
            
    print("[+] Successfully populated contradiction_groups.")
    print("Supabase migration complete!")

if __name__ == "__main__":
    setup_supabase()

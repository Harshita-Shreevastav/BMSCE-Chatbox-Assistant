import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Import the existing data
from knowledge_base import KNOWLEDGE_BASE, CONTRADICTION_GROUPS

def setup_database():
    print("Loading environment variables...")
    load_dotenv()
    
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("MONGO_DB_NAME", "bmsce_chatbot")
    
    print(f"Connecting to MongoDB at {mongo_uri}...")
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return

    db = client[db_name]
    
    # Setup kb_entries collection
    print(f"Setting up kb_entries collection with {len(KNOWLEDGE_BASE)} entries...")
    kb_collection = db.kb_entries
    
    # Clear existing data to avoid duplicates on re-run
    kb_collection.delete_many({})
    
    # Insert new data
    if KNOWLEDGE_BASE:
        kb_collection.insert_many(KNOWLEDGE_BASE)
    print("kb_entries collection populated.")
    
    # Setup contradiction_groups collection
    print("Setting up contradiction_groups collection...")
    cg_collection = db.contradiction_groups
    
    # Clear existing data
    cg_collection.delete_many({})
    
    # Format contradiction groups for MongoDB
    # Convert from dict to list of documents
    cg_docs = [{"group_name": name, "entry_ids": ids} for name, ids in CONTRADICTION_GROUPS.items()]
    
    if cg_docs:
        cg_collection.insert_many(cg_docs)
    print("contradiction_groups collection populated.")
    
    print("\nDatabase setup complete!")
    print(f"Database: {db_name}")
    print(f"Collections: {db.list_collection_names()}")

if __name__ == "__main__":
    setup_database()

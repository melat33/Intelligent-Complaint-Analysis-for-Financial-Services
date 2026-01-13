# inspect_vectorstore.py
import os
import sqlite3
import json
from pathlib import Path

def inspect_chroma_store(store_path):
    """Inspect Chroma vector store contents"""
    
    print(f"🔍 Inspecting vector store at: {store_path}")
    print("=" * 60)
    
    # Check the directory structure
    store_path = Path(store_path)
    if not store_path.exists():
        print("❌ Directory does not exist!")
        return
    
    # List all items
    print("📁 Directory structure:")
    for item in store_path.rglob("*"):
        indent = "  " * (len(item.relative_to(store_path).parts) - 1)
        if item.is_file():
            size_mb = item.stat().st_size / (1024 * 1024)
            print(f"{indent}📄 {item.name} ({size_mb:.2f} MB)")
        else:
            print(f"{indent}📂 {item.name}/")
    
    # Check SQLite database
    db_path = store_path / "chroma.sqlite3"
    if db_path.exists():
        print(f"\n💾 Database file: {db_path.name} ({db_path.stat().st_size / (1024*1024):.2f} MB)")
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # List all tables
            print("\n📊 Database Tables:")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                print(f"  • {table[0]}")
                
                # Count rows in each table
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
                count = cursor.fetchone()[0]
                print(f"    Rows: {count}")
            
            # Check collections
            print("\n📚 Collections:")
            cursor.execute("SELECT id, name, metadata FROM collections;")
            collections = cursor.fetchall()
            
            if not collections:
                print("  ❌ No collections found!")
            else:
                for col_id, col_name, col_metadata in collections:
                    print(f"  • {col_name} (ID: {col_id})")
                    
                    # Parse metadata if it exists
                    if col_metadata:
                        try:
                            metadata = json.loads(col_metadata)
                            print(f"    Metadata: {metadata}")
                        except:
                            print(f"    Metadata: {col_metadata}")
                    
                    # Count embeddings in this collection
                    cursor.execute(f"SELECT COUNT(*) FROM embeddings WHERE collection_id = '{col_id}';")
                    embedding_count = cursor.fetchone()[0]
                    print(f"    Embeddings: {embedding_count}")
                    
                    # Get sample embeddings
                    cursor.execute(f"""
                        SELECT id, document, metadata 
                        FROM embeddings 
                        WHERE collection_id = '{col_id}' 
                        LIMIT 2;
                    """)
                    samples = cursor.fetchall()
                    
                    if samples:
                        print("    Sample documents:")
                        for i, (emb_id, document, metadata) in enumerate(samples):
                            doc_preview = document[:100].replace('\n', ' ') + "..." if len(document) > 100 else document
                            print(f"      {i+1}. ID: {emb_id[:20]}...")
                            print(f"         Content: {doc_preview}")
                    
            conn.close()
            
        except Exception as e:
            print(f"❌ Error reading database: {e}")
    
    # Check the UUID directory
    uuid_dir = store_path / "a9fcb694-97e0-4476-877d-616c7a174303"
    if uuid_dir.exists() and uuid_dir.is_dir():
        print(f"\n📂 UUID Directory contents:")
        parquet_files = list(uuid_dir.glob("*.parquet"))
        if parquet_files:
            print(f"  Found {len(parquet_files)} Parquet file(s):")
            for pf in parquet_files:
                size_mb = pf.stat().st_size / (1024 * 1024)
                print(f"  • {pf.name} ({size_mb:.2f} MB)")
        else:
            print("  No Parquet files found")
    
    print("\n" + "=" * 60)

def test_chroma_access(store_path):
    """Test accessing the vector store via Chroma API"""
    print("\n🧪 Testing Chroma API Access:")
    print("-" * 40)
    
    try:
        import chromadb
        
        # Try to connect
        client = chromadb.PersistentClient(path=str(store_path))
        
        # List collections
        collections = client.list_collections()
        
        if not collections:
            print("❌ No collections accessible via API")
            return False
        
        print(f"✅ Connected successfully!")
        print(f"📚 Collections found: {len(collections)}")
        
        for collection in collections:
            print(f"\n  Collection: {collection.name}")
            count = collection.count()
            print(f"    Documents: {count}")
            
            # Try to get metadata
            try:
                metadata = collection.metadata or {}
                print(f"    Metadata: {metadata}")
            except:
                pass
            
            # Get a sample
            if count > 0:
                try:
                    results = collection.peek(limit=1)
                    if results['documents']:
                        sample = results['documents'][0]
                        preview = sample[:150].replace('\n', ' ') + "..." if len(sample) > 150 else sample
                        print(f"    Sample: {preview}")
                except Exception as e:
                    print(f"    ⚠️  Could not get sample: {e}")
        
        return True
        
    except ImportError:
        print("❌ chromadb not installed. Install with: pip install chromadb")
        return False
    except Exception as e:
        print(f"❌ Error accessing Chroma: {e}")
        return False

if __name__ == "__main__":
    # Use your vector store path
    store_path = "notebooks/vector_store_1768244751"
    
    # Inspect file structure
    inspect_chroma_store(store_path)
    
    # Test API access
    test_chroma_access(store_path)
    
    print("\n" + "=" * 60)
    print("📋 Summary:")
    print(f"Path: {store_path}")
    print("If collections show but your app says 'no collections', check:")
    print("1. Collection name mismatch")
    print("2. Path in your app code")
    print("3. Permissions")
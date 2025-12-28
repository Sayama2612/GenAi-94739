import chromadb

# db = chromadb.Client(settings=chromadb.Settings(persist_directory="./knowledge_base"))
# collection = db.get_or_create_collection("resumes")
# collection.add(ids=["resume_id"], embeddings=[], metadatas=[], documents=[])
# db.persist()

db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection("resumes")
collection.add(ids=["resume_id"], metadatas=[{"type": "resume"}], documents=["This is a sample resume text for testing"])

print(collection.count())
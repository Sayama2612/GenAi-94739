import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="demo")

raw_text= """
  "Soccer" redirects here. For other uses, see Soccer (disambiguation).
Association football

The attacking player (#10) attempts to kick the ball into the net behind the opposing team's goalkeeper (here wearing red and yellow) to score a goal.
Highest governing body	FIFA
Nicknames	
The beautiful gameThe World's Game[1][2]
First played	December, 1863[3]
Characteristics
Contact	Yes
Team members	11 per side:
Goalkeeper
Defenders
Midfielders
Forwards
Mixed-sex	No, separate competitions
Type	
Team sportball game
Equipment	Football (or soccer ball)
Football boots
Shin guards
Kits
Gloves (for goalkeepers)
Venue	Football pitch (also known as football field, football ground, soccer field, soccer pitch, or "pitch")
Glossary	Glossary of association football
Presence
Country or region	Worldwide
Olympic	Men's since the 1900 Olympics and women's since the 1996 Olympics
Paralympic	5-a-side since 2004 and 7-a-side from 1984 to 2016
Association football, more commonly known as football or soccer,[a] is a team sport played between two teams of 11 players who almost exclusively use their feet to propel a ball around a rectangular field called a pitch.
"""

chunks = text_splitter.split_text(raw_text)

embeddings = embed_model.embed_documents(chunks)

ids = [f"doc_{i}" for i in range(len(chunks))]
metadatas = [{"source":"example.txt", "chunk_id":i} for i in range(len(chunks))]

# print(chunks)

# print("*********************************************")

# print(embeddings)

# print("*********************************************")

# print(metadatas)

# Add to chroma
collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=chunks)
# client.persist()

#Read (similarity search)
query = "How do soccer players train?"
query_embeddings = embed_model.embed_query(query)

# results = collection.query(query_embeddings=[query_embeddings], n_results=2)

# print(results)

#inspect the result
# for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
#     print(meta, "-->", doc)
    
# for distance in results["distances"][0]:
#     print(distance)


#update = delete + reinsert

collection.delete(ids=["doc_3"])

updated_text = "Professoinal soccer players train daily with coaches."
updated_embeddings = embed_model.embed_documents([updated_text]) 

collection.add(ids=["doc_3"], embeddings=updated_embeddings, metadatas=[{"source": "exapmle.txt", "chunk_id": 3}], documents=[updated_text])

results = collection.query(query_embeddings=[query_embeddings], n_results=2)

print(results)  

print(collection.count())

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(meta, "-->", doc)
    
for distance in results["distances"][0]:
    print(distance)   
    
collection.delete(where={"source": "example.txt"})   

print(collection.count())   
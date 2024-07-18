from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
from transformers import AutoTokenizer, AutoModel, pipeline
import torch
import faiss
import json
import sys

# Load text content
with open("C:\Users\Yadav Ji\Documents\GitHub\textbook-QA-system\data\train-v2.0.json", "r") as file:
    text_content = json.load(file)

# Create BM25 index using Whoosh
def create_bm25_index():
    schema = Schema(title=TEXT(stored=True), content=TEXT)
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    for page_num, text in text_content.items():
        writer.add_document(title=str(page_num), content=text)
    writer.commit()

def search_bm25(query_str):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        return [result["content"] for result in results]

# Create BERT embeddings using FAISS
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def encode_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings

texts = list(text_content.values())
embeddings = torch.cat([encode_text(text) for text in texts])

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings.numpy())

def search_faiss(query_str):
    query_embedding = encode_text(query_str).numpy()
    distances, indices = index.search(query_embedding, k=5)
    return [texts[idx] for idx in indices[0]]

if __name__ == "__main__":
    create_bm25_index()
    query = sys.argv[1]
    bm25_results = search_bm25(query)
    faiss_results = search_faiss(query)
    print("BM25 Results:", bm25_results)
    print("FAISS Results:", faiss_results)

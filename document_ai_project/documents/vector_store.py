import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import itertools
import numpy as np

client = chromadb.PersistentClient(
    path="/data/chroma",
    settings=Settings(anonymized_telemetry=False)
)

collection = client.get_or_create_collection("documents")
embedding_func = embedding_functions.DefaultEmbeddingFunction()


def flatten_embedding(embedding):
    if hasattr(embedding, "tolist"):
        embedding = embedding.tolist()
    # If it's a list of lists (multi-vector), average them
    if any(isinstance(i, list) for i in embedding):
        embedding = np.array(embedding)
        embedding = np.mean(
            embedding, axis=0
        ).tolist()
        # Ensure float
        embedding = [float(x) for x in embedding]
        return embedding


def get_embedding(embedding_func, text):
    embedding = embedding_func(text)
    embedding = flatten_embedding(embedding)
    # If embedding has tolist() method, convert it
    if hasattr(embedding, "tolist"):
        embedding = embedding.tolist() 

    if any(isinstance(i, list) for i in embedding):
        embedding = list(itertools.chain.from_iterable(embedding))
    # Cast all values to float
    embedding = [float(x) for x in embedding]

    return embedding


def upsert_document(doc_id, text, metadata):
    try:
        # Generate embedding
        embedding = get_embedding(embedding_func, text)

        if not all(isinstance(x, (int, float)) for x in embedding):
            raise ValueError("Embedding contains non-numeric values")

        # Ensure doc_id is string
        doc_id = str(doc_id)

        # Debug output
        print(f"UPSERTING: {doc_id} | embedding size: {len(embedding)} | metadata keys: {list(metadata.keys())}")

        # Perform upsert
        collection.upsert(
            documents=[text],
            ids=[doc_id],
            metadatas=[metadata],
            embeddings=[embedding]
        )

        # After
        print(f"Collection size after upsert: {len(collection.get()['ids'])}")

    except Exception as e:
        print(f"Failed to upsert document {doc_id}: {e}")


def query_similar_document(text):
    embedding = get_embedding(embedding_func, text)
    result = collection.query(
        query_embeddings=[embedding],
        n_results=1)
    
    first_doc = {
        'id': result['ids'][0][0] if result['ids'][0] else None,
        'document': (
            result['documents'][0][0]
            if result['documents'][0]
            else None
        ),
        'metadata': (
            result['metadatas'][0][0]
            if result['metadatas'][0]
            else None
        ),
    }

    return first_doc
from datasets import load_dataset
from random import choice
from transformers import AutoModel, AutoTokenizer
import torch
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import CollectionStatus

import json

def read_json(path): #read in json file
    with open(path) as f:
        data = json.load(f)
    return data

class QdrantSearch:

    def __init__(self, resumes, job):
        self.resumes = resumes
        self.job = job
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = "news_embeddings"
        dim_size = 4096
        self.client.recreate_collection(
            collection_name = self.collection_name,
            vectors_config = models.VectorParams(size=dim_size, distance=models.Distance.COSINE)
        )
    
    def get_embeddings(self, text):
    
    def update_client(self):
        vectors = []
        ids = []
        for i, r in enumerate(self.resumes):
            vector, size = self.get_embeddings(r)
            vectors.append(vector)
            ids.append(i)
        self.client.upsert(
            collection_name = self.collection_name,
            points = models.Batch(
                ids = ids,
                vectors = vectors,
                payloads = [{'text': r} for r in self.resumes]
            )
        )
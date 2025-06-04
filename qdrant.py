from datasets import load_dataset
from random import choice
from transformers import AutoModel, AutoTokenizer
import torch
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import CollectionStatus

dataset = load_dataset("ag_news", split="train")

for i in range(5):
    random_sample = choice(range(len(dataset)))
    print(f"Sample {i+1}")
    print("=" * 70)
    print(dataset[random_sample]['text'])
    print()
id2label = {str(i): label for i, label in enumerate(dataset.features["label"].names)}

def get_lenght_of_text(example):
    example['length_of_text'] = len(example['text'])
    return example

dataset = dataset.map(get_lenght_of_text)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModel.from_pretrained('gpt2')#.to(device) # switch this for GPU
tokenizer.pad_token = tokenizer.eos_token
text = "What does a cow use to do math? A cow-culator."
inputs = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors="pt")#.to(device)
toks = tokenizer.convert_ids_to_tokens(inputs.input_ids[0])
tokenizer.convert_tokens_to_string(toks)
with torch.no_grad():
    embs = model(**inputs)
def mean_pooling(model_output, attention_mask):

    token_embeddings = model_output[0]
    input_mask_expanded = (attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float())
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask
embedding = mean_pooling(embs, inputs["attention_mask"])
def embed_text(examples):
    inputs = tokenizer(
        examples["text"], padding=True, truncation=True, return_tensors="pt"
    )#.to(device)
    with torch.no_grad():
        model_output = model(**inputs)
    pooled_embeds = mean_pooling(model_output, inputs["attention_mask"])
    return {"embedding": pooled_embeds.cpu().numpy()}

small_set = (
    dataset.shuffle(42)
           .select(range(1000))
           .map(embed_text, batched=True, batch_size=128)
)

n_rows = range(len(small_set))
small_set = small_set.add_column("idx", n_rows)

def get_names(label_num):
    return id2label[str(label_num)]

label_names = list(map(get_names, small_set['label']))
small_set = small_set.add_column("label_names", label_names)

dim_size = len(small_set[0]["embedding"]) # we'll need the dimensions of our embeddings

client = QdrantClient(host="localhost", port=6333)

my_collection = "news_embeddings"
client.recreate_collection(
    collection_name=my_collection,
    vectors_config=models.VectorParams(size=dim_size, distance=models.Distance.COSINE)
)
payloads = small_set.select_columns(["label_names", "text"]).to_pandas().to_dict(orient="records")

client.upsert(
    collection_name=my_collection,
    points=models.Batch(
        ids=small_set["idx"],
        vectors=small_set["embedding"],
        payloads=payloads
    )
)

client.scroll(
    collection_name=my_collection, 
    limit=10,
    with_payload=False, # change to True to see the payload
    with_vectors=False  # change to True to see the vectors
)

query1 = small_set[100]['embedding']

client.search(
    collection_name=my_collection,
    query_vector=query1,
    limit=3
)

query2 = {"text": dataset[choice(range(len(dataset)))]['text']}
query2 = embed_text(query2)['embedding'][0, :]
query2.tolist()

client.search(
    collection_name=my_collection,
    query_vector=query2.tolist(),
    limit=5
)

business = models.Filter(
    must=[models.FieldCondition(key="label_names", match=models.MatchValue(value="Business"))]
)

client.search(
    collection_name=my_collection,
    query_vector=query2.tolist(),
    query_filter=business,
    limit=5
)
import pymongo
import requests

client = pymongo.MongoClient("mongodb+srv://sourabh05:tEiUFc7FS2NPxa9P@cluster0.qz6zsyi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client.sample_mflix
collection = db.movies

hf_token = "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"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2" 

# "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding (text: str) -> list[float]:

    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text, "options": {"wait for model": True}})

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")
    
    return response.json()

# print(generate_embedding("freeCodeCamp is awesome"))


for doc in collection.find({'plot':{"$exists": True}}).limit(50):
   doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
   collection.replace_one({'_id': doc['_id']}, doc)

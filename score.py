from qdrant_client import QdrantClient
from typing import List
import json

def read_json(path): #read in json file
    with open(path) as f:
        data = json.load(f)
    return data

def get_score(resume, jd):
    documents: List[str] = [resume] #resume: str
    client = QdrantClient("http://localhost:6333")
    client.set_model("sentence-transformers/all-MiniLM-L6-v2") #model?
    
    client.add(
        collection_name = "my_collection",
        documents = documents,
    )

    search_result = client.query(
        collection_name = "my_collection", query_text = jd
    )

    return search_result

if __name__ == "__main__":
    # To give your custom resume use this code
    #resume_dict = read_config(
    #    READ_RESUME_FROM
    #    + "/Resume-alfred_pennyworth_pm.pdf83632b66-5cce-4322-a3c6-895ff7e3dd96.json"
    #)
    #job_dict = read_config(
    #    READ_JOB_DESCRIPTION_FROM
    #    + "/JobDescription-job_desc_product_manager.pdf6763dc68-12ff-4b32-b652-ccee195de071.json"
    #)
    resume_dict = read_json('extracted_resume.json')
    job_dict = read_json('extracted_skills_csoaf_jd1.json')
    resume_keywords = resume_dict["keywords"]
    job_description_keywords = job_dict

    resume_string = " ".join(resume_keywords)
    jd_string = " ".join(job_description_keywords)
    final_result = get_score(resume_string, jd_string)
    for r in final_result:
        print(r.score)
# keywords
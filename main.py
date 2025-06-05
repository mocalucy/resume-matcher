import os
import json
import argparse
import glob
from src.resume_parser import to_JSON
from src.utils import read_pdf
from src.score import get_score
from qdrant_client import QdrantClient

# === Qdrant Cleanup: Delete all collections ===
client_cleanup = QdrantClient("http://localhost:6333")
for collection in client_cleanup.get_collections().collections:
    print(f"Deleting Qdrant collection: {collection.name}")
    client_cleanup.delete_collection(collection_name=collection.name)

def main():
    # === Argument Parsing ===
    parser = argparse.ArgumentParser(description="Parse resumes and compare to job description.")
    parser.add_argument("--input", "-i", required=True, help="Path to input resume PDF(s). Can be a single file, multiple files separated by commas, or a directory containing PDFs")
    parser.add_argument("--jobdesc", "-j", required=True, help="Path to job description PDF file")
    parser.add_argument("--output", "-o", default="extracted_resume.json", help="Path to save parsed resume JSON")
    parser.add_argument("--save-json", action="store_true", help="Save parsed resume data to JSON files")
    args = parser.parse_args()

    # === Get list of resume files ===
    resume_files = []
    if os.path.isdir(args.input):
        resume_files = glob.glob(os.path.join(args.input, "*.pdf"))
    else:
        resume_files = [f.strip() for f in args.input.split(",")]

    if not resume_files:
        print(f"❌ No resume files found in: {args.input}")
        return

    if not os.path.exists(args.jobdesc):
        print(f"❌ Job description file not found: {args.jobdesc}")
        return

    # === Parse Job Description First ===
    print(f"📄 Reading job description: {args.jobdesc}")
    jd_text = read_pdf(args.jobdesc)
    print("🧠 Parsing job description...")
    jd_data = to_JSON(jd_text)
    jd_keywords = jd_data.get("keywords", [])
    jd_string = " ".join(jd_keywords)

    # === Qdrant Setup ===
    collection_name = "resume_matcher_collection"
    client = QdrantClient("http://localhost:6333")
    client.set_model("sentence-transformers/all-MiniLM-L6-v2")

    # === Process and Add Each Resume ===
    print("\n📊 Processing Resumes:")
    resume_texts = []
    resume_names = []
    for resume_file in resume_files:
        if not os.path.exists(resume_file):
            print(f"❌ Resume file not found: {resume_file}")
            continue
        print(f"\n📄 Reading resume: {resume_file}")
        resume_text = read_pdf(resume_file)
        print("🧠 Parsing resume...")
        resume_data = to_JSON(resume_text)
        
        # Save JSON file only if --save-json flag is set
        if args.save_json:
            output_file = f"{os.path.splitext(os.path.basename(resume_file))[0]}_analysis.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(resume_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Resume saved to: {output_file}")
        
        resume_keywords = resume_data.get("keywords", [])
        resume_string = " ".join(resume_keywords)
        resume_texts.append(resume_string)
        resume_names.append(os.path.basename(resume_file))

    # Add all resumes to Qdrant at once
    if resume_texts:
        client.add(collection_name=collection_name, documents=resume_texts)
    else:
        print("No valid resumes to process.")
        return

    # Query Qdrant with job description
    results = get_score(jd_string)

    # Print similarity scores for each resume
    print("\n🔎 Match Scores:")
    for i, r in enumerate(results):
        name = resume_names[i] if i < len(resume_names) else f"Resume {i+1}"
        print(f"{name}: Score: {r.score:.4f}")

if __name__ == "__main__":
    main()

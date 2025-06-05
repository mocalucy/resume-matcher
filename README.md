# 🔍 Resume Matcher: AI-Powered Resume-to-Job Matching

Resume Matcher is an intelligent tool that leverages NLP and vector search to semantically match resumes to job descriptions. Instead of relying on simple keyword overlap, it captures the meaning behind the content, making it easier to identify the most relevant candidates.

🚀 Core Features:

📄 Resume & JD Parsing – Extracts structured data and keywords using NLP pipelines.

🧠 Semantic Embeddings – Transforms text into vector representations with sentence-transformers.

⚡ Fast Similarity Search – Uses Qdrant (a vector database) to score and rank resumes against a given job description.

📈 Insightful Scoring – Displays relevance scores to help recruiters quickly find top matches.

## Features

- Parse PDF resumes and extract key information
- Compare multiple resumes against a job description
- Calculate semantic similarity scores
- Support for multiple input formats (single file, multiple files, or directory)
- Save parsed resume data to JSON files

## Prerequisites

- Python 3.8+
- Qdrant vector database
- Required Python packages (see Installation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-matcher.git
cd resume-matcher
```

2. Create and activate a conda environment:
```bash
conda create -n vol python=3.12
conda activate vol
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Start Qdrant server (using Docker):
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

5. Download required NLTK data (required for text processing):
```bash
# NLTK requires additional data files for text processing
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"
```

## Usage

The script can be used in three ways:

1. **Single Resume**:
```bash
python main.py -i "path/to/resume.pdf" -j "path/to/job_description.pdf"
```

2. **Multiple Resumes** (comma-separated):
```bash
python main.py -i "resume1.pdf,resume2.pdf" -j "job_description.pdf"
```

3. **Directory of Resumes**:
```bash
python main.py -i "path/to/resumes/directory" -j "job_description.pdf"
```

### Arguments

- `-i, --input`: Path to input resume(s). Can be:
  - A single PDF file
  - Multiple PDF files separated by commas
  - A directory containing PDF files
- `-j, --jobdesc`: Path to job description PDF file
- `-o, --output`: (Optional) Path to save parsed resume JSON (default: "extracted_resume.json")
- `--save-json`: (Optional) Save parsed resume data to JSON files. If not specified, only scores will be displayed.

### Output

For each resume, the script:
1. (Optional) Creates a JSON file with parsed information (named `{resume_name}_analysis.json`) if `--save-json` is specified
2. Calculates and displays a similarity score against the job description

Example output:
```
📄 Reading job description: job_description.pdf
🧠 Parsing job description...

📊 Processing Resumes:
📄 Reading resume: resume1.pdf
🧠 Parsing resume...
✅ Resume saved to: resume1_analysis.json  # Only shown if --save-json is used

🔎 Match Scores:
resume1.pdf: Score: 0.7973
```

## Project Structure

```
resume-matcher/
├── main.py              # Main script
├── src/
│   ├── resume_parser.py # Resume parsing logic
│   ├── score.py         # Similarity scoring
│   └── utils.py         # Utility functions
└── data/               # Sample resumes and job descriptions
```

## How It Works

1. **Resume Parsing**: Extracts text and key information from PDF resumes
2. **Job Description Processing**: Parses the job description PDF
3. **Vector Similarity**: Uses Qdrant and sentence transformers to calculate semantic similarity
4. **Scoring**: Compares each resume against the job description and outputs similarity scores

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

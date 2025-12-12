# RAG AI Project - Video Transcription & LLM Integration

A Retrieval-Augmented Generation (RAG) system that converts YouTube videos to text, creates embeddings, and uses an LLM to answer questions based on video content.

## Project Overview

This project implements an end-to-end RAG pipeline:

1. **Convert videos to audio** (MP3 format)
2. **Transcribe audio to text** using OpenAI Whisper
3. **Create structured chunks** and merge them for better context
4. **Generate embeddings** and store them locally
5. **Answer user queries** using cosine similarity + OpenAI LLM

## Project Structure

```
├── 01_videos_to_mp3.py          # Convert video files to MP3
├── 02_mp3_to_chunks.py          # Transcribe MP3 to text chunks using Whisper
├── merge_chunk.py                # Merge 5 small chunks into larger chunks
├── 03_main.py                    # Generate embeddings & process user queries
├── embeddings.joblib             # Stored embeddings (generated on first run)
├── prompt.txt                    # User prompt from last query
├── response.txt                  # LLM response from last query
├── audios/                       # MP3 files (not included in repo - too large)
├── jsons/                        # Original text chunks from Whisper
├── newJsons/                     # Merged chunks (larger, more meaningful)
└── Videos/                       # Original video files (not included in repo)
```

## Setup & Installation

1. **Clone the repository** and navigate to the project directory:

```bash
cd "RAG AI Project"
```

2. **Create and activate virtual environment**:

```bash
python -m venv rag_env
# On Windows:
rag_env\Scripts\activate
# On macOS/Linux:
source rag_env/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set up OpenAI API key**:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`

## Usage

This is a ready-to-use project with pre-processed JSON chunks from the **Code with Harry Web Development Course** (first 18 videos). Simply run the main file to start!

### Quick Start

```bash
python 03_main.py
```

**First Run**: Type `0`

- Creates embeddings from all chunks in `newJsons/` folder
- Stores embeddings in `embeddings.joblib` for fast retrieval

**Subsequent Runs**: Run the main file again

- Type `0`: Regenerate all embeddings
- Type `1`: Enter your query
  - System finds the most relevant chunks from the course videos
  - Sends query + context to OpenAI LLM
  - Saves your prompt to `prompt.txt` and response to `response.txt`

### Project Contents

This project includes content from:

- **18 Web Development Videos** from Code with Harry
- **Pre-processed JSON chunks** in `newJsons/` folder
- **Merged chunks** for better context (5 chunks merged per file)
- **Ready-to-use embeddings pipeline**

### Example Queries

- "What are semantic tags in HTML?"
- "How do CSS selectors work?"
- "Explain the CSS Box Model"
- "What is the difference between inline and block elements?"

## How It Works

### Embedding & Retrieval

- Uses OpenAI's embedding model to create vector representations of text chunks
- Stores embeddings locally in `embeddings.joblib` for fast retrieval
- Uses **cosine similarity** to find chunks most relevant to user queries

### LLM Integration

- Initially attempted local LLM (did not perform well)
- **Current**: OpenAI API integration
- Passes user query + top relevant chunks to the LLM for context-aware responses
- Responses are saved for reference

## Key Files

| File                  | Purpose                                  |
| --------------------- | ---------------------------------------- |
| `01_videos_to_mp3.py` | Video → MP3 conversion                   |
| `02_mp3_to_chunks.py` | MP3 → Text chunks (Whisper)              |
| `merge_chunk.py`      | Merge small chunks into larger ones      |
| `03_main.py`          | Embeddings generation & query processing |
| `embeddings.joblib`   | Stored embeddings (auto-generated)       |

## Dependencies

- `openai` - OpenAI API & Whisper
- `numpy` - Numerical computations
- `scikit-learn` - Cosine similarity
- `joblib` - Embedding storage
- `python-dotenv` - Environment variables

## Notes

- **Large Files**: `audios/`, `Videos/`, and `embeddings.joblib` are not included in the repo due to size constraints
- **First Run**: Type `0` to generate embeddings from the `newJsons/` folder
- **Chunking Strategy**: Original chunks from Whisper are small; merging 5 chunks at a time creates more meaningful context for the LLM

## Course

Last project in my Data Science course by Code with Harry to complete the course.

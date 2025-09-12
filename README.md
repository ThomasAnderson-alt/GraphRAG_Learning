# GraphRAG Learning

A project for advanced retrieval-augmented generation (RAG) using graph-based methods, supporting global, local, and DRIFT search, as well as entity-based question generation.

## Project Structure

```
GraphRAG/
├── GraphRAG_Test/
│   ├── .env
│   ├── .vscode/
│   ├── GrapRAG_test.py
│   ├── GraphRAG.venv/
│   └── ragtest/
│       ├── fix_missing_embeddings.py
│       ├── generate_missing_community_report.py
│       ├── settings.yaml
│       ├── prompts/
│       ├── input/
│       ├── output/
│       ├── cache/
│       ├── logs/
│       └── __pycache__/
└── Program Result/
    ├── fix_missing_embeddings.py
    ├── GraphRAG_QueryEngine_result.md
    └── settings.yaml
```

## Folder and File Summaries

### GraphRAG_Test/

- **.env**: Stores environment variables, including API keys for LLM access.
- **.vscode/**: VS Code workspace settings.
- **GrapRAG_test.py**: (Empty) Placeholder for test scripts.
- **GraphRAG.venv/**: Python virtual environment for dependencies.

#### ragtest/

- **fix_missing_embeddings.py**: Script to generate missing embeddings for community reports using OpenAI API and LanceDB.
- **generate_missing_community_report.py**: Script to backfill missing community reports for specified community IDs using LLMs.
- **settings.yaml**: Main configuration file for models, input/output, workflow, and search settings.
- **prompts/**: Contains prompt templates for various LLM tasks (search, summarization, extraction, etc.).
- **input/**: Stores input data files (e.g., `book.txt`).
- **output/**: Stores output data, including Parquet files for communities, reports, entities, relationships, and LanceDB vector stores.
- **cache/**: Caches intermediate results for community reporting, graph extraction, summarization, and embeddings.
- **logs/**: Log files for process tracking.
- ****pycache**/**: Python bytecode cache.

### Program Result/

- **fix_missing_embeddings.py**: (Duplicate) Script for fixing missing embeddings.
- **GraphRAG_QueryEngine_result.md**: Markdown summary of the Query Engine's capabilities and environment.
- **settings.yaml**: (Duplicate) Configuration file.

---

## Main Features

- **Global, Local, and DRIFT Search**: Advanced search capabilities using LLMs and graph-based context.
- **Entity-based Question Generation**: Generate questions based on extracted entities.
- **Embeddings and Vector Search**: Uses LanceDB for storing and querying embeddings.
- **Highly Configurable**: All major settings are controlled via YAML config files.

## Getting Started

1. Clone the repository and set up the Python environment using the provided `.venv`.
2. Set your API key in `.env`.
3. Adjust `settings.yaml` as needed for your use case.
4. Use the scripts in `ragtest/` to process data, generate reports, and fix embeddings.

## Prompts

Prompt templates for LLM tasks are stored in `ragtest/prompts/` and referenced in the config.

## Data

- **Input**: Place your source text or data in `ragtest/input/`.
- **Output**: Results, embeddings, and reports are saved in `ragtest/output/`.

## Logs

Process logs are stored in `ragtest/logs/`.

---

Let me know if you want to add more details or sections!

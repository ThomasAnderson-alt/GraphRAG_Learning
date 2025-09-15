=======

# 🚀 GraphRAG Learning Project

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![GraphRAG](https://img.shields.io/badge/Framework-GraphRAG-blueviolet)](https://microsoft.github.io/graphrag/)
[![LanceDB](https://img.shields.io/badge/Vector_Store-LanceDB-yellowgreen)](https://lancedb.github.io/lancedb/)
[![OpenAI API](https://img.shields.io/badge/API-OpenAI-brightgreen)](https://platform.openai.com/docs/api-reference)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> > > > > > > # 80da456 (README.md update)

# 🚀 GraphRAG Learning Project

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![GraphRAG](https://img.shields.io/badge/Framework-GraphRAG-blueviolet)](https://microsoft.github.io/graphrag/)
[![LanceDB](https://img.shields.io/badge/Vector_Store-LanceDB-yellowgreen)](https://lancedb.github.io/lancedb/)
[![OpenAI API](https://img.shields.io/badge/API-OpenAI-brightgreen)](https://platform.openai.com/docs/api-reference)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> > > > > > > 80da456 (README.md update)

---

<<<<<<< HEAD

```text
GraphRAG/
├── GraphRAG_Test/
│   ├── .env
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
│       └── logs/
└── Program Result/
    ├── GraphRAG_QueryEngine_result.md
    └── settings.yaml
```

---

## Core Components

### Query Engine

The query engine is the core of this project, capable of performing three distinct types of search. The examples below are based on the analysis of _A Christmas Carol_.

#### Global Search

- **Use Case**: Answering high-level, summarization questions about the entire story.
- **Process**: Involves a map-reduce process where multiple "analyst" LLM calls run in parallel to analyze data chunks, followed by a reduce phase to synthesize a final answer.
- **Example Query**: `What are the top themes in this story?`
- **Example Response**: `The top theme of the story is the moral and spiritual transformation of Ebenezer Scrooge, driven by compassion, community, and supernatural intervention...`

#### Local Search

- **Use Case**: Answering specific questions about an entity or its relationships.
- **Process**: A single, focused LLM call that uses context from the most relevant text units and community data.
- **Example Query**: `Who is Scrooge and what are his main relationships?`
- **Example Response**: `Ebenezer Scrooge is a miserly businessman who undergoes a transformative journey after interacting with three ghosts...`

#### DRIFT Search

- **Use Case**: Answering complex, investigative questions that may not have a direct answer in the text, requiring deeper exploration.
- **Process**: An iterative process that starts with an initial query, builds local context, synthesizes information, and generates follow-up questions to explore the data further.
- **Example Query**: `How might Scrooge's childhood events have indirectly led to his loneliness in adulthood?`
- **Example Response**: `Exposure to Social Contrasts: Growing up as the son of a wealthy merchant... Orphanhood and Neglect: The death of Scrooge's father left him orphaned...`

### Key Scripts

- **`GraphRAG_Test/ragtest/fix_missing_embeddings.py`**: A utility script to generate and backfill missing vector embeddings for community reports. This is crucial for ensuring that DRIFT search functions correctly, as it relies on a complete set of embeddings in the LanceDB vector store.
- **`GraphRAG_Test/ragtest/generate_missing_community_report.py`**: This script backfills missing community reports for specified community IDs. It can also be used to regenerate a report with a richer, more detailed prompt if the initial one is insufficient.

### Configuration (`settings.yaml`)

The `settings.yaml` file is the central configuration for the entire GraphRAG pipeline. Key sections include:

- **`models`**: Defines the LLM and embedding models to be used, including API endpoints, keys, and performance settings (e.g., `TPM`, `RPM`, `concurrent_requests`).
- **`input`**: Specifies the location and type of input data.
- **`chunks`**: Controls how source documents are divided into smaller pieces for processing.
- **`output`**, **`cache`**, **`reporting`**: Define where final results, intermediate data, and logs are stored.
- **`vector_store`**: Configures the LanceDB vector database.
- **`workflow`**: Outlines the steps of the indexing pipeline, such as `extract_graph`, `summarize_descriptions`, and `community_reports`.
- **`query`**: Contains settings for `local_search`, `global_search`, and `drift_search`, including prompt locations and context token limits.

---

=======

## 📖 Overview

GraphRAG Learning is an advanced Retrieval-Augmented Generation (RAG) project leveraging graph-based methods for enhanced information retrieval and question answering. It supports:

- 🌐 **Global Search**: High-level, summarization questions
- 🔍 **Local Search**: Direct, factual entity-based queries
- 🧭 **DRIFT Search**: Iterative, investigative exploration
- 🏷️ **Entity-based Question Generation**

The repository is pre-configured for Charles Dickens' _A Christmas Carol_ and demonstrates a full RAG pipeline with LanceDB vector search and OpenAI-compatible LLMs.

---

## 🗂️ Table of Contents

- [✨ Features](#-features)
- [📁 Project Structure](#-project-structure)
- [🧩 Core Components](#-core-components)
- [🚦 Getting Started](#-getting-started)
- [🔄 Data Flow](#-data-flow)
- [📝 License](#-license)

---

## ✨ Features

- **Multi-Strategy Search**: Global, Local, and DRIFT search for flexible information retrieval
- **Entity-based Question Generation**: Generate questions from extracted entities
- **Configurable Pipeline**: All major settings in `settings.yaml`
- **LanceDB Vector Search**: Fast, scalable embedding storage
- **Prompt Templates**: Modular prompt design for LLM tasks
- **Reproducible Environment**: Pre-built Python 3.11+ virtual environment

---

## 📁 Project Structure

```text
GraphRAG/
├── GraphRAG_Test/
│   ├── .env                  # API keys and environment variables
│   ├── GraphRAG.venv/        # Python virtual environment
│   └── ragtest/
│       ├── fix_missing_embeddings.py         # Script to backfill missing vector embeddings
│       ├── generate_missing_community_report.py # Script to regenerate community reports
│       ├── settings.yaml                     # Main pipeline configuration
│       ├── prompts/                         # Prompt templates for LLM tasks
│       ├── input/                           # Input data (e.g., book.txt)
│       ├── output/                          # Output data (Parquet, LanceDB, etc.)
│       ├── cache/                           # Intermediate results
│       └── logs/                            # Log files
└── Program Result/
    ├── GraphRAG_QueryEngine_result.md       # Query engine analysis and results
    └── settings.yaml                        # (Duplicate) Pipeline configuration
```

---

## 🧩 Core Components

### ⚙️ Query Engine

Performs three main search types, each powered by LLMs and graph context:

- **Global Search**: Map-reduce LLM analysis for broad themes
- **Local Search**: Focused entity/relationship queries
- **DRIFT Search**: Iterative, context-building exploration

### 🛠️ Key Scripts

- `fix_missing_embeddings.py`: Ensures all community reports have vector embeddings for DRIFT search
- `generate_missing_community_report.py`: Backfills or regenerates community reports for missing IDs

### ⚙️ Configuration (`settings.yaml`)

Centralizes all pipeline, model, and workflow settings:

- LLM and embedding model selection
- Input/output/cache directory structure
- Workflow steps (graph extraction, summarization, reporting)
- Query prompt locations and context limits

---

## 🚦 Getting Started

### 🛠️ Prerequisites

> > > > > > > 80da456 (README.md update)

- Python 3.11+
- OpenAI-compatible API key (pre-configured for SiliconFlow)

<<<<<<< HEAD

### Prerequisites

- Python 3.11+
- An API key for an OpenAI-compatible service. This project is pre-configured for SiliconFlow.

### Setup

1. **Clone the repository**:

   ```sh
   git clone <repository-url>
   cd GraphRAG_Learning
   ```

2. **Activate the Virtual Environment**:
   The project includes a pre-configured virtual environment.

   ```powershell
   # On Windows
   .\GraphRAG\GraphRAG_Test\GraphRAG.venv\Scripts\Activate.ps1
   ```

3. **Set Environment Variables**:
   Create a `.env` file in the `GraphRAG/GraphRAG_Test/` directory and add your API key:

   ```text
   GRAPHRAG_API_KEY="your-api-key-here"
   ```

### Running the Indexing Pipeline

# Before you can run queries, you must first process your input data. The following command will initialize the project structure and run the full indexing pipeline based on the settings in `settings.yaml`.

### ⚡ Setup

1. **Clone the repository**

   ```sh
   git clone <repository-url>
   cd GraphRAG_Learning
   ```

2. **Activate the virtual environment**

   ```powershell
   .\GraphRAG\GraphRAG_Test\GraphRAG.venv\Scripts\Activate.ps1
   ```

3. **Set your API key**

   - Create a `.env` file in `GraphRAG/GraphRAG_Test/`:

     ```env
     GRAPHRAG_API_KEY="your-api-key-here"
     ```

### 🏗️ Running the Indexing Pipeline

> > > > > > > 80da456 (README.md update)

```sh
graphrag --init --root ./GraphRAG/GraphRAG_Test/ragtest
```

<<<<<<< HEAD
This will read the data from `ragtest/input/`, process it, and store the output in `ragtest/output/`.

### Running Queries

Once the indexing is complete, you can run queries using the following commands.

#### Global Search Query

```sh
graphrag query --root ./GraphRAG/GraphRAG_Test/ragtest --method global "What are the top themes in this story?"
```

#### Local Search Query

```sh
graphrag query --root ./GraphRAG/GraphRAG_Test/ragtest --method local "Who is Scrooge and what are his main relationships?"
```

#### DRIFT Search Query

````sh
=======
This processes input data and prepares all outputs for querying.

### 🔎 Running Queries

```sh
# Global Search
graphrag query --root ./GraphRAG/GraphRAG_Test/ragtest --method global "What are the top themes in this story?"
# Local Search
graphrag query --root ./GraphRAG/GraphRAG_Test/ragtest --method local "Who is Scrooge and what are his main relationships?"
# DRIFT Search
>>>>>>> 80da456 (README.md update)
graphrag query --root ./GraphRAG/GraphRAG_Test/ragtest --method drift "How might Scrooge's childhood events have indirectly led to his loneliness in adulthood?"
````

---

<<<<<<< HEAD

## Data Flow

- **Input (`ragtest/input/`)**: Place your source text files here. The project is pre-loaded with `book.txt`.
- **Cache (`ragtest/cache/`)**: Stores intermediate results from the indexing pipeline to speed up subsequent runs.
- **Output (`ragtest/output/`)**: Contains the final processed data, including Parquet files for entities, relationships, and communities, as well as the LanceDB vector store.
- **Logs (`ragtest/logs/`)**: Records logs from the indexing and query processes for debugging.
- # **Prompts (`ragtest/prompts/`)**: Contains all the prompt templates used by the LLMs for various tasks.

## 🔄 Data Flow

- **Input**: `ragtest/input/` — Source text files (e.g., `book.txt`)
- **Cache**: `ragtest/cache/` — Intermediate pipeline results
- **Output**: `ragtest/output/` — Final data (entities, relationships, communities, LanceDB)
- **Logs**: `ragtest/logs/` — Process logs
- **Prompts**: `ragtest/prompts/` — All LLM prompt templates

---

---

## 🤝 Contributing

We welcome contributions to **GraphRAG Learning**! To contribute:

1. Fork the repository and create your branch from `master`.
2. Ensure your code follows the existing style and includes appropriate tests/documentation.
3. Open a pull request with a clear description of your changes and reference any related issues.
4. For major changes, please open an issue first to discuss your proposal.

**Code of Conduct:** Please be respectful and constructive in all interactions.

---

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

> > > > > > > 80da456 (README.md update)

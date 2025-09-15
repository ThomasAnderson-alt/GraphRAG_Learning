# 📈 GraphRAG Learning Project

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![GraphRAG](https://img.shields.io/badge/Microsoft-GraphRAG-orange?style=for-the-badge&logo=microsoft)

## 📖 About The Project

This project is a learning exercise to understand and implement Microsoft's GraphRAG. It demonstrates how to use GraphRAG to build a Retrieval-Augmented Generation (RAG) system that leverages graph-based data structures for enhanced information retrieval and generation.

The project processes a text document (`book.txt`), builds a graph from it, and then uses this graph to answer questions.

## 🚀 Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- Python 3.11
- A virtual environment manager (e.g., `venv`)

### Installation

1. **Clone the repo**

   ````sh
   git clone https://github.com/ThomasAnderson-alt/GraphRAG_Learning.git
   ```plaintext

   ````

2. **Navigate to the project directory**

   ```sh
   cd GraphRAG_Learning/GraphRAG/GraphRAG_Test
   ```

3. **Create and activate a virtual environment**

   ```sh
   python -m venv GraphRAG.venv
   .\GraphRAG.venv\Scripts\Activate.ps1
   ```

4. **Install the required packages**
   The required packages are included in the `GraphRAG.venv` folder. If you need to reinstall them, you can use the `pip freeze` command on the existing environment to generate a `requirements.txt` file.

## ⚙️ Usage

The main logic is within the `ragtest` directory.

1. **Configure your settings**
   Modify the `settings.yaml` file to configure the GraphRAG pipeline. This includes setting up your LLM provider, embedding models, and other parameters. You will also need to create a `.env` file with your API keys.

2. **Run the GraphRAG pipeline**
   The `graphrag.exe` in the `GraphRAG.venv/Scripts` directory can be used to run the pipeline.

   ```sh
   # Example of running the pipeline
   .\GraphRAG.venv\Scripts\graphrag.exe --root . --config settings.yaml
   ```

## 📂 Project Structure

```plaintext
--- IGNORE ---
GraphRAG/
├── GraphRAG_Test/
│   ├── GraphRAG.venv/      # Virtual environment
│   ├── ragtest/
│   │   ├── input/
│   │   │   └── book.txt    # Input text data
│   │   ├── output/         # Output from the GraphRAG pipeline
│   │   ├── prompts/        # Prompts for the LLM
│   │   ├── settings.yaml   # Configuration for the pipeline
│   │   └── ...
│   └── ...
└── Program Result/
    ├── GraphRAG_QueryEngine_result.md # Example query results
    └── ...
```

## 📊 Results

The `output` directory in `ragtest` contains the results of the GraphRAG pipeline, including:

- `communities.parquet`
- `community_reports.parquet`
- `documents.parquet`
- `entities.parquet`
- `relationships.parquet`
- `text_units.parquet`
- A LanceDB vector database in the `lancedb` subdirectory.

An example of query results can be found in `Program Result/GraphRAG_QueryEngine_result.md`.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

# GraphRAG Query Engine Analysis

This document provides a detailed analysis of the GraphRAG Query Engine's capabilities, using Charles Dickens' _A Christmas Carol_ as the sample dataset. It covers the environment setup, model configurations, and a deep dive into the supported search methods: **Global Search**, **Local Search**, and **DRIFT Search**.

---

## 1. Environment and Configuration

### 1.1. Execution Environment

| Parameter          | Value    |
| :----------------- | :------- |
| **Environment**    | `.venv`  |
| **Python Version** | `3.11.9` |

### 1.2. Indexing Parameters

| Parameter         | Value  |
| :---------------- | :----- |
| **Chunk Size**    | `2000` |
| **Chunk Overlap** | `50`   |

### 1.3. Model Configuration

The following models were used for the different search methods. Note that DRIFT search required a model change due to JSON output requirements.

| Model Type            | Model Name                  | TPM   | RPM  | Max Output Tokens | Used For              |
| :-------------------- | :-------------------------- | :---- | :--- | :---------------- | :-------------------- |
| **Chat Model**        | `Qwen/Qwen3-8B`             | 50000 | 1000 | -                 | Global & Local Search |
| **Embedding Model**   | `Qwen/Qwen3-Embedding-0.6B` | 50000 | 1000 | -                 | Global & Local Search |
| **Chat Model (JSON)** | `THUDM/GLM-4-9B-0414`       | 20000 | 500  | 512               | DRIFT Search          |
| **Embedding Model**   | `BAAI/bge-m3`               | -     | -    | -                 | DRIFT Search          |

---

## 2. Query Engine Capabilities

The GraphRAG Query Engine is capable of performing the following tasks:

- **Global Search**: For broad, high-level analysis.
- **Local Search**: For specific, factual queries.
- **DRIFT Search**: For complex, investigative questions.
- **Entity-based Question Generation**

The following sections provide a detailed look at each search method.

---

## 3. Search Method Deep Dive

### 3.1. Global Search

**Best for:** High-level, summarization questions about the entire dataset.

#### Example: Top Themes

**Query:**

```bash
graphrag query \
--root ./ragtest \
--method global \
--query "What are the top themes in this story?"
```

**Response:**

> The top theme of the story is the moral and spiritual transformation of Ebenezer Scrooge, driven by compassion, community, and supernatural intervention, as evidenced by his interactions with the Cratchit family, Fred, and the three spirits, with the COUNTING-HOUSE symbolizing his materialistic nature [Data: Reports (29, 18, 21, 9, 103, +more)].

- **Time to execute:** ~4 minutes
- **Process:**
  1. **Map Phase**: Analyzes data chunks using `global_search_map_system_prompt.txt`.
  2. **Reduce Phase**: Synthesizes a final answer using `global_search_reduce_system_prompt.txt`.
  3. **Knowledge Enhancement**: Refines the answer with `global_search_knowledge_system_prompt.txt`.

**Configuration (`settings.yaml`):**

```yaml
global_search:
  max_context_tokens: 3000 # Total context for each analyst
  data_max_tokens: 3000 # Data size per analyst
  map_max_length: 150 # Individual analyst report length
  reduce_max_length: 200 # Final synthesized answer length
  dynamic_search_threshold: 1 # Relevance threshold
  dynamic_search_num_repeats: 1 # Single analysis pass
```

---

### 3.2. Local Search

**Best for:** Direct questions about a specific entity or its relationships.

#### Example: Scrooge's Relationships

**Query:**

```bash
graphrag query \
--root ./ragtest \
--method local \
--query "Who is Scrooge and what are his main relationships? Answer in one paragraph of no more than five sentences."
```

**Response:**

> Ebenezer Scrooge is a miserly businessman who undergoes a transformative journey after interacting with three ghosts: the Ghost of Christmas Past, Present, and Future [Data: Relationships (15, 34, 170)]. His primary relationships include his nephew Fred, who challenges his coldness with warmth and humour during Christmas gatherings [Data: Entities (156, 14), Relationships (14, 181)], his niece Fan, who shares familial bonds and playful moments with Fred [Data: Entities (119), Relationships (130, 135)], and Jacob Marley, his deceased business partner whose ghost confronts him about his past actions [Data: Entities (33), Relationships (33, 12)]. Scrooge also interacts with Bob Cratchit, his clerk, during the Christmas dinner and a meeting where Cratchit expresses gratitude for Scrooge’s nominal kindness [Data: Entities (158, 158), Relationships (183, 185, 186)]. Additionally, he has connections to characters like the schoolmaster and the undertaker’s man, who represent pivotal moments in his past [Data: Relationships (56, 155)].

- **Time to execute:** ~1 minute
- **Process:** A single-pass process using `local_search_system_prompt.txt`.

**Configuration (`settings.yaml`):**

```yaml
local_search:
  max_context_tokens: 4000 # Total context size for the single call
  text_unit_prop: 0.5 # Proportion of text units vs. communities
  community_prop: 0.1 # Proportion of community data
```

---

### 3.3. DRIFT Search

**Best for:** Investigative and complex analytical questions that require iterative exploration.

#### Example: The Roots of Scrooge's Loneliness

**Query:**

```bash
graphrag query \
--root ./ragtest \
--method drift \
--query "How might Scrooge's childhood events have indirectly led to his loneliness in adulthood? Answer in one paragraph."
```

**Response:**

> **Exposure to Social Contrasts:** Growing up as the son of a wealthy merchant in London exposed Scrooge to the stark differences between wealth and poverty. This early exposure may have fostered a sense of entitlement and detachment from the struggles of others, contributing to a lack of empathy and social connection later in life [Data: Scrooge's Childhood and Loneliness (1, 2)].
>
> **Orphanhood and Neglect:** The death of Scrooge's father left him orphaned, placing him under the care of his cold and authoritarian sister, Fan. This early experience of familial neglect and emotional distance may have been a significant factor in his emotional isolation [Data: Scrooge's Childhood and Loneliness (2)].
>
> **Lack of Stable Family Structure:** Fan's subsequent marriage and move to another country further removed Scrooge from any stable family support system. Navigating adulthood with limited emotional support from family likely contributed to his sense of being alone [Data: Scrooge's Childhood and Loneliness (2)].
>
> **Rejection of Kindness and Love:** Scrooge's decision to break off his engagement to Belle due to financial concerns rather than emotional connection highlights his obsession with money and rejection of meaningful personal relationships. This rejection likely deepened his sense of loneliness [Data: Scrooge's Childhood and Loneliness (2)].

- **Time to execute:** ~1 minute
- **Process:**
  1. **Initial Query**: `drift_search_system_prompt.txt`
  2. **Context Building**: `local_search_system_prompt.txt`
  3. **Data Synthesis**: `drift_reduce_prompt.txt`
  4. **Follow-up Queries**: `basic_search_system_prompt.txt`

**Configuration (`settings.yaml`):**

```yaml
drift_search:
  concurrency: 1 # Sequential processing
  primer_folds: 1 # Number of primer analyses
  data_max_tokens: 800 # Context size per search
  reduce_max_tokens: 300 # Final synthesis token limit
  n_depth: 1 # Iteration depth
  drift_k_followups: 2 # Number of follow-up questions
```

---

## 4. Summary Comparison

| Feature          | Global Search                    | Local Search                  | DRIFT Search                             |
| :--------------- | :------------------------------- | :---------------------------- | :--------------------------------------- |
| **Use Case**     | Broad, comprehensive analysis    | Direct, factual questions     | Investigative, complex questions         |
| **Output**       | List of themes & central players | Relevant text chunks & quotes | Synthesized narrative with connections   |
| **Performance**  | Slower (~4 min)                  | Fastest (~1 min)              | Fast, but depends on complexity (~1 min) |
| **Token Limits** | No practical limit               | Can encounter limits          | Can encounter limits                     |
| **Process**      | Map-Reduce                       | Single-pass                   | Iterative exploration                    |

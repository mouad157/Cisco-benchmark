# Cisco-benchmark

This repository contains the code deliverables for Cisco WP1 Use-Case #2:
“Systematic LLM benchmarking for organizational use”

The repository is organized into three main modules, each housed in its own directory:

## 📁 QA (Question Answering Benchmark)
The [QA module](https://github.com/mouad157/Cisco-benchmark/tree/main/QA) tests the performance of various LLMs (from different providers such as OpenAI/Anthropic) on MCQ datasets and saving the runs to MongoDB. It includes functionality to:

- Run standardized QA benchmarks

- Evaluate and log results

- Save benchmarking runs to MongoDB for reproducibility and analysis

➡️ See [QA/README.md](https://github.com/mouad157/Cisco-benchmark/blob/main/QA/README.md) for setup, supported providers, and data schema.

## 📁 QG (Question Generation)
The [QG module](https://github.com/mouad157/Cisco-benchmark/tree/main/QG) is responsible for generating multiple-choice questions using *Key Topics* and *Key Terms* of a given content.

➡️ See [QG/README.md](https://github.com/mouad157/Cisco-benchmark/blob/main/QG/README.md) for details on usage and configuration.

## 📁 TextChunker
The [TextChunker module](https://github.com/mouad157/Cisco-benchmark/tree/main/TextChunker) is an LLM-based text chunking tool to extract sections and metadata from the full text of large PDF documents (such as textbooks). It extracts and segments meaningful content sections along with associated metadata. This tool helps prepare large, unstructured documents for downstream NLP tasks.

➡️ See [TextChunker/README.md](https://github.com/mouad157/Cisco-benchmark/blob/main/TextChunker/README.md) for instructions and file format details.

Our web-based demo based on the above code can be accessed at https://nlp-demos.online/qg/

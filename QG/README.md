# 🧠 MCQ Generator

This project leverages OpenAI's API to generate multiple-choice questions (MCQs) from a given input file using configurable settings.

---

## 📦 Features

- Generate high-quality MCQs from textual content.
- Easy configuration of input/output paths and OpenAI API parameters.
- Clean and modular code structure for easy customization.

---

## 🛠️ Requirements

Before running the code, ensure all necessary libraries are installed. Use the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

All configurable parameters are located in the ```MCQConfig.py``` file. Before running the script, update the following variables:

```
# MCQconfig.py

# Path to your input file (e.g., a .txt or .csv file)
input_file_path = "path/to/your/input/file.txt"

# Path where the generated MCQs will be saved
output_file_path = "path/to/your/output/file.csv"

# Your OpenAI API key
api_key = "your_openai_api_key"

# Model to use (e.g., "gpt-4", "gpt-3.5-turbo")
model_name = "gpt-4"
```
## 🚀 How to Run

Once you've configured your settings, run the main script:

```
python ExtractMCQForContent.py
```

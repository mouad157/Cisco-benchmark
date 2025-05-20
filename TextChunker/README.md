# 📝 TextChunker

**TextChunker** is a lightweight utility for breaking large `.txt` or `.pdf` documents into manageable and meaningful chunks using configurable parameters. It supports metadata extraction and section identification powered by OpenAI models.


## 🚀 Features

- Chunk large text or PDF files intelligently
- Use OpenAI models to assist with metadata extraction
- Easy-to-edit config file for flexibility
- Outputs structured chunks into a target folder
- Outputs metadata file in ```.json``` format


## 🧱 Requirements

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration
Modify the config file named Config.py in the root of your project directory with the following structure:

```
## openai params
# openai model name for metadata extraction and section name look up
modelname = "gpt-4o-mini"
# openai API key
openai_key = "your-openai-key"

## I/O params
# input file path (.txt or .pdf)
inptxtfile = "./path/to/input.txt"
# output folder path
outdir = "./path/to/folder"

## section param
# typical average section length
avgseclen = 2048
```
🔐 Note: Keep your OpenAI API key secure

## 🏃 How to Run
Once your configuration file is ready, run the main script:
```
python SimplePDFChunker.py
```
The script will:

- Read the input file

- Extract relevant metadata

- Chunk the content based on the structure of the file (sections and subsections) and avgseclen

- Save the resulting chunks in the specified outdir

## 📁 Output
Output files will be saved in the folder specified in outdir.

## 🧠 Model Support
This tool uses OpenAI models (e.g., gpt-4o-mini) for:

- Section name lookup

- Metadata generation

Ensure your API key is valid and the model name is supported in your OpenAI account.

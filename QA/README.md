# Evaluator
## AI Model Evaluation for Question Answering

### 📌 Overview
This project evaluates the performance of different AI models (OpenAI GPT, Mistral, DeepSeek, and Anthropic) 
on question-answering tasks. It:
- Predicts question types using a fine-tuned T5-large model.
- Generates model answers for given questions.
- Compares generated answers with ground truth answers.
- Computes similarity scores to measure model accuracy.
- Saves results in a CSV file and optionally stores them in a MongoDB database.

### 🚀 Features
- Supports multiple AI models (OpenAI, Mistral, DeepSeek, and Anthropic).
- Fine-tuned T5-large model for question classification.
- Automatic evaluation with scoring metrics.
- MongoDB storage for result tracking.

### 🔧 Setup & Installation

#### 1️⃣ Clone the Repository
```sh
git clone https://github.com/mouad157/Evaluator.git
cd Evaluator
```
#### 2️⃣ Install Dependencies

Make sure you have Python 3 installed, then run:

```pip install -r requirements.txt```

### 🏃‍♂️ Usage
#### 1️⃣ Running Model Evaluation
To evaluate a model using a dataset, call the evaluate function:
```
from src.evaluator import evaluate

input_file = "data/questions.csv"  # Path to your CSV file
model_name = "gpt-4o"  # Change to your model
model_type = "openai"  # Change to your model type, options are ["openai","mistral","deepseek","anthropic"]
api_key = "your-api-key"  # Replace with your key
system_prompt = "Answer concisely." # Replace with the prompt you want to give to the model
output_file = "output.csv" # (optional) Replace with the name of the output_file make sure it's a csv file

df, avg_score = evaluate(input_file,model_type, model_name, api_key, system_prompt, output_file)

print(f"Model accuracy: {avg_score:.2f}%")
```

#### 2️⃣ Saving Results to MongoDB
```
from src.main import save_mongodb

mongo_client = "mongodb://localhost:27017"
database_name = "AI_Evaluation"
collection_name = "Results"

save_mongodb(df, mongo_client, database_name, collection_name)
print("Results saved to MongoDB!")
```

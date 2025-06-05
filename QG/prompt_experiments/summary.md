In the default setting for generating MCQs, we adopt an iterative process.
That is, for a given content, and each keyphrase/keytopic extracted for the content, a list of prompts are executed with each 
keyphrase/keytopic. This results in long runtimes during QG

Will asking the LLM to generate all of the questions together still yield equivalent results
in terms of quality of questions, and is this faster? We study this aspect with various GPT LLMs 
and summarize our findings below.

# Runtime Comparison Across Models and Settings

## Objective

This experiment compares the runtime performance of three different models—`gpt-4o-mini`, `gpt-4o`, and `o1`—under `fast` and `slow` settings while processing the same chapter: **"1_Introduction to TCP-IP Networking.txt"**.
"fast" refers to a unified prompt for generating the questions (all keyphrases/keytopics together), while "slow" refers to using a prompts iteratively to generate the questions. We use three main calls in both the fast and the slow version, the first is to generate the MCQ questions from KP, the second to generate the MCQ questions from KT and the last generate MCQ questions from topics while specifying the question type.
All runs used consistent settings:
- `nkps_section=5`
- `nqs_ktopic=3`
- `nqs_pfree=5`
- `ntypedqs_ktopic=1`
-  `inputfile = 1_Introduction to TCP-IP Networking.txt`

## Results

| Model        | Setting | Runtime (s) |
|--------------|---------|-------------|
| gpt-4o-mini  | fast    | 91.83       |
| gpt-4o-mini  | slow    | 236.50      |
| gpt-4o       | fast    | 123.85      |
| gpt-4o       | slow    | 269.71      |
| o1           | fast    | 163.85      |
| o1           | slow    | 811.91      |

## Key Observations

- **`gpt-4o-mini` (fast)** had the shortest runtime (91.83s), making it the most efficient configuration.
- **`o1 (slow)`** was the slowest, taking over **10x longer than `gpt-4o-mini (fast)`**.
- the fast version of gpt-4o-mini has a good question generation quality for the first two calls(as explained above), but the last call(generation of MCQ with KT and types) yields questions and options of a bad quality.
- the fast version of o1 has a good question generation quality over all the 3 calls.
- gpt-4o's fast version falls somewhere in between gpt-4o-mini and o1. the questions generated for the third call are better than those of gpt-4o-mini but still not with a satisfactory quality.
- We can use these unified calls that reduce significantly the question generation times while keeping the quality of generation quite high.

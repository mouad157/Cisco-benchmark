# Experiment Summary: Runtime Comparison Across Models and Settings

## Objective

This experiment compares the runtime performance of three different models—`gpt-4o-mini`, `gpt-4o`, and `o1`—under `fast` and `slow` settings while processing the same chapter: **"1_Introduction to TCP-IP Networking.txt"**.
fast refers to a unified prompt for generating the questions, while slow refers to using a prompts iteratively to generate the questions
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


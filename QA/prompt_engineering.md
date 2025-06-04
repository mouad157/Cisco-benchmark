# Prompt Performance Comparison

## Overview

This document summarizes the results of a comparative experiment between two prompts across three language model families: **Anthropic**, **Mistral**, and **OpenAI**. The evaluation was conducted on two datasets related to networking concepts:

- **IPv Addressing** (25 questions)  
- **IPv Routing** (31 questions)

The prompts are the following:

Prompt 1 ```
SYSPROMPT="You are Cisco CCNA specialist with in-depth knowledge"+\
    " of networking fundamentals, devices, and Cisco products. "
USRPROMPT="Answer the following multiple-choice question: %s. Return only a JSON tuple in the following format"+\
        "{\"answers\"=<JSON list of correct options, example [A, B]>,+\
        \"explanation\"=<justification for the selected answers>}" % question
```
Prompt 2 ```
sysprompt = 
"## answer the following question with the correct letter alone or the correct letters without any separator or explanation" \
     "### for example if the answer is A. TCP, B. IP address. Your answer would be: AB"
usrprompt = question
```

The main metric recorded is the number of failures:
- For prompt 1: the number of times the model failed to parse the question.
- For prompt 2: the number of times the output contained an explaination of the answer and not exclusively what was asked from the LLM.

---

## Results Summary

| Model     | Prompt        | IPv Addressing (25) | IPv Routing (31) |
|-----------|---------------|----------------------|-------------------|
| Anthropic | Prompt 1      | 5                    | 11                |
|           | Prompt 2      | 0                    | 10                |
| Mistral   | Prompt 1      | 5                    | 1                 |
|           | Prompt 2      | 0                    | 0                 |
| OpenAI    | Prompt 1      | 0                    | 0                 |
|           | Prompt 2      | 0                    | 0                 |

---

## Observations

- **Mistral** showed a significant improvement with prompt 2 (0 failures), compared to 6 total failures with prompt 1.
- **Anthropic** performed similarly overall, with a notable reduction in failures on the IPv Addressing dataset using prompt 1.
- **OpenAI** models were robust in both cases, with no failures observed across either prompt or dataset.
- prompt 1 achieved **equal or better performance across all models**, with improvements particularly visible in Mistral and Anthropic models.

---

## Conclusion

The results indicate that prompt 1 generally leads to more consistent and cleaner outputs, particularly with Mistral and Anthropic models. Further testing and analysis could help explore the causes of the remaining Anthropic inconsistencies and generalize these improvements across broader task sets.

These notes contain details of our experiments with various prompts used in QA.
Example MCQ files from CCNA are included.

# QA Performance Comparison

## Overview

This document summarizes the results of a comparative experiment between three prompts across three language model families: **Anthropic**, **Mistral**, and **OpenAI**. The evaluation was conducted on two datasets related to networking concepts:

- **IPv Addressing** (25 questions)  
- **IPv Routing** (31 questions)

The prompts are the following:

 - Prompt 1:
```
SYSPROMPT="You are Cisco CCNA specialist with in-depth knowledge"+\
    " of networking fundamentals, devices, and Cisco products. "
USRPROMPT="Answer the following multiple-choice question: %s. Return only a JSON tuple in the following format"+\
        "{\"answers\"=<JSON list of correct options, example [A, B]>,+\
        \"explanation\"=<justification for the selected answers>}" % question
```
 - Prompt 2:
```
sysprompt = 
"## answer the following question with the correct letter alone or the correct letters without any separator or explanation" \
     "### for example if the answer is A. TCP, B. IP address. Your answer would be: AB"
usrprompt = question
```
 - Prompt 3:
```
sysprompt = 
"You are a Cisco systems expert.\n## answer the following multiple-choice question with ONLY the correct letter(s) of the answer options without any separator or explanation.\n" \
         "### For example, if the correct answers are A and B from the options list A. TCP, B. IP address, C. UDP, D. None of the above. Your answer would be: AB"
usrprompt = question
```

The main metric recorded is the number of failures:
- For prompt 1: the number of times the model failed to parse the question.
- For prompt 2 and 3: the number of times the output contained an explaination of the answer and not exclusively what was asked from the LLM.

for example, this would be a failed output of prompt 2:
```
Looking at this problem, I need to analyze subnetting for network 172.30.0.0 with a /22 mask.

First, let me understand what a /22 mask means:
- /22 = 255.255.252.0
- This uses 22 bits for the network portion
- Since 172.30.0.0 is a Class B network (/16), we're using 6 additional bits for subnetting (22-16=6)
- This gives us 2^6 = 64 subnets

For the subnet increments:
- With a /22 mask, each subnet contains 2^(32-22) = 2^10 = 1024 addresses
- 1024 addresses = 4 blocks of 256
- This means subnets increment by 4 in the third octet

The subnet IDs would be:
- 172.30.0.0
- 172.30.4.0
- 172.30.8.0
- ...continuing...
- 172.30.252.0

Let me verify each option:
- A: "differ by 22 in third octet" - FALSE (they differ by 4)
- B: "differ by 16 in fourth octet" - FALSE (fourth octet stays 0)
- C: "contains 64 subnet IDs" - TRUE (2^6 = 64)
- D: "last subnet is 172.30.252.0" - TRUE (0 + 4×63 = 252)

CD
```

---

## Results Summary

The table below shows the number of "fails" with each prompt (where a fail is registered when the LLM response is not 
in the expected format=> lower the better)

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

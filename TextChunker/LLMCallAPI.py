#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:32:00 2025

@author: sdas
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 15:41:48 2024

@author: sdas
"""



import openai
from Config import openai_key, modelname




GPT_API_KEY = openai_key
CHATGPT_MODEL = modelname
openai.api_key=GPT_API_KEY

def getChatGPTResponse(userprompt, sysprompt="",temperature=0.7):
    
    if sysprompt!="":
        completion = openai.OpenAI(api_key=GPT_API_KEY).chat.completions.create(
        model = CHATGPT_MODEL,

            messages = [ # Change the prompt parameter to the messages parameter
                    {'role': 'system', 'content': sysprompt},
                    {'role': 'user', 'content': userprompt},
                ],
                temperature = temperature
        )
    else:
         completion = openai.OpenAI(api_key=GPT_API_KEY).chat.completions.create(
         model = CHATGPT_MODEL,

             messages = [ # Change the prompt parameter to the messages parameter
                     {'role': 'user', 'content': userprompt},
                 ],
                 temperature = temperature
         )

    return completion.choices[0].message.content


    
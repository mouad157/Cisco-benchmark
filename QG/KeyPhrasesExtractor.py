#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:18:50 2025

@author: sdas
"""


import LLMCallAPI as llm
import ast

SYS_PROMPT="You are a Cisco technical support engineer with in-depth"+ \
     " knowledge of CCNA certification materials and are expert in"+\
        " identifying important concepts related to Cisco domain"

USR_PROMPT="For the given passage extract the top-%s relevant conceptual keyphrases."+\
    " Only return your output as a Python list of strings. output=['', ''...]\n"+\
        "Passage: \n%s"

USR_PROMPT2="Group the given sets of conceptual keyphrases, and select "+\
    "the top-%s most important conceptual keyphrases, given the topic: %s"+\
    " Only return your output as a Python list of strings. output=['', ''...]\n"+\
        "List of keyphrases\n%s"

def parseList(text):
    
    try:
        
        if "[" and "]" in text:
            text = text.split("[")[1].split("]")[0]
            text ="["+text+"]"
        else:
            return None
        kpl = ast.literal_eval(text.replace("output=","").strip())
        return kpl
    except SyntaxError:
        return None
        

def extractKeyPhrases(passage, nkps=10):

    gptop = llm.getLLMResponse(USR_PROMPT%(str(nkps), passage), SYS_PROMPT)
    kpl = parseList(gptop)
    return kpl


def extractKeyPhrasesForPassageSetOnTopic(plist, topic, nkps=10):
    
    secls=[]
    for passage in plist:
        kpl = extractKeyPhrases(passage)
        if kpl is not None:
            secls.append(kpl)
            
    seckpslist=""
    for secl in secls:
       seckpslist += '\n'.join(secl)
       seckpslist += '\n'

    gptop = llm.getLLMResponse(USR_PROMPT2%(topic, seckpslist), SYS_PROMPT)
    kpl = parseList(gptop)

    return kpl

    
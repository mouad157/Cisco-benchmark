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
        " identifying key topics in the content involving the principles, algorithms, methods, and "+\
            " techniques related to Cisco domain. For example, some key topics can be described as: "+\
                "\'Commands to find access ports and assigned VLANs\'"+\
                    "\'Reasons for using VLANs\' and "+\
"\'Key facts about Class A, B, and C networks\'"

USR_PROMPT="For the given passage extract upto top-5 key topics."+\
    " Only return your output as a Python list of strings. output=['', ''...]\n"+\
        "Passage: \n%s"

USR_PROMPT2="Group the given sets of key topics, and select "+\
    "the top-%s most important key topics, for the chapter titled: %s"+\
    " Only return your output as a Python list of strings. output=['', ''...]\n"+\
        "List of key topics\n%s"

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
        
def extractKeyTopics(passage, nkts=5):
    
    gptop = llm.getLLMResponse(USR_PROMPT%(passage), SYS_PROMPT)
    
    kpl = parseList(gptop)
    
    return kpl


def extractKeyTopicsForPassageSetOnTopic(plist, aggtopic, nkts=10):
    
    secls=[]
    for passage in plist:
        kpl = extractKeyTopics(passage)
        if kpl is not None:
            secls.append(kpl)
            
    seckpslist=""
    for secl in secls:
       seckpslist += '\n'.join(secl)
       seckpslist += '\n'

    gptop = llm.getLLMResponse(USR_PROMPT2%(str(nkts), aggtopic, seckpslist), SYS_PROMPT)
    kpl = parseList(gptop)

    return kpl

        
    
    
    
    

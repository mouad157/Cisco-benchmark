#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 11:19:04 2025

@author: sdas
"""



import json
import ast


def parsePythonList(opstring):
    
    opstring = opstring.replace("```python","").replace("```","")
    
    if len(opstring)>20 and "=" in opstring[0:20]:
        opstring=opstring.split("=")[-1]
    try:
        ql = ast.literal_eval(opstring)
        return ql
    except SyntaxError:
        return None


def parseDict(dobj):
    if type(dobj) is dict:
        if "answers" in dobj and "options" in dobj and "question" in dobj:
            return dobj["answers"], dobj["options"], dobj["question"]
        
    return None, None, None  


def parseJSON(opstring):
    
    opstring = opstring.replace("```json","").replace("```","")
    try:
        pl = json.loads(opstring)
        return pl
        
    except ValueError:
        print ("Error parsing JSON from\n"+opstring)
        return None
    
        
    

################

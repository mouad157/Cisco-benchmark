#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:58:21 2025

@author: sdas
"""




from QTypeDefs import qtypes
from LLMCallAPI import getLLMResponse
import LLMOPParser as parser

    
SYS_PROMPT="You are a Cisco technical support engineer with in-depth"+ \
    " knowledge of CCNA certification materials."
        
MCQPFX="Generate exactly one multiple-choice questions based on the content provided."+ \
    " Return your response as a JSON-tuple={\"question\":<the question without the choices>,"+\
  "  \"options\":<JSON list of multiple-choice options, A. B. ...>,"+\
  "\"answers\":<JSON list the correct answers to the question>}"

MCQPROMPTS=[
    MCQPFX+" Use the keyphrase %s.\nContent:\n%s",
    MCQPFX+" The keyphrase %s must be a answer to the question.\nContent:\n%s",
    MCQPFX+" The keyphrase %s must be one of the options for the multiple-choice question.\nContent:\n%s",
    ]

KPF_MCQPROMPT="Generate exactly %s multiple-choice questions based on the content provided."+ \
    " Return your response as a Python list of JSON-tuples. Each JSON tuple is {\"question\":<the question without the choices>,"+\
  "  \"options\":<JSON list of multiple-choice options, A. B. ...>,"+\
  "\"answers\":<JSON list the correct answers to the question>}. \nContent:\n%s"

KT_MCQPROMPT="Generate exactly %s multiple-choice questions"+\
    " based on the content provided for the topic: %s."+ \
    " Return your response as a Python list of JSON-tuples. Each JSON tuple is {\"question\":<the question without the choices>,"+\
  "  \"options\":<JSON list of multiple-choice options, A. B. ...>,"+\
  "\"answers\":<JSON list the correct answers to the question>}. \nContent:\n%s"



qtypedefs_prompt=""
for qt in qtypes:
    (defn, eg) = qtypes[qt]
    qtypedefs_prompt+="\nA question of type \""+qt+"\" is defined as "+defn+"\nFor e.g. "+eg    

QTYPE_SYSPROMPT=SYS_PROMPT+" Consider the following question types"+ \
    "and their definitions "+qtypedefs_prompt
    


KT_TYPEDMCQPROMPT="Generate exactly %s multiple-choice questions of "+\
    " of question type %s based on the content provided for the topic: %s."+ \
    " Return your response as a Python list of JSON-tuples. Each JSON tuple is {\"question\":<the question without the choices>,"+\
  "  \"options\":<JSON list of multiple-choice options, A. B. ...>,"+\
  "\"answers\":<JSON list the correct answers to the question>}. \nContent:\n%s"

  
################


def generateMCQs(fcontent, nmax=5):
    
    csvrows=[]
    
    USRPROMPT= KPF_MCQPROMPT % (str(nmax), fcontent)
    response = getLLMResponse(USRPROMPT, SYS_PROMPT)
    
    print (response)
    ql = parser.parsePythonList(response)
    
    if ql is not None and type(ql) is list:
    
        for mcq in ql:
           
            a, o, q = parser.parseDict(mcq)
            
            if a is not None:
                csvrows.append(["KPF", "NOKP", a, o, q])
            else:
                print ("\nERROR generating or parsing for:\n"+str(mcq))
                continue
    else:
        print ("\nERROR generating or parsing in generateMCQs")
        print ("GPT response\n"+response)
        
    return csvrows



def generateMCQsForKPs(kplist, fcontent):
    
    csvrows=[]
    
     
    for kp in kplist:
        print ("Generating for kp="+kp)
        for mx, mcqp in enumerate(MCQPROMPTS):
            USRPROMPT=mcqp % (kp, fcontent)
            response = getLLMResponse(USRPROMPT, SYS_PROMPT)
            a, o, q = parser.parseJSON(response)
            if a is not None:
                csvrows.append(["MCQP-"+str(mx+1), kp, a, o, q])
            else:
                print ("\nERROR generating or parsing in generateMCQsForKPs for: "+kp)
                print ("GPT response\n"+response)
    
    return csvrows

def generateMCQsForKeyTopics(ktlist, fcontent, nmax=3):
    
    csvrows=[]
    for ktopic in ktlist:
        USRPROMPT= KT_MCQPROMPT % (str(nmax), ktopic, fcontent)
        response = getLLMResponse(USRPROMPT, SYS_PROMPT)
        print ("Generating for key topic="+ktopic)
        #print (response)
        ql = parser.parsePythonList(response)
        
        if ql is not None and type(ql) is list:
        
            for mcq in ql:
               
                a, o, q = parser.parseDict(mcq)
                
                if a is not None:
                    csvrows.append(["KT_MCQP", ktopic, a, o, q])
                else:
                    print ("\nERROR generating or parsing for:\n"+str(mcq))
                    continue
        else:
            print ("\nERROR generating or parsing in generateMCQsForKeyTopics")
            print ("GPT response\n"+response)
        
    return csvrows
     


def generateTypeMCQsForKeyTopics(ktlist, fcontent, nmax=2):
    
    csvrows=[]
    for ktopic in ktlist:
        print ("Generating typed questions for key topic="+ktopic)
        for qt in qtypes:
            USRPROMPT= KT_TYPEDMCQPROMPT % (str(nmax), qt, ktopic, fcontent)
            response = getLLMResponse(USRPROMPT, QTYPE_SYSPROMPT)
            print ("Question Type="+qt)
            #print (response)
            ql = parser.parsePythonList(response)
            
            if ql is not None and type(ql) is list:
            
                for mcq in ql:
                   
                    a, o, q = parser.parseDict(mcq)
                    
                    if a is not None:
                        csvrows.append(["KT_TYPEMCQP_"+qt, ktopic, a, o, q])
                    else:
                        print ("\nERROR generating or parsing for:\n"+str(mcq))
                        continue
            else:
                print ("\nERROR generating or parsing in generateTypeMCQsForKeyTopics")
                print ("GPT response\n"+response)
        
    return csvrows

   

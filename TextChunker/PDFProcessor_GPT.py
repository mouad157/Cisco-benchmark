#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:58:10 2025

@author: sdas
"""


import LLMCallAPI as llm
import LLMOPParser as parser



SYS_PROMPT="You are an efficient PDF parser. "+\
    "From the initial content  of the PDF provided, extract the metadata requested for."
    

PDFTYPES=['book', 'research paper', 'product guide',\
          'technical specification', 'configuration matrix',\
        'presentation slides', 'book chapter', \
            'FAQ document', 'none of the above']
    
PTYPE_PROMPT="Based on the initial content from a PDF, what is the "\
        "most likely type of the document from "+str(PDFTYPES) +\
    " the following list: ? Return only your answer (one of the"+\
            " elements from the list above) in a separate line. Content:\n%s"

SEC_PROMPT="Does the initial content from a PDF include a listing of topics in"+\
    " in the document? If yes, return a Python list of strings, each string "+\
        " being topic title. Else, return an empty list. Content:\n%s"


META_PROMPT="Based on the initial content from a PDF document, extract any "+\
    "relevant metadata. Example metadata includes, title of the document, "+\
    " list of authors, product name and software version information for a "+\
    "technical specification, etc. Return the metadata as a JSON tuple:"+\
        " {\"<field-name>\":<field-value>, ...} For example, for a book, "+\
            "{\"title\":<>, \"authors\":[]}\nContent:\n%s"



def getSectionNames(first_sec):

    sections = []
    response = llm.getChatGPTResponse(SEC_PROMPT%first_sec, SYS_PROMPT)
    pl = parser.parsePythonList(response)
    if pl is not None:
        sections = pl
        
    return sections

def getMetadataAndType(first_sec):
    
    (ptype, metadata) = ("", {})
    response = llm.getChatGPTResponse(PTYPE_PROMPT%first_sec, SYS_PROMPT)
    if response is not None and response.strip()!="":
        ptype = response.strip()
    
        
    response = llm.getChatGPTResponse(META_PROMPT%first_sec, SYS_PROMPT)
    pd = parser.parseJSON(response)
    if pd is not None:
        metadata = pd
        
    return ptype, metadata


            
    
    
            
    
    
    
    
    
    





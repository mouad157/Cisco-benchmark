#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:54:24 2025

@author: sdas
"""


modelname="gpt-4o-mini"


inptxtfile="./texts/9_Spanning Tree Protocol Concepts.txt"
outcsvfile="./output/test.csv"
openai_key = "your_openai_api_key"

##Number of keyphrases to extract for a given section
##For each keyphrase, we apply three prompts to generate 
##three (hopefully) different questions: See MCQGenerator

nkps_section=5  

##Number of questions to generate for a given keytopic
nqs_ktopic=3  
##Number of questions of a specific type: 
##See QTypeDefs to generate for a given keytopic
ntypedqs_ktopic=1  

##Number of questions to generate for a given section
##Without specific keyphrase/keytopic prompting
nqs_pfree=5


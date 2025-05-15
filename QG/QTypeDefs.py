#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:27:54 2024

@author: sdas
"""
#https://ieeexplore-ieee-org.libproxy1.nus.edu.sg/document/5593591

qtypes={
       
"Verification": ("For yes/no responses to factual questions", 
                 "Are headaches associated with high blood pressure?"),
"Disjunctive":	("Questions that require a simple decision between two alternatives.",
                "Is it all the toes? Or just the great toe?"),
"Feature specification": ("Determines qualitative attributes of an object or situation.",
                          "	Could we get a general appearance and vital signs?"),
"Quantification":("Determines quantitative attributes of an object or situation.",
                  "How many lymphocytes does she have?"),
"Definition":("Determine meaning of a concept.","What do you guys know about pernicious anaemia as a disease?"),
"Example":("Request for instance of a particular concept or even type.",
           "When have we seen this kind of patient before?"),
"Comparison":("Identify similarities and differences between two or more objects.",
              "Are there any more proximal lesions that could cause this? I mean I know it's bilateral."),
"Interpretation":("A description of what can be inferred from a pattern of data",
                  "You guys want to tell me what you saw in the peripheral smear?"),
"Causal antecedent":("Asks for an explanation of what state or event causally led to the current state and why.",
                     "What do you guys know about compression leading to numbness and tingling? How that happens?"),
"Causal consequence":("Asks for explanation of consequences of event/state",
                      "What happens when it's, when the, when the neuron's demyelinated?"),
#"Expectational":("Asks about expectations or predictions (including violation of expectation)",
#                 "How much, how much better is her, are her neural signs expected to get?"),
#"Judgmental":("Asks about value placed on an idea, advice, or plan.",
#              "Should we put her to that trouble, do you feel, on the basis of what your thinking is?"),
        }

def getPrompt():
    temp=[]
    for key in qtypes:
        (defn, eg) = qtypes[key]
        temp.append(""+key+"\n"+defn+"\nAn example for this type is -- "+eg+"\n")
        
    prompt = "Given the types of questions defined with examples as follows \n"+'\n'.join(temp)+\
        "\n\nSelect the most suitable question type for the following question?"
        
    return prompt

def getPromptMCQ():

    prompt ="Which of the following categories is most suitable for the question from \""+str(list(qtypes.keys()))+"\"? Question: "

    return prompt


#print (getPromptMCQ())

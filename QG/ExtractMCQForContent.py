#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 11:02:54 2025

@author: sdas
"""

import csv
 

import MCQConfig as config
from KeyPhrasesExtractor import extractKeyPhrases
from KeyTopicsExtractor import extractKeyTopics
from MCQGenerator import generateMCQs, generateMCQsForKPs
from MCQGenerator import generateMCQsForKeyTopics
from MCQGenerator import generateTypeMCQsForKeyTopics

def loadFileContent(inpfile):
    
    fin = open (inpfile, "r",encoding= "utf-8")
    
    passage ='\n'.join(fin.readlines())
    
    return passage



def run2(section_text, out_csvname,kplist,ktlist):    
    
    #section_text = inp_fname.read().decode("utf-8")
    print ("#words in chapter="+str(len(section_text.split())))
    
    #######
    
    
    csvrows = generateMCQs(section_text, config.nqs_pfree)
    print ()
    print ("#questions (from simple prompt) ="+str(len(csvrows)))
    
    #######
    
    #kplist = extractKeyPhrases(section_text, config.nkps_section)
    
    csvrows2=[]
    if kplist is not None:
        print ("Extracted keyphrases:\n"+str('\n'.join(kplist)))
        csvrows2 = generateMCQsForKPs(kplist, section_text)
    
    print ()
    print ("#questions (from keyphrase prompts)="+str(len(csvrows2)))
    csvrows.extend(csvrows2)
    #######
    
    # ktlist = extractKeyTopics(section_text)
    
    csvrows3=[]
    if ktlist is not None:
        print ("Extracted keytopics:\n"+str('\n'.join(ktlist)))
        csvrows3 = generateMCQsForKeyTopics(ktlist, section_text, config.nqs_ktopic)
        csvrows4 = generateTypeMCQsForKeyTopics(ktlist, section_text, config.ntypedqs_ktopic)
    
    print ()
    print ("#questions="+str(len(csvrows3)))
    print ()
    print ("#Typed questions="+str(len(csvrows4)))
    
    csvrows.extend(csvrows3)
    csvrows.extend(csvrows4)
    
    ###########
    
    
    
    if len(csvrows)>0:
        fout = open (out_csvname, "w",newline="")
        csvw = csv.writer(fout, delimiter=",", quoting=csv.QUOTE_ALL)
        csvw.writerow(["PROMPT","Keyphrase/KeyTopic","Answers","Options","Question"])
        listq=[]
        
        for nrx, csvrow in enumerate(csvrows):
            
            if nrx%5==0:
                print ("Example Question\n"+str(csvrow))
                
            #print("++++++",csvrow,"++++++")
            csvw.writerow(csvrow)
            listq.append(csvrow[-1])
        fout.flush()
        
            
        fout.close()
        print ("-------------")
        print ("CSV Output written to "+out_csvname)
        print ("Total questions written="+str(len(listq)))
        print ("-------------")
        print ('\n-'.join(listq))
        
        
    return 

def run(inp_fname, out_csvname):    
    
    section_text = loadFileContent(inp_fname)
    print ("#words in chapter="+str(len(section_text.split())))
    
    #######
    
    
    csvrows = generateMCQs(section_text, config.nqs_pfree)
    print ()
    print ("#questions (from simple prompt) ="+str(len(csvrows)))
    
    #######
    
    kplist = extractKeyPhrases(section_text, config.nkps_section)
    
    csvrows2=[]
    if kplist is not None:
        print ("Extracted keyphrases:\n"+str('\n'.join(kplist)))
        csvrows2 = generateMCQsForKPs(kplist, section_text)
    
    print ()
    print ("#questions (from keyphrase prompts)="+str(len(csvrows2)))
    csvrows.extend(csvrows2)
    #######
    
    ktlist = extractKeyTopics(section_text)
    
    csvrows3=[]
    if ktlist is not None:
        print ("Extracted keytopics:\n"+str('\n'.join(ktlist)))
        csvrows3 = generateMCQsForKeyTopics(ktlist, section_text, config.nqs_ktopic)
        csvrows4 = generateTypeMCQsForKeyTopics(ktlist, section_text, config.ntypedqs_ktopic)
    
    print ()
    print ("#questions="+str(len(csvrows3)))
    print ()
    print ("#Typed questions="+str(len(csvrows4)))
    
    csvrows.extend(csvrows3)
    csvrows.extend(csvrows4)
    
    ###########
    
    
    
    if len(csvrows)>0:
        fout = open (out_csvname, "w",newline="")
        csvw = csv.writer(fout, delimiter=",", quoting=csv.QUOTE_ALL)
        csvw.writerow(["PROMPT","Keyphrase/KeyTopic","Answers","Options","Question"])
        listq=[]
        
        for nrx, csvrow in enumerate(csvrows):
            
            if nrx%5==0:
                print ("Example Question\n"+str(csvrow))
                
            #print("++++++",csvrow,"++++++")
            csvw.writerow(csvrow)
            listq.append(csvrow[-1])
        fout.flush()
        
            
        fout.close()
        print ("-------------")
        print ("CSV Output written to "+out_csvname)
        print ("Total questions written="+str(len(listq)))
        print ("-------------")
        print ('\n-'.join(listq))
        
        
    return 

if __name__=="__main__":
    
    run (config.inptxtfile, config.outcsvfile)
    

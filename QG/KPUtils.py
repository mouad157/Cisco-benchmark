#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:27:13 2025

@author: sdas
"""

import csv
import ast
import sys
import random

import numpy as np

from nltk.stem.porter import *
stemmer = PorterStemmer()


#Variable threshold based on keyphrase length
def getOvlpThreshold(gwds):
    
    nwords = len(gwds)
    
    if nwords <= 2:
        return 1
    elif nwords==3:
        return 2/3
    elif nwords==4:
        return 3/4
    else:
        return 0.6
        


    
  
def matchKP(goldkp, preds_list):
    
    
    gwds_o = goldkp.lower().split()
    gwds = [stemmer.stem(i) for i in gwds_o]
    
    maxovlp=0
    match=""
    for pkp in preds_list:
        pwds = pkp.lower().split()
        ol = 0
        for word in pwds:
            if stemmer.stem(word) in gwds:
                ol+=1
                
        if (ol/(len(gwds)+len(pwds)-ol)) > maxovlp:
            maxovlp = ol/(len(gwds)+len(pwds)-ol)
            match = pkp
    
   # print ("maxovlp is "+str(maxovlp)+" for "+goldkp+" and match="+match)
    if maxovlp >= getOvlpThreshold(gwds):
        return match
    else:
        return None
  
    
def loadGoldKPs(goldcsv):
    kplist={}
    
    fin = open (goldcsv, "r")
    header=[]
    csvr = csv.reader(fin, delimiter=",")
    for row in csvr:
        if len(header)==0:
            header=row
            continue
        
        kp = row[header.index("keyword")]
        chap = str(row[header.index("chapter")])
        if chap not in kplist:
            kplist[chap]=[]
        kplist[chap].append(kp)
        
    return kplist


if __name__=="__main__":
    
    if len(sys.argv)!=3:
        print ("Expecting the following csv files\nargs1: gold.csv (has header columns keyword, chapter)")
        print ("args2: preds.csv (has header columns FinalKPs, ChapID)")
        sys.exit(1)
    
    ######load gold keyphrases
    kplist=loadGoldKPs(sys.argv[1])
    print ("#goldkps="+str(len(kplist)))
    if len(kplist)>0:
        keyl = list(kplist.keys())
        ch = random.randint(0, len(keyl)-1)
        key = keyl[ch]
        print ("keyphrases for key="+str(key)+"\n"+str(kplist[key]))
    
    ######load predicted keyphrases
    inpfile=sys.argv[2]
    fin = open (inpfile, "r")
    csvr = csv.reader(fin, delimiter=",")
    header=[]
    preds={}
    for row in csvr:
        if len(header)==0:
            header = row
            continue
    
        chap = row[header.index("ChapID")].strip()
        kpl = row[header.index("FinalKPs")]
        kpl = ast.literal_eval(kpl)
        preds[chap] =kpl
        
    
    print ("#preds "+str(len(preds)))
    print (preds.keys())
    #print (kplist.keys())
    prkpo_counts={}
    
    for chap in preds:
        
        prkpo_counts[chap]={}
        prkpl = preds[chap]
        
        if chap not in kplist:
            continue
        
        kpl = kplist[chap]
        
        # print (chap)
        # print (kpl)
        # print (prkpl)
        
        for kp in kpl:
            
            match = matchKP(kp, prkpl)
            if match is None:
                continue
            else:
                prkpo_counts[chap][kp.lower()]=match
                print ("\nDEBUG , match="+match +" for "+kp.lower())
                    
                    
                
            
    qol=[]
       
    for chap in kplist:
        print ("======")
        print (chap)
        print ("Gold KPs\n"+str(kplist[chap]))
        print ("\nGPT KPs\n"+str(preds[chap]))
        
        if chap in prkpo_counts:
            print ("\nOverlapping KPs\n"+str(prkpo_counts[chap]))
            
        #print ("#kpl="+str(len(kplist[chap])))
        if chap in prkpo_counts:
            qmap = prkpo_counts[chap]
            print ("#prmatches="+str(len(qmap))+"\tpct=%0.3f"%(len(qmap)/len(kplist[chap])))    
            
            qol.append(len(qmap)/len(kplist[chap]))
        
        
    print ("-------------------------------------")
    print ("Overlaps mean/max/std=%0.3f\t%0.3f\t%0.3f"%(np.mean(qol), np.max(qol), np.std(qol)))    
        
        
        
    

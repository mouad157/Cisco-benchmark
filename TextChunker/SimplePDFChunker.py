#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:40:18 2025

@author: sdas
"""

import os
import PDFProcessor_GPT as pdfprocessor
import regex as re
import json
from util import wizard_chunker, pdf_to_text
from Config import avgseclen, inptxtfile,outdir

AVGSECLEN=avgseclen #words or rather whitespace-separated tokens

def getInitialPagesFromContent(content):
    
    words = content.strip().split()
    mlen = min(len(words), AVGSECLEN)
    first_sec = ' '.join(words[0:mlen])
    
    return first_sec

def extractSections(ordered_sectitles, content):
    
    #find the first mention of the last secname 
    #Assumptions: (1) there is a listing of section names or ToC, so the 
    #actual content starts after the ToC (table of contents)
    #(2) Section names appear in the order listed in ToC
    try:
        toc=""
        APAT = re.compile(r"%s"%ordered_sectitles[-1])
        m = re.search(APAT, content)
        if m is not None:
            toc = content[0:m.end()]
            content = content[m.end():]
    except:
        print ("Error while compiling regular expression ")
        
    print ("DEBUG TOC "+toc)
    parts=[]
    if toc!="":
        parts.append(("begg", toc))
        
    for sx in range(1, len(ordered_sectitles)):
        
        nextsecname = ordered_sectitles[sx]
        try:
            APAT = re.compile("%s"%nextsecname)
            m = re.search(APAT, content)
            if m is not None:
                section = content[0:m.start()]
                content = content[m.start():]
                parts.append(("Sec-"+str(sx), section))
                print ("Match for "+nextsecname)
        except:
            print ("Error while compiling regular expression ")
            continue
            
    if content.strip()!="":
        parts.append(("endg", content))
    print ("#parts "+str(len(parts)))
        
        
    return parts

def checkTooSmall(sections):    
    cnt_small = 0
    
    for sect in sections:
        (_, sec) = sect
        ntok = (len(sec.split()))
        #Section Length is smaller than 5% of average section length
        if ntok < 0.05*AVGSECLEN:
            cnt_small += 1
    
    print ("DEBUG #small sections="+str(cnt_small))
    print ("DEBUG #sections="+str(len(sections)))
    #More than fifty percent are too small
    if (cnt_small/len(sections)) > 0.5:
        return True
    
    return False

def tooBig(section):    
    
    ntok = len(section.split())
    #Section Length is more than twice the average section length
    #Check if can be broken further
    
    if ntok > 2*AVGSECLEN:
        return True
        
    return False

def writeToFile(content, fpath):
    print ("Writing "+fpath)
    fout = open (fpath, "w", encoding="utf-8")
    fout.write(content)
    fout.flush()
    fout.close()

#This is a recursive function for splitting content into sections.
#We make use of ToC/contents listing extraction via LLM
#as well thresholds on average section lengths to decide if a given
#section needs further splitting

def breakSections(first_fewp, content, outfpath_pfx, logfout):
    logfout.flush()
    if first_fewp=="":
        first_fewp = getInitialPagesFromContent(content)
        
    secnames = pdfprocessor.getSectionNames(first_fewp)
    
    logfout.write ("\nDEBUG Extracted Secnames\n"+str(secnames)+"\n")
    sections = []
    if len(secnames)>0:
        sections = extractSections(secnames, content)
        if len(sections)==0 or checkTooSmall(sections):
            #Call Mouad's breaker 
            sections = wizard_chunker(content)
            ##For now just dump the content
            logfout.write("\nSections too small or not found, writing to "+outfpath_pfx)
            for sx, sect in enumerate(sections):
                print ("DEBUG writing sec-"+str(sx))
                logfout.write("\nWriting Section "+str(sx)+ " to "+outfpath_pfx+"."+str(sx))
                writeToFile(sect, outfpath_pfx+"."+str(sx)+".txt")
            ##For now just dump the content
            # writeToFile(content, outfpath_pfx+".txt")    
            # logfout.write("\nSections too small or not found, \
            #         writing all content to "+outfpath_pfx)
        else:       
            print(len(sections))
            logfout.write("\nNumber of sections discovered is:"+str(len(sections)))
            for sx, sect in enumerate(sections):
                (secname, sectxt) = sect
                print ("DEBUG in loop for sec-"+str(sx))
                if tooBig(sectxt):
                    logfout.write("\nSection "+str(sx)+"\t"+secname+" too big breaking")
                    logfout.write ("\n===============")
                    breakSections("", sectxt, outfpath_pfx+"."+str(sx), logfout)
                else:
                    print ("DEBUG writing sec-"+str(sx))
                    logfout.write("\nWriting Section "+str(sx)+"\t"+secname+" to "+outfpath_pfx+"."+str(sx))
                    writeToFile (sectxt, outfpath_pfx+"."+str(sx)+".txt")
    else:
        #Call Mouad's breaker 
        sections = wizard_chunker(content)
        ##For now just dump the content
        logfout.write("\nSections not found, writing to "+outfpath_pfx)
        for sx, sect in enumerate(sections):
            print ("DEBUG writing sec-"+str(sx))
            logfout.write("\nWriting Section "+str(sx)+ " to "+outfpath_pfx+"."+str(sx))
            writeToFile(sect, outfpath_pfx+"."+str(sx)+".txt")
        # writeToFile(content, outfpath_pfx+".txt")            


def new_chunker(inpfile,outdir):
    logfile=outdir+"/test2.log.txt"
    logfout = open (logfile, "w")
    if inpfile.endswith(".pdf"):
        nw_inpfile = inpfile.split('/')[-1]
        outfpfx = outdir+"/"+nw_inpfile.replace(" ","_").replace(".pdf","").strip()
        outfpfx2 = outdir+"/"+nw_inpfile.replace(" ","_").replace(".pdf","_md.json").strip()
        content, _ = pdf_to_text(inpfile)
        first_fewp = getInitialPagesFromContent(content)
        (ptype, metadata) = pdfprocessor.getMetadataAndType(first_fewp)

        
        print ()
        print (inpfile)
        print (ptype)
        print (metadata)
        print ()
        jobj = {"filename":inpfile, "PDF_type":ptype, "Metadata":metadata}
        jobj_asstr = json.dumps(jobj, indent=4)
        with open(outfpfx2, "w") as jfout:
            jfout.write(jobj_asstr)
            jfout.close()
        
        logfout.write("\nProcessing "+inpfile)
        logfout.write("\nType "+str(ptype))
        logfout.write("\nMetadata "+str(metadata))
        logfout.flush()
        if "sections" in metadata.keys():
            if tooBig(content) or len(metadata["sections"])>0:
                breakSections(first_fewp, content, outfpfx, logfout)
            else:
                ##For now just dump the content
                writeToFile(content, outfpfx+".txt")        
        else:
            if tooBig(content):
                breakSections(first_fewp, content, outfpfx, logfout)
            else:
                ##For now just dump the content
                writeToFile(content, outfpfx+".txt")             
            
        logfout.flush()
            
    if inpfile.endswith(".txt"): # and fn.startswith("part"):
        nw_inpfile = inpfile.split('/')[-1]
        outfpfx = outdir+"/"+nw_inpfile.replace(" ","_").replace(".txt","").strip()
        outfpfx2 = outdir+"/"+nw_inpfile.replace(" ","_").replace(".txt","_md.json").strip()
        
        content = ' '.join(open (inpfile, "r", encoding="utf-8").readlines())
        first_fewp = getInitialPagesFromContent(content)
        (ptype, metadata) = pdfprocessor.getMetadataAndType(first_fewp)
        
        print ()
        print (inpfile)
        print (ptype)
        print (metadata)
        print ()
        jobj = {"filename":inpfile, "PDF_type":ptype, "Metadata":metadata}
        jobj_asstr = json.dumps(jobj, indent=4)
        with open(outfpfx2, "w") as jfout:
            jfout.write(jobj_asstr)
            jfout.close()

        logfout.write("\nProcessing "+inpfile)
        logfout.write("\nType "+str(ptype))
        logfout.write("\nMetadata "+str(metadata))

        logfout.flush()
        if "sections" in metadata.keys():
            if tooBig(content) or len(metadata["sections"])>0:
                breakSections(first_fewp, content, outfpfx, logfout)
            else:
                ##For now just dump the content
                writeToFile(content, outfpfx+".txt")        
        else:
            if tooBig(content):
                breakSections(first_fewp, content, outfpfx, logfout)
            else:
                ##For now just dump the content
                writeToFile(content, outfpfx+".txt")
            
        logfout.flush()
            
    logfout.close()
                   
if __name__=="__main__":
    new_chunker(inptxtfile,outdir)

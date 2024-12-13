import sys
import sqlite3
import numpy as np
import copy
from func.identifier import *
from func.daughter import *
from func.preprocess import *
from func.process import *

#DB Creation
# con = sqlite3.connect('./test.db')
con = sqlite3.connect('./nndc-20241101.db')
cur = con.cursor()

#DB Table Creation
cur.execute('''create table decay(
    daughter text, dmass real, disotope text,
    mother text, mmass real, misotope text, mlevel text, mspin text,
    mdecay text, mlife real, mlifeu text, mqval real,
    gamma real, gint real,
    betaend real, bint real,
    ec real, ecbint real, ecint real, ectint real,
    alpha real, aint real,
    delay real, dptl text, dint real, dwidth real);''')

#Read ENSDF
# Number of ENSDF = 300
# for filenum in range(7, 8):
# for filenum in range(1, 2):
for filenum in range(1, 300):
    #filenum을 XXX로 표시
    nfile = format(filenum, '03')
    in_file = open("./ensdf_241101/ensdf.{}".format(nfile), "r")
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print("File Number: ", filenum)
    # file의 각 라인을 읽어서 리스트로 저장
    lines = in_file.readlines()
    print("Totla Line Number: ", len(lines))

    ###################################################
    ## Preprocess
    ###################################################
    ### line modifier and Find blank
    blank_number = []
    new_line = []
    new_line, blank_number = line_modifier(lines)
    # print("new_line: ", new_line)
    # print("blank_number: ", blank_number)
    ###################################################
    ### Find DECAY blocks
    dblock = []
    dblock = find_decay(blank_number, new_line)
    # print("dBlock: ", dblock)
    # print("Number of DECAY Blocks: ", len(dblock))
    # Number of DECAY blocks
    ndblock = len(dblock)
    print("Number of DECAY Blocks: ", ndblock)
    # DECAY block이 없으면 다음 파일로 넘어감
    if ndblock == 0:
        continue
    ###################################################
    
    ###################################################
    ###################################################
    # Main Code
    ###################################################
    ###################################################
 
    ###################################################
    ## DECAY block check
    ## Parent, Decay, Level, Gamma etc Line Check
    for i in range(ndblock):
        ### i-th DECAY block(dblock)을 sblock에 저장
        sblock, lsblock = singleblock(dblock[i])
        #print("sBLOCK:",sblock)
        #print("sBLOCK Length:",lsblock)
        # print("DECAY Block Number:",i)
        ### nParent: int, Others: string
        nParent, nLevel, nGamma, nBeta, nEC, nAlpha, nDelayed = finder(sblock)
        # print("Numbers:",nParent, nLevel, nGamma, nBeta, nEC, nAlpha, nDelayed)
        
        ### SKIP NONE Parent
        if nParent == 0:
            continue
        
        ### Parent Information
        mmass, misotope, mother, mlevel, mspin, mlife, mlifeu, mqval = id_parent(sblock, nParent)
        # print("Parent Information:",mmass, misotope, mother, mlevel, mspin, mlife, mqval)
        ### Daughter Information
        dmass, disotope, daughter, mdecay = id_daughter(sblock)
        # print("Daughter Information:",dmass, disotope, daughter,decay)
        
        ### Initialize
        val_parent={
                'mmass':0, 'misotope':'', 'mother':'',
                'mlevel':'', 'mspin':'', 'mdecay':'',
                'mlife':0, 'mlifeu':'', 'mqval':0
                }
        val_daughter={'dmass':0, 'disotope':'', 'daughter':''}
        ### Fill the dictionary
        val_parent.update({'mmass':mmass, 'misotope':misotope, 'mother':mother, 'mlevel':mlevel, 'mspin':mspin, 'mdecay':mdecay, 'mlife':mlife, 'mlifeu':mlifeu, 'mqval':mqval})
        val_daughter.update({'dmass':dmass, 'disotope':disotope, 'daughter':daughter})

        ### Initilaize
        # val_level={'level':0, 'lspin':'', 'llife':0, 'llifeu':''}

        ### SKIP NONE Level
        if len(nLevel) == 0:
            continue
        ### Level Information
        # level, lspin, llife, llifeu = id_level(sblock, nLevel)
        # print("Level Information:",level, lspin, llife)

        ### Alpha Information 
        val_alpha = {'alpha':0, 'aint':0}
        if len(nAlpha) != 0:
            for i in nAlpha:
                alpha, aint = id_alpha(sblock, i)
                val_alpha.update({'alpha':alpha,'aint':aint})
                cur.execute('''INSERT INTO decay(daughter, dmass, disotope, mother, mmass, misotope, mlevel, mspin, mdecay, mlife, mlifeu, mqval, alpha, aint) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(val_daughter['daughter'],val_daughter['dmass'],val_daughter['disotope'],val_parent['mother'],val_parent['mmass'],val_parent['misotope'],val_parent['mlevel'],val_parent['mspin'],val_parent['mdecay'],val_parent['mlife'],val_parent['mlifeu'],val_parent['mqval'],val_alpha['alpha'],val_alpha['aint']))
                # print("Alpha Information:",alpha, aint)

        ### Beta Information
        val_beta  = {'betaend':0, 'bint':0}
        if len(nBeta) != 0:
            for i in nBeta:
                betaend, bint = id_beta(sblock, i)
                val_beta.update({'betaend':betaend,'bint':bint})
                cur.execute('''INSERT INTO decay(daughter, dmass, disotope, mother, mmass, misotope, mlevel, mspin, mdecay, mlife, mlifeu, mqval, betaend, bint) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(val_daughter['daughter'],val_daughter['dmass'],val_daughter['disotope'],val_parent['mother'],val_parent['mmass'],val_parent['misotope'],val_parent['mlevel'],val_parent['mspin'],val_parent['mdecay'],val_parent['mlife'],val_parent['mlifeu'],val_parent['mqval'],val_beta['betaend'],val_beta['bint']))
                # print("Beta Information:",betaend, bint)

        ### EC Information
        val_ec    = {'ec':0, 'ecbint':0, 'ecint':0, 'ectint':0}
        if len(nEC) != 0:
            for i in nEC:
                ec, ecbint, ecint, ectint = id_EC(sblock,i)
                val_ec.update({'ec':ec,'ecbint':ecbint,'ecint':ecint,'ectint':ectint})
                cur.execute('''INSERT INTO decay(daughter, dmass, disotope, mother, mmass, misotope, mlevel, mspin, mdecay, mlife, mlifeu, mqval, ec, ecbint,ecint, ectint) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(val_daughter['daughter'],val_daughter['dmass'],val_daughter['disotope'],val_parent['mother'],val_parent['mmass'],val_parent['misotope'],val_parent['mlevel'],val_parent['mspin'],val_parent['mdecay'],val_parent['mlife'],val_parent['mlifeu'],val_parent['mqval'],val_ec['ec'],val_ec['ecbint'],val_ec['ecint'],val_ec['ectint']))
                # print("EC info:", ec, ecbint, ecint, ectint)

        ### Gamma Information
        val_gamma = {'gamma':0, 'gint':0}
        if len(nGamma) != 0:
            for i in nGamma:
                gamma, gint = id_gamma(sblock,i)
                val_gamma.update({'gamma':gamma,'gint':gint})
                cur.execute('''INSERT INTO decay(daughter, dmass, disotope, mother, mmass, misotope, mlevel, mspin, mdecay, mlife, mlifeu, mqval, gamma, gint) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(val_daughter['daughter'],val_daughter['dmass'],val_daughter['disotope'],val_parent['mother'],val_parent['mmass'],val_parent['misotope'],val_parent['mlevel'],val_parent['mspin'],val_parent['mdecay'],val_parent['mlife'],val_parent['mlifeu'],val_parent['mqval'],val_gamma['gamma'],val_gamma['gint']))
                # print("Gamma info:", gamma, gint)

        ### Delayed Infomation
        val_delay = {'delay':0, 'dptl':'', 'dint':0, 'dwidth':0}
        if len(nDelayed) != 0:
            for i in nDelayed:
                delay, dptl, dint, dwidth = id_delayed(sblock,i)
                val_delay.update({'delay':delay,'dptl':dptl,'dint':dint,'dwidth':dwidth})
                cur.execute('''INSERT INTO decay(daughter, dmass, disotope, mother, mmass, misotope, mlevel, mspin, mdecay, mlife, mlifeu, mqval, delay, dptl,dint, dwidth) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(val_daughter['daughter'],val_daughter['dmass'],val_daughter['disotope'],val_parent['mother'],val_parent['mmass'],val_parent['misotope'],val_parent['mlevel'],val_parent['mspin'],val_parent['mdecay'],val_parent['mlife'],val_parent['mlifeu'],val_parent['mqval'],val_delay['delay'],val_delay['dptl'],val_delay['dint'],val_delay['dwidth']))
                # print("Delayed info:",dptl,delay,dint,dwidth)
    ###################################################
    in_file.close()

######Commit & Close DB
con.commit()
con.close()

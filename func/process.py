import copy

def finder(testblock):
    nline = 0
    nParent = 0
    nLevel, nGamma, nBeta, nBetaA, nEC, nAlpha, nDelayed = [],[],[],[],[],[],[]
    for i in testblock:
        if i[9:].strip() == '':
            nline += 1
            continue
        ### Identifier
        ### id_05: Any ASCII, id_06: Comment/Delayed, id_07: TYPE, id_08: BLANK
        id_05 = i[5].strip()
        id_06 = i[6].strip()
        id_07 = i[7].strip()
        id_08 = i[8].strip()
        
        if id_05 == '' and id_06 == '' and id_07 == 'P' and id_08 == '':
            nParent = nline
        elif id_05 == '' and id_06 == '' and id_07 == 'L' and id_08 == '':
            nLevel.append(nline)
        elif id_05 == '' and id_06 == '' and id_07 == 'G' and id_08 == '':
            nGamma.append(nline)
        elif id_05 == '' and id_06 == '' and id_07 == 'B' and id_08 == '':
            nBeta.append(nline)
        elif id_05 == 'S' and id_06 == '' and id_07 == 'B' and id_08 == '':
            nBetaA.append(nline)
        elif id_05 == '' and id_06 == '' and id_07 == 'E' and id_08 == '':
            nEC.append(nline)
        elif id_05 == '' and id_06 == '' and id_07 == 'A' and id_08 == '':
            nAlpha.append(nline)
        elif id_05 == '' and id_06 == '' and id_07 == 'D' and id_08 != '':
            nDelayed.append(nline)
        else:
            nline += 1
            continue
        nline += 1
    return nParent, nLevel, nGamma, nBeta, nBetaA, nEC, nAlpha, nDelayed

def singleblock(testblock):
    ### deepcopy를 사용하지 않았을 때, 정보의 손실 발생
    ### 해당 mblock은 하나의 DECAY block을 의미
    sblock = copy.deepcopy(testblock)
    nsblock = len(sblock)

    return sblock, nsblock


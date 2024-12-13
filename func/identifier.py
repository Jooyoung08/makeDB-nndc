import copy

def id_delayed(testblock, testnum):
    dblock = copy.deepcopy(testblock[testnum])
    particle = dblock[8].strip()
    delay = dblock[9:19].strip()
    delint = dblock[21:29].strip()
    delwidth = dblock[39:49].strip()
    return delay, particle, delint, delwidth

def id_gamma(testblock, testnum):
    gblock = copy.deepcopy(testblock[testnum])
    gamma = gblock[9:19].strip()
    g_rint = gblock[21:29].strip()
    return gamma, g_rint

def id_EC(testblock, testnum):
    ecblock = copy.deepcopy(testblock[testnum])
    ec = ecblock[9:19].strip()
    ec_bint = ecblock[21:29].strip()
    ec_int  = ecblock[31:39].strip()
    ec_tint = ecblock[64:74].strip()
    return ec, ec_bint, ec_int, ec_tint

def id_beta(testblock, testnum):
    bblock = copy.deepcopy(testblock[testnum])
    beta_end = bblock[9:19].strip()
    beta_int = bblock[21:29].strip()
    # beta_eva = bblock[29:39].strip()
    # rb_eva.append(beta_eva)

    return beta_end, beta_int

def id_alpha(testblock, testnum):
    ablock = copy.deepcopy(testblock[testnum])
    alpha  = ablock[9:19].strip()
    aint   = ablock[21:29].strip()
    return alpha, aint

def id_level(testblock, testnum):
    lblock = copy.deepcopy(testblock[testnum])
    level  = lblock[9:19].strip()
    lspin  = lblock[21:39].strip()
    llife = lblock[39:49].strip().split()
    nllife = len(llife)
    if level == '0.0' and nllife == 2:
        rllife = llife[0]
        rllifeu = llife[1]
    elif level == '0' and nllife == 2:
        rllife = llife[0]
        rllifeu = llife[1]
    elif llife == 'STABLE':
        llife = ['0.0','STABLE']
        rllife = llife[0]
        rllifeu = llife[1]
    else:
        rllife= '0.0'
        rllifeu = 'NONE'
    return level, lspin, rllife, rllifeu
    
def id_parent(testblock, testline):

    pblock = copy.deepcopy(testblock[testline])
    mmass    = pblock[:3].strip()
    misotope = pblock[3:5].strip()
    mother   = pblock[:5].strip()
    mlevel   = pblock[9:19].strip()
    mspin    = pblock[21:39].strip()
    mqval    = pblock[64:74].strip()
    mlife    = pblock[39:49].strip().split()
    nmlife   = len(mlife)
    if nmlife == 0:
        mlife = [-999.0,'UNKNOWN']
    elif 'STABLE' in mlife:
        mlife = [0.0,'STABLE']
    elif nmlife == 2:
        mlife = [float(mlife[0]),mlife[1]]
    cmlife = mlife[0]
    cmlifeu= mlife[1]

    return mmass, misotope, mother, mlevel, mspin, cmlife, cmlifeu, mqval

def id_daughter(testblock):
    dblock = copy.deepcopy(testblock[0])
    dmass    = dblock[:3].strip()
    disotope = dblock[3:5].strip()
    daughter = dblock[:5].strip()
    decay    = dblock[9:49].strip().split()

    return dmass, disotope, daughter, decay[1]

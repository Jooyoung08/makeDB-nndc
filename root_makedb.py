import sys
import ROOT as root
import sqlite3
import numpy as np
from array import array
import copy
from func.identifier import *
from func.daughter import *
# from makedblib.find_decay import *
from func.preprocess import *

# CERN ROOT
with root.TFile("root-nndc-20241101.root","RECREATE") as ofile:
    tree = root.TTree("nndc","nndc")

    rdaughter    = root.vector('string')()
    rdmass       = array('i',[0])
    rdisotope    = root.vector('string')()
    rmmass       = array('i',[0])
    rmisotope    = root.vector('string')()
    rmother      = root.vector('string')()
    rdecay       = root.vector('string')()
    rspin        = root.vector('string')()
    rlife        = array('f',[0.])
    rlifeu       = root.vector('string')()
    rqval        = array('f',[0.])
    rlevel       = array('f',[0.])
    rl_spin      = root.vector('string')()
    rgamma       = array('f',[0.])
    rg_rint      = array('f',[0.])
    rg_mtrans    = array('f',[0.])
    rg_mratio    = array('f',[0.])
    rg_tconv     = array('f',[0.])
    rg_rttint    = array('f',[0.])
    rgDTYPE      = root.vector('string')()
    rgDTYPEv     = array('f',[0.])
    rbeta_end    = array('f',[0.])
    rb_int       = array('f',[0.])
    rb_logft     = array('f',[0.])
    rbeta_ave    = array('f',[0.])
    rec          = array('f',[0.])
    rec_bint     = array('f',[0.])
    rec_int      = array('f',[0.])
    rec_logft    = array('f',[0.])
    rec_tint     = array('f',[0.])
    recDTYPE     = root.vector('string')()
    recDTYPEv    = array('f',[0.])
    ralpha       = array('f',[0.])
    ra_int       = array('f',[0.])
    ra_hf        = array('f',[0.])
    rdelayed     = array('f',[0.])
    rd_particle  = root.vector('string')()
    rd_int       = array('f',[0.])
    rd_elevel    = array('f',[0.])
    rd_width     = array('f',[0.])
    rd_ang       = array('f',[0.])
    
    tree.Branch('daughter', rdaughter)
    tree.Branch('dmass', rdmass, 'dmass/I')
    tree.Branch('disotope', rdisotope)
    tree.Branch('mmass', rmmass, 'mmass/I')
    tree.Branch('misotope', rmisotope)
    tree.Branch('mother', rmother)
    tree.Branch('decay', rdecay)
    tree.Branch('spin', rspin)
    tree.Branch('life', rlife, 'life/F')
    tree.Branch('lifeu',rlifeu)
    tree.Branch('qval',rqval,'qval/F')
    tree.Branch('level',rlevel,'level/F')
    tree.Branch('l_spin',rl_spin)
    tree.Branch('gamma',rgamma,'gamma/F')
    tree.Branch('g_rint',rg_rint,'g_rint/F')
    # tree.Branch('g_mtrans',rg_mtrans,'g_mtrans/F')
    # tree.Branch('g_mratio',rg_mratio,'g_mratio/F')
    tree.Branch('g_tconv',rg_tconv,'g_tconv/F')
    tree.Branch('g_rttint',rg_rttint,'g_rttint/F')
    # tree.Branch('gDTYPE',rgDTYPE)
    # tree.Branch('gDTYPEv',rgDTYPEv,'gDTYPEv/F')
    tree.Branch('beta_end',rbeta_end,'beta_end/F')
    tree.Branch('b_int',rb_int,'b_int/F')
    # tree.Branch('b_logft',rb_logft,'b_logft/F')
    tree.Branch('beta_ave',rbeta_ave,'beta_ave/F')
    tree.Branch('ec',rec,'ec/F')
    tree.Branch('ec_bint',rec_bint,'ec_bint/F')
    tree.Branch('ec_int',rec_int,'ec_int/F')
    # tree.Branch('ec_logft',rec_logft,'ec_logft/F')
    tree.Branch('ec_tint',rec_tint,'ec_tint/F')
    # tree.Branch('ecDTYPE',recDTYPE)
    # tree.Branch('ecDTYPEv',recDTYPEv,'ecDTYPEv/F')
    tree.Branch('alpha',ralpha,'alpha/F')
    tree.Branch('a_int',ra_int,'a_int/F')
    # tree.Branch('a_hf',ra_hf,'a_hf/F')
    tree.Branch('d_particle',rd_particle)
    tree.Branch('delayed',rdelayed,'delayed/F')
    tree.Branch('d_int',rd_int,'d_int/F')
    # tree.Branch('d_elevel',rd_elevel,'d_elevel/F')
    # tree.Branch('d_width',rd_width,'d_width/F')
    # tree.Branch('d_ang',rd_ang,'d_ang/F')

    #Read ENSDF
    # Number of ENSDF = 300
    # for filenum in range(1, 3):
    for filenum in range(1, 300):
        #filenum을 XXX로 표시
        nfile = format(filenum, '03')
        in_file = open("./ensdf_241101/ensdf.{}".format(nfile), "r")
        print("++++++++++++++++++++++++++++++++++++++++++++")
        print("File Number: ", filenum)
        # file의 각 라인을 읽어서 리스트로 저장
        lines = in_file.readlines()
        print("Totla Line Number: ", len(lines))

        ### Global in each file
        line_number = 0
        blank_number = []
        new_line = []
        gblock = []

        # Block 개수 구하기
        ## block 수 = 빈 칸 수 + 1
        ### 빈 칸을 제거하고 blank 를 제거한 line 리스트
        for line in lines:
            # line 맨 끝 개행문자 '\n'을 제거
            line = line.rstrip()
            # line을 리스트화
            ### line에서 맨 끝 개행문자 '\n'을 제거한 것과 동일
            new_line.append(line)
            # print(line)
            ### block 개수를 구하기 위해 리스트 중간에 ''(blank)를 기준으로 삼음 
            ### '' 의 line number를 저장
            # if line == '':
            if not line:
                blank_number.append(line_number)
            # 다음줄로 넘어가기 전, number 를 1 증가
            line_number += 1
            ### End of line loop
        ### End of block loop
           
        ## make blocks
        nn = 0
        ### i는 blank_number의 index value
        for i in blank_number:
            ### 첫 block은 blank가 없으므로, 첫 block을 따로 저장
            if nn == 0:
                ### block의 첫 index부터 i-1까지 block에 저장
                ### 하나의 block 정보가 리스트로 저장됨
                block = new_line[:i]
            else:
                ### 나머지 block은 blank 다음부터 시작
                ### blank_number[0]가 첫번째 blank number이므로, blank_number[0]+1부터 시작
                ### block의 blank_number[nn-1]+1부터 i-1까지 block에 저장
                block = new_line[blank_number[nn-1]+1:i]
            nn += 1
            # print("Block: ", block[0])

            ## Find DECAY
            ### block의 첫 줄에 해당 정보가 있음
            ### 첫 줄을 list화 하여 'DECAY'가 있는지 확인
            ### 'DECAY'가 있으면 해당 block을 gblock에 저장
            # find_decay = copy.deepcopy(block[0]).split()
            # if 'DECAY' in find_decay:
            #     # print("DECAY Line : ", block)
            #     gblock.append(block)

            fd = find_decay(block)
            if fd !=None:
                gblock.append(fd)
            # print("Find Decay: ", fd)
            # End of make 'DECAY' block

        ### Check gblock
        # print("gBlock: ", gblock)

        ###################################################
        # Number of DECAY blocks
        nblock = len(gblock)
        print("Number of DECAY Blocks: ", nblock)
        # DECAY block이 없으면 다음 파일로 넘어감
        if nblock == 0:
            continue
        ###################################################

        ## Loop for gblock
        ### 0 부터 nblock-1까지 반복
        for i in range(nblock):
            ### i-th gblock을 mblock에 저장
            ### 이 때의 mblock은 한 block의 전체 정보를 가지고 있음
            mblock = copy.deepcopy(gblock[i])
            # print("MBLOCK:",mblock)
            ### Length of mblock
            nmblock = len(mblock)
            # print("MBLOCK Length: ", lmblock)
                
            ## Basic Information
            dmass    = mblock[0][:3].strip()
            daughter = mblock[0][:5].strip()
            disotope = mblock[0][3:5].strip()
            decay    = mblock[0][13:15].strip()
            # print("D_mass:",dmass)
            # print("Daughter:",daughter)
            # print("Disotope:",disotope)
            # print("Decay Mode:",decay)

            ### 첫번째 block 중 daughter 정보 저장
            ### Daughter Dictionary
            info_daughter = {}
            info_daughter={'daughter':daughter, 'dmass':dmass, 'disotope':disotope, 'decay':decay}
            # print("Daughter Information:",info_daughter)
            ### Parent Dictionary
            info_parent = {}
            info_parent={'mmass':0, 'misotope':'', 'mother':'', 'spin':'', 'life':0, 'lifeu':'', 'qval':0.0}
            ### Level Dictionary
            info_level = {}
            info_level={'level':0, 'l_spin':''}
            ### Alpha Dictionary
            info_alpha = {}
            info_alpha={'alpha':0, 'a_int':0, 'a_hf':0}
            ### Beta Dictionary
            info_beta = {}
            info_beta={'beta_end':0, 'b_int':0, 'b_logft':0, 'beta_ave':0}
            ### Gamma Dictionary
            info_gamma = {}
            info_gamma={'gamma':0, 'g_rint':0, 'g_mtrans':0, 'g_mratio':0, 'g_tconv':0, 'g_rttint':0}
            ### Gamma Sub Dictionary
            info_gamma_sub = {}
            info_gamma_sub={'gDTYPE':'', 'gDTYPEv':0}
            ### EC Dictionary
            info_ec = {}
            info_ec={'ec':0, 'ec_bint':0, 'ec_int':0, 'ec_logft':0, 'ec_tint':0, 'ec_ave':0}
            ### EC Sub Dictionary
            info_ec_sub = {}
            info_ec_sub={'ecDTYPE':'', 'ecDTYPEv':0}
            ### Delayed Dictionary
            info_delayed = {}
            info_delayed={'d_particle':'', 'delayed':0, 'd_int':0, 'd_elevel':0, 'd_width':0, 'd_ang':0}
            ### Delayed Sub Dictionary
            # info_delayed_sub = {}
            # info_delayed_sub={'dDTYPE':'', 'dDTYPE_val':0}
                
            ### Global Parent
            mmass = 0
            misotope = ''
            spin_parity = ''
            half_life = 0
            half_lifeu = ''
            qval = 0.0
            ### block 정보 확인
            ### 각 block의 정보를 한 줄씩 읽어서 처리
            #### Level line
            lnum = 0
            level = []
            for k in mblock:
                rblock  = copy.deepcopy(k)
                ### 일부 비어있는 라인은 제외
                check_empty = rblock[9:].strip()
                if not check_empty:
                    lnum += 1
                    continue
                ### History Information 제외
                if 'H' in rblock[7]:
                    lnum += 1
                    continue

                ### Define
                id_mass,id_symbol,id_continue,id_comment,id_type = identifier(rblock)
                # id_mass     = rblock[:3].strip()
                # id_symbol   = rblock[3:5].strip()
                # id_continue = rblock[5].strip()
                # id_comment  = rblock[6].strip()
                # id_type     = rblock[7].strip()
                # print("ID Mass:",id_mass)
                # print("ID Symbol:",id_symbol)
                # print("ID Continue:",id_continue)
                # print("ID Comment:",id_comment)
                # print("ID Type:",id_type)
                    
                ### Parent Information
                if id_type == 'P' and id_comment == '' and id_continue == '':
                    # print("Parent :", rblock)
                    mmass       = id_mass.strip()
                    misotope    = id_symbol.strip()
                    mother      = rblock[:5].strip()
                    spin_parity = rblock[21:39].strip()
                    thalf_life   = list(rblock[39:49].strip().split())
                    qval        = rblock[64:74].strip()
                    # print("Mother Mass:",mmass)
                    # print("Mother Isotope:",misotope)
                    # print("Spin Parity:",spin_parity)
                    # print("Q-value:",qval)
                    info_parent.update({'mmass':mmass, 'misotope':misotope, 'mother':mother, 'spin_parity':spin_parity, 'qval':qval})

                    ## Half Life Check
                    lh = len(thalf_life)
                    if lh == 0:
                        half_life = -999.0
                        half_lifeu = 'UNKNOWN'
                        # half_life = [-999.0, 'UNKNOWN']
                        info_parent.update({'life':half_life, 'lifeu':half_lifeu})
                    if half_life == 'STABLE':
                        half_life = -999.0
                        half_lifeu = 'STABLE'
                        # half_life = [-999.0, 'STABLE']
                        info_parent.update({'life':half_life, 'lifeu':half_lifeu})
                    if lh == 2:
                        half_life = thalf_life[0]
                        half_lifeu = thalf_life[1]
                        # print("Half Life:",half_life[0])
                        # print("Half Life Dim:",half_life[1])
                        info_parent.update({'life':half_life, 'lifeu':half_lifeu})
                        
                ## Level Line Number Check
                if id_type == 'L' and id_comment == '' and id_continue == '':
                    level.append(lnum)
                    # print("Level :", k)
                    level_energy = rblock[9:19].strip()
                    level_spin   = rblock[21:39].strip()
                    # print("Level Energy:",level_energy)
                    # print("Level Spin:",level_spin)
                    # print("Level Number:",lnum)
                lnum += 1
               #################################################################
                
            #### Level Information
            # print("Level Information:",level)
            clevel = len(level)
            # print("Number of Level:",clevel)
                
            ##################################################################
            ### Loop for Level
            ##################################################################
            for j in range(clevel):
                # print("--------------------------------------")
                rblock = copy.deepcopy(mblock[level[j]])
                level_energy = rblock[9:19].strip()
                level_spin   = rblock[21:39].strip()
                # print("Level : ", mblock[level[j]])
                # print("Level Energy:",level_energy)
                # print("Level Spin:",level_spin)
                # print("--------------------------------------")
                info_level.update({'level_energy':level_energy, 'level_spin':level_spin})
                   
                ### Level이 있을 때, beta, gamma 등 확인
                k = 1
                while True:
                    if level[j]+k == nmblock:
                        # print("END: Out of Range")
                        break
                    lblock = copy.deepcopy(mblock[level[j]+k])
                    if lblock[7] == 'L':
                        # print("END: New Level Start")
                        break
                    # print("++++++++++++++++++++++++++++++++++++++++++++")
                    # print("TEST after Level : ", lblock)
                    # print("++++++++++++++++++++++++++++++++++++++++++++")
                    k += 1

                    ### Define
                    id_mass,id_symbol,id_continue,id_comment,id_type = identifier(lblock)
                    # print("test : ", identifier(lblock))

                    ### Initilaize
                    info_alpha.update({'alpha':0, 'a_int':0, 'a_hf':0})
                    info_beta.update({'beta_end':0, 'beta_int':0, 'beta_logft':0, 'beta_ave':0})
                    info_gamma.update({'gamma':0, 'g_relint':0, 'g_mtran':0, 'g_mratio':0, 'g_tconv':0, 'g_rttint':0})
                    info_gamma_sub.update({'gDTYPE':'', 'gDTYPEv':0})
                    info_ec.update({'ec':0, 'ec_bp_int':0, 'ec_int':0, 'ec_logft':0, 'ec_tot_int':0, 'ec_ave':0})
                    info_ec_sub.update({'ecDTYPE':'', 'ecDTYPEv':0})
                    info_delayed.update({'d_particle':'', 'delayed':0, 'd_int':0, 'd_elevel':0, 'd_width':0, 'd_ang':0})

                    ### Beta Information
                    if id_type == 'B' and id_comment == '':
                        if id_continue == '':
                    # if lblock[7] == 'B' and lblock[6] == ' ':
                    #     if lblock[5] == ' ':
                            # print("Beta :", lblock)
                            beta_end    = lblock[9:19].strip()
                            beta_int    = lblock[21:29].strip()
                            beta_logft  = lblock[41:49].strip()
                            # print("Beta End Energy:",beta_end)
                            # print("Beta Intensity:",beta_int)
                            # print("Beta Logft:",beta_logft)
                            info_beta.update({'beta_end':beta_end, 'beta_int':beta_int, 'beta_logft':beta_logft})
                        if id_continue == 'S':
                        # if lblock[5] == 'S':
                            # print("Beta DTYPE :", lblock)
                            beta_ave  = list(lblock[9:29].strip().split('='))
                            ba = len(beta_ave)
                            # print("Beta 'S' length:",ba)
                            # print("Beta Average Energy:",beta_ave)
                            if ba == 2:
                                beta_ave  = beta_ave[1].split(' ')
                                # print("Beta Average Energy:",beta_ave[0])
                                info_beta.update({'beta_ave':beta_ave[0]})
                            else:
                                beta_ave  = list(beta_ave[0].split(' '))
                                # print("Beta Average Energy:",beta_ave[0])
                                if 'AP' in beta_ave:
                                    beta_ave.remove('AP')
                                # print("Beta Average Energy:",beta_ave[1])
                                info_beta.update({'beta_ave':beta_ave[1]})

                    ### Gamma Information
                    if id_type == 'G' and id_comment == '': 
                        if id_continue == '':
                    # if lblock[7] == 'G' and lblock[6] == ' ': 
                    #     if lblock[5] == ' ':
                            # print("Gamma :", lblock)
                            g_energy    = lblock[9:19].strip()
                            g_relint    = lblock[21:29].strip()
                            g_multran   = lblock[31:41].strip()
                            g_mixratio  = lblock[41:49].strip()
                            g_totconv   = lblock[55:62].strip()
                            g_rttint    = lblock[64:74].strip()
                            # print("Gamma Energy:",g_energy)
                            # print("Gamma Intensity:",g_relint)
                            # print("Gamma Multipolarity of transition:",g_multran)
                            # print("Gamma Mixing ratio:",g_mixratio)
                            # print("Gamma Total Conversion Coefficient:",g_totconv)
                            # print("Gamma Relative Total Transition Intensity:",g_rttint)
                            info_gamma.update({'gamma':g_energy, 'g_rint':g_relint, 'g_mtran':g_multran, 'g_mratio':g_mixratio, 'g_tconv':g_totconv, 'g_rttint':g_rttint})
                        if id_continue == 'S':
                            # print("Gamma DTYPE:", lblock)
                            gtemp  = lblock[9:].split('$')
                            gtemp  = list(filter(None, gtemp))
                            ngtemp = len(gtemp)
                            # print("Gamma 'S' test:",gtemp)
                            # print("Gamma 'S' num test:",ngtemp)
                            ### Sub-Gamma Information
                            a = 0
                            while a < ngtemp:
                                # print("Gamma 'S' test:",gtemp[a])
                                ### Split with '='
                                temp2 = gtemp[a].split('=')
                                temp2 = list(filter(None, temp2))
                                # print("Gamma 'S' test2:",temp2)
                                ##
                                b = len(temp2)
                                # print("test length", b)
                                ##
                                if b == 2:
                                    # print("Gamma Sub DTYPE:",temp2[0].strip())
                                    temp4 = temp2[1].split(' ')
                                    # print("test temp4 : ", temp4)
                                    temp4 = list(filter(None, temp4))
                                    # print("test temp4 : ", temp4)
                                    # print("Gamma Sub DTYPE Val",temp4[0].strip())
                                    # print("test temp4 : ", temp4)
                                    info_gamma_sub.update({'gDTYPE':temp2[0].strip(), 'gDTYPEv':temp4[0].strip()})
                                else:
                                    # print("Gamma Sub DTYPE:",temp2[0].strip())
                                    temp4 = temp2[0].split(' ')
                                    if 'AP' in temp4:
                                        temp4.remove('AP')
                                    # print("Gamma Sub DTYPE:",temp4[0].strip())
                                    # print("Gamma Sub DTYPE Val:",temp4[1].strip())
                                    info_gamma_sub.update({'gDTYPE':temp4[0].strip(), 'gDTYPEv':temp4[1].strip()})

                                # if 'AP' in temp4:
                                #     temp4.remove('AP')
                                # print("test temp4 : ", temp4)
                                # print("Gamma Sub DTYPE Val",temp4[0].strip())
                                a += 1

                    ### EC Information
                    if id_type == 'E' and id_comment == '':
                        if id_continue == '':
                    # if lblock[7] == 'E' and lblock[6] == ' ':
                    #     if lblock[5] == ' ':
                            ec_energy = lblock[9:19].strip()
                            ec_bp_int = lblock[21:29].strip()
                            ec_int    = lblock[31:39].strip()
                            ec_logft  = lblock[41:49].strip()
                            ec_tot_int= lblock[64:74].strip()
                            # print("EC Energy:",ec_energy)
                            # print("EC b+ Intensity:",ec_bp_int)
                            # print("EC Intensity:",ec_int)
                            # print("EC Logft for (ec+b+) Transition:",ec_logft)
                            # print("EC Total (ec+b+) Decay Intensity:",ec_tot_int)
                            info_ec.update({'ec':ec_energy, 'ec_bp_int':ec_bp_int, 'ec_int':ec_int, 'ec_logft':ec_logft, 'ec_tot_int':ec_tot_int})
                        if id_continue == 'S':
                            # print("EC :", lblock)
                            etemp  = lblock[9:].split('$')
                            etemp  = list(filter(None, etemp))
                            # print("EC 'S' test:",etemp)
                            netemp = len(etemp)
                            # print("EC 'S' num test:",netemp)
                            a = 0
                            while a < netemp:
                                temp2 = etemp[a].split('=')
                                # print("EC Sub DTYPE:",temp2)
                                print("EC Sub DTYPE:",temp2[0].strip())
                                temp3 = temp2[1].lstrip()
                                temp4 = temp3.split(' ')
                                # print("EC Sub DTYPE Val",temp4)
                                # print("EC Sub DTYPE Val",temp4[0].strip())
                                # ec_ave = lblock[13:19].strip()
                                # print("EC else test : ", lblock)
                                # print("EC Average Energy:",ec_ave)
                                info_ec_sub.update({'ecDTYPE':temp2[0].strip(), 'ecDTYPEv':temp4[0].strip()})
                                a += 1

                    ### Alpha Information
                    if id_type == 'A' and id_comment == '':
                        if id_continue == '':
                            a_energy = lblock[9:19].strip()
                            a_int    = lblock[21:29].strip()
                            a_hf     = lblock[31:39].strip()
                            # print("Alpha Energy:",a_energy)
                            # print("Intensity of a-decay branch (percent):",a_int)
                            # print("Alpha Hindrance Factor:",a_hf)
                        # else:
                            # print("test alpha else : ", lblock)
                            info_alpha.update({'alpha':a_energy, 'a_int':a_int, 'a_hf':a_hf})

                    ### Delayed Information
                    if id_type == 'D' and id_comment == '':
                        d_particle = lblock[8].strip()
                        d_energy   = lblock[9:19].strip()
                        d_int      = lblock[21:29].strip()
                        d_elevel   = lblock[31:39].strip()
                        d_width    = lblock[39:49].strip()
                        d_ang      = lblock[55:64].strip()
                        # print("Delayed Particle:",d_particle)
                        # print("Delayed Energy:",d_energy)
                        # print("Intensity of delayed particle (percent):",d_int)
                        # print("Energy of the level in the 'intermediate':",d_elevel)
                        # print("Width of the transition in keV:",d_width)
                        # print("Angular-Momentum transfer of emitted ptl:",d_ang)
                        # if len(id_continue) != 0:
                        # print("test delayed S : ", lblock)
                        info_delayed.update({'d_particle':d_particle, 'delayed':d_energy, 'd_int':d_int, 'd_elevel':d_elevel, 'd_width':d_width, 'd_ang':d_ang})
                        
                # print("++++++++++++++++++++++++++++++++++++++++++++")
                ### Conv for ROOT
                convdmass = int(info_daughter['dmass'])
                convmmass = int(info_parent['mmass'])
                if info_parent['life'] == '':
                    convlife = 0.0
                else:
                    convlife  = float(info_parent['life'])
                if info_parent['qval'] == '':
                    convqval = 0.0
                else:
                    convqval  = float(info_parent['qval'])
                convlevel = float(info_level['level'])
                if info_gamma['gamma'] == '':
                    convgamma = 0.0
                else:
                    convgamma = float(info_gamma['gamma'])
                if info_gamma['g_rint'] == '':
                    convg_rint = 0.0
                else:
                    convg_rint = float(info_gamma['g_rint'])
                if info_gamma['g_mtrans'] == '':
                    convg_mtrans = 0.0
                else:
                    convg_mtrans = float(info_gamma['g_mtrans'])
                if info_gamma['g_mratio'] == '':
                    convg_mratio = 0.0
                else:
                    convg_mratio = float(info_gamma['g_mratio'])
                if info_gamma['g_tconv'] == '':
                    convg_tconv = 0.0
                else:
                    convg_tconv = float(info_gamma['g_tconv'])
                if info_gamma['g_rttint'] == '':
                    convg_rttint = 0.0
                else:
                    convg_rttint = float(info_gamma['g_rttint'])
                if info_gamma_sub['gDTYPEv'] == '':
                    convgDTYPEv = 0.0
                if info_gamma_sub['gDTYPEv'] == 'GT':
                    convgDTYPEv = -999
                else:
                    convgDTYPEv = float(info_gamma_sub['gDTYPEv'])
                if info_beta['beta_end'] == '':
                    convbeta_end = 0.0
                else:
                    convbeta_end = float(info_beta['beta_end'])
                convb_int = float(info_beta['b_int'])
                convb_logft = float(info_beta['b_logft'])
                if info_beta['beta_ave'] == '':
                    convbeta_ave = 0.0
                else:
                    convbeta_ave = float(info_beta['beta_ave'])
                if info_ec['ec'] == '':
                    convec = 0.0
                else:
                    convec = float(info_ec['ec'])
                if info_ec['ec_bint'] == '':
                    convec_bint = 0.0
                else:
                    convec_bint = float(info_ec['ec_bint'])
                if info_ec['ec_int'] == '':
                    convec_int = 0.0
                else:
                    convec_int = float(info_ec['ec_int'])
                if info_ec['ec_logft'] == '':
                    convec_logft = 0.0
                else:
                    convec_logft = float(info_ec['ec_logft'])
                if info_ec['ec_tint'] == '':
                    convec_tint = 0.0
                else:
                    convec_tint = float(info_ec['ec_tint'])
                if info_ec_sub['ecDTYPEv'] == '':
                    convec_DTYPEv = 0.0
                else:
                    convec_DTYPEv = float(info_ec_sub['ecDTYPEv'])
                if info_alpha['alpha'] == '':
                    convalpha = 0.0
                else:
                    convalpha = float(info_alpha['alpha'])
                if info_alpha['a_int'] == '':
                    conva_int = 0.0
                else:
                    conva_int = float(info_alpha['a_int'])
                if info_alpha['a_hf'] == '':
                    conva_hf = 0.0
                else:
                    conva_hf  = float(info_alpha['a_hf'])
                ### Problem
                convdelayed = 0.0
                # if info_delayed['delayed'] == '':
                #     convdelayed = 0.0
                # else:
                #     convdelayed = float(info_delayed['delayed'])
                if info_delayed['d_int'] == '':
                    convd_int = 0.0
                else:
                    convd_int = float(info_delayed['d_int'])
                if info_delayed['d_elevel'] == '':
                    convd_elevel = 0.0
                else:
                    convd_elevel = float(info_delayed['d_elevel'])
                if info_delayed['d_width'] == '':
                    convd_width = 0.0
                else:
                    convd_width = float(info_delayed['d_width'])
                if info_delayed['d_ang'] == '':
                    convd_ang = 0.0
                else:
                    convd_ang = float(info_delayed['d_ang'])

                ### Fill Tree
                rdaughter.push_back(info_daughter['daughter'])
                rdmass[0] = convdmass 
                # rdmass[0] = info_daughter['dmass']
                rdisotope.push_back(info_daughter['disotope'])
                rmmass[0] = convmmass 
                # rmmass[0] = info_parent['mmass']
                rmisotope.push_back(info_parent['misotope'])
                rmother.push_back(info_parent['mother'])
                rdecay.push_back(info_daughter['decay'])
                rspin.push_back(info_parent['spin_parity'])
                rlife[0] = convlife
                # rlife[0] = info_parent['life']
                rlifeu.push_back(info_parent['lifeu'])
                rqval[0] = convqval
                # rqval[0] = info_parent['qval']
                rlevel[0] = convlevel
                # rlevel[0] = info_level['level']
                rl_spin.push_back(info_level['l_spin'])
                rgamma[0] = convgamma
                # rgamma[0] = info_gamma['gamma']
                rg_rint[0] = convg_rint
                # rg_rint[0] = info_gamma['g_rint']
                rg_mtrans[0] = convg_mtrans
                # rg_mtrans[0] = info_gamma['g_mtrans']
                rg_mratio[0] = convg_mratio
                # rg_mratio[0] = info_gamma['g_mratio']
                rg_tconv[0] = convg_tconv
                # rg_tconv[0] = info_gamma['g_tconv']
                rg_rttint[0] = convg_rttint
                # rg_rttint[0] = info_gamma['g_rttint']
                rgDTYPE.push_back(info_gamma_sub['gDTYPE'])
                rgDTYPEv[0] = convgDTYPEv
                # rgDTYPEv[0] = info_gamma_sub['gDTYPEv']
                rbeta_end[0] = convbeta_end
                # rbeta_end[0] = info_beta['beta_end']
                rb_int[0] = convb_int
                # rb_int[0] = info_beta['b_int']
                rb_logft[0] = convb_logft
                # rb_logft[0] = info_beta['b_logft']
                rbeta_ave[0] = convbeta_ave
                # rbeta_ave[0] = info_beta['beta_ave']
                rec[0] = convec
                # rec[0] = info_ec['ec']
                rec_bint[0] = convec_bint
                # rec_bint[0] = info_ec['ec_bint']
                rec_int[0] = convec_int
                # rec_int[0] = info_ec['ec_int']
                rec_logft[0] = convec_logft
                # rec_logft[0] = info_ec['ec_logft']
                rec_tint[0] = convec_tint
                # rec_tint[0] = info_ec['ec_tint']
                recDTYPE.push_back(info_ec_sub['ecDTYPE'])
                recDTYPEv[0] = convec_DTYPEv
                # recDTYPEv[0] = info_ec_sub['ecDTYPEv']
                ralpha[0] = convalpha
                # ralpha[0] = info_alpha['alpha']
                ra_int[0] = conva_int
                # ra_int[0] = info_alpha['a_int']
                ra_hf[0]  = conva_hf
                # ra_hf[0]  = info_alpha['a_hf']
                rd_particle.push_back(info_delayed['d_particle'])
                rdelayed[0] = convdelayed
                # rdelayed[0] = info_delayed['delayed']
                rd_int[0] = convd_int
                # rd_int[0] = info_delayed['d_int']
                rd_elevel[0] = convd_elevel
                # rd_elevel[0] = info_delayed['d_elevel']
                rd_width[0] = convd_width
                # rd_width[0] = info_delayed['d_width']
                rd_ang[0] = convd_ang
                # rd_ang[0] = info_delayed['d_ang']
                tree.Fill()
            ### End of Level loop
        ### End of file loop
        in_file.close()
    tree.Write()

import sys
import sqlite3
import numpy as np
import copy
from func.identifier import *
from func.daughter import *
# from makedblib.find_decay import *
from func.preprocess import *

#DB Creation
con = sqlite3.connect('./test.db')
# con = sqlite3.connect('./nndc-20241101.db')
cur = con.cursor()

#DB Table Creation
cur.execute("create table decay (daughter text, dmass int, disotope text, mmass int, misotope text, mother text, decay text, spin text, life real, lifeu text, qval real, level real, l_spin text, l_life real, l_lifeu text, gamma real, g_rint real, g_mtrans real, g_mratio real, g_tconv real, g_rttint real, gDTYPE text, gDTYPEv real, beta_end real, b_int real, b_logft real, beta_ave real, ec real, ec_bint real, ec_int real, ec_logft real, ec_tint real, ecDTYPE text, ecDTYPEv real, alpha real, a_int real, a_hf real, d_particle text, delayed real, d_int real, d_elevel real, d_width real, d_ang real);")

#Read ENSDF
# Number of ENSDF = 300
# for filenum in range(1, 10):
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

    # Preprocess
    #######################################################
    # Block 개수 구하기
    ## block 수 = 빈 칸 수 + 1
    ### 빈 칸을 제거하고 blank 를 제거한 line 리스트
    for line in lines:
        # line 맨 끝 개행문자 '\n'을 제거
        line = line.rstrip()
        # line = line.lstrip()
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
    # new_line 리스트에는 개행문자가 제거된 line이 저장되어 있음
    # blank_number 리스트에는 빈 줄의 line number가 저장되어 있음
    #######################################################

    #######################################################
    ### Find DECAY blocks
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
    # block 중에서 DECAY block을 gblock에 저장
    # gblock[0]에는 첫번째 DECAY block이 저장되어 있음
    #######################################################

    ###################################################
    ###################################################
    ###################################################
    # Main Code
    ###################################################
    ###################################################
    ###################################################

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
        ### deepcopy를 사용하지 않았을 때, 정보의 손실이 발생
        mblock = copy.deepcopy(gblock[i])
        # print("MBLOCK:",mblock)
        ### Length of mblock
        nmblock = len(mblock)
        # print("MBLOCK Length: ", lmblock)
       
        # Dictionary
        ### Daughter Dictionary
        ### 첫번째 block의 daughter 정보 저장
        info_daughter = {}
        info_daughter={'daughter':'', 'dmass':0, 'disotope':'', 'decay':''}
        # info_daughter={'daughter':daughter, 'dmass':dmass, 'disotope':disotope, 'decay':decay}
        # print("Daughter Information:",info_daughter)
        ### Parent Dictionary
        info_parent = {}
        info_parent={'mmass':0, 'misotope':'', 'mother':'', 'spin':'', 'life':0, 'lifeu':'', 'qval':0.0}
        ### Level Dictionary
        info_level = {}
        info_level={'level':0, 'l_spin':'', 'l_life':0, 'l_lifeu':''}
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
        
        ### block 정보 확인
        ### 각 block의 정보를 한 줄씩 읽어서 처리
        #### Find Level line
        lnum = 0
        level = []
        for k in mblock:
            ### 각 라인을 deepcopy
            rblock  = copy.deepcopy(k)
            ### 일부 비어있는 라인은 제외
            check_empty = rblock[9:].strip()
            if not check_empty:
                # print("EMPTY :", lnum)
                lnum += 1
                continue
            ### History Information 제외
            # if 'H' in rblock[7]:
            #     print("History :", lnum)
            #     lnum += 1
            #     continue

            ### Define
            id_mass,id_symbol,id_continue,id_comment,id_type = identifier(rblock)
         
            ### DECAY block의 첫 줄에는 DECAY 정보가 있음
            ## Basic Information
            if lnum == 0:
                basic   = copy.deepcopy(rblock)
                # print("Basic Information:",basic)
                # print("daughter :", basic[:5].strip())
                # print("dmass :", basic[:3].strip())
                # print("disotope :", basic[3:5].strip())
                sbasic = copy.deepcopy(rblock[:39]).split()
                # print("decay", sbasic[2].strip())
                info_daughter.update({'daughter':basic[0][:5].strip(), 'dmass':basic[0][:3].strip(), 'disotope':basic[0][3:5].strip(), 'decay':basic[2].strip()})
  
            else:
                ### Parent Information
                if id_type == 'P' and id_comment == '' and id_continue == '':
                    # print("Parent :", rblock)
                    mmass       = id_mass.strip()
                    misotope    = id_symbol.strip()
                    mother      = rblock[:5].strip()
                    spin_parity = rblock[21:39].strip()
                    thalf_life   = list(rblock[39:49].strip().split())
                    qval        = rblock[64:74].strip()
                    # print("DECAY Block:",mblock[0])
                    # print("Parent :", rblock)
                    # print("Mother Mass:",mmass)
                    # print("Mother Isotope:",misotope)
                    # print("Spin Parity:",spin_parity)
                    # print("Q-value:",qval)
                    # print("Half Life:",thalf_life)
                    info_parent.update({'mmass':mmass, 'misotope':misotope, 'mother':mother, 'spin_parity':spin_parity, 'qval':qval})

                    ### Half Life Check
                    lh = len(thalf_life)
                    if len(thalf_life) == 0:
                        half_life = -999.0
                        half_lifeu = 'UNKNOWN'
                        # half_life = [-999.0, 'UNKNOWN']
                        # print("Unknown Half Life")
                        info_parent.update({'life':half_life, 'lifeu':half_lifeu})
                    if  thalf_life == 'STABLE':
                        half_life = -888.0
                        half_lifeu = 'STABLE'
                        # half_life = [-999.0, 'STABLE']
                        # print("Stable Nuclei")
                        info_parent.update({'life':half_life, 'lifeu':half_lifeu})
                    if lh == 2:
                        half_life = thalf_life[0]
                        half_lifeu = thalf_life[1]
                        # print("Normal Half Life")
                        # print("Half Life:",half_life[0])
                        # print("Half Life Dim:",half_life[1])
                        info_parent.update({'life':half_life, 'lifeu':half_lifeu})
                
                ### Level Line Number Check
                if id_type == 'L' and id_comment == '' and id_continue == '':
                    level.append(lnum)
                    # print("Level :", k)
                    # print("test level :", rblock)
                    # level_energy = rblock[9:19].strip()
                    # level_spin   = rblock[21:39].strip()
                    # print("Level Energy:",level_energy)
                    # print("Level Spin:",level_spin)
                    # print("Level Number:",lnum)
            
            lnum += 1
            ##################################################################
        
        ##### Level Information
        ## print("Level Information:",level)
        clevel = len(level)
        # print("Number of Level:",clevel)
        if not level:
            continue
        
        ###################################################################
        #### Loop for Level
        ###################################################################
        #### 각 Level 마다 
        print("level",level)
        for j in level:
        # for j in range(clevel):
            # print("--------------------------------------")
            rblock = copy.deepcopy(mblock[j])
            print("rblock : ", rblock)
            print("number of mblock : ", len(mblock))
            # rblock = copy.deepcopy(mblock[level[j]])
            level_energy = rblock[9:19].strip()
            level_spin   = rblock[21:39].strip()
            level_decay  = rblock[39:49].strip().split()
            # print("Level : ", mblock[j])
            # print("Level : ", mblock[level[j]])
            # print("Level Energy:",level_energy)
            # print("Level Spin:",level_spin)
            # print("--------------------------------------")
            if not level_decay:
                rlevel_decay = [-999.0, 'UNKNOWN']
                # print("Unknown Half Life")
            elif level_decay[0] == '?':
                rlevel_decay = [-999.0, 'UNKNOWN']
            elif level_decay[0] == 'STABLE':
                rlevel_decay = [-888.0, 'STABLE']
                # print("Stable Nuclei")
            else:
                rlevel_decay = level_decay
                # print("Normal Half Life")
            # print("Level Decay:",level_decay)
            # print("rLevel Decay:",rlevel_decay)
            info_level.update({'level':level_energy, 'l_spin':level_spin, 'l_life':rlevel_decay[0], 'l_lifeu':rlevel_decay[1]})
           
            ### Level이 있을 때, beta, gamma 등 확인
            ### nmblock: 해당 block의 길이
            k = 1
            # print("nmblock : ", nmblock)
            while True:
                if j+k == nmblock:
                    print("***END: Out of Range", k)
                    break
                lblock = copy.deepcopy(mblock[j+k])
                llblock = len(lblock)
                if llblock < 8:
                    print("***Skip: short",k)
                    k += 1
                    continue
                if lblock[7] == 'L' and lblock[6] == ' ' and lblock[8] == ' ':
                    print("***END: New Level Start",k)
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
                        print("Beta End Energy:",beta_end)
                        print("Beta Intensity:",beta_int)
                        print("Beta Logft:",beta_logft)
                        info_beta.update({'beta_end':beta_end, 'beta_int':beta_int, 'beta_logft':beta_logft})
                    # if id_continue == 'S':
                    # # if lblock[5] == 'S':
                    #     # print("Beta DTYPE :", lblock)
                    #     beta_ave  = list(lblock[9:29].strip().split('='))
                    #     ba = len(beta_ave)
                    #     # print("Beta 'S' length:",ba)
                    #     # print("Beta Average Energy:",beta_ave)
                    #     if ba == 2:
                    #         beta_ave  = beta_ave[1].split(' ')
                    #         print("Beta Average Energy:",beta_ave[0])
                    #         info_beta.update({'beta_ave':beta_ave[0]})
                    #     else:
                    #         beta_ave  = list(beta_ave[0].split(' '))
                    #         print("Beta Average Energy:",beta_ave[0])
                    #         if 'AP' in beta_ave:
                    #             beta_ave.remove('AP')
                    #         print("Beta Average Energy:",beta_ave[1])
                    #         info_beta.update({'beta_ave':beta_ave[1]})
    
                ### Gamma Information
                if id_type == 'G' and id_comment == '': 
                    if id_continue == '':
                # if lblock[7] == 'G' and lblock[6] == ' ': 
                #     if lblock[5] == ' ':
                        print("Gamma :", lblock)
                        g_energy    = lblock[9:19].strip()
                        g_relint    = lblock[21:29].strip()
                        g_multran   = lblock[31:41].strip()
                        g_mixratio  = lblock[41:49].strip()
                        g_totconv   = lblock[55:62].strip()
                        g_rttint    = lblock[64:74].strip()
                        print("Gamma Energy:",g_energy)
                        print("Gamma Intensity:",g_relint)
                        print("Gamma Multipolarity of transition:",g_multran)
                        print("Gamma Mixing ratio:",g_mixratio)
                        print("Gamma Total Conversion Coefficient:",g_totconv)
                        print("Gamma Relative Total Transition Intensity:",g_rttint)
                        info_gamma.update({'gamma':g_energy, 'g_rint':g_relint, 'g_mtran':g_multran, 'g_mratio':g_mixratio, 'g_tconv':g_totconv, 'g_rttint':g_rttint})
                    
                    #if id_continue == 'S':
                    #    # print("Gamma DTYPE:", lblock)
                    #    gtemp  = lblock[9:].split('$')
                    #    gtemp  = list(filter(None, gtemp))
                    #    ngtemp = len(gtemp)
                    #    # print("Gamma 'S' test:",gtemp)
                    #    # print("Gamma 'S' num test:",ngtemp)
                    #    ### Sub-Gamma Information
                    #    a = 0
                    #    while a < ngtemp:
                    #       # print("Gamma 'S' test:",gtemp[a])
                    #        ### Split with '='
                    #        temp2 = gtemp[a].split('=')
                    #        temp2 = list(filter(None, temp2))
                    #        # print("Gamma 'S' test2:",temp2)
                    #        ##
                    #        b = len(temp2)
                    #        # print("test length", b)
                    #        ##
                    #        if b == 2:
                    #            # print("Gamma Sub DTYPE:",temp2[0].strip())
                    #            temp4 = temp2[1].split(' ')
                    #            # print("test temp4 : ", temp4)
                    #            temp4 = list(filter(None, temp4))
                    #            # print("test temp4 : ", temp4)
                    #            # print("Gamma Sub DTYPE Val",temp4[0].strip())
                    #            # print("test temp4 : ", temp4)
                    #            info_gamma_sub.update({'gDTYPE':temp2[0].strip(), 'gDTYPEv':temp4[0].strip()})
                    #        else:
                    #            # print("Gamma Sub DTYPE:",temp2[0].strip())
                    #            temp4 = temp2[0].split(' ')
                    #            if 'AP' in temp4:
                    #                temp4.remove('AP')
                    #            # print("Gamma Sub DTYPE:",temp4[0].strip())
                    #            # print("Gamma Sub DTYPE Val:",temp4[1].strip())
                    #            info_gamma_sub.update({'gDTYPE':temp4[0].strip(), 'gDTYPEv':temp4[1].strip()})

                    #        # if 'AP' in temp4:
                    #        #     temp4.remove('AP')
                    #        # print("test temp4 : ", temp4)
                    #        # print("Gamma Sub DTYPE Val",temp4[0].strip())
                    #        a += 1

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
                    
                    # if id_continue == 'S':
                    #     # print("EC :", lblock)
                    #     etemp  = lblock[9:].split('$')
                    #     etemp  = list(filter(None, etemp))
                    #     # print("EC 'S' test:",etemp)
                    #     netemp = len(etemp)
                    #     # print("EC 'S' num test:",netemp)
                    #     a = 0
                    #     while a < netemp:
                    #         temp2 = etemp[a].split('=')
                    #         # print("EC Sub DTYPE:",temp2)
                    #         print("EC Sub DTYPE:",temp2[0].strip())
                    #         temp3 = temp2[1].lstrip()
                    #         temp4 = temp3.split(' ')
                    #         # print("EC Sub DTYPE Val",temp4)
                    #         # print("EC Sub DTYPE Val",temp4[0].strip())
                    #         # ec_ave = lblock[13:19].strip()
                    #         # print("EC else test : ", lblock)
                    #         # print("EC Average Energy:",ec_ave)
                    #         info_ec_sub.update({'ecDTYPE':temp2[0].strip(), 'ecDTYPEv':temp4[0].strip()})
                    #         a += 1

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
                cur.execute("INSERT INTO decay (daughter, dmass, disotope, mmass, misotope, mother, decay, spin, life, lifeu, qval, level, l_spin, l_life, l_lifeu, gamma, g_rint, g_mtrans, g_mratio, g_tconv, g_rttint, gDTYPE, gDTYPEv, beta_end, b_int, b_logft, beta_ave, ec, ec_bint, ec_int, ec_logft, ec_tint, ecDTYPE, ecDTYPEv, alpha, a_int, a_hf, d_particle, delayed, d_int, d_elevel, d_width, d_ang) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);" , (info_daughter['daughter'],info_daughter['dmass'],info_daughter['disotope'],info_parent['mmass'],info_parent['misotope'],info_parent['mother'],info_daughter['decay'],info_parent['spin_parity'],info_parent['life'],info_parent['lifeu'],info_parent['qval'],info_level['level'],info_level['l_spin'],info_level['l_life'],info_level['l_lifeu'],info_gamma['gamma'],info_gamma['g_rint'],info_gamma['g_mtrans'],info_gamma['g_mratio'],info_gamma['g_tconv'],info_gamma['g_rttint'],info_gamma_sub['gDTYPE'],info_gamma_sub['gDTYPEv'],info_beta['beta_end'],info_beta['b_int'],info_beta['b_logft'],info_beta['beta_ave'],info_ec['ec'],info_ec['ec_bint'],info_ec['ec_int'],info_ec['ec_logft'],info_ec['ec_tint'],info_ec_sub['ecDTYPE'],info_ec_sub['ecDTYPEv'],info_alpha['alpha'],info_alpha['a_int'],info_alpha['a_hf'],info_delayed['d_particle'],info_delayed['delayed'],info_delayed['d_int'],info_delayed['d_elevel'],info_delayed['d_width'],info_delayed['d_ang']))
        ### End of Level loop

    ### End of file loop
    in_file.close()

#####Commit & Close DB
con.commit()
con.close()

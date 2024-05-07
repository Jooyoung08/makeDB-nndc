import sqlite3

#DB Creation
con = sqlite3.connect('./nndc-20240507.db')
cur = con.cursor()

#Table Creation
cur.execute("create table decay (daughter text, dmass int, disotope text, mother text, mmass int, misotope text, dmode text, spin text, hlife real, hlifed text, qval real, genergy real, gint real, bendenergy real, bint real, baveenergy real, ecenergy real, ecbpint real, ecint real, ectotint real, ecaveenergy real, aenergy real, aint real);")

#Read ENSDF
for filenum in range(1, 300):
    #filenum을 XXX로 표시
    nfile = format(filenum, '03')
    in_file = open("./ensdf_240402/ensdf.{}".format(nfile), "r")
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print("File Number: ", filenum)
    lines = in_file.readlines()
    print("Line Number: ", len(lines))
    number = 0
    linenumber = []
    for line in lines:
        number += 1

        #Decay Search - Head
        head = line[5:9]
        if head != "    ":
            continue
    
        #NUCID, Nuclide identification, Mass & element
        daughter    = line[0:5].strip()
        dmass       = line[0:3].strip()
        disotope    = line[3:5].strip()

        #Decay Search
        decay = line[9:39].split()
        decay = tuple(decay)
        if len(decay)>2 and decay[2] == "DECAY":
            linenumber.append(number-1)
            mother      = decay[0]
            decay_mode  = decay[1]
            mmass       = line[9:12].strip()
            misotope    = line[12:14].strip()
            # print(mother, mmass, misotope, daughter, dmass, disotope, decay_mode)

##################################################
            #Parent Detail
            pnum = 0
            while number+pnum<len(lines):
                parent = lines[number+pnum]
                parent_check = parent[5:9].strip()
                if parent_check == "P":
                    spin_parity = parent[21:39].strip()
                    # halflife    = parent[39:49].split()
                    halflife    = parent[39:49].strip()
                    print("RAW halflife: ", halflife)
                    if halflife == "":
                        halflife = ["0", "NA"]
                    else:
                        halflife = halflife.split()
                    print("Half life (list): ", halflife)
                    if len(halflife) < 2:
                        halflife = ["0", "NA"]
                    halflife    = tuple(halflife)
                    qvalue      = parent[64:74].strip()
                    if qvalue == "":
                        qvalue = 0
                    print('--------------------------------------------')
                    print("Half life (tuple): ", halflife)
                    print("Parent Nucl: ", mother, "| Daughter Nucl: ", daughter, "| Decay Mode: ", decay_mode)
                    print("Spin Parity: ", spin_parity, "| Halflife: ", halflife[0], "Halflife Dim.: ", halflife[1], "| Q-value: ", qvalue)
                    pnum = 1
                    break
                else:
                    pnum += 1
##################################################
            #Gamma Search
            gnum = 1
            while number+gnum<len(lines):
                gamma = lines[number+gnum]
                if gamma == "\n":
                    break
                gamma_check = gamma[5:9].strip()
                if gamma_check == "G":
                    g_energy = gamma[9:19].strip()
                    if g_energy == "":
                        g_energy = "0"
                    g_int    = gamma[21:29].strip()
                    if g_int == "":
                        g_int = "0"
                    print("Gamma Energy: ", g_energy, "| Gamma Intensity: ", g_int)
                    cur.execute("INSERT INTO decay (daughter, dmass, disotope, mother, mmass, misotope, dmode, spin, hlife, hlifed, qval, genergy, gint) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);" , (daughter, dmass, disotope, mother, mmass, misotope, decay_mode, spin_parity, halflife[0], halflife[1], qvalue, g_energy, g_int))
                    gnum += 1
                if gamma_check == "":
                    break
                else:
                    gnum += 1
##################################################
            #Beta Search
            bnum = 1
            bnum2= 0
            while number+bnum<len(lines):
                beta = lines[number+bnum]
                if beta == "\n":
                    break
                beta_check = beta[5:9].strip()
                if beta_check == "B":
                    b_end_energy = beta[9:19].strip()
                    if b_end_energy == "":
                        b_end_energy = "0"
                    b_int     = beta[21:29].strip()
                    if b_int        == "":
                        b_int        = "0"
                    print("Beta Energy: ", b_end_energy, "| Beta Int: ", b_int)
                    cur.execute("INSERT INTO decay (daughter, dmass, disotope, mother, mmass, misotope, dmode, spin, hlife, hlifed, qval, bendenergy, bint) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);" , (daughter, dmass, disotope, mother, mmass, misotope, decay_mode, spin_parity, halflife[0], halflife[1], qvalue, b_end_energy, b_int))
                    while number+bnum<len(lines):
                        beta_add     = lines[number+bnum2]
                        if beta_add == "\n":
                            break
                        beta_add2    = beta_add[5:9].replace(" ","")
                        # print("Beta_add2", beta_add2)
                        if beta_add2 == "SB": 
                            b_ave_energy = beta_add[13:19].strip()
                            if b_ave_energy == "":
                                b_ave_energy = 0
                            print("Beta Ave Energy: ", b_ave_energy)
                            cur.execute("INSERT INTO decay (daughter, dmass, disotope, mother, mmass, misotope, dmode, spin, hlife, hlifed, qval, bendenergy, bint, baveenergy) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);" , (daughter, dmass, disotope, mother, mmass, misotope, decay_mode, spin_parity, halflife[0], halflife[1], qvalue, b_end_energy, b_int, b_ave_energy))
                            break
                        else:
                            bnum2 += 1
                    break
                else:
                    bnum += 1

##################################################
            #EC Search
            enum = 1
            enum2= 0
            while number+enum<len(lines):
                ec = lines[number+enum]
                if ec == "\n":
                    break
                ec_check = ec[5:9].strip()
                if ec_check == "E":
                    ec_energy = ec[9:19].strip()
                    if ec_energy == "":
                        ec_energy = 0
                    ec_bp_int    = ec[21:29].strip()
                    if ec_bp_int == "":
                        ec_bp_int = 0
                    ec_int       = ec[31:39].strip()
                    if ec_int == "":
                        ec_int = 0
                    ec_tot_int = ec[64:74].strip()
                    if ec_tot_int == "":
                        ec_tot_int = 0
                    print("EC Energy: ", ec_energy, "| EC b+ Int: ", ec_bp_int, "| EC Int: ", ec_int, "| EC Tot. Int: ", ec_tot_int)
                    cur.execute("INSERT INTO decay (daughter, dmass, disotope, mother, mmass, misotope, dmode, spin, hlife, hlifed, qval, ecenergy, ecbpint, ecint, ectotint) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);" , (daughter, dmass, disotope, mother, mmass, misotope, decay_mode, spin_parity, halflife[0], halflife[1], qvalue, ec_energy, ec_bp_int, ec_int, ec_tot_int))
                    while number+enum2<len(lines):
                        ec_add     = lines[number+enum2]
                        if ec_add == "\n":
                            break
                        ec_add2    = ec_add[5:9].replace(" ","")
                        ec_add3    = ec_add[9:12].rstrip()
                        if ec_add2 == "SE" and ec_add3 == "EAV": 
                            ec_ave_energy = ec_add[13:19].strip()
                            if ec_ave_energy == "":
                                ec_ave_energy = 0
                            print("EC Ave Energy: ", ec_ave_energy)
                            cur.execute("INSERT INTO decay (daughter, dmass, disotope, mother, mmass, misotope, dmode, spin, hlife, hlifed, qval, ecenergy, ecbpint, ecint, ectotint, ecaveenergy) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);" , (daughter, dmass, disotope, mother, mmass, misotope, decay_mode, spin_parity, halflife[0], halflife[1], qvalue, ec_energy, ec_bp_int, ec_int, ec_tot_int, ec_ave_energy))
                            break
                        else:
                            enum2 += 1
                    break
                else:
                    enum += 1
#################################################################
            #Alpha Search
            anum = 1
            while number+anum<len(lines):
                alpha = lines[number+anum]
                if alpha == "\n":
                    break
                alpha_check = alpha[5:9].strip()
                if alpha_check == "A":
                    a_energy = alpha[9:19].strip()
                    if a_energy == "":
                        a_energy = 0
                    a_int    = alpha[21:29].strip()
                    if a_int == "":
                        a_int = 0
                    print("Alpha Energy: ", a_energy, "| Alpha Int: ", a_int)
                    cur.execute("INSERT INTO decay (daughter, dmass, disotope, mother, mmass, misotope, dmode, spin, hlife, hlifed, qval, aenergy, aint) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);" , (daughter, dmass, disotope, mother, mmass, misotope, decay_mode, spin_parity, halflife[0], halflife[1], qvalue, a_energy, a_int))
                    anum += 1
                else:
                    anum += 1
##################################################
    #file close
    in_file.close()

#Commit & Close DB
con.commit()
con.close()

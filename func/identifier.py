def identifier(testblock):

    ### Record Type of ENSDF
    id_mass     = testblock[:3].strip()
    id_symbol   = testblock[3:5].strip()
    id_continue = testblock[5].strip()
    id_comment  = testblock[6].strip()
    id_type     = testblock[7].strip()

    # if id_type == 'P':
    #     print("ID Type: Parent")
    # if id_type == 'B':
    #     print("ID Type: Beta-")
    # if id_type == 'G':
    #     print("ID Type: Gamma")
    # if id_type == 'E':
    #     print("ID Type: EC/beta+")
    # if id_type == 'H':
    #     print("ID Type: History")
    # if id_type == 'R':
    #     print("ID Type: Reference")
    # if id_type == 'X':
    #     print("ID Type: Cross Reference")
    # if id_type == 'Q':
    #     print("ID Type: Q-value")
    # if id_type == 'N' and id_comment == '':
    #     print("ID Type: Normalization")
    # if id_type == 'N' and id_comment == 'P':
    #     print("ID Type: Production Normalization")
    # if id_type == 'L':
    #     print("ID Type: Level")
    # if id_type == 'A':
    #     print("ID Type: Alpha")
    # if id_type == 'D':
    #     print("ID Type: Delayed")
    # # else:
    # #     print("ID Type: unknown")

    return id_mass, id_symbol, id_continue, id_comment, id_type

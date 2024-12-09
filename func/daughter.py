def daughter(testblock):
    dmass = testblock[0][:3].strip()
    daughter = testblock[0][:5].strip()
    disotope = testblock[0][3:5].strip()
    decay = testblock[0][12:14].strip()

    return dmass, daughter, disotope, decay

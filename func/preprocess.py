import copy

def find_decay(testblock):
    t_block = copy.deepcopy(testblock[0]).split()

    if 'DECAY' in t_block:
        return testblock
    else:
        return None


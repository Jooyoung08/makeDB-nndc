import copy

def line_modifier(testlines):
    new_line = []
    blank_line = []
    line_number = 0
    for line in testlines:
        ### line에서 오른쪽 공백 제거
        line = line.rstrip()
        new_line.append(line)
        ### line이 공백인 경우 line_number를 blank_line에 추가
        if not line:
            blank_line.append(line_number)
        line_number += 1
    return new_line, blank_line

def find_decay(testblank, testline):
    nn = 0
    dblock = []
    for i in testblank:
        ### 첫 block은 blank가 없으므로, 첫 block을 따로 처리
        if nn == 0:
            ### block의 첫 index 부터 i-1 index까지를 block에 저장
            ### 하나의 block 정보가 리스트 형태로 저장
            block = testline[:i]
        else:
            ### 나머지 block은 blank 다음부터 시작
            ### blank_number[nn-1]+1 index 부터 i-1 index까지를 block에 저장
            block = testline[testblank[nn-1]+1:i]
        nn += 1

        ### block의 첫 줄을 확인하여 DECAY가 있는지 확인
        ### block의 첫 줄을 복사
        t_block = copy.deepcopy(block[0]).split()
        ### DECAY가 있는 block만 전체 block을 dblock에 추가
        if 'DECAY' in t_block:
            dblock.append(block)
        else:
            continue
    return dblock

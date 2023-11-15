import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
#from collections import deque

def run(indata):
    L = indata.split('\n\n')
    
    count = 0
    for l in L:
        fields = [f.split(':')[0] for f in l.replace('\n', ' ').split(' ')]

        if 'byr' not in fields:
            continue
        elif 'iyr' not in fields:
            continue
        elif 'eyr' not in fields:
            continue
        elif 'hgt' not in fields:
            continue
        elif 'hcl' not in fields:
            continue
        elif 'ecl' not in fields:
            continue
        elif 'pid' not in fields:
            continue
        elif 'cid' not in fields:
            print('missing cid... ignore')
        count += 1

    print("Part 1: {}".format(count))
    clipboard_set("{}".format(count))

    # ----------- PART 2 -----------
    #
    count = 0
    for l in L:
        fields = dict()
        for f in l.replace('\n', ' ').split(' '):
            if len(f) > 0:
                fields[f.split(':')[0]] = f.split(':')[1]

        if 'byr' not in fields:
            continue
        elif 'iyr' not in fields:
            continue
        elif 'eyr' not in fields:
            continue
        elif 'hgt' not in fields:
            continue
        elif 'hcl' not in fields:
            continue
        elif 'ecl' not in fields:
            continue
        elif 'pid' not in fields:
            continue
        elif 'cid' not in fields:
            print('missing cid... ignore')
        

        if len(fields['byr']) != 4 or int(fields['byr']) < 1920 or int(fields['byr']) > 2002:
            continue
        
        if len(fields['iyr']) != 4 or int(fields['iyr']) < 2010 or int(fields['iyr']) > 2020:
            continue
        
        if len(fields['eyr']) != 4 or int(fields['eyr']) < 2020 or int(fields['eyr']) > 2030:
            continue
        
        if not fields['hgt'].endswith('cm') and not fields['hgt'].endswith('in'):
            continue
        elif fields['hgt'].endswith('cm') and ( int(fields['hgt'][:-2]) < 150 or int(fields['hgt'][:-2]) > 193 ):
            continue
        elif fields['hgt'].endswith('in') and ( int(fields['hgt'][:-2]) < 59 or int(fields['hgt'][:-2]) > 76 ):
            continue
        
        if not fields['hcl'].startswith('#') or len(fields['hcl']) != 7:
            continue
        elif any([(c < '0' or '9' < c) and (c < 'a' or 'f' < c) for c in fields['hcl'][1:]]):
            continue
        
        if fields['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            continue

        if len(fields['pid']) != 9 or any([(c < '0' or '9' < c) for c in fields['pid']]):
            continue

        count += 1
    
    answer = count
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=4, year=2020)
    run(indata)


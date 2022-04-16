import copy
import os
import time

import argparse
import json
import pickle

import lz4.block
import numpy as np
from sty import fg, bg, ef, rs

LOCAL_MAP_SIZE = 15

def print_canvas(data_map, data_frame, focus_id=9999):

    dmap = copy.deepcopy(data_map)
    h, w = len(dmap), len(dmap[0])
    cx, cy = -1, -1
    
    for idx, val in data_frame['player'].items():
        if int(idx) == focus_id:
            cx = val['base']['c']
            cy = val['base']['r']
            
        xx = val['base']['c']
        yy = val['base']['r']

        hp_ratio = float(val['resource']['health']['val'])/float(val['resource']['health']['max'])
        if hp_ratio <= 0.5:
            label = chr(ord('a')+val['base']['population'])
        else:
            label = chr(ord('A')+val['base']['population'])
            
        if val['status']['freeze'] != 0:
            label += 'f'
        elif 'attack' in val['history']:
            label += val['history']['attack']['style'][0]
        else:
            label += ' '
        
        dmap[yy][xx] = fg(10+val['base']['population'])+label+fg.rs

    for idx, val in data_frame['npc'].items():
        if int(idx) == focus_id:
            cx = val['base']['c']
            cy = val['base']['r']

        xx = val['base']['c']
        yy = val['base']['r']

        hp_ratio = float(val['resource']['health']['val'])/float(val['resource']['health']['max'])
        if hp_ratio <= 0.5:
            label = val['base']['name'][0].lower()
        else:
            label = val['base']['name'][0]
            
        if val['status']['freeze'] != 0:
            label += 'f'
        elif 'attack' in val['history']:
            label += val['history']['attack']['style'][0]
        else:
            label += ' '

        dmap[yy][xx] = fg.red+label+fg.rs
        
    if focus_id > 999:
        canvas = ''

        for yy in range(h):
            for xx in range(w):
                ele = dmap[yy][xx]
                if type(ele) == str:
                    canvas += ele
                elif ele in [0]:
                    canvas += '  '
                elif ele in [1]:
                    canvas += '. '
                elif ele in [2]:
                    canvas += '  '
                elif ele in [3]:
                    canvas += '  '
                elif ele in [4]:
                    canvas += '  '
                elif ele in [5]:
                    canvas += '. '
                elif ele in [6]:
                    canvas += '  '
                else:
                    canvas += '  '
            canvas += '\n'
    else:
        canvas = ''


        for yy in range(LOCAL_MAP_SIZE*2+1):
            for xx in range(LOCAL_MAP_SIZE*2+1):
                ele = dmap[cy+yy-LOCAL_MAP_SIZE][cx+xx-LOCAL_MAP_SIZE]
                if type(ele) == str:
                    canvas += ele
                elif ele in [0]:
                    canvas += '  '
                elif ele in [1]:
                    canvas += '. '
                elif ele in [2]:
                    canvas += '  '
                elif ele in [3]:
                    canvas += '  '
                elif ele in [4]:
                    canvas += '  '
                elif ele in [5]:
                    canvas += '. '
                elif ele in [6]:
                    canvas += '  '
                else:
                    canvas += '  '
            canvas += '\n'

    print(canvas)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('filename', type=str, help='name of replay')
    parser.add_argument('--focus_id', type=int, default=9999, help='agent id, default 9999')
    args = parser.parse_args()

    filename = args.filename
    focus_id = args.focus_id

    if filename.split('.')[-1] == 'json':
        data = json.load(open(filename))
    elif filename.split('.')[-1] == 'replay':            
        with open(filename, 'rb') as fp:
            dt = fp.read()
            data = pickle.loads(lz4.block.decompress(dt))
    else:
        raise NotImplementedError('file type does not not support.')

    for ii in range(len(data['packets'])-1):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_canvas(data['map'], data['packets'][1+ii], focus_id)

        print('\tTime: {}\t AgentID: {}'.format(ii, focus_id))
        time.sleep(0.1)
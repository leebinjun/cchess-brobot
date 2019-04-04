# -*- coding: utf-8 -*-
# 中国象棋电脑应用规范(五)：中国象棋通用引擎协议 http://www.xqbase.com/protocol/cchess_ucci.htm

import importlib
import re
import sys
import time

import sys
sys.path.append(r".\strategy\moonfish")
from moonfish import *
import tools

# position fen rCbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/7C1/9/RNBAKABNR b - - 0 1
# go time 500 depth 5
class StrategyMoonfish:

    def __init__(self):
        # print name of chess engine
        self.pos = tools.parseFEN('2ba3r1/5k3/b8/1n3N2C/4p4/3R2R2/9/5p1r1/4p4/5K3 w moves d4d8 d9e8 f6d7 b6d7 g4f4 d7f6 f4f6')#tools.FEN_INITIAL)
        self.searcher = Searcher()
        self.forced = False
        self.our_time, self.opp_time = 1000, 1000 # time in centi-seconds
        self.stack = []
        print('Moonfish')

    def get_move(self, position = "rCbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/7C1/9/RNBAKABNR", 
                 player = "b", times = 1000, depth = 6, show_thinking = 1):   
        
        smove = "position fen " + position + " " + player + " - - 0 1"
        params = smove.split(' ', 2)
        if params[1] == 'fen':
            fen = params[2]
            pos = tools.parseFEN(fen)
            color = RED if fen.split()[1] == 'w' else BLACK

        smove = "go time " + str(times) + " depth " + str(depth)
          
        if smove.startswith('go'):
            #  default options
            # depth = depth
            movetime = -1

            # parse parameters
            params = smove.split(' ')
            if len(params) == 1: return

            i = 0
            while i < len(params):
                param = params[i]
                if param == 'depth':
                    i += 1
                    depth = int(params[i])
                if param == 'time':
                    i += 1
                    movetime = int(params[i])
                i += 1

            forced = False

            moves_remain = 40

            start = time.time()
            ponder = None
            for s_score in self.searcher._search(pos):
                moves = tools.pv(self.searcher, pos, include_scores=False)

                if show_thinking:
                    entry = self.searcher.tp_score.get((pos, self.searcher.depth, True))
                    score = int(round((entry.lower + entry.upper)/2))
                    usedtime = int((time.time() - start) * 1000)
                    moves_str = moves #if len(moves) < 15 else ''
                    print('info depth {} score {} time {} nodes {} pv {}'.format(self.searcher.depth, score, usedtime, self.searcher.nodes, moves_str))

                if len(moves) > 5:
                    ponder = moves[1]
                
                #将军死和被将军死 才会出现MATE_UPPER的值
                if (s_score >= MATE_UPPER) or (s_score <= -MATE_UPPER): 
                    break
            
                if movetime > 0 and (time.time() - start) * 1000 > movetime:
                    break

                if self.searcher.depth >= depth:
                    break

            entry = self.searcher.tp_score.get((pos, self.searcher.depth, True))
            m, s = self.searcher.tp_move.get(pos), entry.lower
            # We only resign once we are mated.. That's never?
            if s == -MATE_UPPER:
                print('resign')
            else:
                moves = moves.split(' ')
                if show_thinking:
                    if len(moves) > 1:
                        print('bestmove ' + moves[0] + ' ponder ' + moves[1])
                    else:
                        print('bestmove ' + moves[0])
        return moves[0]

if __name__ == '__main__':
    amoonfish = StrategyMoonfish()
    situation = "rCbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/7C1/9/RNBAKABNR"
    move = amoonfish.get_move(position=situation, show_thinking = False)
    print(move)




# rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1
# go time 1000 increment 0
'''
Moonfish
1554391592.142086
input: rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1
1554391609.3560708
1554391609.3560708
input: go time 1000 increment 0
1554391686.868504
info depth 1 score 10953 time 9 nodes 62 pv d4d8
info depth 2 score -38 time 45 nodes 303 pv d4d8 f8f9 i6b6
info depth 3 score 10971 time 98 nodes 675 pv d4d8 f8f9 d8d9
info depth 4 score -8 time 374 nodes 1876 pv d4d8 f8f9 d8d9 f9f8 d9h9 h2h9 i6b6
info depth 5 score 10950 time 3090 nodes 17467 pv g4g8 f8f7 g8g7 f7f8 g7g8 loop
bestmove g4g8 ponder f8f7
1554391689.959681
'''
'''

TicTacToe game implementation

MIT License
Copyright (c) 2019 Daniel Marchasin (daniel@vt77.com)
See LICENSE file 

'''

import logging

win_lines = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
]

logger = logging.getLogger(__name__)



class TicTacToeGame():
    def __init__(self,board):
        self.board = board
        self.winline = None       
        self.finished,self.winner = self._finished()

    @staticmethod
    def creategame():
        logger.info("Create new game")
        return [0,0,0,0,0,0,0,0,0]

    def _finished(self):

        winner = None

        for i,line in enumerate(win_lines):
            winner_score = 0
            for p in line:
                winner_score = winner_score + self.board[p]
 
            if winner_score == -3:
                self.winline = i
                return (True,-1)
 
            if winner_score == 3:
                self.winline = i
                return (True,1)
        
        busy = 0
        for i in range(0,9):
            if self.board[i] != 0:
                busy = busy + 1

        return (busy==9,None)

    def move(self,player,move):
       logger.info("Make move . Player %s Move %s" % (player,move))
       if self.board[move] != 0:
            raise Exception('Illegal move')
       self.board[move] = player
       self.finished,self.winner = self._finished()
       logger.info("New state %s" % self )
       return self.board


    def __str__(self):
        return "Board %s. Finished : %s . Winner %s (%s)" % (self.board, self.finished, self.winner, self.winline )    

    

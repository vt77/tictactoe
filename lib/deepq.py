#!/usr/bin/python3
'''

Simple q-learning algorithm implementation

MIT License
Copyright (c) 2019 Daniel Marchasin (daniel@vt77.com)
See LICENSE file 

'''


import random
import logging
import pickle

dataset = {}
history = []

model_filename = 'data/.deepq.pickle'
logger = logging.getLogger(__name__)

try:
    dataset = pickle.load( open( model_filename , "rb" ) )
except FileNotFoundError:
    pickle.dump( dataset , open( model_filename , "wb" ) )

def get_features(data,act):
    features_bin  = 0
    board = data.copy()
    board[act] = 1
    for p in range(0,9):
        features_bin = features_bin << 2
        if board[p] == 1:
            features_bin = features_bin | 0x01
        if board[p] == -1:
            features_bin = features_bin | 0x02
    return features_bin


def rebuild_q_table(history,award):

    global dataset

    GRADIENT = 0.90
    gamma = 1
    logger.debug("[RECALCQ]Process award %s" % (award))
    data_list = pickle.load( open( model_filename , "rb" ) )

    for f in reversed(history):
       score = gamma * award;
       ''' Use simple moving avarage'''       
       logger.debug("[RECALCQ]Process history prev score %s(%s)" % (f,dataset.get(f,0)))
       dataset[f] = dataset.get(f,0) + score
       logger.debug("[RECALCQ]Process history %s Score %s(%s)" % (f,score,dataset[f]))
       gamma = gamma * GRADIENT
    
    pickle.dump( dataset , open( model_filename , "wb" ) )



def update_stats(board,winner):
    
    global history

    award = 0.5 #Draw is still good 
    if winner == 1:
        award = 1
    if winner == -1:
        award = -1

    rebuild_q_table(history,award)
    history.clear() 
     


def make_move(board):
    logger.debug("[MAKEMOVE]Process board : %s" % board)
    
    scores = []
    for p in range(0,9):
        if board[p] != 0:
                continue
        f = get_features(board,p)
        scores.append((p, dataset.get(f,0),f))
    
    best_score = max(scores,key=lambda tup: tup[1])[1]
    logger.debug("[MAKEMOVE]Scores : %s Max: %s"  % (scores,best_score) );
    actions = [ (p[0],p[2]) for p in scores if p[1] == best_score]
    #Curiosity makes me smarter.
    if best_score != 0:
        curiosity = [ (p[0],p[2]) for p in scores if p[1] > -1 and p[1] < best_score ]
        if(len(curiosity) > 0):
            logger.debug("[MAKEMOVE][CURIOSITY]Scores : %s"  % (curiosity) );
            actions = actions + curiosity
    #Select random from all avaliable moves
    logger.debug("[MAKEMOVE]Best : %s" % actions ) 
    act = random.choice (actions)
    history.append(int(act[1]))
    logger.debug("[MAKEMOVE]Selected action : %s" % act[0] )

    return act[0]

if __name__ == '__main__':

    import sys,os

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler( logging.StreamHandler(sys.stdout) )
    
    board = [-1,-1,-1,0,0,0,1,1,0]
    print( make_move(board)  )


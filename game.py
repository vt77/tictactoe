#!/usr/bin/python3

import os,sys
import logging
import json
import uwsgi
import uuid
import traceback
import hashlib

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

lh = logging.StreamHandler(sys.stdout)
lh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
lh.setFormatter(formatter)
logger.addHandler(lh)

dataset = {}

from lib import deepq as brain 
from lib.tictactoe import TicTacToeGame as gamehandler
from lib import storage

last_score_key = ''

def parse_input_json(env):
    request_body_size = int(env.get('CONTENT_LENGTH', 0))
    request_body = env['wsgi.input'].read(request_body_size)
    return json.loads(request_body.decode('utf-8'))


def get_best_score(game_data):

    bestscorecache = uwsgi.cache_get('bestscore')
    if bestscorecache is None:
          logger.debug('Load scores')
          scores = storage.get_top_scores(10) 
          uwsgi.cache_update('bestscore',json.dumps(scores).encode('utf-8'))
          bestscorecache = uwsgi.cache_get('bestscore')

    scorehash = hashlib.md5(bestscorecache).hexdigest()
    if scorehash != game_data.get('bestscore',''):
           logger.debug('Send new score to client')
           game_data['bestscore'] = scorehash
           return json.loads( bestscorecache.decode('utf-8') );

    return None
 

def update_best_scores(game_data):
    logger.debug('Update user score')
    storage.update_user_score(game_data['user_id'],game_data['score1'],game_data['score2'])
    uwsgi.cache_del('bestscore') #this will recalculate bestscores


def application(env, start_response):
    
    logger.info("[%s]Start new request" % env.get('HTTP_X_REAL_IP','IPUnknown') )
    input = parse_input_json(env)
    logger.debug("Got %s" % input )    
    

    data = {'success':'yes'}
    action = input.get('action','nop') 
    userinfo = None   
 
    try:

        if  action == 'token':
           '''
                Register user and generate token
           '''
 
           userinfo = input.get('userinfo') 
           if userinfo is None:
                raise Exception("Can not create token(1)")

           id =  userinfo.get('id')
           if id is None:
                raise Exception("Can not create token(2)")


           user_id  = storage.get_user_id(id)
           if user_id is None:
                user_id = storage.create_user(id,userinfo)

           '''
            Try to get sessions
           ''' 
           token = uwsgi.cache_get('usersession_%s' % user_id)
           if token is None:
                token = str(uuid.uuid1())
                game_data = {'counter':0,'user_id':user_id,'score1':0,'score2':0}
                input['start'] = 1
                uwsgi.cache_update(token,json.dumps(game_data).encode('utf-8'),600)
           else:
                token = token.decode('utf-8')

           ''' 
            Continue to action play
            If no "move" parameter present it will just return current board
            Good to recconect lost sessions (page refresh) 
           '''

           input['refresh'] = 1
           input['token'] = token
           action = 'play' 

        if action == 'play':
        
            '''
                1. Loads board
                2. Process move if any
            '''

            token = input.get('token',None)
            if token is None:
                raise Exception("Session expired")
         
            ''' Save token to client '''          
            data['token'] = token
            logger.info("Got token %s %s" % (token,hashlib.md5(token.encode('utf-8')).hexdigest()) )

            try: 

                game_data_str = uwsgi.cache_get(token).decode('utf-8')
                logger.info("Cached data %s" % (game_data_str) )
                game_data = json.loads(game_data_str)

            except Exception as e:
                logger.info("Session expired") 
                raise Exception("Session expired")

        
            user_id = game_data['user_id']


            if input.get('start'):
                    logger.info("Start new game")
                    game_data['board'] = gamehandler.creategame()

            game = gamehandler(game_data['board'])

            if input.get('refresh'):
                #Refresh UI
                if 'bestscore' in game_data:
                        game_data['bestscore'] = ''


            '''
            If there is a new move, process it
            '''
            move = input.get('move')
            if move is not None:
                ''' Process opponent's move '''
                logger.info("Process human move %s" % move)
                game_data['board'] = game.move(-1,move)
                if not game.finished:
                    ai_move  = brain.make_move(game_data['board']) 
                    game_data['board'] = game.move(1,ai_move)                

                if game.finished:
                    brain.update_stats(game_data['board'],game.winner)
                    if game.winner == -1:
                        game_data['score1'] = game_data['score1'] + 1
                    if game.winner == 1:
                        game_data['score2'] = game_data['score2'] + 1
                    update_best_scores(game_data)
 
            if game.finished:
                    if game.winner is not None:
                        data['winner'] = game.winner
                        data['winline'] = game.winline
 
            game_data['counter'] = storage.update_games_count(user_id,game_data['counter'] + 1 )         
 
            best_score = get_best_score(game_data)
 
            logger.info("New data to save %s" % game_data) 
            uwsgi.cache_update(token,json.dumps(game_data).encode('utf-8'),600)
            uwsgi.cache_update('usersession_%s' % user_id,token.encode('utf-8'),600)


            data['counter'] = game_data['counter'];
            data['board'] = game_data['board']
            data['score_h'] =  game_data['score1']
            data['score_ai'] = game_data['score2']
            data['finished'] = game.finished

            if best_score is not None:
                 data['bestscore'] = best_score

    except Exception as e:
        logger.error(traceback.format_exc())
        data = {'success':'no','error': str(e) }

    start_response('200 OK', [('Content-Type','application/json')])
    return [json.dumps(data).encode('utf-8')]

if __name__ == '__main__':
    env = dict(os.environ)
    print( application(env,lambda a,b : print( "Start response  : %s => %s" % (a,b) ) ) );

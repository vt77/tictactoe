'''

Storage helper class

MIT License
Copyright (c) 2019 Daniel Marchasin (daniel@vt77.com)
See LICENSE file 

'''



import os.path
import sqlite3
import logging


logger = logging.getLogger(__name__)

dbfilename = 'data/.gamedata.db'


if not os.path.isfile(dbfilename):
    with sqlite3.connect(dbfilename) as conn:
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,socialid varchar(128), name varchar(128),email varchar(128), image varchar(128),score_h integer,score_ai integer)")
        conn.execute("CREATE UNIQUE INDEX index_socialid ON users(socialid)")
        conn.execute("CREATE INDEX index_score ON users(score_h)")


def update_user_score(id,wins,loses):
    with sqlite3.connect(dbfilename) as conn:
        conn.execute("UPDATE users SET score_h=?,score_ai=? WHERE id=?",(wins,loses,id))   

def update_games_count(id,count):
    with sqlite3.connect(dbfilename) as conn:
        conn.execute("UPDATE users SET games_count=? where id=?",(count,id))
    return count

def create_user(socialid,user_data):
    user_id = None
    with sqlite3.connect(dbfilename) as conn:
        cur = conn.execute("INSERT INTO users (socialid,name,email,image,score_h,score_ai) VALUES (?,?,?,?,0,0)", (socialid,user_data['name'],user_data['email'],user_data['image']))
        user_id = cur.lastrowid
    return user_id


def get_user_id(social_id):
    logger.info("Getting user by SocialID %s" % social_id )
    with sqlite3.connect(dbfilename) as conn:
        cur = conn.execute("SELECT id,email FROM  users WHERE socialid=?",[social_id])
        if not cur:
            logger.info("[STORAGE]User not found. ID: %s" % social_id)
            return None
    
        row = cur.fetchone()
    if row is None:
        return None

    logger.info("[STORAGE]Found user : : %s ", row[1])
    return row[0]


def get_top_scores(num):
    with sqlite3.connect(dbfilename) as conn:
       cur = conn.execute("SELECT name,image,score_h,score_ai FROM users order by score_h desc limit 10")
       best_scores = [dict(zip(['name','image','score_h','score_ai'],list(s))) for s in cur]
    return best_scores

if __name__ == '__main__':

    import sys,os

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler( logging.StreamHandler(sys.stdout) )

    print(get_top_scores(10))


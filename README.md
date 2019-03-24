# TicTacToe ML

--- 
Simple pure python q-learning algorithm implementation


## Disclaimer

This repository just a sample was written to my presentation at ML Meetup. 
You may take ideas, but it's not intended to run in production environment.

## Reinforcement Learning
Is a kind of unsupervised ML where _agent_ communicating with _environment_ and learns to take _actions_ to earn best result
Optionally some curiosity behavour may be implemented to give agent a chance to explore best strategy.

__Q-Learning__ is a alghoritm (aka function) creating policy which tells agent what action can be performed in each environment state. Because agent cant't get score (and recaculate policy) immediatly after each action (move) it should "remember" all moves and states in the round and calculate _gradient_ of scores


## About TicTacToe implementation 
TicTacToe is a pure python implementation of Q-Learnig alghoritm. Used just for POC.

Because of not big number of unique combinations it stores all seen "positions" in python dictionary. 

The key is a _features vector_ build out of 3x3 squire board and packed to single integer.

The value is a gradiented score related to board state

Some curiosity implemented, so algoritm  can "improve" it's strategy during learning

### Installing and testing
To test algorithm simple game.py script included in this project

Installing as simple as install new uwsgi process if you know exactly what you do. Check ttt.ini for more info.

__Warning__ change user/group of running process. Running as root may make you system potencially vulnerable


* Clone repository 
* Point nginx _/tictactoe_ location to the root of cloned repository
* Configure _/tictactoe/ai_ location as proxy_pass to http://127.0.0.1:9092
* Make _data_ directory writebale for the script user
* Run run.sh in tmux session or any other way you like 
* Open in browser http://[_yourdomain|localhost_]/tictactoe

__Note:__ Google login may not work from your domain till you change google-signin-client_id meta in index.html 

 
__Nginx configuration example__

```nginx
    location ~/tictactoe
    {
    	root /var/www;
	    index index.html;
    }
    
    location ~/tictactoe/ai*
    {
        error_log  /var/log/nginx/tictactoe.error.log error;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://127.0.0.1:9092;
    }
```


## Results
We played with this alghoritm couple of hours. 
It was very impressive to see how algo learns and becomes a real player from kiddy randomizer
After about 1000 rounds the algo plays good enouph but still has many loses. 

Now it plays much better. You can try it by your self and  [__Play DEMO__](https://vt77.com/tictactoe)




## License
MIT license . You may use it for any purpose without warranty 

## Further learning 
[wikipedia Reinforcement_learning](https://en.wikipedia.org/wiki/Reinforcement_learning)

[wikipedia Q-learning](https://en.wikipedia.org/wiki/Q-learning)



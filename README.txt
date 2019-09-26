TowerJumpers:
A game made using python and compiled for the web using "Transcrypt". 


INSTALL:
Transcrypt: https://www.transcrypt.org/
Python3: https://python.org

BUILD:
Assuming you were able to install transcrypt successfully, you should be able to compile
the game code to javascript using the following command. 

transcrypt TowerJumpers.py


RUNNING: 
Because this is supposed to run in the browser, you will have to run a local webserver 
to be able to play the game. Fortunately, python3 already comes with a simple WebServer. 

python http.server 

open your favorite browser and point it to http://localhost:8000/index.html
if everything went right you should be able to play the game. 


HOW TO PLAY:
press space to jump to the upper level of the tower. Since the character auto runs it
can change direction only when it hits a wall. Try to go as high as possible. 

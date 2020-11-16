README

To run the code, type "python game.py" in the appropriate directory

The algorithm will prompt you to decide which side you want to play (Black or White). If W is typed you will play White and the AI will play Black. If B is typed, you will play Black and the AI will play White.

Entering invalid queries (Anything other than "B", "b", "W", or "w") will result in two AI's playing against each other.

At each turn, the game will return a list of valid moves that you can make. Enter the piece you want to move and where you want to move it in the following format: 
X1,Y1 X2,Y2

or for a starting move:
X1,Y1 0

For example, if the game says: 
Black move set [[(5, 3), (7, 3)], [(8, 8), (8, 6)], [(8, 8), (8, 4)]]

and you want to move the piece at (8,8) to (8,4), type:
8,8 8,4

If you want the AI to play against a player that plays random moves, comment out lines 205 to 209 and uncomment lines 188 to 202 in game.py
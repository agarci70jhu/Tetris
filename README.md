# Tetris
Developer: Angel Garcia Mejia

# Introduction
In Tetris, players complete lines by moving differently shaped pieces (tetrominoes), which descend onto the playing field. The completed lines disappear and grant the player points, and the player can proceed to fill the vacated spaces. The game ends when the uncleared lines reach the top of the playing field

# Class 1: Main
This class is the master class of the entire file. It is used to initialize and run other classes and is the only class that is ran in the if __name__ == '__main__': statement.

# Class 2: Game
This class is by the far the most important since it holds the logic behind how pieces move and keeping tracking of user inputs. It also is the foundational groundwork for the game functionality itself.

# Class 3: Tetromino
This class is used to create tetromino objects to represent pieces present in the game.

# Class 4: Block
This class is used to build the visual representation of tetrominoes seen in the game.

# Class 5: Menu
This class is used to create and visualize a menu. The game can be paused at any time with SPACE or ESC keys.

# Class 6: Button
This class is used to give functionality to the buttons seen in the menu. It registers user mouse clicks and translates it into an action

# Class 7: Timer
This class creates a timer that keeps track of time passed in the game and ensures user inputs run smoothly.

# Class 8: Preview
This class creates a preview of the upcoming tetrominoes

# Class 9: Score
This class keeps track of the user's score, lines cleared, and current level

# How to use
1) Download code, graphics, images, and music from the github repository (the latter three must stay in their respective folders to ensure the code can access the files properly)
1) Ensure pygame is installed
3) Run main.py to start the game
4) A menu will appear with three options (resume, options, and quit)
   - RESUME will start the game and resume it when paused (SPACE and ESC keys pause game)
   - OPTIONS will take you to another menu that lets you disable audio using "AUDIO SETTINGS." The other settings have not been developed
   - Quit will exit the game. Can also be exited using the "x" button in the topright of the window
5) The game ends when your pieces overlap at the top. The game will automatically close when you lose

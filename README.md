# Vantablack

![Vantablack Logo](https://github.com/Sorahawk/vantablack-maze-game/blob/master/vantablack_logo.jpg)

Vantablack is a short maze runner game, made with Python, set in a pitch black maze where you can only see one step ahead. Unicode characters (UTF-8 encoded) are used to display the game board in a command line environment (like Python IDLE).

Website: https://sorahawk.itch.io/vantablack


## Prerequisites

* Python 3.7 / 3.8
    * _Python IDLE (Recommended)_
    * `libdw 4.3.0`


## Setup

To run Vantablack:

1. Clone or download the repository

**Note: Windows Command Prompt may be unable to display the Unicode characters correctly.  
Please use Python IDLE as specified to ensure the best experience.**

2. Run the game in Python IDLE:  

```
      i. Right-click on vantablack.py.  
     ii. Select "Edit with IDLE" to launch IDLE.  
    iii. Press F5 to run the script.
```


## Features

* 3 unique handcrafted maze levels.
* Top 3 scores for each level are featured in the Hall of Fame.
* Progress reset (high scores and level unlocks) can be performed from Settings.


## How to Play

In each level, **you** (⛹) are given a certain number of moves.

Your goal is to locate the **door** ( ⩎) as quickly as possible.

However, the maze is pitch black, so you can only see the **spaces** (⯀) next to you.

Every game, a number of **traps** ( ⚠) are spawned randomly throughout the map.  
If you step on one, it'll cost you 3 moves to disarm.

Some levels might also have a couple of **Chrono Artifacts** (⏱)!  
Each artifact collected will give you 5 bonus moves.

Lastly, you might run into the **Vantablack Horror** (☣) as you make your way through the maze.  
It is possible to slay this beast for an astounding 15 moves.  
In the case that you choose to run, this maze terror will chase you down for 3 turns.

> Level 2 is designed to discourage players from killing the monster.  
> Players will not have enough moves left to to reach the exit.


## Repository Breakdown

* `monsterstateclass.py`
    * State Machine to determine the Vantablack Horror's movement type each turn, given a certain input
    * _Modules used:_ `libdw.sm`

* `cellclass.py`
    * Design concept based on nodes from data structures like BST
    * Links up with neighbouring cells to form the movement network of the maze

* `levelclass.py`
    * Builds the movement network every game
    * Displays the player and adjacent cells within the map
    * Moves the player and Vantablack Horror
    * _Modules used:_
        * `random`
        * `numpy`
        * `monsterstateclass`
        * `cellclass`

* `vantablack.py`
    * The main script of this game.
    * Displays warning of possible display issues if not being executed in IDLE.
    * Displays Main Menu, Hall of Fame, Settings, and other screens
    * Reads and writes to `vantablack_highscores.txt`, which stores game progress
    * _Modules used:_
        * `sys`
        * `levelclass`


## Video Demonstration

https://youtu.be/HW5udC-EPLI

# Ai_Plays_Tetris

Deep QLearning agent learns to solve a game of tetris

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

The code runs on python3
you'll need the following libraries

```
pygame

numpy

keras + tensorflow
```

### Installing



make sure you have a python3 setup up and running

then to install the needed libraries

```
pip install pygame numpy keras tensorflow
```

to make sure everything is up and running

```
python main.py
```
this should start a game of tetris where you can play it yourself 


### Break down into file system and Algorithms used

the code is divided into two parts, the game, and the solver

```
GAME
```
for the game folder 'config.py' holds some of the constants and settings used for the GUI,
'Tetris.py' holds the code for building the game with pygame GUI.

```
Solver
```
The Solver contains the DQN Agent class

1)  DeepQLearning.py
        For this project I tried the most straightforward and basic strategy. Give the agent the full grid and let it decide what to do.

        The DQN uses a convolutional neural network
        the network takes the entire grid and calculates the qValues for the next action
        

        For the first 1000 games the agent was a bit dumb, almost random in its decision, eventually it was playing nicely, not the best in the world but okay behaviour

    
    An epsilon policy was used, where an epsilon value to decide between exploitation and exploration. An epsilon decay was used to push the agent towards less randomization later on.

    the reward system was simple, hence not great.
    The reward policy pushes the agent to not build extremely tall structures by penalizing the hight, as well as rewards it for fully completed rows. Furthermore, a positive reward was used for droping a structure below the highest level structure to push it towards filling the lower parts of the grid.

Mostly the agent has 1-20 steps where the reward is 0. Time between structure spawn and its impact. Since there is negative rewards, this pushes the agent to take its time falling down to reduce negative inforcement. Furthermore, this causes a slight issue where the training data is full of 0 reward points.


### Running the Agents

in the main file,
comment the game.run() function and uncomment the agent.solve() function

## Summary

A smart cab is a self-driving car from the not-so-distant future that ferries people from one arbitrary location to another. In this project, we will use reinforcement learning to train a smart cab drive. In particular, the Q-learning algorithm will be implemented in a simulated environment to learn the optimal actions to take for the cab to drive to a certain target location.

The simulated environment is a grid world comprising a primary driving agent (the smart cab) and several dummy agents as traffic. There are traffic lights at all intersections, the primary driving agent needs to learn to drive according to traffic and light situations.

## Install

This project requires Python 2.7 with the pygame library installed:

https://www.pygame.org/wiki/GettingStarted

Numpy is also needed and can be installed here:

http://www.scipy.org/scipylib/download.html

## Code

`smartcab/agent.py` is the main file that implements the algorithm.

## Run

Make sure you are in the top-level project directory `smartcab/` (that contains this README). Then run:

```python smartcab/agent.py```

OR:

```python -m smartcab.agent```

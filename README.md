# İzmir University of Economics SE420 AI Project 2023-2024

1. The game is set in a 3x3 grid with nine rooms, each represented by a letter (A-I).
2. Players input the initial room (source) and the destination room (goal), along with specifying walls between certain rooms.
3. Movements are allowed in four directions, with costs associated:
```
    2 for right or left,
    1 for up or down.
```
5. Users choose between two search strategies:
```
     Uniform Cost Search
     A* Search, using Manhattan distance as heuristics.
```
7. The search process continues until the 10th expanded node, and the program prints each state during expansion, comparing them with the goal state.
8. The game provides a dynamic environment for users to experiment with different scenarios, observing how the robot navigates through the grid based on their inputs and chosen search algorithm.

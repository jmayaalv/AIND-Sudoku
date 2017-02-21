# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

A: The naked twins strategy works by identifying the boxes, inside a unit, that have the same 2 digits as possible solutions and eliminating the digits from the other boxes that have other digits.

Constraint propagation is used here because although it can't determined the correct value for the twin boxes, we can be sure that none of the other boxes in the peer will have one of those values. The values are only feasible in the twin boxes.

The algorithm implemented starts identifying the twins, this is done by filtering the boxes with a pair of digits (boxes_with_pair) and then iterating over the peers to find a box with the same digits. (twin)
Once the twins have been identified, the digits in the twins are removed from the other peers in the unit.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Having each digit in each of the diagonals in the square is another constraint to the problem. To add the constraint I just needed to add two more units, one for the left and one for the right diagonals, to the list of units in the game.

By adding the additional diagonal units, new constraints are introduced to the problem. This constrains force the algorithm to discard a solution when there is a repeated digit in the diagonals. It's important to notice that the algorithms to find the sudoku solution
  didn't really change, however with the new restrictions the algorithms would, most probably, take a few more iteration to find a solution.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
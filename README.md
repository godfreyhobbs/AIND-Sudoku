# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins' solution allows the elimination of the twin's peer's values that are constrained by the naked twins.  For example, if a Sudoku unit (a row, a column or a 3X3 square) has two boxes with value '42' then no other peer contained in that unit can have either the digit '4' or the digit '2'.  more info: http://www.sudokudragon.com/tutorialhiddentwins.htm.  This can be extended to naked tripits.  
This helps reduce the search tree when trying to solve harder games making the solver more efficient.

I do not recommend googling 'naked twins' :(.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku puzzle game has a new rule. The two main diagonals of the puzzle board are included in the unitlist.  The unitlist will now have rows, columns or 3X3 squares and the two diagonals.  This additional puzzle rule must be used when selecting each box's value.  This can lead to a smaller search spaces and better puzzle solving.

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

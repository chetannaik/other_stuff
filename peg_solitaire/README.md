# Peg Solitaire
###### Implementation of peg solitaire in Python along with Iterative Deepening Search and A* Search algorithms to solve the puzzle.

 `A* Search` `Iterative Deepening Search`

#### Summary
The peg solitaire board is implemented using a board class present in the file `board.py`. This class stores the state of the board in a 1D array and has methods to perform operations on the board like getting all possible moves from the current state of the board, moving to the next state, plotting the board and saving it as image file and others. All the classes, methods in this file and other files are fully documented.

- The `ids.py` file which contains implementation of iterative deepening search (IDS). The `iterative_deepening_search` function calls `depth_limited_search` function for various depth values until the goal state is reached.
- The `pruned_ids.py` file which contains implementation of pruned IDS. The `iterative_deepening_search` function calls `depth_limited_search` function for various depth values until the goal state is reached.
- The `astar.py` file which contains implementation of A* search. The `a_star_search` function uses heuristic to reach the goal state.
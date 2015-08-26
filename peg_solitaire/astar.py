from guppy import hpy

import board
import heapq
import numpy as np
import time


class Graph:
    """Graph class that models a graph.

    This class has stores the hash table containing board state hash as key
    and board state as the value. It has methods to get neighbors, get edge
    cost and update the hash table. The methods in this class use Board class
    methods for some of its operations.

    Attributes:
        hash_table: A python dictionary containing hash of the board state as
        key and board state as value.
    """
    def __init__(self, board_object):
        """Constructor that initializes hash table using passed Board class
        object."""
        self.hash_table = {}
        board_hash = hash(board_object)
        self.hash_table[board_hash] = board_object.get_board_state()

    def neighbors(self, state_hash):
        """Gets the hashes of neighbor states using hash of current state."""
        state = self.get_state_from_hash(state_hash)
        neighbors = self.get_neighbors(state)
        neighbor_hashes = self.update_hash_table(neighbors)
        return neighbor_hashes

    def get_state_from_hash(self, state_hash):
        """Returns Board state given its hash."""
        return self.hash_table[state_hash]

    def update_hash_table(self, neighbors):
        """Updates the class variable and returns neighbor hashes."""
        _neighbor_hashes = []
        for transition, neighbor in neighbors:
            temp_board = board.Board(neighbor)
            self.hash_table[hash(temp_board)] = neighbor
            _neighbor_hashes.append((transition, hash(temp_board)))
        return _neighbor_hashes

    @staticmethod
    def edge_cost():
        """Returns edge cost which is defined to be 1 for this graph."""
        return 1

    @staticmethod
    def get_neighbors(state):
        """Gets the neighbor states using current state."""
        input_state = board.Board(state)
        transitions = input_state.get_possible_transitions()
        states = []
        for transition in transitions:
            current_state = input_state.copy()
            current_state.move(*transition)
            states.append((transition, current_state.get_board_state()))
        return states


class PriorityQueue:
    """PriorityQueue class that models a priority queue using heapq library.

    This class has stores the elements in a array and maintains min_heap
    property. The node with least 'priority' value will be returned when this
    is popped.

    Attributes:
        elements: A python list that stores item while maintaining min heap
        property.
    """
    def __init__(self):
        self.elements = []

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def is_empty(self):
        return len(self.elements) == 0


def heuristic_cost_1(graph, goal_state, node_hash):
    """Returns the difference between the number of pegs in the node and the
    goal states."""
    node_state = graph.get_state_from_hash(node_hash)
    node_state_board = board.Board(node_state)
    node_state_stats = node_state_board.get_board_stats()
    goal_state_board = board.Board(goal_state)
    goal_state_stats = goal_state_board.get_board_stats()
    return node_state_stats[1] - goal_state_stats[1]


def heuristic_cost_2(graph, goal_state, node_hash):
    """Returns the sum of manhattan distances of every peg from the peg in the
    center of the board."""
    node_state = graph.get_state_from_hash(node_hash)
    distance = []
    for i in node_state:
        if i == 1:
            x_loc, y_loc = board.get_peg_coordinates_from_number(i)
            manhattan_distance = (abs(4 - x_loc) + abs(4 - y_loc))
            distance.append(manhattan_distance)
    average_distance = np.array(distance).sum()
    return average_distance


def a_star_search(start, goal, simple=False):
    """A* Search method.

    Args:
        start: A list of numbers representing initial state.
        goal: A list of numbers representing final goal state.
        simple: A boolean which is used to switch between the two heuristics.
            If this is set as true, heuristic_cost_1 is chosen otherwise,
            heuristic_cost_2 is chosen. By default it is set as false.

    Returns: A tuple containing the number of nodes expanded and a python
    dictionary containing parent pointers of every explored state's hash.
    """
    start_state = board.Board(start)
    start_hash = hash(start_state)
    goal_state = board.Board(goal)
    goal_hash = hash(goal_state)

    graph = Graph(start_state)
    parent = dict()
    parent[start_hash] = None
    path_cost = dict()
    path_cost[start_hash] = 0

    fringe = PriorityQueue()
    fringe.put(start_hash, 0)
    count = 0

    while not fringe.is_empty():
        current = fringe.get()
        count += 1

        if current == goal_hash:
            break

        for transition, child_hash in graph.neighbors(current):
            g_cost = path_cost[current] + graph.edge_cost()
            if child_hash not in path_cost or g_cost < path_cost[child_hash]:
                parent[child_hash] = (transition, current)
                path_cost[child_hash] = g_cost
                if simple:
                    h_cost = heuristic_cost_1(graph, goal, child_hash)
                else:
                    h_cost = heuristic_cost_2(graph, goal, child_hash)
                f_cost = g_cost + h_cost
                fringe.put(child_hash, f_cost)
    return count, parent


def backtrack(parent, start, goal):
    """This methods backtracks and returns the path to the goal from start
    state using parent pointer dictionary, start state and goal state as
    inputs"""
    start_state = board.Board(start)
    start_hash = hash(start_state)
    goal_state = board.Board(goal)
    state = hash(goal_state)

    answer = []
    while state != start_hash:
        cur_state = state
        transition, state = parent[state]
        answer.append((transition, cur_state))
    return answer[::-1]


def plot_path(answer, start):
    """Plots the path and saves it as a set of images showing moves taken to
    reach goal state from start state."""
    my_board = board.Board(start)
    my_board.plot_board(name="move 0")
    for m_num, step in enumerate(answer):
        move, state_hash = step
        my_board.move(*move)
        name = "move %d" % (m_num + 1)
        my_board.plot_board(name=name)


def main():
    # Cross Configuration
    root = board.translate_input_to_array(['--000--',
                                           '--0X0--',
                                           '00XXX00',
                                           '000X000',
                                           '000X000',
                                           '--000--',
                                           '--000--'])

    # Plus Configuration
    # root = board.translate_input_to_array(['--000--',
    #                                        '--0X0--',
    #                                        '000X000',
    #                                        '0XXXXX0',
    #                                        '000X000',
    #                                        '--0X0--',
    #                                        '--000--'])

    # Fireplace Configuration
    # root = board.translate_input_to_array(['--XXX--',
    #                                        '--XXX--',
    #                                        '00XXX00',
    #                                        '00X0X00',
    #                                        '0000000',
    #                                        '--000--',
    #                                        '--000--'])

    # Up Configuration
    # root = board.translate_input_to_array(['--0X0--',
    #                                        '--XXX--',
    #                                        '0XXXXX0',
    #                                        '000X000',
    #                                        '000X000',
    #                                        '--XXX--',
    #                                        '--XXX--'])

    # Pyramid Configuration
    # root = board.translate_input_to_array(['--000--',
    #                                        '--0X0--',
    #                                        '00XXX00',
    #                                        '0XXXXX0',
    #                                        'XXXXXXX',
    #                                        '--000--',
    #                                        '--000--'])

    # Diamond Configuration
    # root = board.translate_input_to_array(['--0X0--',
    #                                        '--XXX--',
    #                                        '0XXXXX0',
    #                                        'XXX0XXX',
    #                                        '0XXXXX0',
    #                                        '--XXX--',
    #                                        '--0X0--'])

    # Start Configuration
    # root = board.translate_input_to_array(['--XXX--',
    #                                        '--XXX--',
    #                                        'XXXXXXX',
    #                                        'XXX0XXX',
    #                                        'XXXXXXX',
    #                                        '--XXX--',
    #                                        '--XXX--'])

    # Goal Configuration
    goal = board.translate_input_to_array(['--000--',
                                           '--000--',
                                           '0000000',
                                           '000X000',
                                           '0000000',
                                           '--000--',
                                           '--000--'])

    hp = hpy()
    before = hp.heap()
    start_time = time.time()
    count, parent = a_star_search(root, goal, simple=False)
    end_time = time.time()
    after = hp.heap()
    leftover = after - before
    answer = backtrack(parent, root, goal)

    print "Total number of nodes expanded: %d" % count
    print "Answer depth: %d" % len([move for move, _ in answer])
    print "Moves: %s" % [move for move, _ in answer]
    print "Time: %d seconds\n" % (end_time - start_time)
    print leftover

    # plot_path(answer, root)


if __name__ == '__main__':
    main()

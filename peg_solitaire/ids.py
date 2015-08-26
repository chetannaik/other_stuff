from guppy import hpy

import board
import time

solution_moves = []


def iterative_deepening_search(root, goal):
    """Iterative Deepening Search method.

    Args:
        root: A list of numbers representing initial state.
        goal: A list of numbers representing final goal state.

    Returns:
        i: A number representing the depth of the solution.
        total_count: A number representing the total number if nodes expanded.
        solution_moves: A list of tuples representing the moves required to
            reach goal state.
    """
    root_state = board.Board(root)
    goal_state = board.Board(goal)
    root_hash = hash(root_state)
    goal_hash = hash(goal_state)
    i = 0
    total_count = 0
    while root_hash != goal_hash:
        root_state = board.Board(root)
        count = 0
        root_hash, count = depth_limited_search(root_state, goal_state, i,
                                                count)
        # print "Depth: ", i, "\tNumber of nodes expanded: ", count
        total_count += count
        i += 1
        if i > 30:
            print "Breaking. Depth > 30"
            break
    return i, total_count


def depth_limited_search(node_state, goal_state, depth, count):
    """Depth Limited Search method.

    Args:
        node_state: An object of Board class with the intermediate state.
        goal_state: An object of Board class with the goal state.
        depth: A number which represents the maximum depth that the method
            can go to.
        count: A number representing the total number if nodes expanded till
            the method was called.
        solution_moves: A list of tuples representing the moves required to
            reach goal state.

    Returns: A tuple containing the child_state hash, updated number of nodes
        explored ans updated solution_moves list.
    """
    if hash(node_state) == hash(goal_state):
        return hash(node_state), count
    elif depth >= 0:
        for transition in node_state.get_possible_transitions():
            count += 1
            child_state = node_state.copy()
            child_state.move(*transition)
            if hash(child_state) == hash(goal_state):
                solution_moves.append(transition)
                return hash(child_state), count
            ans_hash, count = depth_limited_search(child_state, goal_state,
                                                   depth-1, count)
            if ans_hash:
                solution_moves.append(transition)
                return ans_hash, count
    return False, count


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
    depth, count = iterative_deepening_search(root, goal)
    after = hp.heap()
    end_time = time.time()
    leftover = after - before

    moves = solution_moves[::-1]
    print "Total number of nodes expanded: %d" % count
    print "Answer depth: %d" % depth
    print "Moves: %s" % moves
    print "Time: %d seconds\n" % (end_time - start_time)
    print leftover

    # board.plot_answer(root, moves)


if __name__ == '__main__':
    main()

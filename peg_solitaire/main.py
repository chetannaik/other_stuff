from guppy import hpy
import board
import pruned_ids
import ids
import astar
import time


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
    count, parent = astar.a_star_search(root, goal)
    end_time = time.time()
    after = hp.heap()
    answer = astar.backtrack(parent, root, goal)
    leftover = after - before

    print "A* Search: Total Manhattan distance heuristic"
    print "Total number of nodes expanded: %d" % count
    print "Answer depth: %d" % len([move for move, _ in answer])
    print "Moves: %s" % [move for move, _ in answer]
    print "Time: %d seconds" % (end_time - start_time)
    # print leftover
    print "---\n"


    before = hp.heap()
    start_time = time.time()
    count, parent = astar.a_star_search(root, goal, simple=True)
    end_time = time.time()
    after = hp.heap()
    answer = astar.backtrack(parent, root, goal)
    leftover = after - before

    print "A* Search: Number of pegs heuristic"
    print "Total number of nodes expanded: %d" % count
    print "Answer depth: %d" % len([move for move, _ in answer])
    print "Moves: %s" % [move for move, _ in answer]
    print "Time: %d seconds" % (end_time - start_time)
    # print leftover
    print "---\n"

    before = hp.heap()
    start_time = time.time()
    depth, count = pruned_ids.iterative_deepening_search(root, goal)
    end_time = time.time()
    after = hp.heap()
    leftover = after - before

    moves = pruned_ids.solution_moves[::-1]
    print "Pruned Iterative Deepening Search:"
    print "Total number of nodes expanded: %d" % count
    print "Answer depth: %d" % depth
    print "Moves: %s" % moves
    print "Time: %d seconds" % (end_time - start_time)
    # print leftover
    print "---\n"

    before = hp.heap()
    start_time = time.time()
    depth, count = ids.iterative_deepening_search(root, goal)
    end_time = time.time()
    after = hp.heap()
    leftover = after - before

    moves = ids.solution_moves[::-1]
    print "Iterative Deepening Search:"
    print "Total number of nodes expanded: %d" % count
    print "Answer depth: %d" % depth
    print "Moves: %s" % moves
    print "Time: %d seconds" % (end_time - start_time)
    # print leftover
    print "---\n"


if __name__ == '__main__':
    main()

# game.py

# importing the logic.py file
# where we have written all the
# logic functions used.
import game_logic
import numpy as np
import random


def check_monotonic(mat):
    np_mat = np.asarray(mat)
    max_index = np.argmax(np_mat)
    if max_index == 0:  # top left corner
        row_vector = np_mat[0,:]  # : means the all column
        column_vector = np_mat[:,0]
    elif max_index == 12:  # bottom left corner
        row_vector = np_mat[-1, :]  # -1 last in the array
        column_vector = np_mat[:, 0]
    elif max_index == 3:  # top right corner
        row_vector = np_mat[0, :]
        column_vector = np_mat[:, -1]
    elif max_index == 15:  # bottom right
        row_vector = np_mat[-1, :]
        column_vector = np_mat[:, -1]
    else:
        return False

    row_increasing = np.all(row_vector[1:] >= row_vector[:-1])
    row_decreasing = np.all(row_vector[1:] < row_vector[:-1])

    column_increasing = np.all(column_vector[1:] >= column_vector[:-1])
    column_decreasing = np.all(column_vector[1:] < column_vector[:-1])

    return row_decreasing or row_increasing or column_decreasing or column_increasing


# Driver code
def play(agent):
    # calling start_game function
    # to initialize the matrix
    mat = game_logic.start_game()
    game_over = False
    score = 0
    while not game_over:

        op_list = agent.run(mat)
        changed = False
        counter = 0
        while not changed and counter <= 3:

            x = op_list[counter][1]
            # we have to move up
            if x == 0:
                mat, changed = game_logic.move_up(mat)

            # to move down
            elif x == 1:
                mat, changed = game_logic.move_down(mat)

            # to move left
            elif x == 2:
                mat, changed = game_logic.move_left(mat)

            # to move right
            elif x == 3:
                mat, changed = game_logic.move_right(mat)

            counter += 1
            # soring system (updated to strategy B)
        """max_index = np.argmax(mat)

        if not(max_index == 0 or max_index == 12 or max_index == 3 or max_index == 15):
            score -= 10

        res = check_monotonic(mat)
        if res is True:
            score += 20"""

        status = game_logic.get_current_state(mat)
        if status == 'GAME NOT OVER':
            r = random.randint(1, 10)
            if r < 9:
                game_logic.add_new_2(mat)
            else:
                game_logic.add_new_4(mat)
        else:
            game_over = True

    return np.amax(mat) * 5 + score, np.amax(mat)  # return max value - the fitness of the chromosome
    # return np.amax(mat) + score, np.amax(mat)  # return max value - the fitness of the chromosome


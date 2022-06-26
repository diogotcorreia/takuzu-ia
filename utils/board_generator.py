from takuzu import Takuzu, Board
from search import (
    Problem,
    greedy_search,
)


class MultiSolutionProblem(Problem):
    """Delegates to a problem, keeps multiple goal states"""

    def __init__(self, problem, goal_len_limit):
        self.problem = problem
        self.goal_len_limit = goal_len_limit
        self.found = set()

    def actions(self, state):
        return self.problem.actions(state)

    def result(self, state, action):
        return self.problem.result(state, action)

    def goal_test(self, state):
        result = self.problem.goal_test(state)
        if result:
            self.found.add(state.board.cells)
            # reach the end if we found enough goal states
            return len(self.found) >= self.goal_len_limit
        return result

    def path_cost(self, c, state1, action, state2):
        return self.problem.path_cost(c, state1, action, state2)

    def value(self, state):
        return self.problem.value(state)

    def __getattr__(self, attr):
        return getattr(self.problem, attr)

    def __repr__(self):
        return "found states count: {:4d}".format(len(self.found))


def empty_board_of_size(size):
    return Board(
        tuple(tuple(2 for i in range(size)) for j in range(size))
    ).calculate_state()


def has_only_one_solution(board):
    board_obj = Board(board).calculate_state()

    problem = MultiSolutionProblem(Takuzu(board_obj), 2)
    greedy_search(problem)
    return len(problem.found) == 1


def remove_cells(board):
    def remove_and_test(board_to_test, index):
        row, col = index // len(board_to_test), index % len(board_to_test)

        if board_to_test[row][col] == 2:
            return (False, board_to_test)

        mutated_row = board_to_test[row][:col] + (2,) + board_to_test[row][col + 1 :]
        mutated_board = board_to_test[:row] + (mutated_row,) + board_to_test[row + 1 :]

        if has_only_one_solution(mutated_board):
            return (True, mutated_board)
        else:
            return (False, board_to_test)

    changed = True
    while changed:

        for i in range(len(board) ** 2):
            success, new_board = remove_and_test(board, i)
            changed = changed or success
            board = new_board

        changed = False

    return board


if __name__ == "__main__":
    board = empty_board_of_size(10)
    # board = Board.parse_instance_from_stdin()

    problem = Takuzu(board)
    generatorProblem = MultiSolutionProblem(problem, 50)
    greedy_search(generatorProblem)

    for i, goal in enumerate(generatorProblem.found):
        print("--- BOARD ---")
        board_with_holes = remove_cells(goal)
        print(Board(board_with_holes))

        with open(f"size{len(goal):0>2}_{(i+1):0>2}.in", "w") as file:
            file.write(f"{len(goal)}\n{Board(board_with_holes)}\n")
        with open(f"size{len(goal):0>2}_{(i+1):0>2}.out", "w") as file:
            file.write(f"{Board(goal)}\n")

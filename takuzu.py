# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 03:
# 99209 Diogo Romão Cardoso
# 99211 Diogo Torres Correia

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, cells):
        self.cells = cells
        self.size = len(cells)
        self.complete_rows = set()
        self.complete_cols = set()

    def calculate_state(self):
        """Calcula os valores do estado interno, para ser usado
        no tabuleiro inicial."""
        self.remaining_cells = []
        # Counts are stored at (zero_count, one_count) pairs for each row/column
        self.col_counts = ()
        self.row_counts = ()

        for col in range(self.size):
            for row in range(self.size):
                if self.cells[row][col] == 2:
                    self.remaining_cells.append((row, col))

        for col in range(self.size):
            zero_count, one_count = 0, 0
            for row in range(self.size):
                if self.cells[row][col] == 0:
                    zero_count += 1
                elif self.cells[row][col] == 1:
                    one_count += 1
            self.col_counts += ((zero_count, one_count),)
        for row in range(self.size):
            zero_count, one_count = 0, 0
            for col in range(self.size):
                if self.cells[row][col] == 0:
                    zero_count += 1
                elif self.cells[row][col] == 1:
                    one_count += 1
            self.row_counts += ((zero_count, one_count),)
        return self

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.cells[row][col]

    def get_row(self, row: int):
        return self.cells[row]

    def get_col(self, col: int):
        return tuple(self.cells[row][col] for row in range(self.size))

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        return (self.get_number(row + 1, col), self.get_number(row - 1, col))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_number(row, col - 1), self.get_number(row, col + 1))

    def adjacent_numbers_by_vec(
        self, row: int, col: int, vec: (int, int)
    ) -> (int, int):
        """Returns values determined by adding the vector to the position
        once and twice"""
        vec_row, vec_col = vec
        first_row, first_col = (row + vec_row, col + vec_col)
        second_row, second_col = (row + vec_row * 2, col + vec_col * 2)
        return (
            self.get_number(first_row, first_col),
            self.get_number(second_row, second_col),
        )

    def set_number(self, row: int, col: int, value: int):
        """Devolve um novo Board com o novo valor na posição indicada"""

        def sum_value_to_count(count_tuple):
            zeros, ones = count_tuple
            return (zeros, ones + 1) if value == 1 else (zeros + 1, ones)

        def check_complete_line(count_tuple, completed_set, get_line):
            zeros, ones = count_tuple
            if zeros + ones == self.size:
                completed_set.add(get_line())

        new_row = self.cells[row][:col] + (value,) + self.cells[row][col + 1 :]
        new_cells = self.cells[:row] + (new_row,) + self.cells[row + 1 :]

        line_count = sum_value_to_count(self.col_counts[col])
        check_complete_line(line_count, self.complete_cols, lambda: self.get_col(col))

        new_col_counts = (
            self.col_counts[:col] + (line_count,) + self.col_counts[col + 1 :]
        )

        line_count = sum_value_to_count(self.row_counts[row])
        check_complete_line(line_count, self.complete_rows, lambda: self.get_row(row))

        new_row_counts = (
            self.row_counts[:row] + (line_count,) + self.row_counts[row + 1 :]
        )

        new_board = Board(new_cells)
        new_board.remaining_cells = self.remaining_cells[1:]
        new_board.col_counts = new_col_counts
        new_board.row_counts = new_row_counts

        return new_board

    def get_remaining_cells_count(self):
        """Devolve o número de posições em branco"""
        return len(self.remaining_cells)

    def get_next_cell(self):
        return self.remaining_cells[0]

    def __repr__(self):
        return "\n".join(map(lambda x: "\t".join(map(str, x)), self.cells))

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        board_size = int(input())
        cells = []
        for _ in range(board_size):
            row = sys.stdin.readline().strip("\n")
            cells.append(tuple(map(int, row.split("\t"))))
        return Board(tuple(cells)).calculate_state()


class BoardIterator:
    def __init__(self, board: Board):
        self.board = board

    def can_place_col_row(self, counts):
        """Returns which values can be placed in a column or row"""
        zeros, ones = counts

        if zeros + ones == self.board.size:
            # column is full
            return ()

        max_of_type = np.ceil(self.board.size / 2)

        # if more zeros than half the size, we can only place ones
        if zeros >= max_of_type:
            return (1,)
        # if more ones than half the size, we can only place zeros
        if ones >= max_of_type:
            return (0,)
        # otherwise, we can place either
        return (0, 1)

    def can_place_position(self, row, col):
        """Returns which values can be placed in a position, according
        to the first rule (count of different values must be the same for
        every column and role)"""

        possible_cols = self.can_place_col_row(self.board.col_counts[col])
        possible_rows = self.can_place_col_row(self.board.row_counts[row])

        intersection = tuple(
            number for number in possible_cols if number in possible_rows
        )

        return intersection

    def check_adjacent(self, row, col, number):
        """Returns true if the number can be placed in the given position
        according to the adjacency rule"""
        invalid_result = (number, number)
        return (
            self.board.adjacent_vertical_numbers(row, col) != invalid_result
            and self.board.adjacent_horizontal_numbers(row, col) != invalid_result
            and self.board.adjacent_numbers_by_vec(row, col, (1, 0)) != invalid_result
            and self.board.adjacent_numbers_by_vec(row, col, (-1, 0)) != invalid_result
            and self.board.adjacent_numbers_by_vec(row, col, (0, 1)) != invalid_result
            and self.board.adjacent_numbers_by_vec(row, col, (0, -1)) != invalid_result
        )

    def check_duplicate_col_row(self, row, col, number):
        """Returns true if the number can be placed in the given position
        according to the duplicate rule"""

        def check_complete_line(count_tuple, completed_set, get_line):
            zeros, ones = count_tuple
            if zeros + ones + 1 == self.board.size:
                return get_line() not in completed_set
            return True

        def set_number(line, index):
            return line[:index] + (number,) + line[index + 1 :]

        return check_complete_line(
            self.board.col_counts[col],
            self.board.complete_cols,
            lambda: set_number(self.board.get_col(col), col),
        ) and check_complete_line(
            self.board.row_counts[row],
            self.board.complete_rows,
            lambda: set_number(self.board.get_row(row), row),
        )

    def __iter__(self):
        self.row, self.col = self.board.get_next_cell()

        placeable = self.can_place_position(self.row, self.col)

        return map(
            lambda x: (self.row, self.col, x),
            filter(
                lambda x: self.check_adjacent(self.row, self.col, x)
                and self.check_duplicate_col_row(self.row, self.col, x),
                placeable,
            ),
        )

    def __next__(self):
        raise StopIteration()


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = TakuzuState(board)
        super().__init__(state)
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        return BoardIterator(state.board)

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row, col, value) = action
        return TakuzuState(state.board.set_number(row, col, value))

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return state.board.get_remaining_cells_count() == 0

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance_from_stdin()
    takuzu = Takuzu(board)
    goal_node = depth_first_tree_search(takuzu)
    print(goal_node.state.board)
    pass

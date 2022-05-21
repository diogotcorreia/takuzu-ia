# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 03:
# 99209 Diogo Romão Cardoso
# 99211 Diogo Torres Correia

import sys
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

    def calculate_state(self):
        """Calcula os valores do estado interno, para ser usado
        no tabuleiro inicial."""
        self.remaining_cells_count = 0
        for y in self.cells:
            for x in y:
                if x == 2:
                    self.remaining_cells_count += 1
        return self

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row <= self.size and 0 <= col <= self.size:
            return self.cells[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        return (self.get_number(row + 1, col), self.get_number(row - 1, col))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_number(row, col - 1), self.get_number(row, col + 1))

    def set_number(self, row: int, col: int, value: int):
        """Devolve um novo Board com o novo valor na posição indicada"""
        new_row = self.cells[row][:col] + (value,) + self.cells[row][col + 1 :]
        new_cells = self.cells[:row] + (new_row,) + self.cells[row + 1 :]

        new_board = Board(new_cells)
        new_board.remaining_cells_count = self.remaining_cells_count - 1

        return new_board

    def get_remaining_cells_count(self):
        """Devolve o número de posições em branco"""
        return self.remaining_cells_count

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


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = TakuzuState(board)
        super().__init__(state)
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
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

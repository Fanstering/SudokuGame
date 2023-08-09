import copy
import random


class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = None  # 保存数独的解决方案

    def generate(self, difficulty):
        self._generate_solution()  # 生成完整解的数独谜题
        # 保留原矩阵备份
        self.solution = copy.deepcopy(self.board)

        self._remove_cells(difficulty)  # 根据难度级别移除部分格子

    def _generate_solution(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = 0  # 初始化数独面板

        self._fill_cells()

    def _fill_cells(self):
        def is_valid(num, row, col):
            for i in range(9):
                if self.board[row][i] == num or self.board[i][col] == num:
                    return False
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if self.board[i][j] == num:
                        return False
            return True

        def solve():
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        for num in range(1, 10):
                            if is_valid(num, i, j):
                                self.board[i][j] = num
                                if solve():
                                    return True
                                self.board[i][j] = 0
                        return False
            return True

        solve()

    def _remove_cells(self, difficulty):
        if difficulty == 'easy':
            num_cells_to_remove = 40
        elif difficulty == 'medium':
            num_cells_to_remove = 50
        elif difficulty == 'hard':
            num_cells_to_remove = 60
        else:
            raise ValueError("Invalid difficulty level")

        # 随机选择并移除一些格子
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for i, j in cells[:num_cells_to_remove]:
            self.board[i][j] = 0

    def solve_sudoku(self):
        # 创建一个副本用于求解
        solved_board = [row[:] for row in self.board]

        # 使用回溯算法求解数独
        if self._solve(solved_board):
            return solved_board
        else:
            return None

    def _solve(self, board):
        empty_cell = self._find_empty_cell(board)
        if not empty_cell:
            return True  # 数独已经解出
        row, col = empty_cell

        for num in range(1, 10):
            if self._is_valid(board, row, col, num):
                board[row][col] = num

                if self._solve(board):
                    return True

                board[row][col] = 0

        return False

    def _find_empty_cell(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def _is_valid(self, board, row, col, num):
        # 检查行、列和3x3子网格是否合法
        return (
                self._is_valid_row(board, row, num) and
                self._is_valid_col(board, col, num) and
                self._is_valid_subgrid(board, row, col, num)
        )

    def _is_valid_row(self, board, row, num):
        return num not in board[row]

    def _is_valid_col(self, board, col, num):
        return num not in [board[row][col] for row in range(9)]

    def _is_valid_subgrid(self, board, row, col, num):
        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True



def main():
    generator = SudokuGenerator()
    generator.generate('easy')
    for row in generator.board:
        print(row)


if __name__ == "__main__":
    main()

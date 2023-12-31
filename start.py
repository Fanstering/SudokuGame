import tkinter as tk
from tkinter import messagebox
from sudoku_generator import SudokuGenerator


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("数独游戏")

        self.generator = SudokuGenerator()
        self.generator.generate('easy')
        self.board = self.generator.board
        self.solution_window = None  # 自动解答窗口

        self.create_main_panel()

    #  创建主面板
    def create_main_panel(self):
        panel_size = 500  # 整体面板大小
        cell_size = (panel_size) // 9  # 计算格子大小，减去9个间距

        main_panel = tk.Frame(self.root, width=panel_size, height=panel_size)
        main_panel.pack()

        # self.sudoku_panel = tk.Frame(main_panel, width=cell_size * 9, height=cell_size * 9, bg='white')
        self.sudoku_panel = tk.Canvas(main_panel, width=cell_size * 9, height=cell_size * 9, bg='white')
        self.sudoku_panel.pack(side=tk.LEFT)

        button_panel = tk.Frame(main_panel, width=panel_size - cell_size * 9, height=cell_size * 9,
                                padx=10, pady=10)
        button_panel.pack(side=tk.LEFT)

        # 获取 self.root 的总尺寸
        root_width = main_panel.winfo_reqwidth()
        root_height = main_panel.winfo_reqheight()

        # 计算屏幕中央位置
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - root_width) // 2
        y_position = (screen_height - root_height) // 2

        self.root.geometry(f"+{x_position}+{y_position}")  # 设置窗口尺寸和位置


        self.create_sudoku_board(self.sudoku_panel)
        self.create_buttons(button_panel)

        self.draw_grid(self.sudoku_panel, cell_size/1.31)  # 画出不重叠的3x3小方格和黑色粗线

    def draw_grid(self, panel, cell_size):
        for i in range(1, 9):
            if i % 3 == 0:
                line_width = 3
            else:
                line_width = 0

            # 画横线
            panel.create_line(0, i * cell_size, 9 * cell_size, i * cell_size, width=line_width)

            # 画竖线
            panel.create_line(i * cell_size, 0, i * cell_size, 9 * cell_size, width=line_width)



    # 创建数独面板
    def create_sudoku_board(self, panel):
        self.entry_grid = [[None for _ in range(9)] for _ in range(9)]  # 创建一个二维数组用于保存所有的Entry
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(panel, width=2, font=('Helvetica', 24), justify='center', validate='key')  # 创建一个输入框组件
                entry.grid(row=i, column=j, padx=1, pady=1)  # 将输入框放置在指定行列，并设置边距
                entry.row = i  # 将当前行信息绑定到Entry
                entry.column = j  # 将当前列信息绑定到Entry
                entry.configure(validatecommand=(entry.register(self.validate_input), '%P'))  # 设置输入验证的命令和参数
                value = self.board[i][j]  # 获取数独的值
                if value != 0:
                    entry.insert(0, str(value))  # 如果值不为0，在输入框中插入该值
                    entry.configure(state='readonly')  # 非空缺位置设置为只读状态
                # entry.configure(background='white')  # 设置默认的背景颜色为白色
                self.entry_grid[i][j] = entry  # 将Entry添加到二维数组中
                if value == 0:
                    entry.configure(background='lightgray')  # 如果值为0，将空缺位置的背景颜色设置为灰色
                # print(entry.winfo_width(),entry.winfo_height())




    # 验证输入
    def validate_input(self, new_value):
        if new_value == '' or (new_value.isdigit() and 1 <= int(new_value) <= 9):
            return True
        return False

    # 创建按钮模块
    def create_buttons(self, panel):
        button_width = 15  # 设置按钮的宽度
        button_height = 2  # 设置按钮的高度

        solve_button = tk.Button(panel, text="解答", command=self.check_solution, bg='#DDEEDD', fg='blue', bd=4,
                                 width=button_width, height=button_height)
        solve_button.pack(pady=10)

        generate_button = tk.Button(panel, text="生成数独", command=self.show_difficulty_dialog, bg='#DDEEDD', fg='green',
                                    bd=4,
                                    width=button_width, height=button_height)
        generate_button.pack(pady=10)

        solve_auto_button = tk.Button(panel, text="自动解答", command=self.solve_and_show_solution, bg='#DDEEDD',
                                      fg='purple', bd=4,
                                      width=button_width, height=button_height)
        solve_auto_button.pack(pady=10)


    # 生成谜题模块
    def show_difficulty_dialog(self):
        difficulty_window = tk.Toplevel(self.root)
        difficulty_window.title("选择难度")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 300
        window_height = 150

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        difficulty_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set('easy')

        difficulty_frame = tk.Frame(difficulty_window)
        difficulty_frame.pack()

        difficulties = ['easy', 'medium', 'hard']
        for diff in difficulties:
            rb = tk.Radiobutton(difficulty_frame, text=diff, variable=self.difficulty_var, value=diff)
            rb.pack()

        confirm_button = tk.Button(difficulty_window, text="确认",
                                   command=lambda: self.generate_sudoku(difficulty_window))
        confirm_button.pack()

    def generate_sudoku(self, difficulty_window):
        difficulty = self.difficulty_var.get()
        self.generator.generate(difficulty)
        self.board = self.generator.board
        self.update_sudoku_board()
        difficulty_window.destroy()

    def update_sudoku_board(self):
        for widget in self.sudoku_panel.winfo_children():
            widget.destroy()  # 删除原来的数独面板

        self.create_sudoku_board(self.sudoku_panel)  # 创建新的数独面板

    # 验证模块
    def check_solution(self):
        user_solution = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                entry = self.entry_grid[i][j]  # 修改为使用 entry_grid
                value = entry.get()
                if value and value.isdigit():
                    user_solution[i][j] = int(value)
                else:
                    messagebox.showinfo("提示", "请填写所有格子再进行解答验证。")
                    return

        if self.is_solution_correct(user_solution):
            messagebox.showinfo("结果", "恭喜！答案正确！")
        else:
            messagebox.showinfo("结果", "很遗憾，答案错误。请检查您的填写。")

    def is_solution_correct(self, user_solution):
        for i in range(9):
            for j in range(9):
                if user_solution[i][j] != self.generator.solve_sudoku()[i][j]:
                    return False
        return True


    # 自动解迷模块
    def solve_and_show_solution(self):
        solved_board = self.generator.solve_sudoku()
        if solved_board:
            self.show_solution_window(solved_board)
        else:
            messagebox.showinfo("提示", "无解")

    def show_solution_window(self, solved_board):
        if self.solution_window is None:
            solution_window = self.solution_window = tk.Toplevel(self.root)
            solution_window.title("数独解答")


            for i in range(9):
                for j in range(9):
                    value = solved_board[i][j]
                    bg_color = 'white' if self.board[i][j] == value else 'lightgray'
                    entry = tk.Label(solution_window, text=str(value), font=('Helvetica', 24), width=2, height=1,
                                     bg=bg_color)
                    entry.grid(row=i, column=j, padx=1, pady=1)

            # 在窗口关闭时设置回调函数
            self.solution_window.protocol("WM_DELETE_WINDOW", self.on_auto_solve_window_close)
        else:
            messagebox.showinfo("提示", "窗口已存在")

    def on_auto_solve_window_close(self):
        # 窗口关闭时，重置 self.auto_solve_window 为 None
        self.solution_window.destroy()
        self.solution_window = None


def main():
    root = tk.Tk()
    game = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

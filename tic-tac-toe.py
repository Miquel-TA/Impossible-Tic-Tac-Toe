import tkinter as tk
from tkinter import messagebox

def is_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]
    return [player, player, player] in win_conditions

def get_empty_positions(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def minimax(board, depth, is_maximizing, alpha, beta):
    global calculation_count
    calculation_count += 1

    if is_winner(board, "X"):
        return 10, None
    elif is_winner(board, "O"):
        return -10, None
    elif not get_empty_positions(board):
        return 0, None

    if is_maximizing:
        max_eval = float('-inf')
        best_move = None
        for position in get_empty_positions(board):
            board[position[0]][position[1]] = "X"
            eval, _ = minimax(board, depth + 1, False, alpha, beta)
            board[position[0]][position[1]] = " "
            if eval > max_eval:
                max_eval = eval
                best_move = position
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for position in get_empty_positions(board):
            board[position[0]][position[1]] = "O"
            eval, _ = minimax(board, depth + 1, True, alpha, beta)
            board[position[0]][position[1]] = " "
            if eval < min_eval:
                min_eval = eval
                best_move = position
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def click(row, col):
    global player_turn
    if player_turn and board[row][col] == " ":
        button_list[row][col].config(text="O", state="disabled")
        board[row][col] = "O"
        player_turn = False
        check_game_state()
        if not game_over:
            computer_move()

def computer_move():
    global calculation_count, player_turn
    calculation_count = 0
    _, move = minimax(board, 0, True, float('-inf'), float('inf'))
    if move:
        row, col = move
        board[row][col] = "X"
        button_list[row][col].config(text="X", state="disabled")
    player_turn = True
    print(f"Calculations performed: {calculation_count}")
    check_game_state()

def check_game_state():
    global game_over
    if is_winner(board, "X"):
        messagebox.showinfo("Game Over", "X wins!")
        game_over = True
    elif is_winner(board, "O"):
        messagebox.showinfo("Game Over", "O wins!")
        game_over = True
    elif not get_empty_positions(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        game_over = True
    if game_over:
        for row in button_list:
            for button in row:
                button.config(state="disabled")

def reset_game():
    global board, player_turn, game_over
    board = [[" " for _ in range(3)] for _ in range(3)]
    for row in button_list:
        for button in row:
            button.config(text="", state="normal")
    player_turn = True
    game_over = False

root = tk.Tk()
root.title("Tic Tac Toe")

board = [[" " for _ in range(3)] for _ in range(3)]
button_list = []
player_turn = True
game_over = False
calculation_count = 0

for row in range(3):
    row_list = []
    for col in range(3):
        button = tk.Button(root, text="", font=("Arial", 24), width=5, height=2,
                           command=lambda r=row, c=col: click(r, c))
        button.grid(row=row, column=col)
        row_list.append(button)
    button_list.append(row_list)

reset_button = tk.Button(root, text="Reset Game", font=("Arial", 16), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)

root.mainloop()

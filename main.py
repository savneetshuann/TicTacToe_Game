# Tic Tac Toe game


import random
import tkinter
from tkinter import *
import sqlite3
from functools import partial
from tkinter import messagebox
from copy import deepcopy

# sign variable to decide the turn of which player
sign = 0

# Creates an empty board
global board

board = [[" " for x in range(3)] for y in range(3)]


# Check l(O/X) won the match or not
# according to the rules of the game
def winner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))


# Configure text on button while playing with another player
def get_value(i, j, gb, l1, l2):
    global sign

    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    if winner(board, "X"):
        gb.destroy()
        print(username1)  # testing value
        print(username2)
        box = messagebox.showinfo("Winner", "Player 1 won the match")

        conn = sqlite3.connect('player_info.db')
        c = conn.cursor()
        c.execute("SELECT * FROM players WHERE user_name =? ", (username1,))
        count = int(len(c.fetchall()))
        print(count)
        if count == 0:
            print("in insert")
            c.execute("insert INTO players(user_name,no_of_wins,no_of_loss,points) VALUES(?, 1,0,10)", (username1,))
        else:
            print("in update")
            c.execute("""UPDATE players SET no_of_wins = no_of_wins + 1  WHERE user_name = 
                ?""", (username1,))
            c.execute("""UPDATE players SET points = points + 10  WHERE user_name = 
                ?""", (username1,))
        c.execute("SELECT * FROM players WHERE user_name =? ", (username2,))
        count = int(len(c.fetchall()))
        print(count)
        if count == 0:
            print("in insert2")
            c.execute("insert INTO players(user_name,no_of_wins,no_of_loss,points) VALUES(?, 0,1,0)", (username2,))
        else:
            print("in update2")
            c.execute("""UPDATE players SET no_of_loss = no_of_loss + 1  WHERE user_name = 
                        ?""", (username2,))

        conn.commit()
        conn.close()


    elif winner(board, "O"):
        gb.destroy()
        box = messagebox.showinfo("Winner", "Player 2 won the match")
        conn = sqlite3.connect('player_info.db')
        c2 = conn.cursor()
        c2.execute("SELECT * FROM players WHERE user_name =? ", (username2,))
        count = int(len(c2.fetchall()))
        print(count)
        if count == 0:
            print("in insertplayer2")
            c2.execute("insert INTO players(user_name,no_of_wins,no_of_loss,points) VALUES(?, 1,0,10)", (username2,))
        else:
            print("in update")
            c2.execute("""UPDATE players SET no_of_wins = no_of_wins + 1  WHERE user_name = 
                       ?""", username2)
            c2.execute("""UPDATE players SET points = points + 10  WHERE user_name = 
                       ?""", username2)
        c2.execute("SELECT * FROM players WHERE user_name =? ", (username1,))
        count = int(len(c2.fetchall()))
        print(count)
        if count == 0:
            print("in insert2")
            c2.execute("insert INTO players(user_name,no_of_wins,no_of_loss,points) VALUES(?, 0,1,0)", (username1,))
        else:
            print("in update2")
            c2.execute("""UPDATE players SET no_of_loss = no_of_loss + 1  WHERE user_name = 
                               ?""", (username1,))
        conn.commit()
        conn.close()

    elif isfull():
        gb.destroy()
        box = messagebox.showinfo("Tie Game", "Tie Game")





# Check the board is full or not
def isfull():
    flag = True
    for i in board:
        if i.count(' ') > 0:
            flag = False
    return flag


# Create the GUI of game board for play along with another player
def gameboard_players(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            if board[i][j] != ' ':
                board[i][j] = ' '
                print("in if cond")
            print(board)
            n = j
            button[i].append(j)
            get_t = partial(get_value, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()
def machine():
    possiblemove = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                possiblemove.append([i, j])
    move = []
    if possiblemove == []:
        return
    else:
        for let in ['O', 'X']:
            for i in possiblemove:
                boardcopy = deepcopy(board)
                boardcopy[i[0]][i[1]] = let
                if winner(boardcopy, let):
                    return i
        corner = []
        for i in possiblemove:
            if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corner.append(i)
        if len(corner) > 0:
            move = random.randint(0, len(corner) - 1)
            return corner[move]
        edge = []
        for i in possiblemove:
            if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                edge.append(i)
        if len(edge) > 0:
            move = random.randint(0, len(edge) - 1)
            return edge[move]


# Configure text on button while playing with system
def get_value_pc(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    x = True
    if winner(board, "X"):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Winner", "Player won the match")
        conn = sqlite3.connect('player_info.db')
        c = conn.cursor()
        c.execute("SELECT * FROM players WHERE user_name =? ", (user_name,))
        count = int(len(c.fetchall()))
        print(count)
        if count == 0:
            print("in insert")
            c.execute("insert INTO players(user_name,no_of_wins,no_of_loss,points) VALUES(?, 1,0,10)", (user_name,))
        else:
            print("in update")
            c.execute("""UPDATE players SET no_of_wins = no_of_wins + 1  WHERE user_name = 
                      ?""", (user_name,))
            c.execute("""UPDATE players SET points = points + 10  WHERE user_name = 
                      ?""", (user_name,))

        conn.commit()
        conn.close()

    elif winner(board, "O"):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Winner", "Computer won the match")

    elif isfull():
        gb.destroy()
        x = False
        box = messagebox.showinfo("Tie Game", "Tie Game")
    if x:
        if sign % 2 != 0:
            move = machine()
            button[move[0]][move[1]].config(state=DISABLED)
            get_value_pc(move[0], move[1], gb, l1, l2)


# Create the GUI of game board for play along with system
def gameboard_pc(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            if board[i][j] != ' ':
                board[i][j] = ' '
            n = j
            button[i].append(j)
            get_t = partial(get_value_pc, i, j, game_board, l1, l2)
            button[i][j] = Button(game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()

# db connections
def connection():
    conn = sqlite3.connect('player_info.db')
    curs = conn.cursor()

    # create table
    curs.execute("""Create table IF NOT EXISTS players(id integer PRIMARY KEY AUTOINCREMENT,user_name text, no_of_wins integer, no_of_loss integer, 
                 points  integer)""")

    # commit changes
    conn.commit()
    conn.close()
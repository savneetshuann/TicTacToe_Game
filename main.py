# Tic Tac Toe game
#Github Project Link: https://github.com/savneetshuann/TicTacToe_Game
import tkinter
from PIL import ImageTk, Image
import PIL.Image
import os
import numpy as np  # using numpy library
import random
import tkinter as tk  # using tkinter library for GUI
from tkinter import *
import sqlite3
from tkinter import ttk  # using tkinter library for  tkinter tree table
import matplotlib.pyplot as plt  # using matplotlib for plotting of graph
from functools import partial  # importing partial function
from tkinter import messagebox
from copy import deepcopy  # for recursive copying

# sign variable to decide the turn of which player
from PIL import ImageTk

sign = 0

# Creates an empty board
global board

board = [[" " for x in range(3)] for y in range(3)]  # empty board


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
        messagebox.showinfo("Winner", "Player 1 won the match")

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

    # winner board for player 2 winning the game
    elif winner(board, "O"):
        gb.destroy()
        messagebox.showinfo("Winner", "Player 2 won the match")
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
                       ?""", (username2,))
            c2.execute("""UPDATE players SET points = points + 10  WHERE user_name = 
                       ?""", (username2,))
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
        messagebox.showinfo("Tie Game", "Tie Game")


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
            print(board)
            n = j
            button[i].append(j)
            get_t = partial(get_value, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()


# machine logic for tictactoe
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
                boardcopy = deepcopy(board)  # using deepcopy
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
        messagebox.showinfo("Winner", "Player won the match")
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
        messagebox.showinfo("Winner", "Computer won the match")

    elif isfull():
        gb.destroy()
        x = False
        messagebox.showinfo("Tie Game", "Tie Game")
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


# Initialize the game board to play with system
def with_machine(game_board, username):
    global user_name
    user_name = username.get()
    game_board.destroy()
    game_board = Tk()
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player : X", width=10)
    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Computer : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_pc(game_board, l1, l2)


# Initialize the game board to play with another player
def with_player(game_board, user_name1, user_name2):
    global username1
    global username2
    username1 = user_name1.get()
    username2 = user_name2.get()
    print(username1)
    print(username2)

    game_board.destroy()
    game_board = Tk()
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player 1 : X", width=10)

    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Player 2 : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_players(game_board, l1, l2)

    # clear text box


# gameboard for single player
def open_single():
    game_board = Tk()
    wpc = partial(with_machine, game_board)
    user_name_label = Label(game_board, text="Enter your username: ")
    user_name_label.grid(row=0, column=0)
    user_name = Entry(game_board, width=30)
    user_name.grid(row=1, column=0, padx=10)
    submit_btn = Button(game_board, text="Play", command=lambda: wpc(user_name), activeforeground='white',
                        activebackground="grey", bg="blue", fg="white", font='Gabriola', width=7)
    submit_btn.grid(row=2, column=0, pady=10, padx=10)
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


# menu method for multi player plays
def open_multiple(menu):
    top = Tk()
    user_name_label1 = Label(top, text="Enter username for Player1: ")
    user_name_label1.grid(row=0, column=0)
    user_name1 = Entry(top, width=30)  # user1 from here need to insert in database
    user_name1.grid(row=1, column=0, padx=10)

    user_name_label2 = Label(top, text="Enter username for Player2: ")
    user_name_label2.grid(row=2, column=0)
    user_name2 = Entry(top, width=30)
    user_name2.grid(row=3, column=0, padx=10)
    wpl = partial(with_player, top)
    submit_btn = Button(top, text="Play", command=lambda: wpl(user_name1, user_name2), activeforeground='white',
                        activebackground="grey", bg="blue", fg="white", font='Gabriola', width=7)
    submit_btn.grid(row=4, column=0, pady=10, padx=10)
    top.mainloop()


# top ranked players bar graph
def top_play():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    con = sqlite3.connect('player_info.db')
    cur = con.cursor()
    cur.execute(
        'SELECT * FROM(SELECT user_name,points, RANK() OVER (ORDER BY points DESC) PRANK FROM players) WHERE '
        'PRANK <=3')
    # the data
    data = []
    xTickMarks = []

    for row in cur:
        data.append(int(row[1]))
        xTickMarks.append(str(row[0]))
    con.commit()
    con.close()
    # necessary variables
    ind = np.arange(len(data))  # the x locations for the groups
    width = 0.35  # the width of the bars

    # the bars
    rects1 = ax.bar(ind, data, width,
                    color='black',
                    error_kw=dict(elinewidth=2, ecolor='red'))

    # axes and labels
    ax.set_xlim(-width, len(ind) + width)
    ax.set_ylim(0, 100)

    ax.set_ylabel('POINTS')  # Y axis
    ax.set_xlabel('NAMES')  # X axis
    ax.set_title('TOP RATED PLAYERS (RANK WISE )')  # Title of bar graph

    ax.set_xticks(ind + width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=10)

    plt.show()


# method for scoreboard
def scoreboard():
    def View():  # Method to View the data into the Scoreboard Table
        con1 = sqlite3.connect('player_info.db')
        cur1 = con1.cursor()
        cur1.execute("Select user_name,no_of_wins,points from players")
        rows = cur1.fetchall()

        for row in rows:
            print(row)

            tree.insert("", tk.END, values=row)

        con1.close()

    root = tk.Tk()

    tree = ttk.Treeview(root, column=("c1", "c2", "c3"), show='headings')

    tree.column("#1", anchor=tk.CENTER)

    tree.heading("#1", text="NAME")

    tree.column("#2", anchor=tk.CENTER)

    tree.heading("#2", text="WINS")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="POINTS")
    tree.pack()
    View()
    root.mainloop()


# creating the GUI for the game
def run():
    menu = Tk()
    menu.geometry("650x650")
    menu.title("Tic Tac Toe")
    menu.iconbitmap('Tic_tac_toe.ico')

    # loading the image
    image = PIL.Image.open("Tic_tac_toe.png")
    # image = image.resize((450, 350), Image.ANTIALIAS)
    resized = image.resize((200, 200), PIL.Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized)

    panel = tkinter.Label(menu, image=img)

    panel.pack(side="top", padx=20)

    head = Label(menu, text="Welcome to Tic-Tac-Toe",
                 activeforeground='white',
                 activebackground="black", bg="white",
                 fg="black", width=500, font='Modern', bd=5)

    menu1 = Button(menu, text="Single Player", command=open_single, activeforeground='white',
                   activebackground="grey", bg="blue", fg="white",
                   width=500, font='Gabriola', bd=5)

    menu2 = Button(menu, text="Multi Player", command=lambda: open_multiple(menu), activeforeground='white',
                   activebackground="grey", bg="blue", fg="white",
                   width=500, font='Gabriola', bd=5)

    menu3 = Button(menu, text="Scoreboard", command=scoreboard, activeforeground='white',
                   activebackground="grey", bg="blue", fg="white",
                   width=500, font='Gabriola', bd=5)

    menu4 = Button(menu, text="Top Players", command=top_play, activeforeground='white',
                   activebackground="grey", bg="blue", fg="white",
                   width=500, font='Gabriola', bd=5)

    menu5 = Button(menu, text="Exit", command=menu.quit, activeforeground='white',
                   activebackground="grey", bg="blue", fg="white",
                   width=500, font='Gabriola', bd=5)

    head.pack(side='top')
    panel.pack(side="top", padx=10)
    menu1.pack(side='top', padx=10)
    menu2.pack(side='top', padx=10)
    menu3.pack(side='top', padx=10)
    menu4.pack(side='top', padx=20)
    menu5.pack(side='top', padx=20)
    menu.mainloop()


# table creation
connection()

# execute the program
run()

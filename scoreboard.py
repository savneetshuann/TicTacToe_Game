from tkinter import ttk  # we use ttk for more advance styles and tree frame in scoreboard
import tkinter as tk
import sqlite3


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

button1 = tk.Button(text="Display data", command=View)

button1.pack(pady=10)

root.mainloop()

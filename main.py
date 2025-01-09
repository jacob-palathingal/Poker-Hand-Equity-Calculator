import tkinter as tk
# Dropdown values for cards
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['s', 'h', 'd', 'c']
# GUI Initialization
root = tk.Tk()
root.title("Texas Hold'em Odds Calculator")
root.geometry("900x600")

# Player input fields
player_cards = [[tk.StringVar(), tk.StringVar()] for _ in range(6)]
player_suits = [[tk.StringVar(), tk.StringVar()] for _ in range(6)]

for i in range(6):
    tk.Label(root, text=f"Player {i + 1}").grid(row=i, column=0)
    tk.OptionMenu(root, player_cards[i][0], *VALUES).grid(row=i, column=1)
    tk.OptionMenu(root, player_suits[i][0], *SUITS).grid(row=i, column=2)
    tk.OptionMenu(root, player_cards[i][1], *VALUES).grid(row=i, column=3)
    tk.OptionMenu(root, player_suits[i][1], *SUITS).grid(row=i, column=4)

# Community card fields
tk.Label(root, text="Community Cards").grid(row=6, column=0)
c1, s1 = tk.StringVar(), tk.StringVar()
c2, s2 = tk.StringVar(), tk.StringVar()
c3, s3 = tk.StringVar(), tk.StringVar()
c4, s4 = tk.StringVar(), tk.StringVar()
c5, s5 = tk.StringVar(), tk.StringVar()

tk.OptionMenu(root, c1, *VALUES).grid(row=6, column=1)
tk.OptionMenu(root, s1, *SUITS).grid(row=6, column=2)
tk.OptionMenu(root, c2, *VALUES).grid(row=6, column=3)
tk.OptionMenu(root, s2, *SUITS).grid(row=6, column=4)
tk.OptionMenu(root, c3, *VALUES).grid(row=6, column=5)
tk.OptionMenu(root, s3, *SUITS).grid(row=6, column=6)
tk.OptionMenu(root, c4, *VALUES).grid(row=6, column=7)
tk.OptionMenu(root, s4, *SUITS).grid(row=6, column=8)
tk.OptionMenu(root, c5, *VALUES).grid(row=6, column=9)
tk.OptionMenu(root, s5, *SUITS).grid(row=6, column=10)

root.mainloop()


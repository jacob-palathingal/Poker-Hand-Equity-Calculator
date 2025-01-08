import tkinter as tk

# GUI Initialization
root = tk.Tk()
root.title("Texas Hold'em Odds Calculator")
root.geometry("400x300")

# Player 1 Card Inputs
tk.Label(root, text="Player 1 Card 1").grid(row=0, column=0)
player_card1 = tk.StringVar()
player_suit1 = tk.StringVar()
tk.Entry(root, textvariable=player_card1).grid(row=0, column=1)
tk.Entry(root, textvariable=player_suit1).grid(row=0, column=2)

tk.Label(root, text="Player 1 Card 2").grid(row=1, column=0)
player_card2 = tk.StringVar()
player_suit2 = tk.StringVar()
tk.Entry(root, textvariable=player_card2).grid(row=1, column=1)
tk.Entry(root, textvariable=player_suit2).grid(row=1, column=2)

# Results Display
result_label = tk.Label(root, text="Results will appear here.")
result_label.grid(row=2, column=0, columnspan=3, pady=10)

# Run GUI
root.mainloop()


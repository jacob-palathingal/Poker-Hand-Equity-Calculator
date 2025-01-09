import tkinter as tk
from deuces import Card, Evaluator, Deck

# Dropdown values for cards
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['s', 'h', 'd', 'c']

# Function to calculate odds for up to 6 players
def calculate_odds():
    try:
        players = []
        for i in range(6):  # Iterate through player inputs
            card1 = player_cards[i][0].get() + player_suits[i][0].get()
            card2 = player_cards[i][1].get() + player_suits[i][1].get()
            if card1 and card2:
                players.append([Card.new(card1), Card.new(card2)])

        # Get community cards
        community_deck = []
        if c1.get() and s1.get():
            community_deck.append(Card.new(c1.get() + s1.get()))
        if c2.get() and s2.get():
            community_deck.append(Card.new(c2.get() + s2.get()))
        if c3.get() and s3.get():
            community_deck.append(Card.new(c3.get() + s3.get()))
        if c4.get() and s4.get():
            community_deck.append(Card.new(c4.get() + s4.get()))
        if c5.get() and s5.get():
            community_deck.append(Card.new(c5.get() + s5.get()))

        # Initialize Evaluator and Deck
        evaluator = Evaluator()
        deck = Deck()

        # Remove all known cards (player and community cards) from the deck
        for player in players:
            for card in player:
                deck.cards.remove(card)
        for card in community_deck:
            deck.cards.remove(card)

        # Monte Carlo simulation for equity calculation
        win_counts = [0] * len(players)
        tie_counts = [0] * len(players)
        num_trials = 10000  # Number of simulations

        for _ in range(num_trials):
            deck.shuffle()
            remaining_board = deck.draw(5 - len(community_deck))
            full_board = community_deck + remaining_board

            scores = [evaluator.evaluate(full_board, player) for player in players]
            min_score = min(scores)
            winners = [i for i, score in enumerate(scores) if score == min_score]

            if len(winners) == 1:
                win_counts[winners[0]] += 1
            else:
                for winner in winners:
                    tie_counts[winner] += 1

        # Calculate equity percentages
        results = []
        for i in range(len(players)):
            win_percent = (win_counts[i] / num_trials) * 100
            tie_percent = (tie_counts[i] / num_trials) * 100
            results.append(f"Player {i + 1}: Win = {win_percent:.2f}%, Tie = {tie_percent:.2f}%")

        result_label.config(text="\n".join(results))
    except Exception as e:
        result_label.config(text=f"Error: {e}")

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


import tkinter as tk
from deuces import Card, Evaluator, Deck
import random

# Dropdown values for cards:
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['s', 'h', 'd', 'c']

# Hand rankings map
HAND_RANKINGS = {
    1: "Royal Flush",
    2: "Straight Flush",
    3: "Four of a Kind",
    4: "Full House",
    5: "Flush",
    6: "Straight",
    7: "Three of a Kind",
    8: "Two Pair",
    9: "One Pair",
    10: "High Card"
}

def get_hand_rank_class(evaluator, board, hand):
    """Get the hand rank class (e.g., Full House, Flush, etc.)"""
    # For preflop, we need to evaluate just the hole cards
    if not board:
        # Convert hole cards to ranks for pair detection
        ranks = [Card.get_rank_int(card) for card in hand]
        if ranks[0] == ranks[1]:
            return 9  # One Pair
        return 10  # High Card
    
    score = evaluator.evaluate(board, hand)
    rank_class = evaluator.get_rank_class(score)
    
    # Double check for two pair and three of a kind scenarios
    # Convert all cards to ranks for counting
    all_cards = hand + board
    ranks = [Card.get_rank_int(card) for card in all_cards]
    rank_counts = {}
    for rank in ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    
    pairs = sum(1 for count in rank_counts.values() if count == 2)
    three_of_kinds = sum(1 for count in rank_counts.values() if count == 3)
    
    # Override rank class if necessary
    if three_of_kinds == 1:
        return 7  # Three of a Kind
    elif pairs == 2:
        return 8  # Two Pair
    elif pairs == 1:
        return 9  # One Pair
        
    return rank_class
    
def calculate_odds():
    try:
        players = []
        # Gather player card inputs
        for i in range(6):
            card1_str = player_cards[i][0].get() + player_suits[i][0].get()
            card2_str = player_cards[i][1].get() + player_suits[i][1].get()
            
            if player_cards[i][0].get() and player_suits[i][0].get() \
               and player_cards[i][1].get() and player_suits[i][1].get():
                card1 = Card.new(card1_str)
                card2 = Card.new(card2_str)
                players.append([card1, card2])

        if not players:
            raise ValueError("At least one player's hole cards must be entered.")

        # Gather community card inputs
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
        
        if len(community_deck) > 5:
            raise ValueError("Cannot have more than 5 community cards.")

        # Determine the current street based on number of community cards
        if len(community_deck) == 0:
            street = "Preflop"
            cards_to_come = 5
        elif len(community_deck) == 3:
            street = "Flop"
            cards_to_come = 2
        elif len(community_deck) == 4:
            street = "Turn"
            cards_to_come = 1
        elif len(community_deck) == 5:
            street = "River"
            cards_to_come = 0
        else:
            raise ValueError("Invalid number of community cards. Must be 0 (preflop), 3 (flop), 4 (turn), or 5 (river).")

        # Create deck and remove known cards
        deck = Deck()
        known_cards = []
        for player in players:
            known_cards.extend(player)
        known_cards.extend(community_deck)
        
        deck.cards = [card for card in deck.cards if card not in known_cards]
        remaining_cards = deck.cards.copy()

        # Monte Carlo simulation
        win_counts = [0] * len(players)
        tie_counts = [0] * len(players)
        num_trials = 10000
        evaluator = Evaluator()

        # Get current hand type for each player
        current_hands = []
        for player in players:
            rank_class = get_hand_rank_class(evaluator, community_deck, player)
            current_hands.append(HAND_RANKINGS.get(rank_class, "Unknown"))

        for _ in range(num_trials):
            trial_cards = remaining_cards.copy()
            random.shuffle(trial_cards)
            
            trial_board = community_deck.copy()
            if cards_to_come > 0:
                trial_board.extend(trial_cards[:cards_to_come])
            
            scores = []
            for player in players:
                score = evaluator.evaluate(trial_board, player)
                scores.append(score)
            
            min_score = min(scores)
            winners = [i for i, score in enumerate(scores) if score == min_score]

            if len(winners) == 1:
                win_counts[winners[0]] += 1
            else:
                for w in winners:
                    tie_counts[w] += 1

        # Calculate equity percentages and prepare results
        results = [f"Current Street: {street}\n"]

        # Add player results with their current hand
        for i in range(len(players)):
            win_percent = (win_counts[i] / num_trials) * 100
            tie_percent = (tie_counts[i] / num_trials) * 100
            equity = win_percent + (tie_percent / len(players))
            
            results.append(f"Player {i + 1}:")
            results.append(f"Current Hand: {current_hands[i]}")
            results.append(f"Equity: Win = {win_percent:.2f}%, Tie = {tie_percent:.2f}%, Total = {equity:.2f}%\n")

        result_label.config(text="\n".join(results))

    except Exception as e:
        result_label.config(text=f"Error: {e}")

def reset_fields():
    # Clear all player fields
    for i in range(6):
        player_cards[i][0].set('')
        player_suits[i][0].set('')
        player_cards[i][1].set('')
        player_suits[i][1].set('')
    # Clear community fields
    c1.set(''), s1.set('')
    c2.set(''), s2.set('')
    c3.set(''), s3.set('')
    c4.set(''), s4.set('')
    c5.set(''), s5.set('')
    # Reset result label
    result_label.config(text="Results will appear here.")

# GUI Setup
root = tk.Tk()
root.title("Texas Hold'em Odds Calculator")
root.geometry("900x700")

# Create StringVars for each player's cards
player_cards = [[tk.StringVar(), tk.StringVar()] for _ in range(6)]
player_suits = [[tk.StringVar(), tk.StringVar()] for _ in range(6)]

# Labels and OptionMenus for 6 players
for i in range(6):
    tk.Label(root, text=f"Player {i + 1}").grid(row=i, column=0, padx=5, pady=5, sticky='w')
    tk.OptionMenu(root, player_cards[i][0], *VALUES).grid(row=i, column=1)
    tk.OptionMenu(root, player_suits[i][0], *SUITS).grid(row=i, column=2)
    tk.OptionMenu(root, player_cards[i][1], *VALUES).grid(row=i, column=3)
    tk.OptionMenu(root, player_suits[i][1], *SUITS).grid(row=i, column=4)

# Community card labels and OptionMenus
tk.Label(root, text="Community Cards").grid(row=6, column=0, padx=5, pady=5, sticky='w')

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

# Add instructions label
instructions = """
Instructions:
- Preflop: Enter only player hole cards
- Flop: Enter player cards and first 3 community cards
- Turn: Enter player cards and first 4 community cards
- River: Enter player cards and all 5 community cards
"""
instructions_label = tk.Label(root, text=instructions, justify=tk.LEFT)
instructions_label.grid(row=9, column=0, columnspan=11, padx=5, pady=5, sticky='w')

# Buttons
calculate_button = tk.Button(root, text="Calculate Odds", command=calculate_odds)
calculate_button.grid(row=7, column=0, columnspan=5, pady=10)

reset_button = tk.Button(root, text="Reset", command=reset_fields)
reset_button.grid(row=7, column=5, columnspan=5, pady=10)

# Result display label
result_label = tk.Label(root, text="Results will appear here.", justify=tk.LEFT)
result_label.grid(row=8, column=0, columnspan=11, padx=5, pady=5, sticky='w')

root.mainloop()
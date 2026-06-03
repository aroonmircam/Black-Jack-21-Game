import random

deck = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def get_value(card):
    if card in "JQK":
        return 10
    if card == "A":
        return 11
    return int(card)

def get_total(hand):
    score = sum(get_value(card) for card in hand)
    aces = hand.count("A")
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def draw_card(card_rank):
    return [
        "┌─────┐",
        f"│ {card_rank:<2}  │",
        "│     │",
        f"│  {card_rank:>2} │",
        "└─────┘"
    ]

def display_hand(hand, name):
    print("\n" + name)
    for i in range(5):
        print(" ".join(draw_card(card)[i] for card in hand))
    print("Total:", get_total(hand))


class BlackjackGame:
    def __init__(self):
        self.balance = 100
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def show_menu(self):
        print("\n" + "="*30)
        print("      MAIN MENU")
        print(f"Current Balance: ${self.balance}")
        print(f"Record: {self.wins} W / {self.losses} L / {self.ties} D")
        print("="*30)
        print("1. Play a round")
        print("2. Quit game")
        return input("Select an option: ")

    def play_round(self):
        if self.balance <= 0:
            print("\nYou ran out of money! Here is a $50 courtesy refill.")
            self.balance = 50

        while True:
            try:
                bet = int(input(f"\nHow much do you want to bet? (Max: ${self.balance}): "))
                if 0 < bet <= self.balance:
                    break
                print("Invalid amount.")
            except ValueError:
                print("Please enter a valid number.")

        shoe = deck * 4
        random.shuffle(shoe)

        player_hand = [shoe.pop(), shoe.pop()]
        dealer_hand = [shoe.pop(), shoe.pop()]

        while True:
            display_hand(player_hand, "YOUR HAND")
            print(f"\nDealer shows: {dealer_hand[0]} [?]")

            if get_total(player_hand) > 21:
                break

            action = input("\n(h)it or (s)tand?: ").lower()
            if action == "h":
                player_hand.append(shoe.pop())
            else:
                break

        player_score = get_total(player_hand)

        if player_score <= 21:
            while get_total(dealer_hand) < 17:
                dealer_hand.append(shoe.pop())

        dealer_score = get_total(dealer_hand)

        display_hand(player_hand, "YOUR FINAL HAND")
        display_hand(dealer_hand, "DEALER FINAL HAND")

        if player_score > 21:
            print("\nBust! You went over 21. You lose the round.")
            self.balance -= bet
            self.losses += 1
        elif dealer_score > 21:
            print(f"\nDealer bust! You win ${bet}.")
            self.balance += bet
            self.wins += 1
        elif player_score > dealer_score:
            print(f"\nYou win the round! You win ${bet}.")
            self.balance += bet
            self.wins += 1
        elif player_score < dealer_score:
            print("\nDealer wins. You lose your bet.")
            self.balance -= bet
            self.losses += 1
        else:
            print("\nIt's a tie! Your bet is refunded.")
            self.ties += 1


def main():
    print("Welcome to BLACKJACK 21")
    game = BlackjackGame()

    while True:
        choice = game.show_menu()
        if choice == "1":
            game.play_round()
        elif choice == "2":
            print("\nThanks for playing! Your final stats were:")
            print(f"Wins: {game.wins} | Losses: {game.losses} | Ties: {game.ties}")
            print(f"You leave with: ${game.balance}")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
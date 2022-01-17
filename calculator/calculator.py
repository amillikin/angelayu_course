############### Blackjack Project #####################

#Difficulty Normal 😎: Use all Hints below to complete the project.
#Difficulty Hard 🤔: Use only Hints 1, 2, 3 to complete the project.
#Difficulty Extra Hard 😭: Only use Hints 1 & 2 to complete the project.
#Difficulty Expert 🤯: Only use Hint 1 to complete the project.

############### Our Blackjack House Rules #####################

## The deck is unlimited in size. 
## There are no jokers. 
## The Jack/Queen/King all count as 10.
## The the Ace can count as 11 or 1.
## Use the following list as the deck of cards:
## cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
## The cards in the list have equal probability of being drawn.
## Cards are not removed from the deck as they are drawn.
## The computer is the dealer.

import random
# from replit import clear
from art import logo
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

# Accepts a player's hand in list format, returns sum of cards in hand
def hand_total(player_hand):
  return sum(player_hand)

# Checks if hand is bust (over 21)
def bust(player_hand):
  return hand_total(player_hand) > 21

# Appends a random card to the player's hand and returns that player's hand
def hit(player_hand, player_name):
  hit_card = cards[random.randint(0,12)]
  print(f"{player_name} hit {hit_card}")
  player_hand.append(hit_card)
  return player_hand

# If a player's hand is bust and has an ace used as an 11, swap to 1
def ace_swap(player_hand):
  while bust(player_hand) and 11 in player_hand:
    player_hand[player_hand.index(11)] = 1
  return player_hand

def deal():
  hands_of_cards = {
    "dealer": [],
    "user": []
  }
  hands_of_cards["dealer"] = hit(hands_of_cards["dealer"], "Dealer")
  for add_card in range(2):
    hands_of_cards["user"] = hit(hands_of_cards["user"], "User")
  return hands_of_cards

def declare_winner(hands_of_cards):
  if hands_of_cards["dealer"] > hands_of_cards["user"]:
    print("Dealer wins. Better luck next time.")
  elif hands_of_cards["dealer"] < hands_of_cards["user"]:
    print("You have won! Congratulations.")
  else:
    print("Hands are tied. This is a standoff.")

def blackjack():
  hands_of_cards = deal()

  print(f"Your cards: {hands_of_cards['user']}, " + \
        f"current score: {hand_total(hands_of_cards['user'])}\n" + \
        f"Computers first card: {hand_total(hands_of_cards['dealer'])}")

  # Offer user to hit until bust or stand
  stand = False
  while not stand and not bust(hands_of_cards["user"]):
    response = input("Type 'y' to get another card, type 'n' to pass:\n")
    if response == "y":
      hands_of_cards["user"] = hit(hands_of_cards["user"],"User")
      hands_of_cards["user"] = ace_swap(hands_of_cards["user"])
    else:
      stand = True

  if bust(hands_of_cards["user"]):
    print(f"You have lost. Bust with score: {hand_total(hands_of_cards['user'])}")
  else:
    print(f"You stand with score: {hand_total(hands_of_cards['user'])}")
    # Dealer's actions
    while hand_total(hands_of_cards["dealer"]) < 17:
      hands_of_cards["dealer"] = hit(hands_of_cards["dealer"], "Dealer")
      hands_of_cards["dealer"] = ace_swap(hands_of_cards["dealer"])
    if bust(hands_of_cards["dealer"]):
      print(f"You have won!\n \
              Dealer bust with score: {hand_total(hands_of_cards['dealer'])}")
    else:
      declare_winner(hands_of_cards)

  print(f"Your cards: {hands_of_cards['user']}\n" + \
        f"Your total: {hand_total(hands_of_cards['user'])}\n" + \
        f"Computer cards: {hands_of_cards['dealer']}\n" + \
        f"Computer total: {hand_total(hands_of_cards['dealer'])}")

print(logo)
response = input("Welcome to some Blackjack game. Shall I deal a hand for us?\n").lower()

still_playing = True
while still_playing:
  if response in ("yes","y"):
    blackjack()
    response = input("Continue playing?\n").lower()
    #clear()
  else:
    print("Well, in that case, have a good day.")
    still_playing = False

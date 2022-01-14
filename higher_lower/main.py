from art import logo
from art import vs
from game_data import data
import random
import os

def get_random_item():
  return random.choice(data)

def correct_answer(selection_a, selection_b, choice):
  return (selection_a["follower_count"] > selection_b["follower_count"] and \
         choice == "A") or \
         selection_a["follower_count"] == selection_b["follower_count"]

def draw_screen_vs(selection_a, selection_b, score):
  os.system('clear')
  print(logo)
  if score > 0:
    print(f"You're right! Current score: {score}.")
  print(f"Compare A: {selection_a['name']}, " + \
        f"a {selection_a['description']}, " + \
        f"from {selection_a['country']}.\n" + \
        vs + "\n" + \
        f"Compare B: {selection_b['name']}, " +
        f"a {selection_b['description']}, from {selection_b['country']}.")

game_over = False
score = 0
while not game_over:

  competitors = [get_random_item(), get_random_item()]
  while competitors[0]["name"] == competitors[1]["name"]:
    competitors[1] = get_random_item()
  draw_screen_vs(competitors[0], competitors[1], score)
  choice = input("Who has more followers? Type 'A' or 'B': ").upper()
  while choice not in ("A","B" ):
    choice = input("Not a valid choice, please select 'A' or 'B': ")

  if correct_answer(competitors[0], competitors[1], choice):
    score += 1
  else:
    game_over = True
    os.system('clear')
    print(logo)
    print(f"Sorry, that's wrong. Final score: {score}")
     
    


  

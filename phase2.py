import cards
import player
import poker
import hand_strength
import pickle
import phase1



dataset_src = open("dataset_huge","r")
dataset = pickle.load(dataset_src)
dataset_src.close()

print(dataset)

def isset(var, v):
  try:
      var[v]
      return True
  except KeyError:
      return False

# Takes two cards c1 and c2. 
def fetch_rollout_data(players, hole_cards):
  val1 = "%s,%s" % (hole_cards[0][0], hole_cards[1][0])
  val2 = "%s,%s" % (hole_cards[1][0], hole_cards[0][0])

  suits = "suited" if cards.card_suit(hole_cards[0]) == cards.card_suit(hole_cards[1]) else "unsuited"

  print("Players: %s" % players)

  if isset(dataset[players], val1):
    return dataset[players][val1][suits]
  
  if isset(dataset[players], val2):
    return dataset[players][val2][suits]

  return False



class Phase2(player.Player):
  def take_action(self, highest_bet, pot, players, position, shared_cards):
    if len(shared_cards) < 1: # pre-flop
      
      # Fetch information from stored data for rollout simulations.

      strength = fetch_rollout_data(players, self.cards)

    else:
      # Use hand strength calculations
      hand = hand_strength.HandStrength(players)
      strength = hand.calculations(self.cards, shared_cards)

    # We now have strength. Use this to take actions. 

    # Simple solutions for testing (don't take pre/post flop into account)

    if strength > 0.7: # raise
      return self.raise_action(highest_bet)
    elif strength > 0.3: # call
      return self.call_action(highest_bet)
    else: #fold
      return self.fold_action()







  
  


# Play styles:
# "tight_passive"
# "tight_aggressive"
# "loose_passive"
# "loose_aggressive"


players = [
  Phase2("Mikael", 1000, "loose_aggressive"), 
  Phase2("Marius", 1000, "loose_aggressive"),
  Phase2("Martin", 1000, "loose_aggressive"),
  Phase2("Jostein", 1000, "loose_passive"),
  Phase2("Emil", 1000, "loose_passive"),
  phase1.Phase1("Steinar", 1000, "loose_passive"),
  phase1.Phase1("Stian", 1000, "loose_passive"),
  phase1.Phase1("Selmer", 1000, "tight_passive"),
  phase1.Phase1("Ole Jorgen", 1000, "tight_passive"),
  phase1.Phase1("Andre the giant", 1000, "tight_aggressive")
]

p = poker.poker(players, 10);

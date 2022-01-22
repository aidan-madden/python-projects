from random import randint

class Card:
	'''
	A class to represent a single Card.
	
	...

	Attributes
	__________

	suit : str
		suit of the card (hearts, spades, clubs, diamonds)
	value: str
		value of the card (Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King)

	'''
	def __init__(self, suit, value):
		'''
		Constructs the necessary suit and value attributes for the Card object.
		'''	
	
		self.suit = suit
		self.value = value

	def __repr__(self):
		'''
		Returns printable representation of the Card object (example: Ace of spades).
		'''
		return f"{self.value} of {self.suit}"
class Deck: 
	'''
	A class to represent a single Deck of cards.

	...

	Attributes
	_________

	suits : list
		all possible suits for a Card

	values : list
		all possible values for a Card

	cards : list
		all Card objects contained in a given Deck
	'''
	
	suits = ['hearts','spades','clubs','diamonds']
	values = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

	def __init__(self, suits = suits, values = values, cards = []):
		'''
		Builds an ordered list of 52 Card objects and assigns to the cards attribute. If a list of Card objects is provided by the shuffle method, assign this list instead. 
		'''

		if cards:
			self.cards = cards
		else:
			for suit in suits:
				for value in values:
					cards.append(Card(suit,value))
			self.cards = cards		
	
class Dealer:

	'''
	A class to represent a single Dealer.

	Methods
	_______
	shuffle():
		Reset and shuffle the deck of cards. 

	deal_one_card():
		Deals one card from the top of the deck.
	'''

	def __init__(self):
		'''
		Assigns a Deck object to the deck attribute.	
		'''
		self.deck = Deck()

	def shuffle(self):
		'''
		Reset and shuffle the deck.

		A shuffled list of Card objects is built by popping a randomly generated index from the existing cards list and returning to a temporary new_cards list. Once all Card objects are exhausted from the cards list, a new Deck object is created using the new_cards list as an argument and assigned to the deck attribute.  	
		'''
		self.deck = Deck()
		new_cards = []
		for i in range(len(self.deck.cards) - 1, -1, -1):
			random_index = randint(0,i)
			new_cards.append(self.deck.cards.pop(random_index))
		self.deck = Deck(cards=new_cards)

	def deal_one_card(self):
		'''
		A single Card object is popped from the end of the cards list and returned to the user. Once all 52 cards are dealt, an error message is printed. 
		'''
		try:
			return self.deck.cards.pop()
		except	IndexError:
			print("All cards have been dealt. Please use the shuffle() method to reset and shuffle the deck, if desired.")			

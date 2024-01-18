from tkinter import *
import random
from PIL import Image, ImageTk
#Pip install Pillow ^


root = Tk()
root.title('Codemy.com - Card Deck')
root.iconbitmap(r'C:\Users\joann\OneDrive\Puck\kaarten')
root.geometry("900x500")
root.configure(background="green")


# Shuffle The Cards
def shuffle():
	# Define Our Deck
    colors = ["green", "purple", "red"]
    shapes = ["diamond", "oval", "squiggle"]
    shadings = ["filled", "shaded", "empty"]
    numbers = ["1", "2", "3"]

    global deck
    deck =[]
	
    for color in colors:
		for shape in shapes:
			for shading in shadings:
				for number in numbers:
					deck.append(f'{color}_{shape}_{shading}_{number}')
	print(deck)

	# Create our players
    global dealer, player
	dealer = []
	player = []

	# Grab a random Card For Dealer
	card = random.choice(deck)
	# Remove Card From Deck
	deck.remove(card)
	# Append Card To Dealer List
	dealer.append(card)
	# Output Card To Screen
	global dealer_image
	dealer_image = (f'C:\Users\joann\OneDrive\Puck\kaarten\{card}.png')
	dealer_label.config(image=dealer_image)

	# Grab a random Card For Player
	card = random.choice(deck)
	# Remove Card From Deck
	deck.remove(card)
	# Append Card To Dealer List
	player.append(card)
	# Output Card To Screen
	global player_image
	player_image = (f'C:\Users\joann\OneDrive\Puck\kaarten\{card}.png')
	player_label.config(image=player_image)

	#player_label.config(text=card)

	# Put number of remaining cards in title bar
	root.title(f'Codemy.com - {len(deck)} Cards Left')


# Deal Out Cards
def deal_cards():
	try:
		# Get the deler Card
		card = random.choice(deck)
		# Remove Card From Deck
		deck.remove(card)
		# Append Card To Dealer List
		dealer.append(card)
		# Output Card To Screen
		global dealer_image
		dealer_image = resize_cards(f'images/cards/{card}.png')
		dealer_label.config(image=dealer_image)
		#dealer_label.config(text=card)

		# Get the player Card
		card = random.choice(deck)
		# Remove Card From Deck
		deck.remove(card)
		# Append Card To Dealer List
		player.append(card)
		# Output Card To Screen
		global player_image
		player_image = (f'C:\Users\joann\OneDrive\Puck\kaarten\{card}.png')
		player_label.config(image=player_image)
		#player_label.config(text=card)


		# Put number of remaining cards in title bar
		root.title(f'Codemy.com - {len(deck)} Cards Left')

	except:
		root.title(f'Codemy.com - No Cards In Deck')




my_frame = Frame(root, bg="green")
my_frame.pack(pady=20)

# Create Frames For Cards
dealer_frame = LabelFrame(my_frame, text="Dealer", bd=0)
dealer_frame.grid(row=0, column=0, padx=20, ipadx=20)

player_frame = LabelFrame(my_frame, text="Player", bd=0)
player_frame.grid(row=0, column=1, ipadx=20)

# Put cards in frames
dealer_label = Label(dealer_frame, text='')
dealer_label.pack(pady=20)

player_label = Label(player_frame, text='')
player_label.pack(pady=20)


# Create a couple buttons
shuffle_button = Button(root, text="Shuffle Deck", font=("Helvetica", 14), command=shuffle)
shuffle_button.pack(pady=20)

card_button = Button(root, text="Get Cards", font=("Helvetica", 14), command=deal_cards)
card_button.pack(pady=20)



# Shuffle Deck On Start
shuffle()


root.mainloop()
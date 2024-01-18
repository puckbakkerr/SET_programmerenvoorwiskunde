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
    				deck.append(f'{color}{shape}{shading}{number}')
    print(deck)
	
shuffle()


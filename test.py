#hey Luka even kijken of dit werkt groetjess 
#hallo, het werk :)

#Color: red=0 green=1 purple=2
#shape: oval=0 diamond=1 squiggle=2
#shading: filled=0 shaded=1 empty=2
#number: 0=1 1=2 2=3

class SetCard:
    def __init__(self, shape, color, number, shading):
        self.shape = shape
        self.color = color
        self.number = number
        self.shading = shading

    def __eq__(self, other):
        return (
            self.shape == other.shape and
            self.color == other.color and
            self.number == other.number and
            self.shading == other.shading
        )

    def __repr__(self):
        return f"SetCard(color={self.color}, shape={self.shape}, shading={self.shading}, number={self.number})"
    


def is_set(card1, card2, card3):
        return (
            (card1.color + card2.color + card3.color)%3 ==0 and
            (card1.shape + card2.shape + card3.shape)%3 ==0 and
            (card1.shading + card2.shading + card3.shading)%3 ==0 and
            (card1.number + card2.number + card3.number)%3 ==0
        )

card1 = SetCard(color=0, shape=0, shading=0, number=0)
print(card1)
card2 = SetCard(color=0, shape=0, shading=0, number=0)
print(card1)
card3 = SetCard(color=0, shape=0, shading=0, number=0)
print(card1)

print(is_set(card1, card2, card3))
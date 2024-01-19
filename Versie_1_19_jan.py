import itertools
import random
from itertools import combinations
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from itertools import cycle
import os
import time



class SetCard:
    def __init__(self, color, shape, shading, number):
        self.color = color
        self.shape = shape
        self.shading = shading
        self.number = number
        self.image_name = f"{color}{shape}{shading}{number}"

    def get_image_path(self, folder="kaarten"):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, folder, f"{self.image_name}.gif")



# Example usage:
# Creating a SetCard object with color='red', shape='oval', shading='empty', number=2
red_oval_empty_2 = SetCard('red', 'oval', 'empty', 2)

# Accessing the image path for the card
image_path = red_oval_empty_2.get_image_path()
print(f"Image path for the card: {image_path}")



class SetDeck:
    def __init__(self):
        self.cards = self._generate_deck()
        self.shuffle_deck()

    def _generate_deck(self):
        colors = ['red', 'green', 'purple']
        shapes = ['oval', 'diamond', 'squiggle']
        fills = ['empty', 'shaded', 'filled']
        numbers = [1, 2, 3]

        all_cards = [SetCard(color, shape, fill, number)
                     for color, shape, fill, number in itertools.product(colors, shapes, fills, numbers)]

        return all_cards

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            print("The deck is empty.")
            return None



# Example usage:
set_deck = SetDeck()

# Shuffle the deck
set_deck.shuffle_deck()

# Deal and print the first 12 cards from the shuffled deck
for _ in range(12):
    card = set_deck.deal_card()
    if card:
        print(f"Card: {card.color} {card.shape} {card.shading} {card.number} - Image Path: {card.get_image_path()}")


class Table:
    def __init__(self, set_deck):
        self.set_deck = set_deck
        self.table_cards = []

    def fill_table(self):
        while len(self.table_cards) < 12:
            new_card = self.set_deck.deal_card()
            if new_card:
                self.table_cards.append(new_card)

    def display_table(self):
        for index, card in enumerate(self.table_cards, start=1):
            print(f"{index}. Card: {card.color} {card.shape} {card.shading} {card.number} - Image Path: {card.get_image_path()}")


    def select_cards(self, indices):
        selected_cards = []
        for index in indices:
            if 1 <= index <= len(self.table_cards):
                selected_cards.append(self.table_cards[index - 1])
            else:
                print(f"Invalid index: {index}. Index should be between 1 and {len(self.table_cards)}.")

        return selected_cards

    def is_set(self, selected_cards):
        for attr in ['color', 'shape', 'shading', 'number']:
            values = set(getattr(card, attr) for card in selected_cards)
            if len(values) == 2:
                return False  # If there are two different values for any attribute, it's not a set
        return True
    
    def find_all_sets(self):
        all_sets = []
        for card_combination in combinations(self.table_cards, 3):
            if self.is_set(card_combination):
                all_sets.append(list(card_combination))
        return all_sets

    def find_set(self):
        for card_combination in combinations(self.table_cards, 3):
            if self.is_set(card_combination):
                return list(card_combination)
        return None





# Example usage:
# Assuming you already have a SetDeck object named set_deck
table = Table(set_deck)

# Fill the table with 12 cards
table.fill_table()

# Display the initial table
print("Initial Table:")
table.display_table()


# Select three cards from the table (for example, indices 1, 3, and 5)
selected_indices = [1, 3, 5]
selected_cards = table.select_cards(selected_indices)

# Display the selected cards
print("\nSelected Cards:")
for card in selected_cards:
    print(f"Card: {card.color} {card.shape} {card.shading} {card.number} - Image Path: {card.get_image_path()}")


# Check if the selected cards form a set
if table.is_set(selected_cards):
    print("\nThe selected cards form a set!")
else:
    print("\nThe selected cards do not form a set.")


# Find all sets on the table
all_sets = table.find_all_sets()

# Display all sets found
print("\nAll Sets on the Table:")
for idx, card_set in enumerate(all_sets, start=1):
    print(f"Set {idx}:")
    for card in card_set:
        print(f"  Card: {card.color} {card.shape} {card.shading} {card.number} - Image Path: {card.get_image_path()}")


# Find one set on the table
found_set = table.find_set()

# Display the found set
if found_set:
    print("\nFound Set:")
    for card in found_set:
        print(f"  Card: {card.color} {card.shape} {card.shading} {card.number} - Image Path: {card.get_image_path()}")
else:
    print("\nNo set found on the table.")




class TableVisualization:
    def __init__(self, table):
        self.table = table
        self.set_deck = set_deck
        self.card_images = self.load_card_images()
        self.selected_cards = []
        self.timer_duration = 30
        self.start_time = time.time()
        self.player_score = 0
        self.computer_score = 0

    def load_card_images(self):
        card_images = {}
        for card in self.table.table_cards:
            image_path = card.get_image_path()
            card_images[card] = pygame.image.load(image_path)
        return card_images

    def display_table(self):
        pygame.init()

        card_width, card_height = self.card_images[self.table.table_cards[0]].get_size()

        window_width = card_width * 4
        window_height = card_height * 3

        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Table Visualization")

        clock = pygame.time.Clock()

        running = True
        while running and self.timer_duration > 0:
            elapsed_time = time.time() - self.start_time
            self.timer_duration = max(5 - int(elapsed_time), 0)

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    selected_card = self.get_card_at_position(x, y)
                    if selected_card:
                        if selected_card in self.selected_cards:
                            self.selected_cards.remove(selected_card)
                        else:
                            self.selected_cards.append(selected_card)

                        if len(self.selected_cards) == 3:
                            self.check_and_update_table()

            window.fill((255, 255, 255))

            x, y = 0, 0
            for card in cycle(self.table.table_cards):
                if card in self.card_images:
                    if card in self.selected_cards:
                        pygame.draw.rect(window, (0, 0, 255), (x, y, card_width, card_height), 5)
                    window.blit(self.card_images[card], (x, y))
                    x += card_width
                    if x >= window_width:
                        x = 0
                        y += card_height
                    if y >= window_height:
                        break

            font = pygame.font.Font(None, 36)
            timer_text = font.render(f"Time Left: {self.timer_duration} seconds", True, (0, 0, 0))
            window.blit(timer_text, (5, window_height - 40))
            
            score_text = font.render(f"Player: {self.player_score}   Computer: {self.computer_score}", True, (0, 0, 0))
            window.blit(score_text, (5, 5))

            pygame.display.flip()
            clock.tick(5)

            # Check if the timer has reached 0
            if self.timer_duration == 0:
                self.find_set_and_replace()

        pygame.quit()

    def get_card_at_position(self, x, y):
        card_width, card_height = self.card_images[self.table.table_cards[0]].get_size()

        column = x // card_width
        row = y // card_height

        index = column + row * 4

        if 0 <= index < len(self.table.table_cards):
            return self.table.table_cards[index]
        else:
            return None

    def check_and_display_set(self):
        if self.table.is_set(self.selected_cards):
            print("Selected Cards Form a Set!")
        else:
            print("Selected Cards Do Not Form a Set.")


    def check_and_update_table(self):
        if self.table.is_set(self.selected_cards):
            print("Selected Cards Form a Set!")

            # Get indices of selected cards
            indices = [self.table.table_cards.index(card) for card in self.selected_cards]

            # Remove selected cards from the table
            for card in self.selected_cards:
                self.table.table_cards.remove(card)

            # Draw three new cards from the deck and add them to the table at the same positions
            for _ in range(3):
                new_card = self.set_deck.deal_card()
                if new_card:
                    self.table.table_cards.insert(indices.pop(0), new_card)
                else:
                    # Handle the case where the deck is empty
                    print("The deck is empty. No more cards can be drawn.")
                    break

            # Clear selected cards list
            self.selected_cards = []

            # Reload card images
            self.card_images = self.load_card_images()

            # Reset the timer
            self.start_time = time.time()
            self.timer_duration = 5

            # Player gets a point for finding a set
            self.player_score += 1

        else:
            print("Selected Cards Do Not Form a Set.")


    def find_set_and_replace(self):
        print("Timer reached 0 seconds. Finding a set and replacing cards.")

        # Find a set on the table
        found_set = self.table.find_set()

        if found_set:
            # Get indices of cards from the found set
            indices = [self.table.table_cards.index(card) for card in found_set]

            # Remove cards from the found set
            for card in found_set:
                self.table.table_cards.remove(card)

            # Draw three new cards from the deck and add them to the table at the same positions
            for _ in range(3):
                new_card = self.set_deck.deal_card()
                if new_card:
                    self.table.table_cards.insert(indices.pop(0), new_card)
                else:
                    # Handle the case where the deck is empty
                    print("The deck is empty. No more cards can be drawn.")
                    break

            # Reload card images
            self.card_images = self.load_card_images()

            # Reset the timer
            self.start_time = time.time()
            self.timer_duration = 30

            # Computer gets a point for finding a set
            self.computer_score += 1

        else:
            print("No set found on the table.")

# Example usage:
# Assuming you already have a SetDeck object named set_deck
table = Table(set_deck)

# Fill the table with 12 cards
table.fill_table()

# Visualize the table
table_visualization = TableVisualization(table)
table_visualization.display_table()


# Display the selected cards
print("Selected Cards:")
for card in table_visualization.selected_cards:
    print(f"  Card: {card.color} {card.shape} {card.shading} {card.number} - Image Path: {card.get_image_path()}")

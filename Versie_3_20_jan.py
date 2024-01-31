# Importing necessary modules for the program.
# We used pygame to create our game, type "pip install pygame" into the terminal if pygame is not yet imported.
import itertools
import random
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import os
import time
import sys

# Represents a card in the game. 
class SetCard:

    # The card gets the attributes color, shape, shading and number.
    def __init__(self, color, shape, shading, number):
        self.color = color
        self.shape = shape
        self.shading = shading
        self.number = number
        # Creates a name for the image of the card. 
        self.image_name = f"{color}{shape}{shading}{number}"
    
    # Returns the file path to the image of a particular card.
    def get_image_path(self, folder="kaarten"):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, folder, f"{self.image_name}.gif")

# Represents the deck of cards used in the game. 
class SetDeck:
    # The deck is created by generating a deck and shuffling it.
    def __init__(self):
        self.cards = self.generate_deck()
        self.shuffle_deck()

    # A deck is created. 
    def generate_deck(self):
        # A list is made with all the possible attributes of a card.
        colors = ['red', 'green', 'purple']
        shapes = ['oval', 'diamond', 'squiggle']
        fills = ['empty', 'shaded', 'filled']
        numbers = [1, 2, 3]

        # A deck of 81 unique cards is created by using intertools to create all the possible combinations of attributes.
        return [SetCard(color, shape, fill, number)
                for color, shape, fill, number in itertools.product(colors, shapes, fills, numbers)]

    # The deck is shuffled. 
    def shuffle_deck(self):
        random.shuffle(self.cards)

    # Deals a card from the deck.
    def deal_card(self):
        # If the deck is empty, a new deck is created and shuffled.
        if not self.cards:
            print("The deck is empty. Creating a new deck and shuffling.")
            self.cards = self.generate_deck()
            self.shuffle_deck()
        # A card is returned by popping the last card in the deck. 
        return self.cards.pop()

# Represents the table with twelve cards.
class Table:
    # A table is created with a reference to a deck and an empty list.
    def __init__(self, set_deck):
        self.set_deck = set_deck
        self.table_cards = []

    # The table is filled with twelve cards.
    def fill_table(self):
        while len(self.table_cards) < 12:
            new_card = self.set_deck.deal_card()
            if new_card:
                self.table_cards.append(new_card)

    # Returns information about the card.
    def card_info(self, card):
        return f"Card: {card.color} {card.shape} {card.shading} {card.number} - Image Path: {card.get_image_path()}"

    # The corresponding cards are selected, given a list of indices.
    def select_cards(self, indices):
        return [self.table_cards[index - 1] for index in indices if 1 <= index <= len(self.table_cards)]

    # Checks if the seclected cards are a set.
    def is_set(self, selected_cards):
        color_mapping = {'red': 0, 'green': 1, 'purple': 2}
        shape_mapping = {'oval': 0, 'diamond': 1, 'squiggle': 2}
        shading_mapping = {'empty': 0, 'shaded': 1, 'filled': 2}

        def convert_to_vector(card):
            return [color_mapping[card.color], shape_mapping[card.shape], shading_mapping[card.shading], card.number]

        # Checks if three cards are selected.
        if len(selected_cards) != 3:
            return False 

        vector1, vector2, vector3 = map(convert_to_vector, selected_cards)

        # Check if the sum of values is 0 (mod 3)
        for i in range(len(vector1)):
            total_sum = vector1[i] + vector2[i] + vector3[i]
            if total_sum % 3 != 0:
                return False
        return True

    # Finds a set on the table.
    def find_set(self):
        return next((list(card_combination) for card_combination in itertools.combinations(self.table_cards, 3)
                     if self.is_set(card_combination)), None)

# Represents the visual aspects of the game and the game mechanics.
class TableVisualization:

    # Initializes the TableVisualization instance.
    def __init__(self, table):
        self.table = table
        self.set_deck = table.set_deck
        self.card_images = self.load_card_images()
        self.selected_cards = []
        self.timer_duration = 5
        self.start_time = time.time()
        self.player_score = 0
        self.computer_score = 0
        self.game_started = False

    # Loads the corresponding images for the cards on the table.
    def load_card_images(self):
        return {card: pygame.image.load(card.get_image_path()) for card in self.table.table_cards}

    # Displays a start screen.
    def display_start_screen(self):
        pygame.init()

        window_width = 400
        window_height = 600

        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Start Screen")

        # Adds the text "Choose your time limit:" to the start screen.
        font = pygame.font.Font(None, 36)
        start_text = font.render("Choose your time limit:", True, (0, 0, 0))

        start_text_rect = start_text.get_rect(center=(window_width // 2, window_height // 4))

        # Makes buttons for the differen time limits. 
        button_width = 100
        button_height = 40

        # Centers the buttons horizontally
        button1_rect = pygame.Rect((window_width - button_width * 3) // 2, window_height // 2, button_width, button_height)
        button2_rect = pygame.Rect(button1_rect.right, window_height // 2, button_width, button_height)
        button3_rect = pygame.Rect(button2_rect.right, window_height // 2, button_width, button_height)

        button1_text = font.render("15 sec", True, (0, 0, 0))
        button1_text_rect = button1_text.get_rect(center=button1_rect.center)

        button2_text = font.render("30 sec", True, (0, 0, 0))
        button2_text_rect = button2_text.get_rect(center=button2_rect.center)

        button3_text = font.render("60 sec", True, (0, 0, 0))
        button3_text_rect = button3_text.get_rect(center=button3_rect.center)

        while True:
        # Depending on which button was pushed, the player gets a 15, 30 or 60 second time limit.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button1_rect.collidepoint(event.pos):
                        self.game_started = True
                        selected_timer_duration = 15
                        self.display_table(selected_timer_duration)
                    elif button2_rect.collidepoint(event.pos):
                        self.game_started = True
                        selected_timer_duration = 30
                        self.display_table(selected_timer_duration)
                    elif button3_rect.collidepoint(event.pos):
                        self.game_started = True
                        selected_timer_duration = 60
                        self.display_table(selected_timer_duration)

            window.fill((255, 255, 255))
            window.blit(start_text, start_text_rect)

            pygame.draw.rect(window, (0, 0, 0), button1_rect, 2)
            window.blit(button1_text, button1_text_rect.topleft)

            pygame.draw.rect(window, (0, 0, 0), button2_rect, 2)
            window.blit(button2_text, button2_text_rect.topleft)

            pygame.draw.rect(window, (0, 0, 0), button3_rect, 2)
            window.blit(button3_text, button3_text_rect.topleft)

            pygame.display.flip()

    # Displays the table.
    def display_table(self, timer_duration):
        pygame.init()

        # Makes a window for the table.
        card_width, card_height = self.card_images[self.table.table_cards[0]].get_size()

        window_width = card_width * 4
        window_height = card_height * 3

        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Table Visualization")

        clock = pygame.time.Clock()

        # Sets and resets the timer.
        self.start_time = time.time() 
        self.timer_duration = timer_duration  

        running = True
        while running:
            # Handles the game loop. 
            elapsed_time = time.time() - self.start_time
            self.timer_duration = max(timer_duration - int(elapsed_time), 0)

            # Handles the events on the table. 
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                # Handles the player clicking a card. 
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
            for card in itertools.cycle(self.table.table_cards):
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

            # Displays the timer and the scores. 
            self.display_info(window, window_height)

            pygame.display.flip()
            clock.tick(5)

            if self.timer_duration == 0:
                self.find_set_and_replace()

                # Clear selected cards when the time limit is up
                self.selected_cards = []

        pygame.quit()

    def get_card_at_position(self, x, y):
    #positioning the cards
        card_width, card_height = self.card_images[self.table.table_cards[0]].get_size()

        column = x // card_width
        row = y // card_height

        index = column + row * 4

        return self.table.table_cards[index] if 0 <= index < len(self.table.table_cards) else None

    def display_info(self, window, window_height):
    #posisioning the display information
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time Left: {self.timer_duration} seconds", True, (0, 0, 0))
        window.blit(timer_text, (5, window_height - 40))

        score_text = font.render(f"Player: {self.player_score}   Computer: {self.computer_score}", True, (0, 0, 0))
        window.blit(score_text, (5, 5))

    def check_and_display_set(self):
    #This is only shown in the terminal and not on the screen
        print("Selected Cards Form a Set!") if self.table.is_set(self.selected_cards) else print("Selected Cards Do Not Form a Set.")

    def display_winner_screen(self, winner):
    #Displaying the winner screen with a button to restart the game.
        pygame.init()

        window_width = 400
        window_height = 200

        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Winner Screen")

        font = pygame.font.Font(None, 36)
        text = font.render(f"{winner} wins!", True, (0, 0, 0))

        button_rect = pygame.Rect(150, 150, 100, 40)
        button_text = font.render("Restart!", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button_rect.center)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        pygame.quit()
                        self.restart_game()

            window.fill((255, 255, 255))
            window.blit(text, (window_width // 2 - text.get_width() // 2, window_height // 2 - text.get_height() // 2))

            pygame.draw.rect(window, (0, 0, 0), button_rect, 2)
            window.blit(button_text, button_text_rect.topleft)

            pygame.display.flip()

    def restart_game(self):
        # Reset the game state here
        set_deck = SetDeck()
        self.table = Table(set_deck)
        self.table.fill_table()

        # Update any other necessary variables or state
        self.selected_cards = []
        self.card_images = self.load_card_images()
        self.start_time = time.time()
        self.timer_duration = 5
        self.player_score = 0
        self.computer_score = 0

        # Display the new game
        table_visualization = TableVisualization(table)
        table_visualization.display_start_screen()

    def check_and_update_table(self):
    #triggered by Players action and check sets on the table 
    #and update accordingly (replacing the cards on the table)
        if self.table.is_set(self.selected_cards):
            indices = [self.table.table_cards.index(card) for card in self.selected_cards]

            for card in self.selected_cards:
                self.table.table_cards.remove(card)

            for _ in range(3):
                new_card = self.set_deck.deal_card()
                if new_card:
                    self.table.table_cards.insert(indices.pop(0), new_card)
                else:
                    print("The deck is empty. No more cards can be drawn.")
                    break

            self.selected_cards = []
            self.card_images = self.load_card_images()
            self.start_time = time.time()
            self.timer_duration = 5
            self.player_score += 1

            if self.player_score == 5:
                self.display_winner_screen("Player")

        else:
            print("Selected Cards Do Not Form a Set.")

    def find_set_and_replace(self):
    #triggered by Timer running out (cumputers turn) 
    #check sets on the table 
    #and update accordingly (replacing the cards on the table)
    #it also removes the first three cards from the table and replace them
        found_set = self.table.find_set()

        if found_set:
            indices = [self.table.table_cards.index(card) for card in found_set]

            for card in found_set:
                self.table.table_cards.remove(card)

            for _ in range(3):
                new_card = self.set_deck.deal_card()
                if new_card:
                    self.table.table_cards.insert(indices.pop(0), new_card)
                else:
                    print("The deck is empty. No more cards can be drawn.")
                    break

            self.card_images = self.load_card_images()
            self.start_time = time.time()
            self.timer_duration = 30
            self.computer_score += 1

            if self.computer_score == 5:
                
                self.display_winner_screen("Computer")

        else:
            print("No set found on the table. Removing the first three cards and drawing new ones.")

            for _ in range(3):
                if self.table.table_cards:
                    self.table.table_cards.pop(0)
                    new_card = self.set_deck.deal_card()
                    if new_card:
                        self.table.table_cards.append(new_card)
                    else:
                        print("The deck is empty. No more cards can be drawn.")
                        break

            self.card_images = self.load_card_images()
            self.start_time = time.time()
            self.timer_duration = 30




set_deck = SetDeck()
table = Table(set_deck)
table.fill_table()

table_visualization = TableVisualization(table)
table_visualization.display_start_screen()

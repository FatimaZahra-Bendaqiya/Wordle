import pygame
import sys
import random
from words import *
from technology import *
from geography import *
from football import *

pygame.init()

SCREEN = pygame.display.set_mode((1050, 525))
pygame.display.set_caption("Menu")

BG = pygame.image.load("Background.png")

# Constants
WIDTH, HEIGHT = 423, 578
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"

CORRECT_WORD = "guess"
ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

GUESSED_LETTER_FONT = pygame.font.Font("FreeSansBold.otf", 20)
AVAILABLE_LETTER_FONT = pygame.font.Font("FreeSansBold.otf", 15)

LETTER_X_SPACING = 85
LETTER_Y_SPACING = 0
LETTER_SIZE = 75

# Global variables

guesses_count = 0
"""
Guesses is a 2D list that will store guesses.
A guess will be a list of letters.
The list will be iterated through.
each letter in each guess will be drawn on the screen.
"""
guesses = [[]] * 6

current_guess = []
current_guess_string = ""
current_letter_bg_x = 2
game_result = ""


class Button():
    """
    object constructor for the buttons that are used like back and quit etc.
    """
    def __init__(self, image, pos, text_input,
                 font, base_color, hovering_color):
        """
        Initializes all the variables
        including text, color, position.
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        updating the screen whenever the mouse is on the word
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """
        checking wheter the word is clicked on it
        """
        if position[0] in range(
             self.rect.left, self.rect.right) and position[1] in range(
                                        self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """
        changing the color of the word if the mouse is above it
        """
        if position[0] in range(
          self.rect.left, self.rect.right) and position[1] in range(
                                       self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                             self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size):
    """
    Returns Press-Start-2P in the desired size
    """
    return pygame.font.Font("font.ttf", size)


def check_guess(guess_to_check):
    """
    Goes through each letter
    checks if it should be green, yellow, or grey.
    """
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    game_decided = False
    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = GREEN
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = YELLOW
                guess_to_check[i].text_color = "white"
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            guess_to_check[i].text_color = "white"
            game_result = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()

    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 2

    if guesses_count == 6 and game_result == "":
        game_result = "L"


def play():
    """
    Starting the game with the general dictionary
    """
    pygame.init()

    SCREEN2 = pygame.display.set_mode((WIDTH, HEIGHT))
    BACKGROUND2 = pygame.image.load("Starting Tiles.png")
    BACKGROUND2_RECT = BACKGROUND2.get_rect(center=(211, 289))
    ICON = pygame.image.load("Icon.png")

    pygame.display.set_caption("Wordle!")
    pygame.display.set_icon(ICON)

    SCREEN2.fill("white")
    SCREEN2.blit(BACKGROUND2, BACKGROUND2_RECT)
    pygame.display.update()

    class Letter:
        """
        creating object letter to be used
        whenever a new letter is needed to be created
        """
        def __init__(self, text, bg_position):
            """
            Initializes all the variables
            including text, color, position, size, etc.
            """
            self.bg_color = "white"
            self.text_color = "black"
            self.bg_position = bg_position
            self.bg_x = bg_position[0]
            self.bg_y = bg_position[1]
            self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
            self.text = text
            self.text_position = (self.bg_x+36, self.bg_position[1]+34)
            self.text_surface = GUESSED_LETTER_FONT.render(self.text,
                                                           True,
                                                           self.text_color)
            self.text_rect = self.text_surface.get_rect(
                                              center=self.text_position)

        def draw(self):
            """
            Puts the letter and text on the screen at the desired positions.
            """
            pygame.draw.rect(SCREEN2, self.bg_color, self.bg_rect)
            if self.bg_color == "white":
                pygame.draw.rect(SCREEN2, FILLED_OUTLINE, self.bg_rect, 3)
            self.text_surface = GUESSED_LETTER_FONT.render(self.text,
                                                           True,
                                                           self.text_color)
            SCREEN2.blit(self.text_surface, self.text_rect)
            pygame.display.update()

        def delete(self):
            """
            Fills the letter's spot with the default square, emptying it.
            """
            pygame.draw.rect(SCREEN2, "white", self.bg_rect)
            pygame.draw.rect(SCREEN2, OUTLINE, self.bg_rect, 3)
            pygame.display.update()

    def play_again():
        """
        Puts the play again,
        whether you guessed right or wrong
        and quit text on the screen.
        """
        SCREEN2.fill("white")
        QUIT_MOUSE_POS = pygame.mouse.get_pos()
        word_was_font = pygame.font.Font("FreeSansBold.otf", 20)
        QUIT_BUTTON = Button(image=None, pos=(WIDTH/2, 450),
                             text_input="QUIT", font=get_font(65),
                             base_color="Black", hovering_color="Green")
        PLAY_AGAIN_BUTTON = Button(image=None, pos=(WIDTH/2, 350),
                                   text_input="PLAY AGAIN", font=get_font(35),
                                   base_color="Black", hovering_color="Green")
        word_was_text = word_was_font.render(f"The word was {CORRECT_WORD}!",
                                             True, "black")
        word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 200))
        game_result_font = pygame.font.Font("FreeSansBold.otf", 20)
        if game_result == 'W':
            game_result_text = game_result_font.render("YOU GUESSED IT RIGHT!",
                                                       True, "black")
            game_result_rect = game_result_text.get_rect(center=(WIDTH/2, 150))
        if game_result == 'L':
            game_result_text = game_result_font.render("NICE TRY!",
                                                       True, "black")
            game_result_rect = game_result_text.get_rect(center=(WIDTH/2, 150))

        SCREEN2.blit(game_result_text, game_result_rect)
        SCREEN2.blit(word_was_text, word_was_rect)
        PLAY_AGAIN_BUTTON.changeColor(QUIT_MOUSE_POS)
        PLAY_AGAIN_BUTTON.update(SCREEN)
        QUIT_BUTTON.changeColor(QUIT_MOUSE_POS)
        QUIT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_AGAIN_BUTTON.checkForInput(QUIT_MOUSE_POS):
                    reset()
                if QUIT_BUTTON.checkForInput(QUIT_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    def reset():
        """
        Resets all global variables to their default states.
        Along with with a new random word
        """
        global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
        SCREEN2.fill("white")
        SCREEN2.blit(BACKGROUND2, BACKGROUND2_RECT)
        guesses_count = 0
        CORRECT_WORD = random.choice(WORDS)
        guesses = [[]] * 6
        current_guess = []
        current_guess_string = ""
        game_result = ""
        pygame.display.update()

    def create_new_letter():
        """
        Creates a new letter and adds it to the guess.
        """
        global current_guess_string, current_letter_bg_x
        current_guess_string += key_pressed
        new_letter = Letter(key_pressed, (current_letter_bg_x,
                                          guesses_count*100+LETTER_Y_SPACING))
        current_letter_bg_x += LETTER_X_SPACING
        guesses[guesses_count].append(new_letter)
        current_guess.append(new_letter)
        for guess in guesses:
            for letter in guess:
                letter.draw()

    def delete_letter():
        """
        Deletes the last letter from the guess.
        """
        global current_guess_string, current_letter_bg_x
        guesses[guesses_count][-1].delete()
        guesses[guesses_count].pop()
        current_guess_string = current_guess_string[:-1]
        current_guess.pop()
        current_letter_bg_x -= LETTER_X_SPACING

    while True:
        if game_result != "":
            play_again()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if (len(current_guess_string) == 5 and
                            current_guess_string.lower() in WORDS):
                        check_guess(current_guess)
                elif event.key == pygame.K_BACKSPACE:
                    if len(current_guess_string) > 0:
                        delete_letter()
                else:
                    key_pressed = event.unicode.upper()
                    if (key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and
                            key_pressed != ""):
                        if len(current_guess_string) < 5:
                            create_new_letter()


def rules():
    """
    Displaying rules of the game.
    Click BACK to get back to main menu.
    """
    while True:
        RULES_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("#b68f40")

        RULES_TEXT1 = get_font(20).render("1.You have to guess the Wordle" +
                                          " in six goes.",
                                          True, "white")
        RULES_TEXT2 = get_font(20).render("2.A correct letter turns green.",
                                          True, "white")
        RULES_TEXT3 = get_font(20).render("3.A correct letter in the wrong" +
                                          " place turns yellow.", True, "white")
        RULES_TEXT4 = get_font(20).render("4.An incorrect letter turns gray.",
                                          True, "white")
        RULES_TEXT5 = get_font(20).render("5.Letters can be used more" +
                                          " than once.", True, "white")

        RULES_RECT1 = RULES_TEXT1.get_rect(center=(525, 126))
        RULES_RECT2 = RULES_TEXT2.get_rect(center=(525, 176))
        RULES_RECT3 = RULES_TEXT3.get_rect(center=(525, 226))
        RULES_RECT4 = RULES_TEXT4.get_rect(center=(525, 276))
        RULES_RECT5 = RULES_TEXT5.get_rect(center=(525, 326))

        SCREEN.blit(RULES_TEXT1, RULES_RECT1)
        SCREEN.blit(RULES_TEXT2, RULES_RECT2)
        SCREEN.blit(RULES_TEXT3, RULES_RECT3)
        SCREEN.blit(RULES_TEXT4, RULES_RECT4)
        SCREEN.blit(RULES_TEXT5, RULES_RECT5)

        RULES_BACK = Button(image=None, pos=(525, 400),
                            text_input="BACK", font=get_font(65),
                            base_color="Black", hovering_color="Green")

        RULES_BACK.changeColor(RULES_MOUSE_POS)
        RULES_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RULES_BACK.checkForInput(RULES_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def options():
    """
    Displaying dictionary options of the game.
    Click BACK to get back to main menu.
    """
    def technology():
        """
        Playing the game only with words about technology
        """
        play().Letter().__init__()
        play().Letter().draw()
        play().Letter().delete()
        play().create_new_letter()
        play().delete_letter()

        def play_again2():
            # Puts the play again text on the screen.
            SCREEN2.fill("white")
            QUIT_MOUSE_POS = pygame.mouse.get_pos()
            word_was_font = pygame.font.Font("FreeSansBold.otf", 20)
            QUIT_BUTTON = Button(image=None, pos=(WIDTH/2, 450),
                                 text_input="QUIT", font=get_font(65),
                                 base_color="Black", hovering_color="Green")
            PLAY_AGAIN_BUTTON = Button(image=None, pos=(WIDTH/2, 350),
                                       text_input="PLAY AGAIN",
                                       font=get_font(35),
                                       base_color="Black",
                                       hovering_color="Green")
            word_was_text = word_was_font.render(f"The word was " +
                                                 "{CORRECT_WORD}!",
                                                 True, "black")
            word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 200))
            game_result_font = pygame.font.Font("FreeSansBold.otf", 20)
            if game_result == 'W':
                game_result_text = game_result_font.render("YOU GUESSED " +
                                                           "IT RIGHT!",
                                                           True, "black")
                game_result_rect = game_result_text.get_rect(
                                                  center=(WIDTH/2, 150))
            if game_result == 'L':
                game_result_text = game_result_font.render("NICE TRY!",
                                                           True, "black")
                game_result_rect = game_result_text.get_rect(
                                                  center=(WIDTH/2, 150))

            SCREEN2.blit(game_result_text, game_result_rect)
            SCREEN2.blit(word_was_text, word_was_rect)
            PLAY_AGAIN_BUTTON.changeColor(QUIT_MOUSE_POS)
            PLAY_AGAIN_BUTTON.update(SCREEN)
            QUIT_BUTTON.changeColor(QUIT_MOUSE_POS)
            QUIT_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_AGAIN_BUTTON.checkForInput(QUIT_MOUSE_POS):
                        reset2()
                    if QUIT_BUTTON.checkForInput(QUIT_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

        def reset2():
            # Resets all global variables to their default states.
            global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
            SCREEN2.fill("white")
            SCREEN2.blit(BACKGROUND2, BACKGROUND2_RECT)
            guesses_count = 0
            CORRECT_WORD = random.choice(TECHNOLOGY)
            guesses = [[]] * 6
            current_guess = []
            current_guess_string = ""
            game_result = ""
            pygame.display.update()
        while True:
            if game_result != "":
                play_again2()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if (len(current_guess_string) == 5 and
                                current_guess_string.lower() in TECHNOLOGY):
                            check_guess(current_guess)
                    elif event.key == pygame.K_BACKSPACE:
                        if len(current_guess_string) > 0:
                            delete_letter()
                    else:
                        key_pressed = event.unicode.upper()
                        if (key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and
                                key_pressed != ""):
                            if len(current_guess_string) < 5:
                                create_new_letter()
            pygame.display.update()

    def geography():
        """
        Playing the game with cities and countries names
        """
        play().Letter().__init__()
        play().Letter().draw()
        play().Letter().delete()
        play().create_new_letter()
        play().delete_letter()

        def play_again3():
            # Puts the play again text on the screen.
            SCREEN2.fill("white")
            QUIT_MOUSE_POS = pygame.mouse.get_pos()
            word_was_font = pygame.font.Font("FreeSansBold.otf", 20)
            QUIT_BUTTON = Button(image=None, pos=(WIDTH/2, 450),
                                 text_input="QUIT", font=get_font(65),
                                 base_color="Black", hovering_color="Green")
            PLAY_AGAIN_BUTTON = Button(image=None, pos=(WIDTH/2, 350),
                                       text_input="PLAY AGAIN",
                                       font=get_font(35),
                                       base_color="Black",
                                       hovering_color="Green")
            word_was_text = word_was_font.render(f"The word was" +
                                                 " {CORRECT_WORD}!",
                                                 True, "black")
            word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 200))
            game_result_font = pygame.font.Font("FreeSansBold.otf", 20)
            if game_result == 'W':
                game_result_text = game_result_font.render("YOU GUESSED" +
                                                           " IT RIGHT!",
                                                           True, "black")
                game_result_rect = game_result_text.get_rect(
                                                  center=(WIDTH/2, 150))
            if game_result == 'L':
                game_result_text = game_result_font.render("NICE TRY!",
                                                           True, "black")
                game_result_rect = game_result_text.get_rect(
                                                  center=(WIDTH/2, 150))

            SCREEN2.blit(game_result_text, game_result_rect)
            SCREEN2.blit(word_was_text, word_was_rect)
            PLAY_AGAIN_BUTTON.changeColor(QUIT_MOUSE_POS)
            PLAY_AGAIN_BUTTON.update(SCREEN)
            QUIT_BUTTON.changeColor(QUIT_MOUSE_POS)
            QUIT_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_AGAIN_BUTTON.checkForInput(QUIT_MOUSE_POS):
                        reset3()
                    if QUIT_BUTTON.checkForInput(QUIT_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

        def reset3():
            # Resets all global variables to their default states.
            global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
            SCREEN2.fill("white")
            SCREEN2.blit(BACKGROUND2, BACKGROUND2_RECT)
            guesses_count = 0
            CORRECT_WORD = random.choice(GEOGRAPHY)
            guesses = [[]] * 6
            current_guess = []
            current_guess_string = ""
            game_result = ""
            pygame.display.update()
        while True:
            if game_result != "":
                play_again3()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if (len(current_guess_string) == 5 and
                                current_guess_string.lower() in GEOGRAPHY):
                            check_guess(current_guess)
                    elif event.key == pygame.K_BACKSPACE:
                        if len(current_guess_string) > 0:
                            delete_letter()
                    else:
                        key_pressed = event.unicode.upper()
                        if (key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and
                                key_pressed != ""):
                            if len(current_guess_string) < 5:
                                create_new_letter()
            pygame.display.update()

    def football():
        """
        Playing the game only with words about football
        """
        play().Letter().__init__()
        play().Letter().draw()
        play().Letter().delete()
        play().create_new_letter()
        play().delete_letter()

        def play_again4():
            # Puts the play again text on the screen.
            SCREEN2.fill("white")
            QUIT_MOUSE_POS = pygame.mouse.get_pos()
            word_was_font = pygame.font.Font("FreeSansBold.otf", 20)
            QUIT_BUTTON = Button(image=None, pos=(WIDTH/2, 450),
                                 text_input="QUIT", font=get_font(65),
                                 base_color="Black", hovering_color="Green")
            PLAY_AGAIN_BUTTON = Button(image=None, pos=(WIDTH/2, 350),
                                       text_input="PLAY AGAIN",
                                       font=get_font(35),
                                       base_color="Black",
                                       hovering_color="Green")
            word_was_text = word_was_font.render(f"The word was" +
                                                 " {CORRECT_WORD}!",
                                                 True, "black")
            word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 200))
            game_result_font = pygame.font.Font("FreeSansBold.otf", 20)
            if game_result == 'W':
                game_result_text = game_result_font.render("YOU GUESSED" +
                                                           " IT RIGHT!",
                                                           True, "black")
                game_result_rect = game_result_text.get_rect(
                                                  center=(WIDTH/2, 150))
            if game_result == 'L':
                game_result_text = game_result_font.render("NICE TRY!",
                                                           True, "black")
                game_result_rect = game_result_text.get_rect(
                                                  center=(WIDTH/2, 150))

            SCREEN2.blit(game_result_text, game_result_rect)
            SCREEN2.blit(word_was_text, word_was_rect)
            PLAY_AGAIN_BUTTON.changeColor(QUIT_MOUSE_POS)
            PLAY_AGAIN_BUTTON.update(SCREEN)
            QUIT_BUTTON.changeColor(QUIT_MOUSE_POS)
            QUIT_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_AGAIN_BUTTON.checkForInput(QUIT_MOUSE_POS):
                        reset4()
                    if QUIT_BUTTON.checkForInput(QUIT_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

        def reset4():
            # Resets all global variables to their default states.
            global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
            SCREEN2.fill("white")
            SCREEN2.blit(BACKGROUND2, BACKGROUND2_RECT)
            guesses_count = 0
            CORRECT_WORD = random.choice(FOOTBALL)
            guesses = [[]] * 6
            current_guess = []
            current_guess_string = ""
            game_result = ""
            pygame.display.update()
        while True:
            if game_result != "":
                play_again4()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if (len(current_guess_string) == 5 and
                                current_guess_string.lower() in FOOTBALL):
                            check_guess(current_guess)
                    elif event.key == pygame.K_BACKSPACE:
                        if len(current_guess_string) > 0:
                            delete_letter()
                    else:
                        key_pressed = event.unicode.upper()
                        if (key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and
                                key_pressed != ""):
                            if len(current_guess_string) < 5:
                                create_new_letter()
            pygame.display.update()

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("#b68f40")

        TECHNOLOGY_BUTTON = Button(image=None, pos=(525, 100),
                                   text_input="TECHNOLOGY", font=get_font(55),
                                   base_color="Black", hovering_color="Green")
        GEOGRAPHY_BUTTON = Button(image=None, pos=(525, 210),
                                  text_input="GEOGRAPHY", font=get_font(55),
                                  base_color="Black", hovering_color="Green")
        FOOTBALL_BUTTON = Button(image=None, pos=(525, 310),
                                 text_input="FOOTBALL", font=get_font(55),
                                 base_color="Black", hovering_color="Green")
        GOBACK_BUTTON = Button(image=None, pos=(525, 450),
                               text_input="BACK", font=get_font(45),
                               base_color="Black", hovering_color="Green")

        TECHNOLOGY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        TECHNOLOGY_BUTTON.update(SCREEN)
        GEOGRAPHY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        GEOGRAPHY_BUTTON.update(SCREEN)
        FOOTBALL_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        FOOTBALL_BUTTON.update(SCREEN)
        GOBACK_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        GOBACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TECHNOLOGY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    technology()
                if GEOGRAPHY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    geography()
                if FOOTBALL_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    football()
                if GOBACK_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    """
    Main menu where a player can choose whether he wants to
    start a new game, get to know rules of the game
    or choose one of the options.
    """
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(540, 80))

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"),
                             pos=(540, 170),
                             text_input="PLAY", font=get_font(50),
                             base_color="#d7fcd4", hovering_color="White")
        RULES_BUTTON = Button(image=pygame.image.load("Rules Rect.png"),
                              pos=(540, 300), text_input="RULES",
                              font=get_font(50),
                              base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Options Rect.png"),
                                pos=(540, 450), text_input="OPTIONS",
                                font=get_font(50),
                                base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, RULES_BUTTON, OPTIONS_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if RULES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rules()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()

        pygame.display.update()


main_menu()

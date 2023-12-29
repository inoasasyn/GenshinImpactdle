import setup
import finder
import random
from datetime import datetime
import pygame
import os

MAP_WIDTH = 1500
MAP_HEIGHT = 800
STANDARD_IMG_SIZE = 150
THICKNESS = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (212, 17, 17)
GREEN = (17, 120, 20)
BLUE = (9, 72, 173)

max_guesses = 5
number_of_additional_properties = 3


class Application:

    def game_in_console(self):
        while True:
            guessed_characters = []
            print("Guess character!")
            guess_counter = 0
            random_number = random.randint(0, len(characters)-1)
            character_to_guess = characters[random_number]
            properties = list(vars(character_to_guess).keys())
            displayed_properties = properties[0:3]
            while len(displayed_properties) < 3+number_of_additional_properties:
                add_properties = random.choices(properties[3:-1], k=number_of_additional_properties)
                if (properties[-1] or properties[-2] not in add_properties) and len(set(add_properties)) == number_of_additional_properties:
                    displayed_properties += add_properties

            while guess_counter < max_guesses:
                guess = input()
                guess_counter += 1
                guessed_character = finder.find_by_name(characters, guess)
                guessed_characters.append(guessed_character)
                for x in displayed_properties:
                    if x == "release_date" or x == "version":
                        correct_date = getattr(character_to_guess, x)
                        guessed_date = getattr(guessed_character, x)
                        if x == "release_date":
                            correct_date = datetime.strptime(correct_date, "%B %d, %Y")
                            guessed_date = datetime.strptime(guessed_date, "%B %d, %Y")
                        correct = correct_date == guessed_date
                        if correct:
                            print(str(x) + ": " + str(getattr(guessed_character, x)) + " is ", str(correct))
                        elif correct_date > guessed_date:
                            print(str(x) + ": " + str(getattr(guessed_character, x)) + " is OLDER")
                        else:
                            print(str(x) + ": " + str(getattr(guessed_character, x)) + " is NEWER")
                    else:
                        correct = getattr(character_to_guess, x) == getattr(guessed_character, x)
                        print(str(x) + ": " + str(getattr(guessed_character, x)) + " is ", str(correct))
                if guessed_character == character_to_guess:
                    print("You WIN!!!")
                    guess_counter = max_guesses + 1

    def draw_table(self, table, displayed_properties, img, screen, character_to_guess, top_left_corner):
        #top_left_corner = (30, img.get_rect().bottom + 50)
        size = (
            (number_of_additional_properties + 3) * 220 + 100 + (
                    THICKNESS * (number_of_additional_properties + 5)),
            (len(table) - 1) * 100 + 50 + (THICKNESS * (len(table) + 1)))
        pygame.draw.rect(screen, WHITE,
                         pygame.Rect((top_left_corner[0] - THICKNESS, top_left_corner[1] - THICKNESS),
                                     size))
        for i in range(len(table)):
            if i == 0:
                t_length = 50
                color = BLUE
            else:
                t_length = 100
                color = BLACK
            for j in range(0, number_of_additional_properties + 4):
                if i == 0 and j == 0:
                    t_width = 100
                    text = "Icon"
                elif j == 0:
                    t_width = 100
                    text = table[i].__getattribute__("name")
                    if table[i] == character_to_guess:
                        color = GREEN
                    else:
                        color = RED
                elif j in [2, 3]:
                    t_width = 100
                    if i == 0:
                        text = table[i][j - 1]
                    else:
                        text = table[i].__getattribute__(displayed_properties[j - 1])
                        if text == character_to_guess.__getattribute__(displayed_properties[j - 1]):
                            color = GREEN
                        else:
                            color = RED
                elif i == 0:
                    t_width = 280
                    text = table[i][j - 1]
                else:
                    t_width = 280
                    text = table[i].__getattribute__(displayed_properties[j - 1])
                    if text == character_to_guess.__getattribute__(displayed_properties[j - 1]):
                        color = GREEN
                    else:
                        color = RED
                        if displayed_properties[j - 1] == "version":
                            if text > character_to_guess.__getattribute__(displayed_properties[j - 1]):
                                text += "  V"
                            else:
                                text += "  ^"
                rect = pygame.Rect(top_left_corner, (t_width, t_length))
                pygame.draw.rect(screen, color, rect)
                if j == 0 and i != 0:
                    path = os.getcwd() + "\\Icons\\" + str(text).replace(" ", "_") + "_Icon.png"
                    t_img = pygame.image.load(path)
                    t_img = pygame.transform.scale(t_img, (t_width, t_width))
                    t_imgRect = t_img.get_rect()
                    t_imgRect.center = rect.center
                    screen.blit(t_img, t_imgRect)
                else:
                    font = pygame.font.Font('freesansbold.ttf', 20)
                    text = text.replace("_", " ")
                    text = font.render(text.capitalize(), True, WHITE)
                    textRect = text.get_rect()
                    textRect.center = rect.center
                    screen.blit(text, textRect)
                top_left_corner = (top_left_corner[0] + t_width + THICKNESS, top_left_corner[1])
            top_left_corner = (30, top_left_corner[1] + t_length + THICKNESS)

        pygame.display.flip()

    def loop(self):

        pygame.init()
        screen = pygame.display.set_mode([MAP_WIDTH, MAP_HEIGHT])
        pygame.display.set_caption("GENSHINDLE")

        running = True
        state = "home_screen"
        color = WHITE

        while running:
            bg = pygame.image.load("BG.png")
            bg = pygame.transform.scale(bg, (MAP_WIDTH, MAP_HEIGHT))
            screen.blit(bg, (0, 0))

            if state == "home_screen":
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render('PRESS KEY TO START', True, WHITE)
                textRect = text.get_rect()
                textRect.center = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
                screen.blit(text, textRect)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        character_to_guess = characters[random.randint(0, len(characters) - 1)]
                        print(character_to_guess.name)
                        guessed_characters = []
                        available_characters = characters.copy()
                        guess_counter = 0
                        current_character = available_characters[0]
                        properties = list(vars(character_to_guess).keys())
                        displayed_properties = properties[0:3]
                        while len(displayed_properties) < 3 + number_of_additional_properties:
                            add_properties = random.choices(properties[3:-1], k=number_of_additional_properties)
                            if (properties[-1] or properties[-2] not in add_properties) and len(
                                    set(add_properties)) == number_of_additional_properties:
                                displayed_properties += add_properties
                        state = "game"
            elif state == "win" or state == "lose":
                if state == "lose":
                    screen.fill(RED)
                    font = pygame.font.Font('freesansbold.ttf', 36)
                    text = font.render('YOU LOSE', True, WHITE)
                    textRect = text.get_rect()
                    textRect.center = (MAP_WIDTH // 2, 50)
                    screen.blit(text, textRect)
                    path = os.getcwd() + "\\Icons\\" + str(character_to_guess.name).replace(" ", "_") + "_Icon.png"
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img, (STANDARD_IMG_SIZE+50, STANDARD_IMG_SIZE+50))
                    imgRect = img.get_rect()
                    imgRect.center = (MAP_WIDTH // 2, 175)
                    screen.blit(img, imgRect)

                    table = [displayed_properties] + [character_to_guess]
                    top_left_corner = (30, img.get_rect().bottom + 100)
                    app.draw_table(table, displayed_properties, img, screen, character_to_guess, top_left_corner)

                else:
                    #screen.fill(BLACK)
                    font = pygame.font.Font('freesansbold.ttf', 36)
                    text = font.render('YOU WON', True, WHITE)
                    textRect = text.get_rect()
                    textRect.center = (MAP_WIDTH // 2 - 80, 100)
                    screen.blit(text, textRect)
                    path = os.getcwd() + "\\Icons\\" + str(current_character.name).replace(" ", "_") + "_Icon.png"
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img, (STANDARD_IMG_SIZE, STANDARD_IMG_SIZE))
                    screen.blit(img, (textRect.right + 10, 10))

                    table = [displayed_properties] + guessed_characters
                    top_left_corner = (30, img.get_rect().bottom + 50)
                    app.draw_table(table, displayed_properties, img, screen, character_to_guess, top_left_corner)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        color = WHITE
                        pygame.display.flip()
                        character_to_guess = characters[random.randint(0, len(characters) - 1)]
                        guessed_characters = []
                        available_characters = characters.copy()
                        guess_counter = 0
                        current_character = available_characters[0]
                        state = "game"
            elif state == "game":
                #screen.fill(BLACK)
                font = pygame.font.Font('freesansbold.ttf', 30)
                text = font.render('Choose character to guess', True, WHITE)
                textRect = text.get_rect()
                textRect.topleft = (10, 10)
                screen.blit(text, textRect)
                path = os.getcwd() + "\\Icons\\" + str(current_character.name).replace(" ", "_") + "_Icon.png"
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (STANDARD_IMG_SIZE, STANDARD_IMG_SIZE))
                screen.blit(img, (textRect.right + 10, 10))

                table = [displayed_properties] + guessed_characters
                top_left_corner = (30, img.get_rect().bottom + 50)
                app.draw_table(table, displayed_properties, img, screen, character_to_guess, top_left_corner)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            c = available_characters.index(current_character)
                            current_character = available_characters[(c+1) % len(available_characters)]
                        elif event.key == pygame.K_LEFT:
                            c = available_characters.index(current_character)
                            current_character = available_characters[(c + len(available_characters) - 1) % len(available_characters)]
                        elif event.key == pygame.K_RETURN:
                            guess_counter += 1
                            guessed_characters.append(current_character)
                            if current_character == character_to_guess:
                                state = "win"
                            else:
                                available_characters.remove(current_character)
                                current_character = available_characters[0]
                                if guess_counter == max_guesses:
                                    state = "lose"
                            pygame.display.flip()


characters = sorted(setup.scrap_all_characters(), key=lambda x: x.name)
app = Application()
app.loop()

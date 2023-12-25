import setup
import finder
import random
from datetime import datetime
import pygame
import os

MAP_WIDTH = 1500
MAP_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (212, 17, 17)
GREEN = (17, 120, 20)

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
                        pygame.draw.rect(screen, GREEN, [0, 0, 10, 10], 1)
                if guessed_character == character_to_guess:
                    print("You WIN!!!")
                    guess_counter = max_guesses + 1

    def draw_table(self):
        running = True
        character_to_guess = characters[random.randint(0, len(characters) - 1)]
        properties = list(vars(character_to_guess).keys())
        displayed_properties = properties[0:3]
        while len(displayed_properties) < 3 + number_of_additional_properties:
            add_properties = random.choices(properties[3:-1], k=number_of_additional_properties)
            if (properties[-1] or properties[-2] not in add_properties) and len(
                    set(add_properties)) == number_of_additional_properties:
                displayed_properties += add_properties

        ###################################33
        table = [displayed_properties] + characters[:5]

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    screen.fill(BLACK)
                    font = pygame.font.Font('freesansbold.ttf', 30)
                    text = font.render('Choose character to guess', True, WHITE)
                    textRect = text.get_rect()
                    textRect.topleft = (10, 10)
                    screen.blit(text, textRect)
                    path = os.getcwd() + "\\Icons\\" + str(characters[0].name).replace(" ", "_") + "_Icon.png"
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img, (100, 100))
                    screen.blit(img, (textRect.right + 10, 10))

                    thickness = 2
                    t_length = 100
                    t_width = 180
                    for i in range(len(table)+1):
                        start_pos = (10, img.get_rect().bottom + 50 + (i*(t_length+thickness)))
                        end_pos = (MAP_WIDTH - 10, img.get_rect().bottom + 50 + (i*(t_length+thickness)))
                        pygame.draw.line(screen, WHITE, start_pos, end_pos, thickness)

                        for j in range(0, number_of_additional_properties + 5):
                            start_pos = (10 + (j*(t_width+thickness)), img.get_rect().bottom + 50)
                            end_pos = (10 + (j*(t_width+thickness)), img.get_rect().bottom + 50 + (t_length*(len(table))) + (thickness*(len(table)+1)))
                            pygame.draw.line(screen, WHITE, start_pos, end_pos, thickness)

                            if i == 0 and j > 0:
                                if j == 1:
                                    to_display = "Icon"
                                elif j > 1:
                                    to_display = table[i][j-2]
                                font = pygame.font.Font('freesansbold.ttf', 15)
                                text = font.render(to_display, True, WHITE)
                                textRect = text.get_rect()
                                textRect.topright = (10 + (j*(t_width+thickness)), img.get_rect().bottom + 50 + (i*(t_length+thickness)))
                                screen.blit(text, textRect)

                    pygame.display.flip()

    def loop(self):
        running = True
        state = "home_screen"
        color = WHITE

        while running:

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
                        available_characters = characters
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
                    textRect.center = (MAP_WIDTH // 2, MAP_HEIGHT // 2 - 50)
                    screen.blit(text, textRect)
                    path = os.getcwd() + "\\Icons\\" + str(character_to_guess.name).replace(" ", "_") + "_Icon.png"
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img, (200, 200))
                    screen.blit(img, (650, 400))
                    pygame.display.flip()
                else:
                    screen.fill(GREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        color = WHITE
                        pygame.display.flip()
                        character_to_guess = characters[random.randint(0, len(characters) - 1)]
                        print(character_to_guess.name)
                        guessed_characters = []
                        available_characters = characters
                        guess_counter = 0
                        current_character = available_characters[0]
                        state = "game"
            elif state == "game":
                screen.fill(BLACK)
                font = pygame.font.Font('freesansbold.ttf', 30)
                text = font.render('Choose character to guess', True, color)
                textRect = text.get_rect()
                textRect.topleft = (10, 10)
                screen.blit(text, textRect)
                path = os.getcwd() + "\\Icons\\" + str(current_character.name).replace(" ", "_") + "_Icon.png"
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (100, 100))
                screen.blit(img, (textRect.right + 10, 10))

                #DRAW TABLE HERE

                pygame.display.flip()
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
                                color = GREEN
                                state = "win"
                            else:
                                color = RED
                                available_characters.remove(current_character)
                                current_character = available_characters[0]
                                if guess_counter == max_guesses:
                                    state = "lose"
                            screen.fill(color)
                            pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode([MAP_WIDTH, MAP_HEIGHT])
pygame.display.set_caption("GENSHINDLE")
characters = setup.scrap_all_characters()
app = Application()
#app.loop()
app.draw_table()

import setup
import finder
import random
from datetime import datetime


def game():
    characters = setup.scrap_all_characters()
    while True:
        print("Guess character!")
        guess_counter = 0
        max_guesses = 5
        number_of_additional_properties = 3
        random_number = random.randint(0, len(characters)-1)
        character_to_guess = characters[random_number]
        properties = list(vars(character_to_guess).keys())
        displayed_properties = properties[0:3]
        while len(displayed_properties) < 3+number_of_additional_properties:
            add_properties = random.choices(properties[3:], k=number_of_additional_properties)
            if (properties[-1] or properties[-2] not in add_properties) and len(set(add_properties)) == number_of_additional_properties:
                displayed_properties += add_properties

        while guess_counter < max_guesses:
            guess = input()
            guess_counter += 1
            guessed_character = finder.find_by_name(characters, guess)
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


game()

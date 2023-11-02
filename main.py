import setup
import finder
import random


def game():
    print("haha")
    characters = setup.scrap_all_characters()
    while True:
        guess_counter = 0
        max_guesses = 5
        number_of_additional_properties = 4
        random_number = random.randint(0, len(characters)-1)
        character_to_guess = characters[random_number]
        properties = list(vars(character_to_guess).keys())
        displayed_properties = properties[0:2]
        while len(displayed_properties) < 2+number_of_additional_properties:
            add_properties = random.choices(properties[2:], k=number_of_additional_properties)
            if (properties[-1] or properties[-2] not in add_properties) and len(set(add_properties)) == number_of_additional_properties:
                displayed_properties += add_properties

        while guess_counter < max_guesses:
            guess = input()
            guess_counter += 1
            guessed_character = finder.find_by_name(characters, guess)
            for x in displayed_properties:
                print(getattr(character_to_guess, x))
                print(getattr(guessed_character, x))


game()

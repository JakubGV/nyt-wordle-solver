import argparse
from wordle_helper.wordle_helper import WordleHelper

def parse_args() -> None:
    parser = argparse.ArgumentParser(description='Helps you solve the NYT Wordle. Good starting words: irate adieu steak tread table audio.')
    parser.parse_args()

def ask_about_word() -> tuple:
    """
    ask_about_word asks the user to enter the colors the Wordle returned
    and returns the colors as a tuple.

    :param word: the word to ask about
    :return: a tuple of colors of each letter
    """
    valid_response = False
    alphabet = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
    while not valid_response:
        ans = input(f"Please enter the colors of the word (e.g. gbbyg): ").lower()
        word_colors = [l for l in ans if l in alphabet]
        if len(word_colors) != 5:
            print("Length of string must be 5 using only letters")
        else:
            valid_response = True

    return tuple(word_colors)

def solve(word_list: list) -> bool:
    """
    solve attempts to solve the Wordle of the day.

    :param word_list: the word_list to find words from
    :return: True if the Wordle was solved, false otherwise
    """
    wordle_solver = WordleHelper(word_list)

    for round in range(6):
        word = input("What word have you entered? ")
        word = word.lower()
        ans = input(f"Was '{word}' the Wordle (Y or N)? ").lower()
        
        if ans == 'y':
            print(f"Congratulations!\nWordle solved in {round+1} tries.")
            return True
        else:
            word_colors = ask_about_word()
        
        next_best_guess = wordle_solver.next_best_word(word, word_colors)
        
        if next_best_guess == '':
            print("Uh-oh. Word list is empty.")
            return False
        elif round != 5:
            print(f"There are {len(wordle_solver.word_list)} potential words.")
            print(f"The best word to guess next is: '{next_best_guess}'")

    return False

def main():
    parse_args()
    
    # Open the word_list file to get guesses from
    with open('word_list.txt', 'r') as word_file:
        word_list = [word.strip() for word in word_file]

    print('-' * 35)
    print("Starting the Wordle solver...")
    
    if not solve(word_list):
        print("Could not solve today's Wordle :(")

    print('-' * 35)

if __name__ == '__main__':
    main()
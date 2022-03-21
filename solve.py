import argparse

def parse_args() -> None:
    parser = argparse.ArgumentParser(description='Helps you solve the NYT Wordle. Good starting words: irate adieu steak tread table audio.')
    parser.parse_args()

def get_score(word: str) -> float:
    """
    get_score returns the 'score' of a word. 
    The score is the sum of individual letter scores. 
    The letter scores correspond to how frequent these letters show up in English words according to [research](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html).

    :param word: the word to find the score of
    :return: a float corresponding to the score of the word
    """
    score_sheet = {
        'e': 56.88,
        'a': 43.31,
        'r': 38.64,
        'i': 38.45,
        'o': 36.51,
        't': 35.43,
        'n': 33.92,
        's': 29.23,
        'l': 27.98,
        'c': 23.13,
        'u': 18.51,
        'd': 17.25,
        'p': 16.14,
        'm': 15.36,
        'h': 15.31,
        'g': 12.59,
        'b': 10.56,
        'f': 9.24,
        'y': 9.06,
        'w': 6.57,
        'k': 5.61,
        'v': 5.13,
        'x': 1.48,
        'z': 1.39,
        'j': 1.00,
        'q': 1.00,
    }

    score = 0.0
    letters_seen = set()
    for letter in word:
        if letter not in letters_seen:
            score += score_sheet[letter]
        letters_seen.add(letter)

    return score

def get_best_word(word_list: list) -> str:
    """
    get_best_word finds the best word to guess for the Wordle by finding the highest score word found by get_score.
    
    :param word_list: the word_list to search through
    :return: the highest scoring word
    """
    best_score = 0.0
    best_word = word_list[0]
    for word in word_list:
        score = get_score(word)
        if score > best_score:
            best_score = score
            best_word = word

    return best_word

def count_letter(word: str, letter: str) -> int:
    """
    count_letter finds the number of `letter`s in the `word`.
    Used to eliminate potential words in the case of duplicate letters in the Wordle.

    :param word: the word to search in
    :param letter: the letter to search for
    :return: the number of occurrences of letter in word
    """
    count = 0
    for l in word:
        if l == letter:
            count += 1

    return count

def delete_indices(word_list: list, indices_to_delete: set) -> None:
    """
    delete_indices removes the indices in `indices_to_delete` from the `word_list`.

    :param word_list: the word list to delete from
    :param indices_to_delete: a set of integer indices to delete from the word_list
    """
    num_deleted = 0
    for index in indices_to_delete:
        del word_list[index - num_deleted]
        num_deleted += 1

def find_duplicate_letter(word: str) -> str:
    """
    find_duplicate_letter finds a duplicate letter in `word`.

    :param word: the word to search in
    :return: the duplicate letter if it exists, otherwise the empty string
    """
    seen = set()
    for letter in word:
        if letter in seen:
            return letter
        else:
            seen.add(letter)

    return ''

def handle_duplicate(word_list: list, word_colors: tuple, word: str, duplicate_letter: str) -> None:
    """
    handle_duplicate handles the case of a word that has duplicate letters in it.
    This function is needed because of special rules pertaining to double letters.

    :param word_list: the word_list to search through
    :param word_colors: the colors of the word guessed
    :param word: the word guessed
    :param duplicate_letter: the letter that appears twice
    """
    index_a = -1
    index_b = -1

    for i, letter in enumerate(word):
        if letter == duplicate_letter:
            if index_a < 0:
                index_a = i
            else:
                index_b = i

    indices_to_delete = set()
    for j, word_list_word in enumerate(word_list):
        if word_colors[index_a] == 'g':
            # Remove any word that doesn't have the first letter in the right spot
            if word_list_word[index_a] != word[index_a]:
                indices_to_delete.add(j)
            
            if word_colors[index_b] == 'g':
                # Remove any word that doesn't have the second letter in the right spot
                if word_list_word[index_b] != word[index_b]:
                    indices_to_delete.add(j)
            
            if word_colors[index_b] == 'y':
                # Remove any word that doesn't have at least 2 instances of the letter or has the second letter in the wrong spot
                if count_letter(word_list_word, word[index_b]) < 2 or word[index_b] == word_list_word[index_b]:
                    indices_to_delete.add(j)
            
            if word_colors[index_b] == 'b':
                # Remove any word that has more than 1 instance of the letter
                if count_letter(word_list_word, word[index_b]) > 1:
                    indices_to_delete.add(j)

        if word_colors[index_a] == 'y':
            # Remove any word that has the first letter in the wrong spot
            if word[index_a] == word_list_word[index_a]:
                indices_to_delete.add(j)

            if word_colors[index_b] == 'g':
                # Remove any word that doesn't have the second letter in the right spot or has less than 2 instances of the letter
                if word_list_word[index_b] != word[index_b] or count_letter(word_list_word, word[index_a]) < 2:
                    indices_to_delete.add(j)

            if word_colors[index_b] == 'y':
                # Remove any word that has the second letter in the wrong spot or has less than 2 instances of the letter
                if word[index_b] == word_list_word[index_b] or count_letter(word_list_word, word[index_a]) < 2:
                    indices_to_delete.add(j)

            if word_colors[index_b] == 'b':
                # Remove any word that has more than 1 instance of the letter
                if count_letter(word_list_word, word[index_a]) > 1:
                    indices_to_delete.add(j)

        if word_colors[index_a] == 'b':
            if word_colors[index_b] == 'g':
                # Remove any word that has more than 1 instance of the letter or doesn't have the second letter in the right spot
                if count_letter(word_list_word, word[index_a]) > 1 or word_list_word[index_b] != word[index_b]:
                    indices_to_delete.add(j)

            if word_colors[index_b] == 'y':
                # Remove any word that has more than 1 instance of the letter or has the second letter in the wrong spot
                if count_letter(word_list_word, word[index_a]) > 1 or word[index_b] == word_list_word[index_b]:
                    indices_to_delete.add(j)

            if word_colors[index_b] == 'b':
                # Remove any word containing the letter
                if word[index_a] in word_list_word:
                    indices_to_delete.add(j)
        
    delete_indices(word_list, indices_to_delete)

def update_word_list(word_list: list, word_colors: tuple, word: str) -> None:
    """
    update_word_list updates the `word_list` according to the colors returned by the Wordle.

    :param word_list: the word_list to update
    :param word_colors: the colors of the letters returned by the Wordle
    :param word: the word that was entered into the Wordle
    """
    duplicate_letter = find_duplicate_letter(word)
    if duplicate_letter != '':
        handle_duplicate(word_list, word_colors, word, duplicate_letter)

    indices_to_delete = set()
    for i, color in enumerate(word_colors):
        for j, word_list_word in enumerate(word_list):
            # Remove the word that wasn't the Wordle
            if word_list_word == word:
                indices_to_delete.add(j)
            
            # Only handle not duplicate letters
            if word[i] != duplicate_letter:
                # Remove any word that doesn't have this letter in the right spot
                if color == 'g' and word_list_word[i] != word[i]:
                    indices_to_delete.add(j)
                
                # Remove any word that doesn't have the letter or has the letter in the wrong spot
                elif color == 'y' and (word[i] not in word_list_word or word[i] == word_list_word[i]):
                    indices_to_delete.add(j)
                
                # Remove any word that has the letter since it shouldn't
                elif color == 'b' and word[i] in word_list_word:
                        indices_to_delete.add(j)
            
    delete_indices(word_list, indices_to_delete)

def ask_about_word(word: str) -> tuple:
    """
    ask_about_word asks the user to enter the colors the Wordle returned.

    :param word: the word to ask about
    :return: a tuple of colors of each letter
    """
    word_colors = []
    for letter in word:
        ans = input(f"What color is the letter '{letter}' (G, Y, or B)? ")
        word_colors.append(ans.lower())

    return tuple(word_colors)

def check_row(word: str, word_list: list) -> bool:
    """
    check_row asks if the word guessed was the Wordle, gets the colors for that word, and updates the word list.

    :param word: the word entered
    :param word_list: the word list to search from
    :return: True if the word was the Wordle, False otherwise
    """
    ans = input(f"Was '{word}' the Wordle (Y or N)? ")
    if ans.lower() == 'y':
        return True
    else:
        word_colors = ask_about_word(word)

    update_word_list(word_list, word_colors, word)

    return False

def solve(word_list: list) -> bool:
    """
    solve attempts to solve the Wordle of the day.

    :param word_list: the word_list to find words from
    :return: True if the Wordle was solved, false otherwise
    """
    for round in range(6):
        word = input("What word have you entered? ")
        word = word.lower()
        if check_row(word, word_list):
            print(f"Congratulations!\nWordle solved in {round+1} tries.")
            return True
        
        if len(word_list) == 0:
            print("Uh-oh. Word list is empty.")
            return False
        elif round != 5:
            print(f"There are {len(word_list)} potential words.")
            best_guess = get_best_word(word_list)
            print(f"The best word to guess next is: '{best_guess}'")

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
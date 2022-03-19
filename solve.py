import argparse

def parse_args() -> None:
    parser = argparse.ArgumentParser(description='Helps you solve the NYT Wordle. Good starting words: irate adieu steak tread table audio.')
    parser.parse_args()

def get_score(word: str) -> float:
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
    best_score = 0.0
    best_word = word_list[0]
    for word in word_list:
        score = get_score(word)
        if score > best_score:
            best_score = score
            best_word = word

    return best_word

def count_letter(word: str, letter: str) -> int:
    count = 0
    for l in word:
        if l == letter:
            count += 1

    return count

def delete_indices(word_list: list, indices_to_delete: set) -> None:
    num_deleted = 0
    for index in indices_to_delete:
        del word_list[index - num_deleted]
        num_deleted += 1

def find_duplicate_letter(word: str) -> str:
    seen = set()
    for letter in word:
        if letter in seen:
            return letter
        else:
            seen.add(letter)

    return ''

def handle_duplicate(word_list, word_colors, word, duplicate_letter):
    index_a = -1
    index_b = -1

    indices_to_delete = set()
    
    for i, letter in enumerate(word):
        if letter == duplicate_letter:
            if index_a < 0:
                index_a = i
            else:
                index_b = i

    for j, word_list_word in enumerate(word_list):
        if word_colors[index_a] == 'g' and word_colors[index_b] == 'g':
            if word_list_word[index_a] != word[index_a] or word_list_word[index_b] != word[index_b]:
                indices_to_delete.add(j)
        
        elif word_colors[index_a] == 'g' and word_colors[index_b] == 'y':
            if word_list_word[index_a] != word[index_a] or (count_letter(word_list_word, word[index_b]) < 2 or word[index_b] == word_list_word[index_b]):
                indices_to_delete.add(j)
        
        elif word_colors[index_a] == 'y' and word_colors[index_b] =='g':
            if (count_letter(word_list_word, word[index_a]) < 2 or word[index_a] == word_list_word[index_a]) or word_list_word[index_b] != word[index_b]:
                indices_to_delete.add(j)

        elif word_colors[index_a] == 'g' and word_colors[index_b] == 'b':
            if word_list_word[index_a] != word[index_a] or count_letter(word_list_word, word[index_b]) > 1:
                indices_to_delete.add(j)
        
        elif word_colors[index_a] == 'b' and word_colors[index_b] == 'g':
            if count_letter(word_list_word, word[index_a]) > 1 or word_list_word[index_b] != word[index_b]:
                indices_to_delete.add(j)

        elif word_colors[index_a] == 'y' and word_colors[index_b] == 'y':
            if count_letter(word_list_word, word[index_a]) < 2 or word[index_a] == word_list_word[index_a] or word[index_b] == word_list_word[index_b]:
                indices_to_delete.add(j)

        elif word_colors[index_a] == 'y' and word_colors[index_b] == 'b':
            if word[index_a] == word_list_word[index_a] or count_letter(word_list_word, word[index_a]) != 1:
                indices_to_delete.add(j)
        
        elif word_colors[index_a] == 'b' and word_colors[index_b] == 'y':
            if count_letter(word_list_word, word[index_a]) != 1 or word[index_b] == word_list_word[index_b]:
                indices_to_delete.add(j)
        
        elif word_colors[index_a] == 'b' and word_colors[index_b] == 'b':
            if word[index_a] in word_list_word:
                indices_to_delete.add(j)

    delete_indices(word_list, indices_to_delete)

def update_word_list(word_list: list, word_colors, word: str) -> None:
    indices_to_delete = set()
    
    duplicate_letter = find_duplicate_letter(word)
    if duplicate_letter != '':
        handle_duplicate(word_list, word_colors, word, duplicate_letter)

    for i, color in enumerate(word_colors):
        for j, word_list_word in enumerate(word_list):
            if word_list_word == word: # Make sure to remove the word that didn't work
                indices_to_delete.add(j)
            
            elif word[i] != duplicate_letter:
                if color == 'g' and word_list_word[i] != word[i]:
                    indices_to_delete.add(j)
                elif color == 'y' and (word[i] not in word_list_word or word[i] == word_list_word[i]):
                    indices_to_delete.add(j)
                elif color == 'b' and word[i] in word_list_word:
                        indices_to_delete.add(j)
            
    delete_indices(word_list, indices_to_delete)

def ask_about_word(word: str) -> tuple:
    word_colors = []
    for letter in word:
        ans = input(f"What color is the letter '{letter}' (G, Y, or B)? ")
        word_colors.append(ans.lower())

    return tuple(word_colors)

def check_row(word: str, word_list: list) -> bool:
    ans = input(f"Was '{word}' the Wordle (Y or N)? ")
    if ans.lower() == 'y':
        return True
    else:
        word_colors = ask_about_word(word)

    update_word_list(word_list, word_colors, word)

    return False

def solve(word_list: list) -> bool:
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
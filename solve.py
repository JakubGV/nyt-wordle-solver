import argparse

def parse_args() -> str:
    parser = argparse.ArgumentParser(description='Help solve the NYT Wordle. Good starting words: irate adieu steak tread table audio.')
    parser.add_argument('starting_word', type=str, help='The word you started with.')

    args = parser.parse_args()

    if len(args.starting_word) != 5:
      raise ValueError("Invalid starting word")

    return args.starting_word

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

def ask_about_word(word: str) -> tuple:
    word_colors = []
    for letter in word:
        ans = input(f"What color is the letter '{letter}' (G, Y, or B)? ")
        word_colors.append(ans.lower())

    return tuple(word_colors)

def update_word_list(word_list: list, word_colors, word: str) -> None:
    indices_to_delete = set()
    for i, color in enumerate(word_colors):
        for j, word_list_word in enumerate(word_list):
            if color == 'g' and word_list_word[i] != word[i]:
                indices_to_delete.add(j)
            elif color == 'y' and word[i] not in word_list_word:
                indices_to_delete.add(j)
            elif color == 'b' and word[i] in word_list_word:
                indices_to_delete.add(j)

    deleted = 0
    for index in indices_to_delete:
        del word_list[index-deleted]
        deleted += 1

def check_row(word: str, word_list: list) -> bool:
    ans = input(f"Was '{word}' the Wordle (Y or N)? ")
    if ans.lower() == 'y':
        return True
    else:
        word_colors = ask_about_word(word)

    update_word_list(word_list, word_colors, word)

    return False
    
def solve(starting_word: str, word_list: list) -> bool:
    word = starting_word
    for round in range(6):
        if check_row(word, word_list):
            print(f"Congratulations!\nWordle solved in {round+1} tries.")
            return True
        
        if len(word_list) == 0:
            print("Uh-oh. Word list is empty.")
            return False
        elif round != 5:
            next_word = get_best_word(word_list)
            print(f"The best word to guess next is: {next_word}")
            word = next_word

    return False

def main():
    starting_word = parse_args()

    with open('word_list.txt', 'r') as word_file:
        word_list = [word.strip() for word in word_file]

    if not solve(starting_word, word_list):
        print("Could not solve today's Wordle :(")

if __name__ == '__main__':
    main()
import argparse

def parse_args() -> None:
    parser = argparse.ArgumentParser(description='Trims a word list to only include 5 letters words.')
    parser.add_argument('file', help='the filename of the word list to trim')
    args = parser.parse_args()

    return args.file

def trim_word_list():
    """
    trim_word_list trims a lists of words to only contain 5 letter words for the Wordle.
    """
    file = parse_args()

    with open(file, 'r') as word_file:
        word_list = [word.strip() for word in word_file]

    new_word_list = [word for word in word_list if len(word) == 5]

    contents = '\n'.join(new_word_list)

    with open(file, 'w') as word_file:
        word_file.write(contents)

def main():
    trim_word_list()

if __name__ == '__main__':
    main()
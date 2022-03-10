import argparse

def parse_args() -> tuple:
  parser = argparse.ArgumentParser(description='Insert a word into the specified word list.')
  parser.add_argument('words', nargs='*', help='The words to insert.')

  args = parser.parse_args()

  if len(args.words) < 1:
    raise ValueError('No word provided to insert')

  return tuple(args.words)

def insert_word(word_list: list, word_to_insert: str) -> bool:
  """
  insert_word inserts a singular word into the specified word_list.

  :param word_list: the word list to insert into
  :param word_to_insert: the word to insert into the word list
  :return: a value of True upon successful insertion, otherwise False
  """
  index_to_insert = 0
  for i, word in enumerate(word_list):
    if word_to_insert < word:
      index_to_insert = i
      break
    elif word_to_insert == word:
      return False
    
    if i == len(word_list) - 1: # take care of inserting at the end of the list
      index_to_insert = len(word_list)

  word_list.insert(index_to_insert, word_to_insert)
  return True
  
def insert_words(word_list: list, words_to_insert: tuple) -> None:
  """
  insert_words tries to insert a tuple of words into the word list and prints which were successful and which weren't.

  :param word_list: the word list to insert into
  :param words_to_insert: the words to attempt to insert into the word list
  """
  success = []
  fail = []
  
  for word in words_to_insert:
    if insert_word(word_list, word):
      success.append(word)
    else:
      fail.append(word)
  
  if len(fail) > 0:
    print(f"Failed to insert: {' '.join(fail)}")
  if len(success) > 0:
    print(f"Successfully inserted: {' '.join(success)}")

def main():
  words_to_insert = parse_args()
  
  file = 'word_list.txt'

  with open(file, 'r') as word_file:
    word_list = [word.strip() for word in word_file]

  insert_words(word_list, words_to_insert)
  
  contents = '\n'.join(word_list)
  
  with open(file, 'w') as word_file:
    word_file.write(contents)

if __name__ == '__main__':
  main()
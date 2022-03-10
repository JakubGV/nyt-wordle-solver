def trim_word_list():
  """
  trim_word_list trims a lists of words to only contain 5 letter words for the Wordle.
  """
  file = 'word_list.txt'

  with open(file, 'r') as word_file:
    word_list = [word.strip() for word in word_file]

  new_word_list = []
  for word in word_list:
    if len(word) == 5:
      new_word_list.append(word)

  contents = '\n'.join(new_word_list)

  with open(file, 'w') as word_file:
    word_file.write(contents)

if __name__ == '__main__':
  trim_word_list()
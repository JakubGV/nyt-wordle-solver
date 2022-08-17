class WordleHelper:
    """
    A class that represents a Wordle helper.

    ...

    Attributes
    ----------
    word_list : list
        the list of words to use

    Methods
    -------
    next_best_word(word_guessed : str, word_colors : str) -> str:
        Returns the next best word given the current word guessed and its colors.
    """
    def __init__(self, word_list: list) -> None:
        self.word_list = word_list

    def _get_word_score(self, word: str) -> float:
        """
        _get_word_score returns the 'score' of a word. 
        The score is the sum of individual letter scores. 
        The letter scores correspond to how frequent these letters show up in English words 
        according to [research](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html).

        :param word: the word to find the score of
        :return: a float corresponding to the score of the word
        """
        score_sheet = {
            'e': 56.88, 'a': 43.31, 'r': 38.64,  'i': 38.45,
            'o': 36.51, 't': 35.43, 'n': 33.92,  's': 29.23,
            'l': 27.98, 'c': 23.13, 'u': 18.51,  'd': 17.25,
            'p': 16.14, 'm': 15.36, 'h': 15.31,  'g': 12.59,
            'b': 10.56, 'f': 9.24,  'y': 9.06,   'w': 6.57,
            'k': 5.61,  'v': 5.13,  'x': 1.48,   'z': 1.39,
            'j': 1.00,  'q': 1.00,
        }

        score = 0.0
        letters_seen = set()
        for letter in word:
            # Only count unique letters to the score to prioritize diverse letters
            if letter not in letters_seen:
                score += score_sheet[letter]
            letters_seen.add(letter)

        return score

    def _get_best_word(self) -> str:
        """
        _get_best_word finds the best word to guess for the Wordle 
        by finding the highest score word found by _get_word_score.
        
        :return: the highest scoring word
        """
        word_scores = [self._get_word_score(word) for word in self.word_list]
        best_score = max(word_scores)
        best_word = self.word_list[word_scores.index(best_score)]

        return best_word

    def _find_duplicate_letter(word: str) -> str:
        """
        _find_duplicate_letter finds a duplicate letter in `word`.

        :param word: the word to search in
        :return: the duplicate letter if it exists, otherwise the empty string
        """
        seen = set()
        for letter in word:
            if letter in seen:
                return letter
            seen.add(letter)

        return ''

    def _count_letter(self, word: str, letter: str) -> int:
        """
        _count_letter counts the number of times `letter` appears in `word`.
        Used to eliminate potential words in the case of duplicate letters.

        :param word: the word to search in
        :param letter: the letter to search for
        :return: the number of occurrences of letter in word
        """
        count = 0
        for l in word:
            if l == letter:
                count += 1

        return count

    def _handle_duplicate(self, word_guessed: str, word_colors: tuple, duplicate_letter: str) -> None:
        """
        _handle_duplicate handles the case of words with duplicate letters and updates the
        internal word_list.
        This function is needed because of special considerations needed for double letters.

        :param word_guessed: the word that was guessed
        :param word_colors: the colors of the word guessed
        :param duplicate_letter: the letter that appears twice
        :return: the updated word list
        """
        index_a = -1
        index_b = -1

        # Get the indices of the duplicate letters
        for i, letter in enumerate(word_guessed):
            if letter == duplicate_letter:
                if index_a < 0:
                    index_a = i
                else:
                    index_b = i

        indices_to_delete = set()
        for j, word_list_word in enumerate(self.word_list):
            if word_colors[index_a] == 'g':
                # Remove any word that doesn't have the first letter in the right spot
                if word_list_word[index_a] != word_guessed[index_a]:
                    indices_to_delete.add(j)
                
                if word_colors[index_b] == 'g':
                    # Remove any word that doesn't have the second letter in the right spot
                    if word_list_word[index_b] != word_guessed[index_b]:
                        indices_to_delete.add(j)
                
                if word_colors[index_b] == 'y':
                    # Remove any word that doesn't have at least 2 instances of the letter or has the second letter in the wrong spot
                    if self._count_letter(word_list_word, word_guessed[index_b]) < 2 or word_guessed[index_b] == word_list_word[index_b]:
                        indices_to_delete.add(j)
                
                if word_colors[index_b] == 'b':
                    # Remove any word that has more than 1 instance of the letter
                    if self._count_letter(word_list_word, word_guessed[index_b]) > 1:
                        indices_to_delete.add(j)

            if word_colors[index_a] == 'y':
                # Remove any word that has the first letter in the wrong spot
                if word_guessed[index_a] == word_list_word[index_a]:
                    indices_to_delete.add(j)

                if word_colors[index_b] == 'g':
                    # Remove any word that doesn't have the second letter in the right spot or has less than 2 instances of the letter
                    if word_list_word[index_b] != word_guessed[index_b] or self._count_letter(word_list_word, word_guessed[index_a]) < 2:
                        indices_to_delete.add(j)

                if word_colors[index_b] == 'y':
                    # Remove any word that has the second letter in the wrong spot or has less than 2 instances of the letter
                    if word_guessed[index_b] == word_list_word[index_b] or self._count_letter(word_list_word, word_guessed[index_a]) < 2:
                        indices_to_delete.add(j)

                if word_colors[index_b] == 'b':
                    # Remove any word that has more than 1 instance of the letter
                    if self._count_letter(word_list_word, word_guessed[index_a]) > 1 or word_guessed[index_b] == word_list_word[index_b]:
                        indices_to_delete.add(j)

            if word_colors[index_a] == 'b':
                # Remove any word with the letter at this position
                if word_guessed[index_a] == word_guessed[word_list_word]:
                    indices_to_delete.add(j)

                if word_colors[index_b] == 'g':
                    # Remove any word that has more than 1 instance of the letter or doesn't have the second letter in the right spot
                    if self._count_letter(word_list_word, word_guessed[index_a]) > 1 or word_list_word[index_b] != word_guessed[index_b]:
                        indices_to_delete.add(j)

                if word_colors[index_b] == 'y':
                    # Remove any word that has more than 1 instance of the letter or has the second letter in the wrong spot
                    if self._count_letter(word_list_word, word_guessed[index_a]) > 1 or word_guessed[index_b] == word_list_word[index_b]:
                        indices_to_delete.add(j)

                if word_colors[index_b] == 'b':
                    # Remove any word containing the letter
                    if word_guessed[index_a] in word_list_word:
                        indices_to_delete.add(j)
            
        # Update the word list
        self.word_list = [word for i, word in enumerate(self.word_list) if i not in indices_to_delete]

    def _update_word_list(self, word_guessed: str, word_colors: tuple) -> None:
        """
        _update_word_list updates self.word_list according to the colors 
        returned by the Wordle.

        :param word_guessed: the word that was guessed
        :param word_colors: the colors of the letters returned by the Wordle
        """
        duplicate_letter = self._find_duplicate_letter(word_guessed)
        if duplicate_letter != '':
            word_list = self._handle_duplicate(word_guessed, word_colors, duplicate_letter)
        
        indices_to_delete = set()
        for i, color in enumerate(word_colors):
            for j, word_list_word in enumerate(word_list):
                # Remove the word that wasn't the Wordle
                if word_list_word == word_guessed:
                    indices_to_delete.add(j)
                
                # Only handle not duplicate letters
                if word_guessed[i] != duplicate_letter:
                    # Remove any word that doesn't have this letter in the right spot
                    if color == 'g' and word_list_word[i] != word_guessed[i]:
                        indices_to_delete.add(j)
                    
                    # Remove any word that doesn't have the letter or has the letter in the wrong spot
                    elif color == 'y' and (word_guessed[i] not in word_list_word or word_guessed[i] == word_list_word[i]):
                        indices_to_delete.add(j)
                    
                    # Remove any word that has the letter since it shouldn't
                    elif color == 'b' and word_guessed[i] in word_list_word:
                        indices_to_delete.add(j)
                
        # Update the word list
        self.word_list = [word for i, word in enumerate(self.word_list) if i not in indices_to_delete]

    def next_best_word(self, word_guessed: str, word_colors: tuple)  -> str:
        """
        next_best_word finds the best word to guess next by analyzing the
        current word guessed and the colors returned by the Wordle to
        update the word list and provide the next highest scoring word.

        :param word_guessed: the word the player guessed
        :param word_colors: the colors of the letters returned by the Wordle
        :return: the best word to guess next
        """
        self._update_word_list(word_guessed, word_colors)
        best_guess = self._get_best_word

        return best_guess
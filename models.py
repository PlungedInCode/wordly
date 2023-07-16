from colorama import Fore, Style
from random_word import Wordnik
import nltk

class WordlyGame:
    def __init__(self: str) -> None:
        self.Validator = InputValidator()
        self.Generator = HiddenWordGenerator()
        self.attempts = 6
        self.guessed_words = []
        self.win = False
    
    def play(self):
        self.game_instruction()
        while self.attempts > 0 and not self.win:
            print(f"Attempts left {self.attempts}")
            guess = input("Enter your guess: ").strip().lower()

            if guess == "/show_attempts":
                print("Guessed words :\n", "\n".join(self.guessed_words))
                continue
            
            if not self.check_guess(guess):
                continue

            if guess == self.Generator.hidden_word:
                self.win = True
            
            checked_guess = self.check(guess)
            self.guessed_words.append(checked_guess)
            print(checked_guess)

            self.attempts -= 1
        
        if not self.win:
            print("Game over. You ran out of attempts.")
            print(f"The hidden word was: {self.Generator.hidden_word}")
        else:
            print("Congratulations! You guessed the word.")
    

    def check_guess(self, guess):
        if not self.Validator.is_valid_guess(guess):
            print("Invalid guess. Please enter a 5-letter word in english.")
            return False
        elif not self.Validator.is_english_word(guess):
            print("There's no such word in English.")
            return False
        elif self.check(guess) in self.guessed_words:
            print("Please try new word")
            return False
        return True
    

    def check(self, guess):
        checked_guess = ""
        for i in range(5):
            if guess[i] == self.Generator.hidden_word[i]:
                checked_guess += (Fore.GREEN + guess[i] + Style.RESET_ALL)
            elif guess[i] in self.Generator.hidden_word:
                checked_guess += (Fore.YELLOW + guess[i] + Style.RESET_ALL)
            else:
                checked_guess += (Fore.RED + guess[i] + Style.RESET_ALL)
        return checked_guess

    @staticmethod
    def game_instruction():
        ramen = Fore.GREEN + "Ra" + Fore.YELLOW + "m" + Fore.RED + "en" + Style.RESET_ALL
        green = Fore.GREEN + "Green" + Style.RESET_ALL
        yellow = Fore.YELLOW + "Yellow" + Style.RESET_ALL
        red = Fore.RED + "Red" + Style.RESET_ALL
        print(f"""Wordle is a single player game
        A player has to guess a five letter hidden word
        You have six attempts
        Your Progress Guide "{ramen}"
        "{green}" - Indicates that the letter at that position was guessed correctly
        "{yellow}" - indicates that the letter at that position is in the hidden word, but in a different position
        "{red}" - indicates that the letter at that position is wrong, and isn't in the hidden word   """)


class HiddenWordGenerator:
    # TODO : Build Wordnik with my own API key
    def __init__(self) -> None:
        self.Generator = Wordnik()
        self.hidden_word = self.generate_hidden_word()

    def generate_hidden_word(self) -> str:
        word = self.Generator.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun", 
                                              minDictionaryCount=3, minLength=5, maxLength=5)
        while word is None or '-' in word:
            word = self.Generator.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun", 
                                                  minDictionaryCount=3, minLength=5, maxLength=5)
        return word.lower()


class InputValidator:
    def __init__(self) -> None:
        nltk.download('words') 

    @staticmethod
    def is_english_word(word):
        english_words = set(nltk.corpus.words.words())
        return word.lower() in english_words

    @staticmethod
    def is_valid_guess(guess: str) -> bool:
        return len(guess) == 5 and guess.isalpha()

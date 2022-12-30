"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 150989395
Name:       Esa Särkelä
Email:      esa.sarkela@tuni.fi

Wheel of fortune -type game.
https://en.wikipedia.org/wiki/Wheel_of_Fortune_(American_game_show)
FEATURES MISSING:
    -BANDIT slot on the wheel (reduces points to 0 and passes turn)
    -PHRASE HINTS, a hint shown with the phrase
        ex. "WHEEL OF FORTUNE" hint could be "American game show"
    -MULTIPLE ROUNDS WITH SAME PLAYER SCORES
        in actual wheel of fortune points are accrued over a number of rounds

------------------------------------ GUIDE ------------------------------------
The objective of the game is to guess the phrase presented on upper part of
the window as empty slots. The game is played in turns. On their turn a player
may:
        Guess a consonant
        Guess a vowel
        Guess the phrase
Before a players turn a "wheel" is spun and points are presented. Guessing
consonants or vowels is done by pressing the corresponding letter on the
on-screen keyboard. If the player guesses a consonant correct they are awarded
the corresponding amount of points. Guessing a vowel does NOT award points and
instead costs 200 points. A player may not guess a vowel if they do not have
enough points. If a player chooses an incorrect consonant or vowel, the next
player gets their turn. Player turns are displayed between the keyboard
and the phrase in announcer label.
    To win the game, a player may guess the phrase on their turn by pressing
the "?" button on the on-screen keyboard. A pop-up window opens, where the
answer is submitted. If the player guesses correctly, they win with the score
they have accrued. A new game can be initiated by pressing the "new game"
-menu in the top menu bar.
    The number of players can be adjusted by altering the NUMBER_OF_PLAYERS
integer. New phrases can also be added to the PHRASES list if so desired.

Tehtävän arvijoijalle:
Tähtäsin kehittyneeseen käyttöliittymään.
    Ohjelma sisältää käyttöliittymäkomponentteja, joita ei käsitelty kurssilla.
    - Ponnahdusikkuna, kun arvataan lausetta
    - Ikkunan yläosan pudotusvalikko
    Silmukassa luotavia käyttöliittymäkomponentteja
    - Interaktiivinen näppäimistö ja arvatut kirjaimet
"""

from tkinter import *
import random

# List of solution phrases to be chosen from.
PHRASES = ["WHEEL OF FORTUNE", "TAMPERE UNIVERSITY",
           "OBJECT ORIENTED PROGRAMMING", "PROGRAMMING WITH PYTHON",
           "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"]
# QWERTY -"alphabet"
QWERTY = "QWERTYUIOPASDFGHJKLZXCVBNM?"
# Vowels and consonants
VOWELS = "AEIOU"
CONSONANTS = "QWRTYPSDFGHJKLZXCVBNM"
# Number of players
NUMBER_OF_PLAYERS = 2

class Player:
    """
    Player class for wheel of fortune.
    """

    def __init__(self, name):
        """
        Players have a name and a score.

        :param name: string, name
        """
        self.__name = name
        self.__score = 0

    def get_name(self):
        """
        Name getter.

        :return: string, Player name
        """
        return self.__name

    def get_score(self):
        """
        Score getter.

        :return: int, Player score
        """
        return self.__score

    def gain_points(self, points):
        """
        Add points to players' score. Return True if adding was successful
        and False otherwise.

        :param points: int, points to be added to <self.__score>.
        :return: boolean, whether adding points was successful.
        """

        # Check if <points> is an integer. Print an error message and return
        # False if not.
        if type(points) != int:
            print(f"'{points}' is not an integer!")
            return False
        # Check if <points> is positive. Print an error message and return
        # False if not.
        if points < 0:
            print(f"'{points} is not positive!")
            return False

        # Add <points> to <self.__score> and return True.
        self.__score += points
        return True

    def lose_points(self, points):
        """
        Reduce points from players' score. Return True if reduction was
        successful and False otherwise.

        :param points: int, points to be reduced from <self.__score>.
        :return: boolean, whether reducing points was successful.
        """

        # Check if <points> is an integer. Print an error message and return
        # False if not.
        if type(points) != int:
            print(f"'{points}' is not an integer!")
            return False
        # Check if <points> is positive. Print an error message and return
        # False if not.
        if points < 0:
            print(f"'{points} is not positive!")
            return False
        # Check if reduction would result in <self.__score> being negative.
        # Print an error message and return False if it would.
        if self.__score - points < 0:
            print(f"Score cannot be negative!")
            return False

        # Reduce <points> from <self.__score> and return True.
        self.__score -= points
        return True

    def reset_score(self):
        """
        Resets player score to zero.
        """

        self.__score = 0

class Fortunegame:
    def __init__(self):

        # Initialize and configure game window
        self.__window = Tk()
        self.__window.title("Wheel of Fortune")
        self.__window.configure(bg='#129A5C')

        # Create a bookkeeping list for players and initialize turn and roll
        # trackers. Fill in the player information.
        self.__players = []
        self.__whose_turn = 0
        self.__last_roll = 0
        for i in range(NUMBER_OF_PLAYERS):
            self.__players.append(Player(i + 1))

        # Pick a random solution <self.__phrase> from list of phrases
        # <PHRASES>.
        phrase_integer = random.randint(0, len(PHRASES) - 1)
        self.__phrase = PHRASES[phrase_integer]

        # Initialize bookkeeping sets for consonants. This is done to track
        # when all the available consonants in a phrase are used.
        self.__phrase_consonants = set()
        self.__used_consonants = set()
        for character in self.__phrase:
            if character in CONSONANTS:
                self.__phrase_consonants.add(character)

        # Initialize bookkeeping matrices for labels and buttons
        self.__phrase_labels = []
        self.__buttons = []

        # Create Labels for each character in the solution and add some flavor
        # by differentiating between guessable characters and whitespaces.

        # Set first row number as -1, because <self.get_next_row> increments
        # by one and we want the first row to be 0.
        self.__row_number = -1
        row_number = self.get_next_row()

        # Column number tracker for for-loop
        column_number = 0
        for word in self.__phrase.split(" "):
            # Print on next column if phrase length would exceed 12 units
            if len(word) + column_number > 12:
                row_number = self.get_next_row()
                column_number = 0

            # Create labels for each phrase letter and place them to the grid
            # accordingly.
            for i, c in enumerate(word):
                new_label = Label(self.__window, text="",
                                  font=("arial", 25, "bold"), width=2,
                                  relief=GROOVE, borderwidth=3,
                                  background="#E6DCE4")
                new_label.grid(row=row_number, column=column_number, sticky="NW")

                # Place labels to bookkeeping matrix.
                self.__phrase_labels.append(new_label)
                column_number += 1
                # Place an empty label in places of spaces in the actual
                # phrase.
                if i == len(word) - 1:
                    new_label = Label(self.__window, text="",
                                      font=("arial", 25, "bold"), width=2,
                                      relief=None, borderwidth=3,
                                      background="#129A5C")
                    new_label.grid(row=row_number, column=column_number,
                                   sticky="NW")
                    self.__phrase_labels.append(new_label)
                    column_number += 1

        # Create an announcer label, which shows instructions to the player
        self.__announcer = Label(self.__window,
                                 text=f"Player {self.__whose_turn} turn",
                                 font=("arial", 12, "bold"),
                                 width=2, relief=None, borderwidth=3,
                                 background="#129A5C")
        self.__announcer.grid(row=self.get_next_row(), column=0, columnspan=12,
                              sticky=E + W)

        # Create and store point labels to show player scores.
        self.__point_labels = []
        for i in range(NUMBER_OF_PLAYERS):
            text_str = f"Player {self.__players[i].get_name()} score: " \
                       f"{self.__players[i].get_score()}"
            new_point_label = Label(self.__window, text=text_str,
                                    background="#129A5C")
            new_point_label.grid(row=self.get_next_row(), column=0, columnspan=12)
            self.__point_labels.append(new_point_label)

        # Place keyboard buttons. In a standard english QWERTY-keyboard the
        # buttons are set on three rows of decreasing length:
        #       top row: 10 characters from Q to P
        #       middle row: 9 characters from A to L
        #       bottom row: 7 characters from Z to M
        # An additional "?" button is placed for solution guessing on the
        # bottom row.
        character_idx = 0
        for y in range(0, 3):
            row_number = self.get_next_row()
            for x in range(10 - y):
                character = QWERTY[character_idx]
                character_idx += 1

                def button_press(char=character):
                    """
                    Disable pressed button, since it makes no sense to guess
                    the same character twice. Also call check_character
                    function to see if character was part of the phrase.

                    Additionally, if "?" is pressed open the guessing screen
                    and exit function.

                    :param char: string, character pressed
                    """

                    # Check if pressed button was "?" and open the guessing
                    # screen via the <self.open_guess_screen()> function.
                    # Also make the announcer hype up the incoming guess.
                    if char == "?":
                        text_str = f"Player " \
                                   f"{self.__players[self.__whose_turn].get_name()} " \
                                   f"wants to guess!"
                        self.__announcer.configure(text=text_str)
                        self.open_guess_screen()
                        return

                    # Check if chosen character was a vowel and if it was,
                    # check if the player has enough points to buy one.
                    # If not enough points make the announcer scold the player
                    # for trying to cheat.
                    if char in VOWELS:
                        if self.__players[self.__whose_turn].get_score() < 200:
                            self.__announcer.configure(
                                text=f"Player "
                                     f"{self.__players[self.__whose_turn].get_name()} "
                                     f"turn, they rolled "
                                     f"{self.__last_roll}"
                                     f"\nYou dont have enough to buy a vowel! "
                                     f"(cost = 200 points)")
                            return
                        else:
                            self.__players[self.__whose_turn].lose_points(200)

                    # Find QWERTY-index of pressed button to disable it via
                    # <self.__buttons> -list. Perform cosmetic changes as well
                    # for flavor.
                    button_idx = QWERTY.index(char)
                    self.__buttons[button_idx].configure(relief=SUNKEN,
                                                         state="disabled")
                    # Call <check_character> --function to see if pressed
                    # buttons' character matched the solution.
                    # If chosen correctly spin the wheel again and pass the
                    # turn if not.
                    if self.check_character(char):
                        if char not in VOWELS:
                            self.__players[self.__whose_turn].gain_points(self.__last_roll)
                            self.__used_consonants.add(char)
                        self.spin_the_wheel()
                    else:
                        self.change_turn()

                # Create new button with command defined earlier. Set button
                # grid placement using x and y:
                #       x = row coordinate
                #       y = column coordinate
                new_button = Button(self.__window, text=character, width=5,
                                    height=2, bg="#f5f5dc",
                                    borderwidth=5,
                                    command=button_press)
                new_button.grid(row=row_number, column=x) # row=y + 3
                self.__buttons.append(new_button)

        # Make a menubar for possible options and starting a new game.
        menubar = Menu(self.__window)
        options_menu = Menu(menubar, tearoff=0)

        options_menu.add_command(label="New game", command=self.newgame)

        self.__window.config(menu=menubar)

        menubar.add_cascade(label="Options",
            menu=options_menu,
            underline=0
        )

        # Spin the wheel for first player to initialize game.
        self.spin_the_wheel()
        self.__window.mainloop()

    def spin_the_wheel(self):
        """
        Spins the wheel of fortune and sets last rolled value as the rolled
        value. Updates the text fields to show players what was rolled.
        """

        # Wheel values that can be rolled.
        wheel_values = [50, 100, 150, 200]

        # Choose a random wheel value
        spin = random.choice(wheel_values)

        # Update <self.__last_roll> value
        self.__last_roll = spin

        # Update GUI texts
        self.update_text()

    def change_turn(self):
        """
        Passes the turn to the next player.
        """

        # Increment the turn counter.
        self.__whose_turn += 1

        # Roll over turn counter if it exceeds number of players.
        if self.__whose_turn >= NUMBER_OF_PLAYERS:
            self.__whose_turn = 0

        # Spin the wheel for the next player
        self.spin_the_wheel()

    def update_text(self):
        """
        Updates GUI text fields.
        """

        # Update every players' score field with their current scores.
        for i in range(NUMBER_OF_PLAYERS):
            text_str = f"Player {self.__players[i].get_name()} score: " \
                       f"{self.__players[i].get_score()}"
            self.__point_labels[i].configure(text=text_str)

        # Update announcer text with current player and their current roll
        announcer_txt = f"Player {self.__players[self.__whose_turn].get_name()}" \
                        f" turn, they rolled {self.__last_roll}"
        # Add consonant warning to the announcer text if none are left.
        if self.__used_consonants == self.__phrase_consonants:
            consonant_warning = "\nNo more consonants! Only press one if " \
                                "you wish to pass your turn!"
            announcer_txt += consonant_warning
        self.__announcer.configure(text=announcer_txt)

    def check_character(self, char):
        """
        Check if string (character) <char> was a part of the solution
        <self.__phrase>. Return True if it was and False otherwise.

        :param char: string, character to be checked
        :return: boolean
        """

        # Return False if <char> was not part of the solution.
        if char not in self.__phrase:
            return False

        # Index for Label configuration via <self.__phrase_labels>.
        idx = 0

        # Loop through <self.__phrase> and configure corresponding Labels to
        # "reveal" the characters.
        for c in self.__phrase:
            if c == char:
                self.__phrase_labels[idx].configure(text=char)
            idx += 1
        # Return True since the guess was correct.
        return True

    def get_next_row(self):
        # Return next row for Tkinter grid indexing.
        self.__row_number += 1
        return self.__row_number

    def open_guess_screen(self):
        """
        Opens a separate window for the player to take a guess for the
        phrase. The phrase is entered into a Tkinter entry field and submitted
        via a button. The window is destroyed after the guess is taken. The
        parent window cannot be interacted with while pop-up is active.
        """

        def exit_window():
            """
            <guess_button> command function. Makes the guess all uppercase
            and checks if the answer was correct via <is_over>. Closes pop-up
            window.
            """
            guess = guess_entry.get().upper()
            self.is_over(guess)
            guess_win.destroy()
            guess_win.grab_release()

        # Create a secondary window for phrase guessing
        guess_win = Toplevel(self.__window)
        guess_win.grab_set()
        guess_win.title("Guess window")

        # Instruction label
        guess_label = Label(guess_win, text="Your guess: ")
        guess_label.pack(side=LEFT)

        # Guess text field
        guess_entry = Entry(guess_win)
        guess_entry.pack(side=LEFT)

        # Guess submission button
        guess_button = Button(guess_win, text="Guess!", command=exit_window)
        guess_button.pack(side=LEFT)

    def is_over(self, phrase):
        """
        Checks if game ends because of a submitted guess. If the phrase was
        correct ends the game by revealing the answer and congratulating the
        player. Also disables the on-screen keyboard.
        """
        # Check if guessed phrase was correct.
        if phrase == self.__phrase:
            # Update announcer text to announce the winner!
            announcer_text = f"Player " \
                             f"{self.__players[self.__whose_turn].get_name()}" \
                             f" wins with a score of " \
                             f"{self.__players[self.__whose_turn].get_score()}!" \
                             f"\n The phrase was {phrase}"
            self.__announcer.configure(text=announcer_text)

            # Disable all the buttons.
            for button in self.__buttons:
                button.configure(relief=SUNKEN, state="disabled")

            # Reveal all the letters in the phrase.
            for char in QWERTY:
                self.check_character(char)

        # Change turn if phrase was not correct.
        else:
            self.change_turn()

    def newgame(self):
        """
        Creates a new game quite crudely by destroying the main window and
        running the entire program again.
        """
        self.__window.destroy()
        self.__init__()

def main():
    Fortunegame()

if __name__ == "__main__":
    main()

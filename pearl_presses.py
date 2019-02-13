#!/usr/bin/python

"""Pearl Presses Game

Displays an LED sequence via the Touch pHAT and keeps track of how well the player can copy the
generated sequence.

"""

import os
import sys
import time
import random
import signal
import touchphat

# GLOBAL VARIABLES
MASTER_SEQUENCE = []
PLAYER_SEQUENCE = []
MIN_INPUT_INDEX = 1
MAX_INPUT_INDEX = 4
IS_ACCEPTING_INPUT = False
IS_PLAYING = False

# Prepare Game
touchphat.all_off()


@touchphat.on_release('Enter')
def start_game(event):
    """Starts game when Enter is pressed the first time

    Starts the game if the IS_PLAYING flag is false. All other Enter presses are ignored after
    IS_PLAYING has been set to true.

    """
    global IS_PLAYING

    if not IS_PLAYING:
        display_starting_animation()
        display_master_sequence()
        IS_PLAYING = True


@touchphat.on_release('Back')
def exit_game(event):
    """Exits game when Back is pressed

    Exits the game by signaling the process to stop.

    """
    signal_quit()


@touchphat.on_release(['A', 'B', 'C', 'D'])
def handle_presses(event):
    """Listens for presses during the game

    Listens for player to press buttons in the sequence when IS_ACCEPTING_INPUT flag is true and
    adds it to the player's sequence. Calls for sequence to be checked after each press. Presses
    will be ignored if IS_ACCEPTING_INPUT is false.

    Args:
        event: A touchphat led event.

    """
    global PLAYER_SEQUENCE

    if IS_ACCEPTING_INPUT:
        PLAYER_SEQUENCE.append(event.name)
        check_presses()


def check_presses():
    """Compares the master sequence to the player's sequence

    Checks if the player sequence is the same as the master sequence. If the player presses a
    button out of turn, the game is ended. If the player perfectly matches the master sequence,
    the game continues.

    """
    global IS_ACCEPTING_INPUT
    global PLAYER_SEQUENCE

    if PLAYER_SEQUENCE[-1] != MASTER_SEQUENCE[len(PLAYER_SEQUENCE) - 1]:
        game_over()
    elif len(PLAYER_SEQUENCE) == len(MASTER_SEQUENCE):
        IS_ACCEPTING_INPUT = False
        PLAYER_SEQUENCE = []
        display_master_sequence()


def display_instructions():
    print """
    Welcome to Pearl Presses!

    Watch as the Touch pHAT displays a sequence for you and try to repeat it.
    Each round, a new press will be added. Try to last as long as possible!

    To start, press ENTER (on the Touch pHAT).
    To quit at anytime, press BACK (on the Touch pHAT) or press CTRL+C (on your keyboard).
    """


def display_starting_animation():
    """Displays animatation at game start

    Lights up LEDs in an animation sequence to signal to the player that the game is about to 
    begin.

    """
    time.sleep(0.5)

    # TODO: Create an animation sequence to display
    # HINT: https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-touch-phat > Controlling the LEDs


def display_master_sequence():
    """Displays master sequence

    Calls for a new led and displays the current sequence for the player to repeat. Sets the
    IS_ACCEPTING_INPUT to true to allow the player to press buttons.

    """
    global IS_ACCEPTING_INPUT

    touchphat.all_off()
    generate_press()

    for led in MASTER_SEQUENCE:
        time.sleep(0.75)
        touchphat.led_on(led)
        time.sleep(0.25)
        touchphat.led_off(led)

    IS_ACCEPTING_INPUT = True


def generate_press():
    """Generate random led to display next

    Randomly selects a new led to add to the master sequence. The possible choices are determined
    by the MIN_INPUT_INDEX and MAX_INPUT_INDEX. Indices 0 (Back) and 5 (Enter) should be avoided to allow for
    starting and exiting the game.

    """
    global MASTER_SEQUENCE

    MASTER_SEQUENCE.append(touchphat.NAMES[random.randint(
        MIN_INPUT_INDEX, MAX_INPUT_INDEX)])


def game_over():
    print 'Oh no! That was the wrong button!'
    display_game_summary()
    signal_quit()


def display_game_summary():
    print 'Score: {}'.format(len(MASTER_SEQUENCE) - 1)

    # TODO: Display the master sequence and the player sequence for comparison
    # HINT: https://docs.python.org/2/library/string.html#string.join


def signal_quit():
    os.kill(os.getpid(), signal.SIGUSR1)


def handle_exit(sig, frame):
    print '\nThanks for playing!'
    sys.exit(0)


if __name__ == '__main__':
    # Set signal handlers
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGUSR1, handle_exit)

    # Start Game
    display_instructions()

    # Keep the python process running
    signal.pause()

#!/usr/bin/python

import os
import sys
import time
import signal
import random

import touchphat
touchphat.all_off()

MASTER_SEQUENCE = []
PLAYER_SEQUENCE = []
MIN_INPUT_INDEX = 1
MAX_INPUT_INDEX = 4
IS_ACCEPTING_INPUT = False
IS_PLAYING = False


@touchphat.on_release('Enter')
def handle_enter(event):
	global IS_PLAYING

	if not IS_PLAYING:
		display_starting_animation()
		display_master_sequence()
		IS_PLAYING = True


@touchphat.on_release('Back')
def handle_back(event):
	exit_game()

@touchphat.on_release(['A','B','C','D'])
def handle_presses(event):
	global IS_ACCEPTING_INPUT
	global PLAYER_SEQUENCE

	if IS_ACCEPTING_INPUT:
		PLAYER_SEQUENCE.append(event.name)

		if len(PLAYER_SEQUENCE) == len(MASTER_SEQUENCE):
			IS_ACCEPTING_INPUT = False

			if PLAYER_SEQUENCE == MASTER_SEQUENCE:
				PLAYER_SEQUENCE = []
				display_master_sequence()
			else:
				game_over()


def display_instructions():
	print '''
	Welcome to Pearl Presses!

	Watch as the Touch pHAT displays a sequence for you and try to repeat it.
	Each round, a new press will be added. Try to last as long as possible!

	To start, press ENTER (on the Touch pHAT).
	To quit at anytime, press BACK (on the Touch pHAT) or press CTRL+C (on your keyboard).
	'''

def display_starting_animation():
	time.sleep(0.5)
	for led in touchphat.NAMES:
		touchphat.led_on(led)
		time.sleep(0.1)
		touchphat.led_off(led)

	for i in range(3):
		touchphat.all_on()
		time.sleep(0.5)
		touchphat.all_off()
		time.sleep(0.5)

def display_master_sequence():
	global IS_ACCEPTING_INPUT

	generate_press()

	for led in MASTER_SEQUENCE:
		time.sleep(0.75)
		touchphat.led_on(led)
		time.sleep(0.25)
		touchphat.led_off(led)

	IS_ACCEPTING_INPUT = True

def display_game_summary():
	print 'Score: {}'.format(len(MASTER_SEQUENCE) - 1)
	print 'Master Presses: {}'.format(', '.join(MASTER_SEQUENCE))
	print 'Your Presses  : {}'.format(', '.join(PLAYER_SEQUENCE))

def generate_press():
	global MASTER_SEQUENCE

	MASTER_SEQUENCE.append(touchphat.NAMES[random.randint(MIN_INPUT_INDEX, MAX_INPUT_INDEX)])

def game_over():
	print 'Oh no! That was the wrong button!'
	display_game_summary()
	exit_game()

def exit_game():
	os.kill(os.getpid(), signal.SIGUSR1)

def handle_exit(sig, frame):
	print '\nThanks for playing!'
	sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGUSR1, handle_exit)

display_instructions()
signal.pause()
### This fork is no longer being supported and has been integrated into Extended Training Mode https://github.com/fangdreth/MBAACC-Extended-Training-Mode

# MBAACC_Training

This is a fork of Training Tool made for Melty Blood Actress Again Current Code developed by Kosunan.

Displays detailed information on frame data and character states, including position, frame advantage, and color coded state information frame by frame. 

Also provides easy access to saving and loading Game States to a press of a button.


# How to run it
1. Download MBAACC_Training.exe from the latest release from this link https://github.com/gonpgonp/MBAACC_Training/releases/latest

2. Run it.

3. Now just open the game and get inside the Training Mode. If the game was already open no need to restart.

# Info guide

## Main info
NOTE: The window size is adjustable horizontally and will likely not show everything by default.

(The window can also be resized vertically, but making it any smaller is glitchy and will cause a scroll bar to appear. To fix issues like this, toggle extra info on and then off again by pressing F7 twice)

The first row displays information for Player 1

	(x, y) position in absolute units
	(x, y) position in visual pixels (half the size of sprite and hitbox pixels)
	Current pattern [current state within that pattern]
	X speed in absolute units
	X acceleration in absolute units
	Y speed in absolute units
	Y acceleration in absolute units
	Health
	Magic Circuit
	Save state hotkey information
	
The second row displays information for Player 2 in the same order

The third row displays some extra information

	The distance between Player 1 and Player 2 in absolute units
	The distance between Player 1 and Player 2 in visual pixels
	Frame advantage (with positive being in Player 1's favor)

The fourth row is just headers to count the frame display below

The fifth row displays frame information for Player 1

	Black with dark letters = Fully actionable
	Black with bright letters = Fully actionable while opponent is not (advantage)
	Green = Not fully actionable (low priority)
	Dark Green = Actionable but unable to block
	Brown = Neutral Frame
	Greenish Brown = Neutral Frame but unable to block
	White = Invuln
	Light Yellow = Jump startup
	Dark Yellow = Clash
	Light Blue = Shield (does not work for some characters)
	Dark Blue = Hitstop
	Dark Gray = Blockstun
	Gray = Hitstun
	Light Gray = Being thrown
	Purple = EX Flash where the player who activated it still moves (e.g. Satsuki continues to wind her arm during 214C EX flash)
	Darkest Gray = EX Flash where neither player moves (most EX flashes; only visible during extra information)
	
	*While fully actionable or in neutral frame, the current pattern is displayed (or advantage if applicable)
	*While not fully actionable, the total duration of inactionability is displayed
	*While in hitstop, hitstun, or blockstun, the amount of remaining hitstun/untech time is displayed

The sixth row displays active frames in red, counting up or "^" if airborne. Underlines the active frames if both.

The seventh row displays projectile active frames in red and assist active frames in orange, counting the total number of hitboxes active.

The next three rows show the same information but for Player 2.

## Extra info
While extra info is displayed several more rows are added

The eleventh row displays information for Player 1

	The number of EX Flash frames remaining
	Guard Gauge [Guard Quality]
	Red Health
	Number of untech scaling hits [untech frames lost from hit count, untech frames lost from special hits (like 5A6AAs)]
	Partner's pattern [current state within that pattern] (Maids, KohaMech, NecoMech)

The twelfth row displays information for Player 2in the same order

The thirteenth row is another headers

The fourteenth row displays A and B presses (signified by the same color as seen in Training Mode's Input Display) and E presses ("E")

The fifteenth row displays C and D presses (same color scheme) and directional inputs (numpad notation except a dot for neutral). Underlined on the frame of crossups.

# Hotkeys

FN1 (in-game control bind which normally controls the dummy) or F2 (on your keyboard) will save the current state

FN2 (in-game control bind which normally resets training) or F6 (on your keyboard) will load the saved state

shift + 1, 2, or 3 will switch between different available save states

F1 will clear all saved states

shift + left or right will scroll through the frame display

F7 will display extra information, as well as disabling the frame display from pausing during hitstop or EX flashes

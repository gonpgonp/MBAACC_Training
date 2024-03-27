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
The first row displays information for Player 1

	1. (x, y) position in absolute units
	2. (x, y) position in visual pixels (half the size of sprite and hitbox pixels)
	3. Current pattern [current state within that pattern]
	4. X speed in absolute units
	5. X acceleration in absolute units
	6. Y speed in absolute units
	7. Y acceleration in absolute units
	8. Health
	9. Magic Circuit
	10. Save state hotkey information
	
The second row displays information for Player 2 in the same order

The third row displays some extra information

	1. The distance between Player 1 and Player 2 in absolute units
	2. The distance between Player 1 and Player 2 in visual pixels
	3. Frame advantage (with positive being in Player 1's favor)

The fourth row is just headers to count the frame display below

The fifth row displays frame information for Player 1

	1. Green = Not fully actionable (low priority)
	2. White = Invuln
	3. Light Yellow = Jump startup
	4. Dark Yellow = Clash
	5. Light Blue = Shield (does not work for some characters)
	6. Dark Blue = Hitstop
	7. Dark Gray = Blockstun
	8. Gray = Hitstun
	9. Light Gray = Being thrown
	10. Brown = Neutral Frame
	11. Black with dark letters = Fully actionable
	12. Black with bright letters = Fully actionable while opponent is not (advantage)
	13. Purple = EX Flash where the player who activated it still moves (e.g. Satsuki continues to wind her arm during 214C EX flash)
	14. Darkest Gray = EX Flash where neither player moves (most EX flashes; only visible during extra information)
	
	*While fully actionable or in neutral frame, the current pattern is displayed (or advantage if applicable)
	*While not fully actionable, the total duration of inactionability is displayed
	*While in hitstop, hitstun, or blockstun, the amount of remaining hitstun/untech time is displayed

The sixth row displays active frames in red, counting up or "^" if airborne. Underlines the active frames if both.

The seventh row displays projectile active frames in red and assist active frames in orange, counting the total number of hitboxes active.

The next three rows show the same information but for Player 2.

## Extra info
While extra info is displayed several more rows are added

The eleventh row displays information for Player 1

	1. The number of EX Flash frames remaining
	2. Guard Gauge [Guard Quality]
	3. Red Health
	4. Number of untech scaling hits [untech frames lost from hit count, untech frames lost from special hits (like 5A6AAs)]
	5. Partner's pattern [current state within that pattern] (Maids, KohaMech, NecoMech)

The twelfth row displays information for Player 2in the same order

The thirteenth row is another headers

The fourteenth row displays A and B presses (signified by the same color as seen in Training Mode's Input Display) and E presses ("E")

The fifteenth row displays C and D presses (same color scheme) and directional inputs (numpad notation except a dot for neutral). Underlined on the frame of crossups.

# Hotkeys

1. FN1 (in-game control bind which normally controls the dummy) or F2 (on your keyboard) will save the current state

2. FN2 (in-game control bind which normally resets training) or F6 (on your keyboard) will load the saved state

3. shift + 1, 2, or 3 will switch between different available save states

4. F1 will clear all saved states

5. shift + left, or right will scroll through the frame display

6. F7 will display extra information, as well as disabling the frame display from pausing during hitstop or EX flashes.

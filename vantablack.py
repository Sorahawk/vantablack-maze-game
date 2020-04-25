import sys
from levelclass import *

def detect_running_idle():
	if ("idlelib" in sys.modules) == False:
		# I faced an issue with getting Windows CMD to print out the Unicode symbols properly and could not fix it
		# I decided that even if I could fix it on my end, on players' end it might probably still have error too
		# Therefore the practical solution at this point would be to redirect players to use IDLE instead
		line1 = '\nNot running the game in IDLE might might lead to some display issues while running the game.'\
				'\n\nFor the best experience, please run the game using Python IDLE.'\
				'\n\nPlease right-click on this script ({}), select "Edit from IDLE", then press F5 to run.'\
				'\n\nPress Enter to proceed.'.format(name_of_file)
		input(line1)  # pause the program to allow players to read above instructions


def verify_integer_input(integerChoice, listOptions):  # listOptions is list of available integer (as string) choices on menu screens
	if integerChoice.isdigit():
		if int(integerChoice) in listOptions:
			return True
	return False


def verify_direction_input(dirn_inp):
	if dirn_inp.isalpha():
		valid = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}

		dirn_inp = dirn_inp.lower()

		if dirn_inp in valid:
			return valid[dirn_inp]

	print("Invalid input detected.\nEnter 'W' to go Up, 'S' to go Down, 'A' to go Left or 'D' to go Right\n")
	return False  # invalid directional input


def write_new_score_file():
	f = open('vantablack_highscores.txt', 'w')

	for level in range(len(available_levels)):
		f.write('5,Apple,3,Bob,0,Candy\n')  # Template high scores for each level

	f.close()


def try_read_score_file():
	try:
		f = open('vantablack_highscores.txt', 'r+')
	except IOError:
		write_new_score_file()  # write a new template highscores file
		f = open('vantablack_highscores.txt', 'r+')

	scores = f.readlines()
	f.close()

	return scores


def verify_unlocked(scores, num_turns_unlock):
	top_score = int(scores.split(',')[0])
	return True if top_score >= num_turns_unlock else False


def find_highest_unlocked_level(scores):
	level_unlocked = 0

	while level_unlocked < len(available_levels) - 1:
		score_unlock_next = available_levels[level_unlocked][2]  # score required to unlock next level, set by me

		if verify_unlocked(scores[level_unlocked], score_unlock_next):
			level_unlocked += 1
		else:  # next level not unlocked, stop at current value of level_unlocked
			break

	return level_unlocked


def select_level(num_levels_unlocked):
	num_levels_unlocked += 1

	line1 = '\n{}There are {} levels unlocked!\n'.format(divider, num_levels_unlocked)
	print(line1)

	for level_num in range(1, num_levels_unlocked + 1):
		print('{}) Level {}'.format(level_num, level_num))

	level_choice = None
	while not level_choice:
		level_choice = input('\nPlease choose a level: ')

		if not verify_integer_input(level_choice, range(1, num_levels_unlocked + 1)):
			print('Invalid input detected. Please enter an integer to choose an unlocked level.')
			level_choice = None

	return int(level_choice) - 1


def get_player_name(high_score):
	player_name = None
	while not player_name:
		player_name = input('\n\n\nYou have earned a place in the Hall of Fame with your score of {}!\nPlease enter your name: '.format(high_score))

		if not player_name.isalnum() or len(player_name) > 15:  # highscore name should only contain alphanumeric characters
			print('Invalid input detected. A maximum of 15 alphanumeric characters are accepted.')
			player_name = None

	return player_name


def update_high_score(new_score, level_scores):
	# receives single line of top 3 highscores and new score, check if new score is a high score
	values = level_scores.split(',')

	for index in (0, 2, 4):  # length of high scores is fixed because there will always be only top 3
		current_score = int(values[index])

		if new_score < current_score:
			pass
		else:
			score_index = index
			name_index = index + 1

			if new_score == current_score:
				if index == 4:  # if same score as 3rd highest score, won't be added to high score
					break
				else:
					score_index += 2  # first come first serve, so shift it behind the older score
					name_index += 2

			# get player name
			player_name = get_player_name(new_score)

			values.insert(score_index, str(new_score))
			values.insert(name_index, player_name)
			break

	if len(values) > 6:
		values = values[0:6]

	return ','.join(values)


def main_menu(first_run=False):
	if first_run:
		detect_running_idle()

	line1 = '\n{}Welcome to Vantablack!\n\n1) Start Game\n2) How to Play\n3) Hall of Fame\n4) Settings\n5) Quit Game'.format(divider)
	print(line1)

	option_choice = None

	while not option_choice:
		option_choice = input('\nSelect an option: ')

		if not verify_integer_input(option_choice, (1, 2, 3, 4, 5)):
			print('Invalid input detected. Please select an option to proceed.')
			option_choice = None

	option_choice = int(option_choice)

	if option_choice == 1:
		start_game()
	elif option_choice == 2:
		how_play()
	elif option_choice == 3:
		hall_fame()
	elif option_choice == 4:
		settings()
	elif option_choice == 5:
		quit_game()


def how_play():
	line1 = "\n{}Your goal is to find the door before your moves run out.\nThe maze is pitch black, so you can only see the spaces adjacent to you."\
			"\n\n\nAlong the way, you might run into traps, or find artifacts!"\
			"\n\n\nHowever, beware the Vantablack Horror. You can run, but it'll chase you.\nIf you fight it, it'll take many moves to kill, so choose wisely!"\
			"\n\n\nWith that, you are ready to take on the maze! Good luck.".format(divider)
	print(line1)

	input('\n\nPress Enter to begin.')
	start_game()


def hall_fame():
	scores = try_read_score_file()
	
	line1 = '\n{}Hall of Fame\n'.format(divider)
	print(line1)

	score_display = []
	level_unlocked = find_highest_unlocked_level(scores)

	for level in range(level_unlocked + 1):
		level_name_string = 'Level {}'.format(level + 1)
		if level == level_unlocked and level < len(available_levels) - 1:
			level_name_string += ' ({} to unlock next level)'.format(available_levels[level][2])

		temp_list = [level_name_string]
		level_scores = scores[level].split(',')

		for index in (0, 2, 4):
			temp_list.append('{}  -  {}'.format(level_scores[index], level_scores[index + 1].strip()))

		score_display.append(temp_list)

	for line in range(4):
		for level in score_display:
			print('{:<30}'.format(level[line]), end='')
		print()

	input('\n\nPress Enter to proceed back to Main Menu.')
	main_menu()


def settings():
	line1 = '\n{}Settings:\n\n1) Reset All Progress (High Scores and Level Unlocks)\n2) Return to Main Menu'.format(divider)
	print(line1)

	option_choice = None

	while not option_choice:
		option_choice = input('\nSelect an option: ')

		if not verify_integer_input(option_choice, (1, 2)):
			print('Invalid input detected. Please select an option to proceed.')
			option_choice = None

	option_choice = int(option_choice)

	if option_choice == 1:
		reset_progress()
	elif option_choice == 2:
		main_menu()


def reset_progress():
	write_new_score_file()
	
	line1 = '\n{}Progress wiped succesfully.'.format(divider)
	print(line1)

	input('\n\nPress Enter to proceed back to Main Menu.')
	main_menu()


def quit_game():
	print('\n{}Thanks for playing!'.format(divider))
	sys.exit()


##############################################################################################################################


def start_game():
	scores = try_read_score_file()
	level_unlocked = find_highest_unlocked_level(scores)

	# let player choose level from unlocked levels if second level or further is unlocked
	if level_unlocked > 0:
		level_selected = select_level(level_unlocked)
	else:
		level_selected = level_unlocked

	# load selected level
	level_contents = available_levels[level_selected]
	chosen_gridmap = level_contents[0]
	level_num_traps = level_contents[1]
	max_num_turns = level_contents[3]
	level_high_score = int(scores[level_selected].split(',')[0])

	# initialise Level object
	running_level = Level(chosen_gridmap, level_num_traps, max_num_turns)
	running_level.start_level()

	while not running_level.completed and running_level.turn_counter > 0:
		print('\n{}'.format(divider))
		running_level.display_new_turn(level_selected, level_high_score)

		dirn = None

		while not dirn:
			dirn_inp = input('\n\nDirection to proceed (W / A / S / D): ')
			dirn = verify_direction_input(dirn_inp)

			if dirn:
				valid_move = running_level.move_player(dirn)

				if valid_move == 'Wall':
					print("There's a wall in your way!\n")
					dirn = None

		if running_level.monster != None:
			running_level.move_monster()

	if running_level.completed:  # reached the door
		current_score = running_level.turn_counter
		print('\n{}You completed Level {} with a score of {}!'.format(divider, level_selected + 1, current_score))

		# function will return a new string if there is a new high score, otherwise old scores will just be written back to the file
		new_level_scores = update_high_score(current_score, scores[level_selected])

		scores[level_selected] = new_level_scores + '\n'

		f = open('vantablack_highscores.txt', 'w')

		for line in scores:
			f.write(line)

		f.close()

		score_unlock_next = available_levels[level_selected][2]

		if level_selected == level_unlocked and level_selected < len(available_levels) - 1:
			if current_score < score_unlock_next:
				print("\n{}You'll need a score of at least {} to unlock the next level.".format(divider, score_unlock_next))
			else:
				print("\n{}You've unlocked the next level! Try it now!".format(divider))
	elif running_level.turn_counter <= 0:  # ran out of turns
		print('\n{}You failed to complete Level {} within {} moves.'.format(divider, level_selected + 1, max_num_turns))

	replay_choice = input("\n\n\n\n\nEnter 'P' to play again or 'R' to return to the Main Menu,\notherwise press Enter to quit the game. ")

	if replay_choice.lower() == 'p':
		start_game()
	elif replay_choice.lower() == 'r':
		main_menu()
	else:
		quit_game()



# Sorahawk
# Each level is designed on paper and converted into this gridmap format
level1_gridmap = [['3b', '2b', '2d', '2b', '2b', '3t', '2b'],\
				['1b', '2b', '2b', '2b', '0b', '3b', '0b'],\
				['3t', '1b', '0b', '2b', '2b', '0b', '1b'],\
				['1b', '0b', '1b', '2m', '1b', '1p', '1b']]

level2_gridmap = [['3b', '2b', '2b', '2d'],\
				['1b', '0b', '0m', '0b'],\
				['1b', '0b', '0b', '0b'],\
				['1p', '0b', '0b', '0b']]

level3_gridmap = [['3b', '2b', '2b', '3b', '2b', '3b', '2b', '2b', '3d', '2b'],\
				['1b', '3b', '1b', '2b', '1b', '0b', '2b', '1t', '3b', '0b'],\
				['1p', '0b', '2b', '0b', '0b', '2b', '1b', '2m', '0b', '3b'],\
				['1b', '3b', '0b', '3b', '0b', '1b', '1b', '1b', '2b', '0b'],\
				['1b', '0b', '2b', '1b', '2b', '2b', '0b', '1b', '2b', '2t']]


available_levels = [(level1_gridmap, 3, 25, 40), (level2_gridmap, 3, 13, 20), (level3_gridmap, 5, 35, 50)]  # (gridmap, num traps, score to unlock next, number of moves given)

divider = '-' * 50 + '\n' * 25
name_of_file = 'vantablack.py'

# run main menu
main_menu(True)

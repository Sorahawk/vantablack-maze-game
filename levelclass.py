import random
import numpy as np
from cellclass import *
from monsterstateclass import *

class Level:
	icon_reference = {None: u'\u2bc0', 'Door': u'\u2a4e', 'Monster': u'\u2623', 'Player': u'\u26f9', 'Trap': u'\u26a0', 'Treasure': u'\u23f1'}
	player, previous_player = None, None  # initialise variables to store player cell and previous player position
	monster, monster_trapped, monster_state = None, False, MonsterState()  # initialise variables to store monster cell and monster state
	completed = False

	def __init__(self, gridmap, num_traps, max_turns):
		# gridmap is the map layout of the level in the form of 2D numpy array
		gridmap = np.array(gridmap)  # convert gridmap list to np.array
		self.gridmap = gridmap
		self.num_traps = num_traps
		self.turn_counter = max_turns

		self.num_rows = gridmap.shape[0]
		self.num_cols = gridmap.shape[1]
		
		self.toprow = '{}{}{}'.format(u'\u231c', u'  -  ' * self.num_cols, u'\u231d')
		self.botrow = '{}{}{}'.format(u'\u231e', u'  -  ' * self.num_cols, u'\u231f')


	def generate_cells(self):
		occupant_reference = {'b': None, 'd': 'Door', 'm': 'Monster', 'p': 'Player', 't': 'Treasure'}

		self.cellmap = np.zeros(self.gridmap.shape, dtype='object')  # initialise new numpy array to store the Cells

		for row in range(self.num_rows):
			for col in range(self.num_cols):
				code = self.gridmap[row, col]

				 # wall_state are my reference codes for whether that cell has left and/or top walls, which determines if the cell will be linked to its corresponding neighbours
				 # 0 means no wall to the left or on top, 1 means left wall, 2 means top wall and 3 means both walls
				wall_state = int(code[0])

				occupant = code[1]

				cell = Cell()

				if occupant == 'p':
					player_row = row
					player_col = col
				else:
					cell.add_occupant(occupant_reference[occupant])

				if occupant == 'm':
					self.monster = cell

				# link neighbouring cells
				if wall_state == 0 or wall_state == 2:
					cell.add_neighbour_horizontal(self.cellmap[row, col - 1])
				if wall_state == 0 or wall_state == 1:
					cell.add_neighbour_vertical(self.cellmap[row - 1, col])

				self.cellmap[row, col] = cell  # store cell in corresponding slot in cellmap

		# add player to appropriate cell after generate the full cellmap because if it is added midway when half the cell network is instantiated,
		# the linkages are not formed yet (especially the bottom neighbour)
		self.player = self.cellmap[player_row, player_col]
		self.player.add_occupant('Player')

		# start monster_state object
		self.monster_state.start()


	def spawn_traps(self):
		while self.num_traps > 0:
			# pick random cell to check if it is occupied by special object
			rand_row = random.randrange(self.num_rows)
			rand_cell = np.random.choice(self.cellmap[rand_row])

			if not rand_cell.is_occupied() and not rand_cell.display:  # latter condition is so that traps will not spawn right beside the player's starting position
				rand_cell.add_occupant('Trap')
				self.num_traps -= 1


	def start_level(self):
		self.generate_cells()
		self.spawn_traps()


	def display_cell_linkage(self):  # testing function to confirm cell linkages correctly matches planned map design
		for row in range(self.num_rows):
			for col in range(self.num_cols):
				cell = self.cellmap[row, col]
				icon = self.icon_reference[cell.occupant]
				print(' {}'.format(icon), end='')

				if cell.up:
					print('|', end='')
				if cell.right:
					print('-', end='')
			print()


	def display_full_map(self):  # testing function to see if entire map matches planned design
		print(self.toprow)

		for row in range(self.num_rows):
			print('|', end='')

			for col in range(self.num_cols):
				cell = self.cellmap[row, col]
				icon = self.icon_reference[cell.occupant]
				print('{}'.format(icon), end='')

			print('|')
		print(self.botrow)


	def display_player(self):
		print(self.toprow)

		for row in range(self.num_rows):
			print('|', end='')

			for col in range(self.num_cols):
				cell = self.cellmap[row, col]

				if not cell.display:
					print(u'     ', end='')
				else:
					icon = self.icon_reference[cell.occupant]
					print('   \u202f{}'.format(icon), end='')

			print('|')
		print(self.botrow)


	def display_turn_counter(self, level_selected, level_high_score):
		line1 = 'Level {}\n\nNumber of moves left: {}\tHigh Score: {}\n'.format(level_selected + 1, self.turn_counter, level_high_score)
		print(line1)


	def display_symbols_legend(self):
		line1 = u"\nIcon Reference\n\n\u202f\u26f9: The player. That's you!\n\u202f\u2bc0: Nothing special. Adjacent space.\n\u202f\u2a4e: The exit. Find this!"\
		"\n\u23f1: Chrono Artifact!  +5 moves.\n\u202f\u26a0: It's a trap!  -3 moves."\
		"\n\u202f\u2623: The Vantablack Horror.  -15 moves.\n    It'll chase you for a while if you run.\n\n\n"

		print(line1)


	def display_new_turn(self, level_selected, level_high_score):
		self.display_symbols_legend()
		self.display_turn_counter(level_selected, level_high_score)
		self.display_player()


	def move_player(self, dirn):
		turn_modifiers = {None: 0, 'Monster': -14, 'Trap': -2, 'Treasure': +6}

		neighbour, encountered = self.player.move_occupant_dirn(dirn)

		if not neighbour:  # no neighbouring cell due to wall
			return 'Wall'

		self.previous_player = self.player
		self.player = neighbour
		self.turn_counter -= 1

		if encountered == 'Door':
			self.completed = True
			return
		elif encountered == 'Monster':
			self.monster = None

		change = turn_modifiers[encountered]
		self.turn_counter += change

		return change


	def move_monster(self):
		if self.monster_trapped:
			state_input = 1
			self.monster_trapped = False
		else:
			neighbourList = self.monster.get_neighbours()

			for neighbour in neighbourList:
				if neighbour == self.player:
					state_input = 1
					break
				elif neighbour == self.previous_player:
					state_input = 2
					break
				else:
					if neighbour.occupant == 'Door':  # do not allow monster to move on to door cell
						neighbourList.remove(neighbour)
					
					state_input = 0

		movement_type = self.monster_state.step(state_input)

		if movement_type == 0:  # do not move for one turn
			return
		elif movement_type == 1:  # move randomly
			next_cell = np.random.choice(neighbourList)
		elif movement_type == 2:  # follow player
			next_cell = self.previous_player

		neighbour, encountered = self.monster.move_occupant_reference(next_cell)

		if not neighbour:
			# technically should be a redundant catch case but I encountered a bug where the monster ate the player (which should not be able to happen),
			# causing the player to disappear yet self.player remained and could still see the last position of player and the adjacent cells but could not move anymore
			# either way, could not reproduce the bug again so I added this in which is my best guess at catching the bug.
			return
		else:
			self.monster = neighbour

			if encountered == 'Trap':
				self.monster_trapped = True

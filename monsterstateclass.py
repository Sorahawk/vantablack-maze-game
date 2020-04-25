from libdw import sm

class MonsterState(sm.SM):
	start_state = 'wandering'  # default state of monster is moving randomly
	track_timer = 2

	def get_next_values(self, state, inp):
		if state == 'wandering':
			if inp == 0:  # nothing special
				return 'wandering', 1  # default movement type 1 - wandering
			elif inp == 1:  # either stepped on trap or met a player
				return 'pausing', 0  # movement type 0 - not moving
			elif inp == 2: 
				return 'tracking', 2  # movement type 2 - following player
		elif state == 'pausing':
			if inp == 0:
				return 'wandering', 1
			elif inp == 1:
				return 'pausing', 0
			elif inp == 2:
				return 'tracking', 2
		elif state == 'tracking':
			if self.track_timer == 0:  # timer to stop tracking player over
				self.track_timer = 2
				return 'pausing', 0  # pause another turn before going back to default wandering
			else:
				self.track_timer -= 1
				return 'tracking', 2  # continue following player

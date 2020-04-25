class Cell:
	left, right, up, down = [None for x in range(4)]  #initialise neighbouring cells
	occupant = None
	display = False

	def add_neighbour_horizontal(self, other):
		self.left = other
		other.right = self


	def add_neighbour_vertical(self, other):
		self.up = other
		other.down = self


	def get_neighbours(self):
		directions = ['left', 'right', 'up', 'down']
		neighbourList = []

		for dirn in directions:
			neighbour = getattr(self, dirn)
			
			if neighbour:
				neighbourList.append(neighbour)

		return neighbourList


	def is_occupied(self):
		return True if self.occupant else False


	def add_occupant(self, occupant):
		if occupant == 'Player':  # change self.display for current cell and linked cells to True
			self.display_on()

		self.occupant = occupant


	def rem_occupant(self):
		if self.occupant == 'Player':
			self.display_off()

		self.occupant = None


	def move_occupant_dirn(self, dirn):
		other = getattr(self, dirn)  # get corresponding neighbouring cell based on dirn input

		if not other:  # no neighbouring cell in that direction due to wall
			return None, None
		
		occupant = self.occupant
		encountered = other.occupant

		self.rem_occupant()
		other.add_occupant(occupant)

		return other, encountered  # return new cell and item that player has encountered


	def move_occupant_reference(self, other):
		occupant = self.occupant
		encountered = other.occupant

		if occupant == 'Player':
			return None, None

		self.rem_occupant()
		other.add_occupant(occupant)

		return other, encountered  # return item that monster encountered


	def display_on(self):
		# turn self.display to True for current and linked cells
		self.display = True

		neighbourList = self.get_neighbours()

		for neighbour in neighbourList:
			neighbour.display = True


	def display_off(self):
		# reverse of display_on()
		self.display = False

		neighbourList = self.get_neighbours()

		for neighbour in neighbourList:
			neighbour.display = False

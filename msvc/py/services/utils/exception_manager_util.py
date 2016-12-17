
########################################################
# Exception when data in db is empty.
########################################################
class EmptyData(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
class UserInput:
	# when generated will ask a question of the user and check the type of their response
	def __init__(self, question, type):
		type_dict = {"str": (lambda x: str(x)), "int": (lambda x: int(x)), "float": (lambda x: float(x))}
		while True:
			try:
				self.answer = type_dict[type](input('%s\t' % question))	# trys to convert the answer into the correct type
				break								# break if successful
			except ValueError:
				print("Please use correct type of value (string or number).")	# if not succesful, ask again

	def return_answer(self):
		# returns the user's answer
		return self.answer

	def is_affirmative(self):
		if self.answer.lower() in ['y', 'yes', 'affirmative']:
			return True



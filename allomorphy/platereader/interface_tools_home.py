class Menu:
	# contains options attahced to functions or objects
	def __init__(self, name, options_list, session=None, option_function_pairs=True):
		# creates a menu which is displayed on the shell
		# options_list should contain small lists of ['menu title', actual_function/object]...
		# or it should just contain single entries, not tuples or lists. This is the 'option_function_pairs' boolean.
		self.option_function_pairs = option_function_pairs
		print(self.option_function_pairs)
		self.options = {}
		self.name = name
		self.session = session
		option_count = 1
		for option in options_list:
			self.options[option_count] = option
			option_count += 1
		self.no_options = False

	def display(self):
		# displays the menu on the shell and returns the response, be that a function or object
		if len(self.options.keys()) != 0:
			print('\n\n%s\n\n' % self.name)

			if self.option_function_pairs == True:				# checks whether we have {option: [small list]} 
											# or {option: thing}
				for number, option in self.options.items():		
					print('%s\t%s\n' % (number, option[0]))
				self.response =(UserInput("Select an option", 'int').return_answer())
				try:
					self.options[self.response][1]()
				except KeyError:					# checks it was a valid option
					print("Enter a valid option.")
				except TypeError:					# catches if the option is not a function but an object
					return self.options[self.response][1]	
				except AttributeError:					# similar to above
					return self.options[self.response][1]

			else:
				for number, option in self.options.items():
					print("%s\t%s\n" % (number, option))
				self.response =(UserInput("Select an option", 'int').return_answer())
				try:
					self.options[self.response]()
				except KeyError:					# checks it was a valid option
					print("Enter a valid option.")
				except TypeError:					# catches if the option is not a function but an object
					return self.options[self.response]	
				except AttributeError:					# similar to above
					return self.options[self.response]
		else:
			print("\nNo available options\n")
			self.no_options = True
			hang = input()

	def refresh(self, options_list):
		self.__init__(self.name, options_list, self.session, option_function_pairs=self.option_function_pairs)


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

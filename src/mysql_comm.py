python_command_prefix = '<python>'
mysql_command_prefix = '<mysql>'

def output_print(output) : 
	# print(output)
	for row in output : 
		for element in row : 
			if element == None : 
				element = 'Null'
			print('| ' + str(element))
			if len(row) != 1 : 
				print('\n')

def run_mysql_command(cursor, command_string, print_output=True) :
	try : 
		cursor.execute(command_string)
	except Exception as e : 
		print(e[1])
		return 'error'

	output = cursor.fetchall()
	if print_output == True : 
		output_print(output)
	else : 
		return output

def decode_command(cursor, command_string, print_output=True) : 

	def confirm_last_character(string, required_character) : 
		'''
		returns True if the last character of the string (excluding spaces)
		is the required_character, else returns False
		'''
		for i in range(len(string)) : 
			if string[len(string) - i - 1] == ' ' : 
				pass
			else : 
				if string[len(string) - i - 1] == required_character : 
					return True
				else : 
					return False  

	def find_ending_paran(string) : 
		'''
		accepts a string of the form "(... () (...(...)...)() ...)..()"
		and finds the first closing paran for the first opening paran
		returns the index of the closing paran to the first opering paran
		'''	
		paran_count = 0
		first_paran_encountered = False
		for i in range(len(string)) :
			character = string[i] 
			if character == '(' : 
				paran_count += 1
				if paran_count == 1 :
					first_paran_encountered = True
			elif character == ')' : 
				paran_count -= 1 
				if paran_count == 0 and first_paran_encountered == True : 
					return i
		raise RuntimeError('no closing paran found')

	def is_blank(string) : 
		'''
		returns True if the string is empty or only contains spaces
		else returns False
		'''
		if len(string) == 0 : 
			return True
		else : 
			for element in string : 
				if element != ' ' : 
					return False
			return True

	def count_character_in_string(string, character) : 
		count = 0 
		if len(string) == 0 : 
			return 0 
		else : 
			for element in string : 
				if element == character : 
					count += 1
			return count

	a = command_string.split(mysql_command_prefix)
	b = []
	for element in a : 
		b.extend(element.split('('))
	c = []
	for element in b : 
		if is_blank(element) : 
			c.append('(')
		else : 
			c.append(element)

	# check if the command entered was in the correct format
	for i in range(len(c)) : 
		if i%2 == 0 : 
			# even index
			pass
		else : 
			# odd index
			try : 
				if c[i] == '(' and (count_character_in_string('(' + c[i+1], '(') == count_character_in_string('(' + c[i+1], ')')) : 
					pass
				else : 
					raise SyntaxError('syntax error in command : ' + command_string + ' : did you miss an opening or closing paran?')
			except IndexError : 
				raise SyntaxError('syntax error in command : ' + command_string + ' : did you miss an opening or closing paran?')

	# the format of the entered command is correct
	d = []
	i = 0
	while i < len(c) : 
		if c[i] == '(' : 
			index_of_ending_paran = find_ending_paran('(' + c[i+1]) - 1 
			d.append('(' + c[i+1][:index_of_ending_paran] + ')')
			if index_of_ending_paran == len(c[i+1]) - 1 : 
				# nothing after the ending param
				d.append('')
			else : 
				d.append(c[i+1][index_of_ending_paran+1:])
			i += 1
		else : 
			d.append(c[i])
		i += 1

	# finally, run the mysql commands
	e = []
	for element in d : 
		if element[0] == '(' and element[-1] == ')' : 
			# is a mysql command
			mysql_command_output = run_mysql_command(cursor, element[1:-1], print_output = False)
			if mysql_command_output == 'error' : 
				raise RuntimeError('could not run mysql command ' + element[1:-1])
			mysql_command_output_string = '['
			for row in mysql_command_output : 
				# for element in row : 
				# 	mysql_command_output_string += str(element) + ' '
				# mysql_command_output_string += '\\n'
				mysql_command_output_string += str(row) + ','
			mysql_command_output_string = mysql_command_output_string[:-1] + ']'
			e.append(mysql_command_output_string)
		else : 
			e.append(element)

	# finally, run the python command
	command_string = ''
	for element in e : 
		command_string += element
	return command_string


def get_command(cursor, command_string, print_output=True) : 	
	'''
	possible forms of commands : 
		show databases; 	# simple mysql command
		python_command_prefix a = 10; 	# simple python command
		python_command_prefix a = (mysql_command_prefix show databases;)	# complex command
		python_command_prefix a = [(mysql_command_prefix show databases;), (mysql_command_prefix select if from x;)] 
		# more than one mysql commands possible, the only requirement is that 
		# each mysql command follow the syntax '(mysql_command_prefix ...)'
	'''
	if command_string == '' : 
		return
	
	if python_command_prefix not in command_string : 
		# simple mysql command
		return 'mysql_comm.run_mysql_command(cursor, ' + '"' + command_string + '"' + ', print_output=' + str(print_output) + ')'
		run_mysql_command(cursor, command_string, print_output=print_output)

	else : 
		# only one python_command_prefix needs to be in the command string, that
		# too only in the very beginning of the command string. 
		# hence, it is assured that 'command_string.split(python_command_prefix)'
		# command will produce a list with length 2, the first element
		# of which will be an empty string, or a string with spaces
		command_string = command_string.split(python_command_prefix)[1]

		# removing the preceedding spaces, which lead to indentation error when 
		# executing the 'exec' command
		new_command_string = ''
		flag = False
		for element in command_string : 
			if element == ' ' :
				if flag == False : 
					pass
				else : 
					new_command_string += element
			else : 
				new_command_string += element
				if flag == False : 
					flag = True
		command_string = new_command_string

		if mysql_command_prefix not in command_string :
			# simple python command
			return command_string
		else : 
			return decode_command(cursor, command_string)
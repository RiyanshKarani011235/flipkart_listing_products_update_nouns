#!/usr/bin/python

import sys
import MySQLdb
import mysql_comm

if len(sys.argv) == 1 : 
	mysql_terminal = MySQLdb.connect('localhost')
else :
	mysql_terminal = MySQLdb.connect(sys.argv[1])
cursor = mysql_terminal.cursor()	

while True : 
	print_output = False
	command = str(raw_input('mysql> '))
	if(command == '') : 
		pass
	elif mysql_comm.python_command_prefix in command : 
		while len(command) == 0 or command[-1] != ';' : 
			command += '\n'
			command += str(raw_input('    -> '))
		command_to_run = mysql_comm.get_command(cursor, command, print_output = print_output)
		try : 
			exec(command_to_run)
		except Exception as e : 
			print(e)
		# exec(command_to_run)
	else : 
		while len(command) == 0 or command[-1] != ';' : 
			command += ' '
			command += str(raw_input('    -> '))
		if mysql_comm.python_command_prefix not in command : 
			print_output = True	
		command_to_run = mysql_comm.get_command(cursor, command, print_output = print_output)
		try : 
			exec(command_to_run)
		except Exception as e : 
			print(e)
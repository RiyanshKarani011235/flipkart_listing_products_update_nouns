from __future__ import print_function
import sys, os
import MySQLdb
import mysql_comm
import json
import time
import unicodedata
import __init__
from utils import run_command_and_get_output, write_to_output

working_directory = __init__.working_directory
database_name = __init__.database_name
table_name = __init__.table_name

number_of_products = 740826729		# for the flipkart_listing_products_table

####################
# FILE DECLARATIONS
####################

nouns_file = working_directory + "data/nouns.txt"
nouns_synonyms_file = working_directory + "data/noun_synonyms.txt"
logs_file = working_directory + "data/logs.txt"
temp_file = working_directory + 'temp/temp.txt'
output_file = working_directory + 'temp/output.txt'

############################################
# INITIALIZING CONNECTION WITH MYSQL SERVER
############################################

# before initiating this part, make sure that the mysqldb server is running
# and the database is loaded as the name "t

if len(sys.argv) == 1 : 
	mysql_terminal = MySQLdb.connect('localhost')
else :
	mysql_terminal = MySQLdb.connect(sys.argv[1])
cursor = mysql_terminal.cursor()

mysql_comm.run_mysql_command(cursor, 'USE ' + database_name)
mysql_comm.run_mysql_command(cursor, 'SHOW TABLES')


#####################################################################
# CALCULATING NUMBER OF ROWS IN THE "flipkart_listing_products" TABLE
#####################################################################

# uncomment the part below if you don't know the number of rows in the table
# (keeping in mind that it might take a considerable amount of time to do so
# for a large table)
# for the convenience, this has already been done once and is stored as 
# number_of_products = 740826729

# print('calculating the number of rows in the table ...')
# number_of_products = int(mysql_comm.run_mysql_command(cursor, 'SELECT COUNT(*) FROM flipkart_listing_products', print_output=False))
# print('\tnumber of rows --> ' + number_of_products)

def remove_file(filename, supress_output=False) : 
	try : 
		os.remove(filename)
	except OSError as e : 
		if not supress_output : 
			print(e)

def load_data() : 
	'''
	stores breadcrumbs, urls and corresponding id's for products without nouns
	in breadcrumbs_file, urls_file and ids_file respectively
	
	:expects: 
		None
	:returns:
		None
	'''

	print("Log : load_data : started")
	####################
	# FILE DECLARATIONS
	####################

	# store in a location where it can be accessed the fastest
	incorrect_nouns_mysql_output_file = working_directory + 'data/incorrect_nouns/mysql_output.txt'	# temporary file used to store
																									# the output of an sql query

	incorrect_nouns_ag_output_file = working_directory +'data/incorrect_nouns/ag_output_file.txt'	# used to store the output of 
																									# an "ag (grep)" command

	incorrect_nouns_breadcrumbs_file = working_directory + 'data/incorrect_nouns/breadcrumbs.txt'	# used for stroing the breadcrumbs
																									# for products with no nouns

	incorrect_nouns_urls_file = working_directory + 'data/incorrect_nouns/urls.txt'					# used for storing the url's for
																									# products with no nouns so that
																									# they can be used to retrieve 
																									# breadcrumbs in the case none are
																									# available

	incorrect_nouns_output_file = working_directory + 'data/incorrect_nouns/output.txt'

	incorrect_nouns_ids_file = working_directory + 'data/incorrect_nouns/ids.txt'					# used for storing id's for
																									# corresponding products 

	correct_nouns_mysql_output_file = working_directory + 'data/correct_nouns/mysql_output.txt'		# temporary file used to store
																									# the output of an sql query

	correct_nouns_ag_output_file = working_directory +'data/correct_nouns/ag_output_file.txt'		# used to store the output of 
																									# an "ag (grep)" command

	correct_nouns_nouns_file = working_directory + 'data/correct_nouns/nouns.txt'					# used for nouns

	correct_nouns_breadcrumbs_file = working_directory + 'data/correct_nouns/breadcrumbs.txt'		# used for storing breadcrumbs
																									# for products that have nouns

	correct_nouns_ids_file = working_directory + 'data/correct_nouns/ids.txt'						# used for storing id's for 
																									# correspoonding products

	correct_nouns_output_file = working_directory + 'data/correct_nouns/output.txt'

	# cleaning files
	remove_file(incorrect_nouns_mysql_output_file, supress_output=True)
	remove_file(incorrect_nouns_ag_output_file)
	remove_file(incorrect_nouns_breadcrumbs_file)
	remove_file(incorrect_nouns_urls_file)
	remove_file(incorrect_nouns_ids_file)
	remove_file(incorrect_nouns_output_file)

	remove_file(correct_nouns_mysql_output_file, supress_output=True)
	remove_file(correct_nouns_ag_output_file)
	remove_file(correct_nouns_breadcrumbs_file)
	remove_file(correct_nouns_nouns_file)
	remove_file(correct_nouns_ids_file)
	remove_file(correct_nouns_output_file)

	####################################################################################################
	# OBTAINING PRODUCT PMI's FROM "flipkart_listing_products" TABLE WHICH DO NOT HAVE A NOUN ASSOCIATED
	####################################################################################################

	# the pmi's for the proucts not having a noun are stored in the file "incorrect_nouns_ag_output_file.txt, along with their id's"
	print('Log : load_data_without_nouns : reading products\n\t...')
	i = 0

	# initializing initial value of j
	j_max = 1000000
	j = 1
	# while number_of_products/j > 10 :
	# 	j *= 10
	# if j > j_max : 
	# 	j = j_max

	# maximizing the amount of data read from the mysql server in one query
	# since fetching data from the server is computationally expensive
	while j > 0 : 
		while i < number_of_products :
			mysql_command = 'select id, pmi from ' + table_name + ' where id >= ' + str(i) + ' and id < ' + str(i + j) + ' into outfile "' + incorrect_nouns_mysql_output_file + '"'
			mysql_comm.run_mysql_command(cursor, mysql_command, print_output=False)	
			i += j
			os.system("ag -v '\"noun\"' " + incorrect_nouns_mysql_output_file + " >> " + incorrect_nouns_ag_output_file)
			os.system("ag '\"noun\"' " + incorrect_nouns_mysql_output_file + " >> " + correct_nouns_ag_output_file)
			
			#################################################################################
			# OBTAINING NOUNS AND BREADCRUMBS FOR PRODUCTS WHICH DO NOT HAVE NOUNS ASSOCIATED
			#################################################################################
			incorrect_nouns_breadcrumbs_command = "var=$(ag -o '\"breadcrumbs[^\]]*\]' " + incorrect_nouns_ag_output_file
			incorrect_nouns_breadcrumbs_command += ") && echo $var >> " + incorrect_nouns_breadcrumbs_file
			incorrect_nouns_breadcrumbs_command += " && echo \"id=$var ,\" >> " + incorrect_nouns_output_file

			correct_nouns_breadcrumbs_command = "var=$(ag -o '\"breadcrumbs[^\]]*\]' " + correct_nouns_ag_output_file
			correct_nouns_breadcrumbs_command += ") && echo $var >> " + correct_nouns_breadcrumbs_file
			correct_nouns_breadcrumbs_command += " && echo \"id=$var ,\" >> " + correct_nouns_output_file

			os.system(incorrect_nouns_breadcrumbs_command)
			os.system(correct_nouns_breadcrumbs_command)
			
			if i == 3 : 
				raise SystemExit(0)
			else : 
				print(i)

			os.system("var=$(ag -o '\"breadcrumbs[^\]]*\]' " + incorrect_nouns_ag_output_file  + ") && echo $var >> " + incorrect_nouns_breadcrumbs_file + "")
			os.system("ag -o '\"url\":\"[^\"]*\"' " + incorrect_nouns_ag_output_file + " >> " + incorrect_nouns_urls_file)
			os.system("ag -o '\"noun\":[^:]*\",' " + correct_nouns_ag_output_file + " >> " + correct_nouns_nouns_file)
			os.system("ag -o '\"breadcrumbs[^\]]*\]' " + correct_nouns_ag_output_file  + " >> " + correct_nouns_breadcrumbs_file)
			
			##########################################################
			# OBTAINING AND STORING CORRESPONDING ID's IN THE IDS FILE
			##########################################################

			os.system("ag -o ':.*\t{\"id' " + incorrect_nouns_ag_output_file + " | ag -o ':.*\t' | ag -o '[^:]*\t' >> " + incorrect_nouns_ids_file)
			os.system("ag -o ':.*\t{\"id' " + correct_nouns_ag_output_file + " | ag -o ':.*\t' | ag -o '[^:]*\t' >> " + correct_nouns_ids_file)

			# Cleaning up before next iteration and printing
			remove_file(incorrect_nouns_ag_output_file)
			remove_file(correct_nouns_ag_output_file)
			remove_file(incorrect_nouns_mysql_output_file)
			print_string = '\treading upto id : ' + str(i) + ' / ' + str(number_of_products) 
			print(print_string, end='\r')
			sys.stdout.flush()
		i -= j
		j = j / 10

	# print('Log : load_data_without_nouns : Loading breadcrumbs and urls\n\t...')


	# print('Log : load_data_without_nouns : getting associated ids\n\t...')

	# number_of_products_without_nouns = ''
	# with open(incorrect_nouns_ag_output_file, 'r') as f : 
	# 	number_of_products_without_nouns = len(f.read().split('\n'))
	# with open(incorrect_nouns_ag_output_file, 'r') as f :
	# 	ids = [] 
	# 	lines = f.read().split('\n')
	# 	for line in lines : 
	# 		ids.append(line.split('\t')[0].split(':')[-1])
	# 	print("\tgot the ids")

	# 	with open(incorrect_nouns_ids_file, 'w') as f :
	# 		f.write('')
	# 	with open(incorrect_nouns_ids_file, 'a') as f : 
	# 		for id in ids : 
	# 			f.write(str(id) + '\n') 
		
	# 	print('\tdone writing ids to incorrect_nouns_ids_file')
	# print('Log : load_data_without_nouns number of products without nouns : ' + str(number_of_products_without_nouns))

	# number_of_products_without_nouns = ''
	# with open(correct_nouns_ag_output_file, 'r') as f : 
	# 	number_of_products_without_nouns = len(f.read().split('\n'))
	# with open(correct_nouns_ag_output_file, 'r') as f :
	# 	ids = [] 
	# 	lines = f.read().split('\n')
	# 	for line in lines : 
	# 		ids.append(line.split('\t')[0].split(':')[-1])

	# try : 
	# 	os.remove(correct_nouns_ids_file)
	# except OSError : 
	# 	pass
	# with open(correct_nouns_ids_file, 'a') as f: 
	# 	for id in ids : 
	# 		f.write(str(id) + '\n')
	# print('Log : load_data_with_nouns : number of products with nouns : ' + str(number_of_products_without_nouns))
	
	print('Log : load_data_without_nouns : DONE')
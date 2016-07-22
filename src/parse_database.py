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
# CALCULATING NUMBER OF ROWS IN THE "flipkart_listing_products_table"
#####################################################################

# uncomment the part below if you don't know the number of rows in the table
# (keeping in mind that it might take a considerable amount of time to do so
# for a large table)
# for the convenience, this has already been done once and is stored as 
# number_of_products = 740826729

# print('calculating the number of rows in the table ...')
# number_of_products = int(mysql_comm.run_mysql_command(cursor, 'SELECT COUNT(*) FROM flipkart_listing_products', print_output=False))
# print('\tnumber of rows --> ' + number_of_products)


def load_data_without_nouns() : 
	####################
	# FILE DECLARATIONS
	####################

	# store in a location where it can be accessed the fastest
	mysql_output_file = working_directory + 'data/incorrect_nouns/mysql_output.txt'	# temporary file used to store
																					# the output of an sql query

	ag_output_file = working_directory +'data/incorrect_nouns/ag_output_file.txt'	# used to store the output of 
																					# an "ag (grep)" command

	breadcrumbs_file = working_directory + 'data/incorrect_nouns/breadcrumbs.txt'	# used for stroing the breadcrumbs
																					# for products with no nouns

	urls_file = working_directory + 'data/incorrect_nouns/urls.txt'					# used for storing the url's for
																					# products with no nouns so that
																					# they can be used to retrieve 
																					# breadcrumbs in the case none are
																					# available

	ids_file = working_directory + 'data/incorrect_nouns/ids.txt'					# used for storing id's for
																					# corresponding products 

	# cleaning up data files
	os.system('rm ' + mysql_output_file)
	os.system('rm ' + ag_output_file)
	os.system('rm ' + breadcrumbs_file)
	os.system('rm ' + urls_file)
	os.system('rm' + ids_file)

	###############################################################################################
	# OBTAINING PRODUCTS FROM "flipkart_listing_products" TABLE WHICH DO NOT HAVE A NOUN ASSOCIATED
	###############################################################################################

	# the pmi's for the proucts not having a noun are stored in the file "ag_output_file.txt, along with their id's"
	print('reading products with no nouns associated\n\t...')
	i = 0

	# initializing initial value of j
	j = 1
	while number_of_products/j > 10 :
		j *= 10

	while j > 0 : 
		while i < 740826729 :
			mysql_command = 'select id, pmi from ' + table_name + ' where id >= ' + str(i) + ' and id < ' + str(i + 100000) + ' into outfile "' + mysql_output_file + '"'
			mysql_comm.run_mysql_command(cursor, mysql_command, print_output=False)	
			i += j
			os.system("ag -v '\"noun\"' " + mysql_output_file + " >> " + ag_output_file)
			os.system('rm ' + mysql_output_file)
			print('\treading upto id : ' + str(i))
		i -= j
		j = j / 10
	print('\tdone')

	#################################################################################
	# OBTAINING NOUNS AND BREADCRUMBS FOR PRODUCTS WHICH DO NOT HAVE NOUNS ASSOCIATED
	#################################################################################

	print('getting associated breadcrumbs and urls\n\t...')
	number_of_products_without_nouns = ''
	with open(ag_output_file, 'r') as f : 
		number_of_products_without_nouns = len(f.read().split('\n'))
	print('number of products without nouns : ' + str(number_of_products_without_nouns))
	with open(ag_output_file, 'r') as f :
		ids = [] 
		lines = f.read().split('\n')
		for line in lines : 
			ids.append(line.split('\t')[0])
		print("\tgot the ids")

		with open(ids_file, 'w') as f :
			f.write('')
		with open(ids_file, 'a') as f : 
			for id in ids : 
				f.write(str(id) + '\n') 
		print('\tdone writing ids to ids_file')

		count = 0
		for id in ids : 
			mysql_command = 'select pmi from flipkart_listing_products where id = ' + str(id) + ' into outfile "' + mysql_output_file + '"'
			mysql_comm.run_mysql_command(cursor, mysql_command, print_output=False)
			# if you get an error here, please install "ag (the silver searcher)"
			os.system("ag -o '\"breadcrumbs[^\]]*\]' " + mysql_output_file  + " >> " + breadcrumbs_file)
			os.system("ag -o '\"url\":\"[^\"]*\"' " + mysql_output_file + " >> " + urls_file)
			os.system('rm ' + mysql_output_file)
			count += 1
			print('\t' + str(count) + ' / ' + str(number_of_products_without_nouns))
			# if(count == 1000) :
			# 	print('\t' + str(id) + ' / ' + str(number_of_products))
			# 	count = 0

	print('hansel and gratel would be proud')

def load_data_with_nouns() : 
	###################
	# FILE DECLARATIONS
	###################

	# store in a location where it can be accessed the fastest
	mysql_output_file = working_directory + 'data/correct_nouns/mysql_output.txt'	# temporary file used to store
																					# the output of an sql query

	ag_output_file = working_directory +'data/correct_nouns/ag_output_file.txt'		# used to store the output of 
																					# an "ag (grep)" command

	nouns_file = working_directory + 'data/correct_nouns/nouns.txt'					# used for nouns

	breadcrumbs_file = working_directory + 'data/correct_nouns/breadcrumbs.txt'		# used for storing breadcrumbs
																					# for products that have nouns

	ids_file = working_directory + 'data/correct_nouns/ids.txt'						# used for storing id's for 
																					# correspoonding products

	# cleaning files
	os.system('rm ' + mysql_output_file)
	os.system('rm ' + ag_output_file)
	os.system('rm ' + breadcrumbs_file)
	os.system('rm ' + nouns_file)

	###########################################################################################
	# OBTAINING PRODUCTS FROM "flipkart_listing_products" TABLE WHICH DO HAVE A NOUN ASSOCIATED
	###########################################################################################

	# the pmi's for the proucts not having a noun are stored in the file "ag_output_file.txt, along with their id's"
	print('reading products with nouns associated\n\t...')
	i = 0

	# initializing initial value of j
	j = 1
	while number_of_products/j > 10 :
		j *= 10


	while j > 0 : 
		while i < 740826729 :
			mysql_command = 'select id, pmi from ' + table_name + ' where id >= ' + str(i) + ' and id < ' + str(i + 100000) + ' into outfile "' + mysql_output_file + '"'
			mysql_comm.run_mysql_command(cursor, mysql_command, print_output=False)	
			i += j
			os.system("ag '\"noun\"' " + mysql_output_file + " >> " + ag_output_file)
			# with open(temp_file, 'r') as f : 
			# 	os.system("echo '" + f.read() + "'' >> " + ag_output_file)
			# try : 
			# 	os.remove(output_file)
			# except OSError : 
			# 	pass
			os.system("ag -o '\"noun\":[^:]*\",' " + ag_output_file + " >> " + nouns_file)
			os.system("ag -o '\"breadcrumbs[^\]]*\]' " + ag_output_file  + " >> " + breadcrumbs_file)
			os.system('rm ' + mysql_output_file)
			print('\treading upto id : ' + str(i))
		i -= j
		j = j / 10
	print('\tdone')

	#############################################################################
	# OBTAINING NOUNS AND BREADCRUMBS FOR PRODUCTS WHICH DO HAVE NOUNS ASSOCIATED
	#############################################################################

	print('getting associated breadcrumbs and urls\n\t...')
	number_of_products_without_nouns = ''
	with open(ag_output_file, 'r') as f : 
		number_of_products_without_nouns = len(f.read().split('\n'))
	print('number of products without nouns : ' + str(number_of_products_without_nouns))
	with open(ag_output_file, 'r') as f :
		ids = [] 
		lines = f.read().split('\n')
		for line in lines : 
			ids.append(line.split('\t')[0])

	############################################
	# STORING CORRESPONDING ID's IN THE IDS FILE
	############################################
	try : 
		os.remove(ids_file)
	except OSError : 
		pass
	with open(ids_file, 'a') as f: 
		for id in ids : 
			f.write(str(id) + '\n')

		# # print(ids)
		# print("\tgot the ids")
		# count = 0
		# for id in ids : 
		# 	mysql_command = 'select pmi from flipkart_listing_products where id = ' + str(id) + ' into outfile "' + mysql_output_file + '"'
		# 	mysql_comm.run_mysql_command(cursor, mysql_command, print_output=False)
		# 	# if you get an error here, please install "ag (the silver searcher)"
		# 	os.system("ag -o '\"breadcrumbs[^\]]*\]' " + mysql_output_file  + " >> " + breadcrumbs_file)
		# 	os.system("ag -o '\"url\":\"[^\"]*\"' " + mysql_output_file + " >> " + urls_file)
		# 	os.system('rm ' + mysql_output_file)
		# 	count += 1
		# 	print('\t' + str(count) + ' / ' + str(number_of_products_without_nouns))
		# 	# if(count == 1000) :
		# 	# 	print('\t' + str(id) + ' / ' + str(number_of_products))
		# 	# 	count = 0

	print('hansel and gratel would be proud')

	''' ---------------------------------------------------------------------------------------------------- '''
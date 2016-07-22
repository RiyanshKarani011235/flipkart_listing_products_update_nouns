#!/usr/bin/python
import os
import sys
import __init__

depth = 2	# how deep is this file with respect to the top level path
			# (for example this file main.py is inside the project folder 
			# inside src, so it is two levels deep)

# setting up the working directory 
path_separator = '/'
if sys.platform.startswith('win') : 
	path_separator = '\\'
working_directory = ''
for element in os.path.realpath(__file__).split(path_separator)[:-depth] : 
	working_directory += element + path_separator

print('Log : working directory : ' + working_directory)
os.chdir(working_directory)

__init__.working_directory = working_directory
__init__.database_name = 'test'
__init__.table_name = 'flipkart_listing_products'

import parse_database_mark2
parse_database_mark2.load_data()
# parse_database.load_data_without_nouns() 	# obtain breadcrumbs, url's, and
# 											# and corresponding id's for 
# 											# products without nouns

# parse_database.load_data_with_nouns()		# obtain nouns, breadcrumbs and
# 											# and corresponding id's for 
# 											# products with nouns

# import update_breadcrumbs
# import create_breadcrumbs_nouns_dictionary
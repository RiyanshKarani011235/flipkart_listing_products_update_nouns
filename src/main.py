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

if not os.path.exists(os.path.join(working_directory, 'data')) : 
	print('initializing data directory')
	os.mkdir(os.path.join(working_directory, 'data'))
if not os.path.exists(os.path.join(working_directory, 'data', 'incorrect_nouns')) : 
	os.mkdir(os.path.join(working_directory, 'data', 'incorrect_nouns'))
if not os.path.exists(os.path.join(working_directory, 'data', 'correct_nouns')) :
	os.mkdir(os.path.join(working_directory, 'data', 'correct_nouns'))

__init__.working_directory = working_directory
__init__.database_name = 'test'
__init__.table_name = 'flipkart_listing_products'

import parse_database_mark2

parse_database_mark2.load_data()
import update_breadcrumbs
import create_breadcrumbs_nouns_dictionary
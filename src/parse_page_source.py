import urllib
import os
from utils import run_command_and_get_output, write_to_output
import __init__

working_directory = __init__.working_directory
# working_directory = '/Users/ironstein/Documents/projects_working_directory/scandid/mark2/'

###################
# FILE DECLARATIONS
###################
temp_file = working_directory + 'temp/temp.txt'
output_file = working_directory + 'temp/output.txt'

dont_return_breadcrumbs = ['Home', ''] # ignore breadcrumbs if listed in this list

def get_breadcrumbs(url) :
	page_source = urllib.urlopen(url).read()
	
	'''
		check if the product exists
		(if 'clp-breadcrumb' is not found in the page source, it 
		means that the page redirected to the flipkart home page, 
		which means that the product does not exist)
	'''
	if 'clp-breadcrumb' not in page_source : 
		return []

	# yes, the product exists
	write_to_output(page_source, output_file)

	# get only the clp-breadcrumb div
	command = "awk '/clp-breadcrumb/,/\<\/div\>/' " + output_file
	output = run_command_and_get_output(command, temp_file)
	write_to_output(output, output_file)

	# get only the values between the starting <a and ending </a>
	command = "awk '/\<a/,/\<\/a\>/' " + output_file
	output = run_command_and_get_output(command, temp_file)
	write_to_output(output, output_file)

	# get only the values between the <a>values...</a>tag
	command = "ag -o '\\t[^\<^\>]*\\n' " + output_file
	output = run_command_and_get_output(command, temp_file)
	write_to_output(output, output_file)

	# remove all the spaces from the output values
	command = "ag -o '[^\\t^\\n].*' " + output_file
	output = run_command_and_get_output(command, temp_file)
	write_to_output(output, output_file)
	
	return_list = []
	with open(output_file, 'r') as f : 
		for line in f.read().split('\n') : 
			if line not in dont_return_breadcrumbs : 
				return_list.append(line)

	print(return_list)
	return return_list
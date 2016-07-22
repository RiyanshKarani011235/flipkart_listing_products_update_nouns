import ast
import __init__

working_directory = __init__.working_directory
number_of_products = 740826729

nouns_file = working_directory + 'data/correct_nouns/nouns.txt'
breadcrumbs_file = working_directory + 'data/correct_nouns/breadcrumbs.txt'
nouns_list_file = working_directory + 'data/correct_nouns/nouns_list.txt'
breadcrumbs_list_file = working_directory + 'data/correct_nouns/breadcrumbs_list.txt'

breadcrumbs_nouns_dictionary = {}
nouns_list = []
breadcrumbs_list = []
with open(nouns_file, 'r') as f :
	nouns_list = f.read().split('\n')
with open(breadcrumbs_file, 'r') as f : 
	breadcrumbs_list = f.read().split('\n')

print('done loading from files ')

new_nouns_list = []
new_breadcrumbs_list = []
count = 0

with open(nouns_list_file, 'w') as f : 
	f.write('[')

with open(breadcrumbs_list_file, 'w') as f : 
	f.write('[')

for breadcrumbs, nouns in zip(breadcrumbs_list, nouns_list) : 
	count += 1
	new_nouns_list.append(nouns.split('"noun":')[-1])
	try : 
		breadcrumb_list = ast.literal_eval(breadcrumbs.split('"breadcrumbs":')[-1])
	except : 
		breadcrumb_list = 'None'
	new_breadcrumbs_list.append(breadcrumb_list)

	with open(nouns_list_file, 'a') as f : 
		f.write(str(new_nouns_list[-1]) + ',')
	with open(breadcrumbs_list_file, 'a') as f : 
		f.write(str(new_breadcrumbs_list[-1]) + ',')

	if count % 1000000 == 0 : 
		print(str(count) + ' / ' + str(number_of_products))

# with open(nouns_list_file, 'w') as f : 
# 	f.write(str(new_nouns_list))
# with open(breadcrumbs_list_file, 'w') as f : 
# 	f.write(str(new_breadcrumbs_list))

print new_nouns_list[:1000]
print new_breadcrumbs_list[:1000]
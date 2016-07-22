import ast
import parse_page_source
import __init__

working_directory = __init__.working_directory

breadcrumbs_file = '/Users/ironstein/Documents/projects_working_directory/scandid/__DATA__/incorrect_nouns/breadcrumbs.txt'
new_breadcrumbs_file = '/Users/ironstein/Documents/projects_working_directory/scandid/__DATA__/incorrect_nouns/new_breadcrumbs.txt'
urls_file = '/Users/ironstein/Documents/projects_working_directory/scandid/__DATA__/incorrect_nouns/urls.txt'

breadcrumbs = []
with open(breadcrumbs_file, 'r') as f : 
	breadcrumbs = f.read().split('\n')
urls = []
with open(urls_file, 'r') as f : 
	urls = f.read().split('\n')
new_breadcrumbs = []
# with open(new_breadcrumbs_file, 'w') as f : 
# 	f.write('')

print('done loading data')
for i in range(10339,len(breadcrumbs)) : 
	breadcrumbs_list = ast.literal_eval(breadcrumbs[i].split(':')[-1])
	if breadcrumbs_list == [] : 
		url = urls[i].split('"url":')[-1][1:-1]
		print(url)
		new_breadcrumbs.append(parse_page_source.get_breadcrumbs(url))
	else : 
		new_breadcrumbs.append(breadcrumbs_list)
	with open(new_breadcrumbs_file, 'a') as f : 
		f.write(str(new_breadcrumbs[-1]) + '\n')
	print(str(i) + ' / ' + str(len(breadcrumbs)))
**Requirements** :

- mysql (obviously)

- the silver searcher (which is a much faster version of grep). Can be
downloaded from [here](<https://github.com/ggreer/the_silver_searcher>)

- awk

 

**Setup** :

<i>run mysql server</i> :

mysqld —datadir=/path/to/loaded/database —skip-grant-tables

(in my case : mysqld
--datadir=/volumes/jarvis/projects\_working\_directory/scandid/data
--skip-grant-tables)

 

<i>connect to mysql server</i> :
mysql -u root

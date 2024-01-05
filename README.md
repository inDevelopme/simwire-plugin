### simwire-plugin-elastic-beanstalk
You can build this application using `docker-compose up --build -d`.


### connect using pycharm
This requires .env.local to have: `MYSQL_PYCHARM_HOST=localhost` AND `RUN_WEB_USING_IDE=1`.
Our PyCharm is configured to run in debugger which as you can imagine greatly improved our development speed.
To make this work we run using application.py 

#### connect using container
This requires .env.local to have `MYSQL_CONTAINER_HOST=mysql` and `RUN_WEB_USING_IDE=0`.
This way the container is connected to directly.

### how we update the requirements file locally
The below code controls the libraries which are installed in the containers and when the code is deployed to AWS EB.

`pip freeze > requirements.txt`  
***OR***  
`pip freeze | sed 's/==/>=/g' > requirements.txt` 

### Connecting to database container
These are the setting you will need to access the container locally.
HOST = localhost
User = root
Password = MYSQL_ROOT_PASSWORD
Database = MYSQL_DATABASE

### Seeding the database container
The database will be created automatically when the application is rebuild using the --build tag. However, the build does not seed the database with data. 
You will have to add your first user for this reason. This addition can be done by simply inserting a user into the user table. 
You do not need to worry about the password column just yet. We will be adding the password column and requiring a password to be set soon. 
Use something like this:  

`insert into simwire_plugin.users (username, email) values ('testing@testing.com', 'testing@testing.com');`



### simwire-plugin-elastic-beanstalk
You can build this application using `docker-compose up --build -d`.


### connect using pycharm
This requires .env.local to have: `MYSQL_PYCHARM_HOST=localhost` AND `ENV_DEBUG=1`.
Our PyCharm is configured to run in debugger which as you can imagine greatly improved our development speed.
To make this work we run using application.py 

#### connect using container
This requires .env.local to have `MYSQL_CONTAINER_HOST=mysql` and `ENV_DEBUG=0`.
This way the container is connected to directly.

### how we update the requirements file locally
The below code controls the libraries which are installed in the containers and when the code is deployed to AWS EB.

`pip freeze > requirements.txt`  
***OR***  
`pip freeze | sed 's/==/>=/g' > requirements.txt` 

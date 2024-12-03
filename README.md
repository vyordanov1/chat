# Django Chat App

Simple chat app built on Django framework utilizing the use of django channels and websockets.

## Installation

This project requires [Docker](https://docs.docker.com/engine/install/) or [Docker Desktop](https://docs.docker.com/desktop/) as well as [Docker compose](https://docs.docker.com/compose/) to run

### Create your .env file with the following content and enter your credentials and django secret key
```
ALLOWED_HOSTS='127.0.0.1,localhost'
DOMAIN='127.0.0.1'
DOMAIN_URL='http://127.0.0.1'
SECRET_KEY=''
STATIC_ROOT='static'
STATIC_URL='/static/'
PSQL_ROOT_PASSWORD=''
POSTGRES_MASTER_USER='postgres'
PSQL_HOST=''
PSQL_PORT='5432'
PSQL_DATABASE=''
PSQL_USER=''
PSQL_PASS=''
PSQL_ENGINE='django.db.backends.postgresql'
DJANGO_CONTAINER_NAME=''
FERNET_KEY=''
```
### Generate Django Secret Key
```
https://djecrety.ir/
```
### You can generate your Fernet key using
```
Fernet.generate_key().decode()
```


## - Run the Project

Use the run script to automatically run the containers
```sh
bash run.sh
```

Or do it manually:

```sh
docker compose build
```
```sh
docker compose up -d psql
```
```sh
docker exec -it psql bash scripts/init.sh
```
```sh
docker compose up -d
```

Every other run only needs
```sh
docker compose up -d
```

Run your project on [127.0.0.1:8081](http://127.0.0.1:8081)

## Post build procedures
--------------------

### Create a superuser for your Django [admin](http://127.0.0.1:8081/admin)

```sh
docker exec -it django-soft bash
python3 app/manage.py createsuperuser
```
Or from outside the container
```sh
docker exec -it django-soft python3 app/manage.py createsuperuser
```


## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>

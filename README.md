# Book catalog API

## Features
* **Django Rest Framework** backend
* **DRF-YASG** docs
* **MariaDB** as database
* **Docker** containers
* **Makefile** automating routine
* **Poetry** managing python packages
* **JWT token** authentication using **Simple JWT** package

## Launch
* Build and start project containers with migrations
```
make build
```
* Stop containers
```
make stop
```
* Start containers
```
make start
```
* Delete containers with images and volumes
```
make delete
```
* Parse books from given **url**, for example
```
make parse url=https://gitlab.grokhotov.ru/hr/python-test-vacancy/-/raw/master/books.json
```
* Create django superuser
```
make superuser
```

API docs are available at **[Swagger UI](http://0.0.0.0:8000/swagger)** or **[ReDoc](http://0.0.0.0:8000/redoc)**

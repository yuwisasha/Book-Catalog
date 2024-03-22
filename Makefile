build:
	docker compose up --build -d
start:
	docker compose start
stop: 
	docker compose stop
parse:
	docker compose exec app python catalog_app/manage.py parse_books $(url)
delete:
	docker-compose down --rmi all --volumes && docker rmi app-app
superuser:
	docker compose exec app python catalog_app/manage.py createsuperuser

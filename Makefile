up:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

migrate:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run web ./manage.py migrate

createsuperuser:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run web ./manage.py createsuperuser

web-shell:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run web bash

logs:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

clean: down
	docker volume rm upimg_fs upimg_db

Pipenfile.lock:

requirements.txt: Pipenfile.lock
	pipenv lock --requirements > requirements.txt

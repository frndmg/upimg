up:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

migrate:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run web ./manage.py migrate

web-shell:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run web bash

Pipenfile.lock:

requirements.txt: Pipenfile.lock
	pipenv lock --requirements > requirements.txt

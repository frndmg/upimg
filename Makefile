up:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

migrate:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run web ./manage.py migrate

web-console:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run web bash

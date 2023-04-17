test:
	python manage.py test

coverage:
	coverage run --source='.' manage.py test

cov-html: coverage
	coverage html

up:
	docker-compose up

build:
	docker-compose build

shell:
	docker-compose exec web bash

requirements:
	python -m pip install -r requirements.txt

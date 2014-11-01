help:
	@echo 'dev        - install dev requirements'
	@echo 'prod       - install prod requirements'
	@echo 'venv       - create virtualenv venv-folder'
	@echo 'production - deploy production'

dev:
	pip install -r requirements/dev.txt --upgrade
	
prod:
	pip install -r requirements/prod.txt --upgrade

venv:
	virtualenv -p `which python2` venv

focusbackup/settings/local.py:
	touch focusbackup/settings/local.py

production:
	git fetch && git reset --hard origin/master
	venv/bin/pip install -r requirements/prod.txt --upgrade
	venv/bin/python manage.py migrate
	venv/bin/python manage.py collectstatic --noinput

.PHONY: help dev prod venv production

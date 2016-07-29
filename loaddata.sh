#!/bin/bash
python manage.py loaddata agentlevels
python manage.py loaddata banks
python manage.py loaddata providers
# python manage.py loaddata levels - having an error for this fixture
python manage.py loaddata gametypes
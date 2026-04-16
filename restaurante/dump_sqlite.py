
import os
import sys

# Switch back to SQLite temporarily to dump data
# We can just manually use the sqlite3 db file and Django with sqlite settings?
# Or we can just set DATABASES in settings.py back to sqlite momentarily?
# Easier: Just run dumpdata using a temporary settings file or modifying the current one involves restart.

# Actually, I can just use the current settings IF I hadn't changed them yet? 
# I ALREADY CHANGED settings.py to MySQL.
# So I cannot dump from SQLite unless I switch back or point to SQLite.

# But I have the `db.sqlite3` file.
# I will create a script `dump_sqlite.py` that configures django to use sqlite, dumps data, then saves to json.

import django
from django.conf import settings
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Configure Django manually to use SQLite
if not settings.configured:
    settings.configure(
        BASE_DIR=BASE_DIR,
        SECRET_KEY='django-insecure-temporary',
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'gestion',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        },
        TIME_ZONE='America/Bogota',
        USE_TZ=True,
    )
    django.setup()

from django.core.management import call_command
import io

def dump_data():
    print("Dumping data from SQLite...")
    output = io.StringIO()
    call_command('dumpdata', exclude=['auth.permission', 'contenttypes'], stdout=output)
    
    data = output.getvalue()
    
    with open('db_dump_utf8.json', 'w', encoding='utf-8') as f:
        f.write(data)
        
    print("Data dumped to db_dump_utf8.json")

if __name__ == '__main__':
    dump_data()

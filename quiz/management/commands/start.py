import logging
import re
import os
import socket
import sys
import time

import django
import gunicorn.app.wsgiapp
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Start, migrate, and collectstatic.'

    def handle(self, *args, **kwargs):
        django.setup()

        self.wait_for_db()
        self.migrate_db()

        if int(os.environ.get('DEBUG', False)):
            call_command('runserver', '127.0.0.1:8000')
        else:
            sys.argv = [
                "gunicorn",
                "--preload",
                "-b", "0.0.0.0:8000",
                "fbla_quiz.wsgi:application",
                "--threads", "8",
                "-w", "4"
            ]

            gunicorn.app.wsgiapp.run()

    @staticmethod
    def wait_for_db():
        database_url = re.search(r'@([\w.]+):(\d+)/', os.environ.get('DATABASE_URL', ''))

        if not database_url:
            raise ImproperlyConfigured('Invalid value set for DATABASE_URL environment variable')

        host = database_url.group(1)
        port = int(database_url.group(2))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for _ in range(10):
            try:
                s.connect((host, port))
                s.shutdown(socket.SHUT_RDWR)

                logging.info('Database is ready')
                break

            except socket.error:
                logging.warning('Database not ready, retrying..')
                time.sleep(0.5)

        else:
            logging.error('Database was not found, exting..')
            sys.exit(1)

    @staticmethod
    def migrate_db():
        for _ in range(10):
            try:
                logging.info('Attempting to run migrations..')
                call_command('migrate')

                logging.info('Migrations applied successfully')
                break

            except OperationalError as error:
                if error.args[0] == 'FATAL:  the database system is starting up\n':
                    logging.warning(
                        'Failed to run migrations: the database system is starting up, retrying..'
                    )
                    time.sleep(0.5)
                else:
                    logging.error(f'Failed to run migrations: {error.args}')
                    sys.exit(1)

        else:
            logging.error('Failed to run migrations, exiting..')
            sys.exit(1)

from fabric.api import *

from fabfile import install_requirements
from fabfile import migrate_db


def build(service=None):
    """Perform pre-installation tasks for the service."""
    pass


def install(service=None):
    """Perform service specific post-installation tasks."""
    install_requirements()
    migrate_db(cmd='python manage.py')

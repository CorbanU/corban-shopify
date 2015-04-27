from .production import Production


class Staging(Production):
    CELERYBEAT_SCHEDULE = {}

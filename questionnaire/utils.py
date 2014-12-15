__author__ = 'guido'

# Timezone support with fallback.
try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


def split_choices(choices_string):
    """
    Convert a comma separated choices string to a list.
    """
    return [x.strip() for x in choices_string.split(",") if x.strip()]
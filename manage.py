#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import os
import sys
from dotenv import load_dotenv

if __name__ == "__main__":

    if 'production' in sys.argv:
        sys.argv = sys.argv[0:len(sys.argv)-1]
        dotenv_path = os.path.join(os.path.dirname(__file__), 'prod.env')
        load_dotenv(dotenv_path)

    if not os.getenv('DJANGO_SETTINGS_MODULE'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "willys_website.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

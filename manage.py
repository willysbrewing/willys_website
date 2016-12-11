#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import os
import sys
from dotenv import load_dotenv

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "willys_website.settings.dev")

    if 'production' in sys.argv:
        dotenv_path = join(dirname(__file__), 'prod.env')
        load_dotenv(dotenv_path)


    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

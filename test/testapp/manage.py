#!/usr/bin/env python
import sys
import os

sys.path.insert(0, os.path.abspath('./../../'))
sys.path.insert(0, os.path.abspath('./../'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

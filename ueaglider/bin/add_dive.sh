#!/bin/bash

/home/pilot/Python/ueaglider-web/venv/bin/python /home/pilot/Python/ueaglider-web/ueaglider/bin/database_edit.py  $(whoami) >> add_dive.log 2>&1
